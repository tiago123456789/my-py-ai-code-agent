import os
from pathlib import Path


def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "List files and directories, constrained to the working directory."

def get_schema():
    return {
    "type": "object",
    "properties": {
        "directory": {
        "type": "string",
        "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
        },
    }
}

def run(working_directory, args):
    abs_working_dir = os.path.abspath(working_directory)
    
    try:
        files_info = []
        for filename in os.listdir(abs_working_dir):
            filepath = os.path.join(abs_working_dir, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
            
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: listing the files {e}"