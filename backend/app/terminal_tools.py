# MyAssistant/backend/app/terminal_tools.py

import asyncio
import os

async def execute_command(command: str, session_id: str) -> dict:
    """
    Executes a shell command within the session's workspace and returns its output.
    """
    session_workspace = os.path.join("sessions", session_id)
    if not os.path.exists(session_workspace):
        os.makedirs(session_workspace)

    try:
        # Use asyncio.create_subprocess_shell to run the command asynchronously
        # and capture its output.
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=session_workspace  # Execute command in the session's workspace
        )

        stdout, stderr = await process.communicate()

        output = stdout.decode().strip()
        error = stderr.decode().strip()

        if process.returncode != 0:
            return {"status": "error", "message": f"Command failed with exit code {process.returncode}.\nError: {error}", "output": output, "error": error}
        else:
            return {"status": "success", "message": "Command executed successfully.", "output": output}
    except Exception as e:
        return {"status": "error", "message": f"Failed to execute command: {e}"}

