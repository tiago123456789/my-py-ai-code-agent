import os
from pathlib import Path


def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "Remove or delete the file"

def get_schema():
    return {
        "type": "object",
        "properties": { 
            "file_name": {
                "type": "string",
                "description": "The file name user wants to see the content"
            }    
        }
    }
    
def run(working_directory, args):
    file_path = args["file_name"]

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        os.remove(abs_file_path)
        return f"File deleted with success {file_path}"
    except Exception as e:
        return f"Error: writing to file: {e}"
    
    

