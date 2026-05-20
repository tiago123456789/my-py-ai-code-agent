import os
import config
from pathlib import Path


def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "Read file or get the content from file or when user said read the file and specific the file name or path, constrained to the working directory."

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

def run(working_directory, args):
    file_path = args["file_name"] 
    
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: \'{file_path}\''
    
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)
            if os.path.getsize(abs_file_path) > config.MAX_CHARS:
                file_content_string += f"[...file '{file_path}' truncated at {config.MAX_CHARS} characters ]"
                
        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


        