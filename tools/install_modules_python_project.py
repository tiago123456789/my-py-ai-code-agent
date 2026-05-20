import os 
import subprocess
from pathlib import Path
import sys


def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "Install modules on python project, if you create a files and this file add a new module, so needs to execute the tool."

def get_schema():
    return {
  "type": "object",
  "properties": {
    "directory": {
      "type": "string",
      "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
    },
    "module": {
      "type": "string",
      "description": "The module name needs to be installed"
    }
  }
}

def run(working_directory, args=None):
    module = args["module"] 
    abs_working_dir = os.path.abspath(working_directory)
    try:
        commands = [sys.executable, "-m", "pip", "install", module]
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

