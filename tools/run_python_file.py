import os 
import subprocess
from pathlib import Path


def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "Run python script, constrained to the working directory."

def get_schema():
    return {
  "type": "object",
  "properties": {
    "directory": {
      "type": "string",
      "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
    },
    "file_name": {
      "type": "string",
      "description": "The file name user wants to see the content"
    }
  }
}

def run(working_directory, args=None):
    file_path = args["file_name"] 
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )
        
        output = []
        
        if result.stdout:
            output.append(f'STDOUT:\n {result.stdout}')
        
        if result.stderr:
            output.append(f'STDERR:\n {result.stderr}')
            
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

