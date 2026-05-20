import os
from pathlib import Path

def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "Use this tool change or modify the code of file"

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
            },
            "content": {
            "type": "string",
            "description": "The file content to be write"
            },
            "mode": {
            "type": "string",
            "enum": ["create", "overwrite", "append"],
            "description": "The file content to be write"
            }
        }
}
    
def run(working_directory, args):
    file_path = args["file_name"]
    content = args["content"]

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
        
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
            with open(abs_file_path, 'w') as f:
                f.write(content)
            return (
                f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            )
    except Exception as e:
        return f"Error: writing to file: {e}"
    
    

