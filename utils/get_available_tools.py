from utils import get_tools_functions_module
import importlib.util
import sys
import json

def get(
    target_dir: str, module_name: str, 
    tools_allowed: dict, 
    tools_descriptions: list, tools_schemas: list
):
    available_functions = []
    for tool_path in get_tools_functions_module.get(target_dir):
        spec = importlib.util.spec_from_file_location(module_name, str(tool_path))

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        tools_allowed[module.get_name()] = True
        tools_descriptions.append(f'Name: {module.get_name()}\nDescription about the tool: {module.get_description()}\n')
        tools_schemas.append(json.dumps({
            "tool": module.get_name(),
            "args": module.get_schema()["properties"]
        }))
        available_functions.append(
            {
                "type": "function",
                "function": {
                    "name": module.get_name(),
                    "description": module.get_description(),
                    "parameters": module.get_schema()
                }
            }
        )
    
    return available_functions
