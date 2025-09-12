
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TerminalTools:
    def __init__(self):
        pass

    async def execute_command(self, command: str, timeout: int = 300) -> str:
        """Executes a shell command and returns its stdout and stderr."""
        logger.info(f"Executing command: {command}")
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

            output = f"STDOUT:\n{stdout.decode().strip()}\n"
            if stderr:
                output += f"STDERR:\n{stderr.decode().strip()}\n"
            if process.returncode != 0:
                output += f"Command exited with code: {process.returncode}\n"

            logger.info(f"Command executed successfully. Return code: {process.returncode}")
            return output
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            logger.error(f"Command timed out after {timeout} seconds: {command}")
            return f"Error: Command timed out after {timeout} seconds."
        except Exception as e:
            logger.error(f"Error executing command \'{command}\': {e}")
            return f"Error executing command \'{command}\': {e}"

# Example usage (for testing purposes)
async def main():
    terminal_tools = TerminalTools()
    print(await terminal_tools.execute_command("ls -la"))
    print(await terminal_tools.execute_command("echo Hello World"))
    print(await terminal_tools.execute_command("python3 -c \"import time; time.sleep(2); print(\\\"Done\\\")\""))
    print(await terminal_tools.execute_command("non_existent_command"))

if __name__ == "__main__":
    asyncio.run(main())

