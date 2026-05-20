from pathlib import Path
import requests
import json

def get_name():
    return (Path(__file__).name).replace(".py", "")

def get_description(): 
    return "Get the todos from dumpjson api."


def get_schema():
    return {
        "type": "object",
        "properties": {}
    }
    
def run(working_directory, args):
    response = requests.get('https://dummyjson.com/todos?limit=10')
    
    if response.status_code == 200:
        return json.dumps(response.json(), indent=4)
        
    return f"Error: request to the URL https://dummyjson.com/todos?limit=10 failed"

    
    

