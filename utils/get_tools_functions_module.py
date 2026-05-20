import os

def get(target_dir):
    tools_path = []
    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)
        if filepath.endswith(".py"):
            tools_path.append(filepath)
    
    return tools_path   
