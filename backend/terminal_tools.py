import subprocess
import os
import asyncio
from typing import Dict, Any

class TerminalTools:
    def __init__(self):
        self.current_directory = os.getcwd()
    
    async def execute_command(self, command: str, working_directory: str = None) -> Dict[str, Any]:
        """
        Execute a shell command and return the output.
        
        Args:
            command: The shell command to execute
            working_directory: Optional working directory for the command
            
        Returns:
            Dictionary containing stdout, stderr, return_code, and working_directory
        """
        if working_directory:
            self.current_directory = working_directory
        
        try:
            # Use asyncio subprocess for non-blocking execution
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.current_directory
            )
            
            stdout, stderr = await process.communicate()
            
            result = {
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace'),
                "return_code": process.returncode,
                "working_directory": self.current_directory,
                "command": command
            }
            
            return result
            
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error executing command: {str(e)}",
                "return_code": -1,
                "working_directory": self.current_directory,
                "command": command
            }
    
    def change_directory(self, path: str) -> str:
        """
        Change the current working directory.
        
        Args:
            path: The path to change to
            
        Returns:
            Success message or error
        """
        try:
            if os.path.isabs(path):
                new_path = path
            else:
                new_path = os.path.join(self.current_directory, path)
            
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_directory = os.path.abspath(new_path)
                return f"Changed directory to: {self.current_directory}"
            else:
                return f"Error: Directory '{path}' does not exist"
                
        except Exception as e:
            return f"Error changing directory: {str(e)}"
    
    def get_current_directory(self) -> str:
        """Get the current working directory."""
        return self.current_directory
    
    async def run_interactive_command(self, command: str, inputs: list = None) -> Dict[str, Any]:
        """
        Run an interactive command with predefined inputs.
        
        Args:
            command: The command to run
            inputs: List of inputs to send to the command
            
        Returns:
            Dictionary containing the command output and status
        """
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.current_directory
            )
            
            if inputs:
                input_data = '\n'.join(inputs) + '\n'
                stdout, stderr = await process.communicate(input_data.encode())
            else:
                stdout, stderr = await process.communicate()
            
            return {
                "stdout": stdout.decode('utf-8', errors='replace'),
                "stderr": stderr.decode('utf-8', errors='replace'),
                "return_code": process.returncode,
                "working_directory": self.current_directory,
                "command": command
            }
            
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error executing interactive command: {str(e)}",
                "return_code": -1,
                "working_directory": self.current_directory,
                "command": command
            }

# Example usage
async def main():
    terminal = TerminalTools()
    
    # Test basic command
    result = await terminal.execute_command("ls -la")
    print("Command output:", result)
    
    # Test directory change
    print(terminal.change_directory("/tmp"))
    print("Current directory:", terminal.get_current_directory())

if __name__ == "__main__":
    asyncio.run(main())

