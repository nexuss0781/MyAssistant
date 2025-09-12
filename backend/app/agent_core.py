import os
import re
from functools import partial
from app import gemini_handler, filesystem_tools, session_manager, browser_tools, terminal_tools
from app.websocket_manager import ConnectionManager

async def generate_plan(user_prompt: str) -> str:
    """
    Generates a plan by combining the agent's constitution with the user's prompt
    and calling the Gemini API.
    """
    try:
        # Construct path to the prompt file relative to this file's location for robustness
        prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prompt.md'))
        with open(prompt_path, 'r', encoding='utf-8') as f:
            constitution = f.read()
        
        full_prompt = f"{constitution}\n\n## User Request\n{user_prompt}"
        
        # Call the Gemini handler to get the plan
        plan = gemini_handler.call_gemini(full_prompt)
        return plan
    except FileNotFoundError:
        # Handle case where the crucial prompt.md file is missing
        raise FileNotFoundError(f"Critical error: prompt.md not found at {prompt_path}")
    except Exception as e:
        # Catch-all for other potential errors during plan generation
        raise Exception(f"Failed to generate plan: {e}")


def parse_plan(plan_text: str) -> list:
    """
    (REFINED in Phase 5) Parses the raw markdown plan from the LLM into a structured list of commands.
    This version robustly handles code fences with language specifiers (e.g., ```python).
    """
    commands = []
    lines = plan_text.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("- [ ]"):
            i += 1
            continue
            
        # Regex to capture TOOL_NAME and its arguments
        match = re.match(r"- \[ \] (\w+):?\s*(.*)", line)
        if not match:
            i += 1
            continue
        
        tool, args = match.groups()
        
        if tool == "ADD_CONTENT":
            path = args.strip()
            content_lines = []
            i += 1
            # Proactively handles code fences with or without language specifiers
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1 # Move past the opening fence
                # Read lines until the closing fence is found
                while i < len(lines) and lines[i].strip() != "```":
                    content_lines.append(lines[i])
                    i += 1
                i += 1 # Move past the closing fence
            commands.append({"tool": tool, "path": path, "content": "\n".join(content_lines)})
        else:
            commands.append({"tool": tool, "args": args.strip()})
            i += 1
            
    return commands


async def execute_plan(commands: list, session_id: str, client_id: str, manager: ConnectionManager):
    """
    Executes a parsed list of commands for a specific session, sending real-time updates.
    """
    # Use functools.partial to pre-fill the session_id for all filesystem tool functions
    tool_map = {
        "CREATE_FILE": partial(filesystem_tools.create_file, session_id=session_id),
        "CREATE_FOLDER": partial(filesystem_tools.create_folder, session_id=session_id),
        "ADD_CONTENT": partial(filesystem_tools.add_content, session_id=session_id),
        "DELETE_FILE": partial(filesystem_tools.delete_file, session_id=session_id),
        "DELETE_FOLDER": partial(filesystem_tools.delete_folder, session_id=session_id),
        "NAVIGATE_TO_URL": partial(browser_tools.navigate_to_url, session_id=session_id),
        "WEB_SEARCH": partial(browser_tools.web_search, session_id=session_id),
        "EXTRACT_CONTENT": partial(browser_tools.extract_content, session_id=session_id),
        "INTERACT_WITH_ELEMENT": partial(browser_tools.interact_with_element, session_id=session_id),
        "TAKE_SCREENSHOT": partial(browser_tools.take_screenshot, session_id=session_id),
        "EXECUTE_COMMAND": partial(terminal_tools.execute_command, session_id=session_id),
    }

    for command in commands:
        tool_name = command["tool"]
        current_task_message = f"{tool_name}: {command.get('path') or command.get('args')}"
        
        # Notify frontend that a task is starting
        await manager.send_personal_message({"type": "task_start", "data": current_task_message}, client_id)

        if tool_name in tool_map:
            try:
                func = tool_map[tool_name]
                if tool_name == "ADD_CONTENT":
                    result = await func(path=command["path"], content=command["content"])
                elif tool_name == "CREATE_FILE" or tool_name == "CREATE_FOLDER" or tool_name == "DELETE_FILE" or tool_name == "DELETE_FOLDER":
                    result = await func(command["args"])
                elif tool_name == "EXECUTE_COMMAND":
                    result = await func(command=command["args"])
                elif tool_name == "NAVIGATE_TO_URL":
                    result = await func(url=command["args"])
                elif tool_name == "WEB_SEARCH":
                    result = await func(query=command["args"])
                elif tool_name == "EXTRACT_CONTENT":
                    args_parts = command["args"].split(maxsplit=1)
                    url = args_parts[0]
                    format_arg = args_parts[1] if len(args_parts) > 1 else "text"
                    result = await func(url=url, format=format_arg)
                elif tool_name == "INTERACT_WITH_ELEMENT":
                    args_parts = command["args"].split(maxsplit=3)
                    url = args_parts[0]
                    selector = args_parts[1]
                    action = args_parts[2]
                    value = args_parts[3] if len(args_parts) > 3 else None
                    result = await func(url=url, selector=selector, action=action, value=value)
                elif tool_name == "TAKE_SCREENSHOT":
                    args_parts = command["args"].split(maxsplit=1)
                    url = args_parts[0]
                    path = args_parts[1] if len(args_parts) > 1 else "screenshot.png"
                    result = await func(url=url, path=path)
                
                # Notify frontend that the task is complete
                await manager.send_personal_message({"type": "task_complete", "data": current_task_message, "result": result}, client_id)


            except Exception as e:
                error_message = f"Error executing '{current_task_message}': {e}"
                await manager.send_personal_message({"type": "error", "data": error_message}, client_id)
                break # Stop execution on error
        elif tool_name == "FINISH":
            final_message = command["args"]
            session_manager.append_to_history(session_id, {"type": "agent", "text": final_message})
            await manager.send_personal_message({"type": "finish", "data": final_message}, client_id)
        else:
            # Handle unknown tools gracefully
            unknown_tool_message = f"Unknown tool '{tool_name}' found in plan. Skipping."
            await manager.send_personal_message({"type": "warning", "data": unknown_tool_message}, client_id)


async def run_agent_task(user_prompt: str, session_id: str, client_id: str, manager: ConnectionManager):
    """
    The main orchestrator for an agent task. It generates, logs, and executes a plan.
    """
    try:
        # Log user prompt and notify frontend
        session_manager.append_to_history(session_id, {"type": "user", "text": user_prompt})
        await manager.send_personal_message({"type": "status", "data": "Generating plan..."}, client_id)
        
        # Generate the plan from the LLM
        plan_text = await generate_plan(user_prompt)
        
        # Log the raw plan and send it to the frontend
        session_manager.append_to_history(session_id, {"type": "agent_plan_text", "text": plan_text})
        await manager.send_personal_message({"type": "plan", "data": plan_text}, client_id)
        
        # Parse and execute the plan
        commands = parse_plan(plan_text)
        await execute_plan(commands, session_id, client_id, manager)
        
    except Exception as e:
        error_message = f"An error occurred in the agent core: {e}"
        # Log any errors and notify the frontend
        session_manager.append_to_history(session_id, {"type": "error", "text": error_message})
        await manager.send_personal_message({"type": "error", "data": error_message}, client_id)
