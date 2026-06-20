#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import sys
import importlib.util
import config
import json
from openai import OpenAI
from utils import get_available_tools

load_dotenv()

import asyncio
from session import session_management
from mcp_tool import mcp_management
from utils import get_messages_session

module_name = "tools"
target_dir = os.path.join(config.PROJECT_FOLDER, "tools")
tools_allowed = {}
tools_descriptions = []
tools_schemas = []   

api_key = os.environ.get("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

working_folder = os.getenv("WF")
file_path_mcp = os.getenv("MCP_FILE") or None
 
mcp_tools = mcp_management.McpTool(file_path_mcp)


old_session_id = None 

if len(sys.argv[1:]) > 0:
    old_session_id = sys.argv[1:][0]
    print("Starting back the session", old_session_id, "\n")

session = session_management.Session(old_session_id)   
messages = get_messages_session.get(session)

async def run_function(name, args):
    if name not in tools_allowed:
        return f"Error: the tool {name} not found"
    
    is_tool_from_mcp_server = mcp_tools.get_is_tool_from_mcp_server()
    if name in is_tool_from_mcp_server and is_tool_from_mcp_server[name] == True:
        return await mcp_tools.run_tool(name, args)

    filepath = os.path.join(target_dir,  f'{name}.py')
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module.run(working_folder or config.WORKING_DIR, args)

async def start():
    models_availables = {}
    models = []
    
    for model in client.models.list():
        if "gpt" in model.id.lower():
            models.append(model.id)
            models_availables[model.id] = True

    model = "gpt-5-nano-2025-08-07"
    enablePlanMode = False
    
    print("Loading MCP servers...")
    await mcp_tools.load_mpc_tools()
    if len(mcp_tools.get_mcp_tools()) > 0:
        print("Set the MCP tools...")
        for tool in mcp_tools.get_mcp_tools():
            tools_allowed[tool["function"]["name"]] = True
        
    if len(messages) == 0:
        messages.insert(
            0,
            { 
                "role": "system",
                "content": "You are a helpful coding agent with access to tools for reading, listing, and editing files in the user's working directory. Use the tools whenever they would let you answer more accurately than guessing. Prefer reading a file over asking the user to paste its contents. When editing, make the smallest change that satisfies the request. Keep replies short." 
            }
        )
        
    while(True):
        user_prompt = input(f"> Tell what you want to do?(Model: {model} | Plan mode: {'Enabled' if enablePlanMode else 'Disabled'})\n")
            
        if user_prompt == "/help":
            print("""
                /models - List all models available
                /set-model <model_id> - Set the model to use
                /plan - Enable plan mode. PS: is good to plan feature before build anything
                /build - Build the plan. PS: execute the plan. Default mode when start the code agent
                /exit - Exit the program
            """)
            continue

        if user_prompt == "/models":
            for model in models:
                print(model)
            continue
        
        if user_prompt == "/plan":
            enablePlanMode = True
            continue
        
        if user_prompt == "/build":
            enablePlanMode = False
            user_prompt = "Build the plan"
        
        if user_prompt.startswith("/set-model"):
            model_id = user_prompt.split(" ")[1]
            if models_availables.get(model_id) == None:
                print("Model not found")
            
            model = model_id
            continue
        
            
        if user_prompt == "/exit": 
            print(f"Continue this session using command: python main.py {session.get_session_id()}")
            sys.exit(0)
            
        messages.append( 
            { "role": "user", "content": user_prompt }
        )
        session.save("user", user_prompt)
            
        while(True):
            print("Bot: Thinking...")
            
            
            tools = (get_available_tools.get(
                    target_dir, module_name, 
                    tools_allowed, 
                    tools_descriptions, tools_schemas    
                ) + (mcp_tools.get_mcp_tools()))
            
            if enablePlanMode == True:
                tools = []
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
            )

            msg = response.choices[0].message
            messages.append(msg);
            
            session.save(msg.role, msg.content or "")

            if msg.tool_calls == None or len(msg.tool_calls) == 0: 
                print(f'Bot: {msg.content}\n');
                break;

            if msg.tool_calls:

                for tool_call in msg.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    print(f"Bot: Executing the function {function_name} | args {arguments}...")
                    result = await run_function(function_name, arguments)
                    print(f"Result: {result}\n")
                    
                    session.save("assistant", json.dumps({
                        "role": "assistant",
                        "content": None,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": function_name, 
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]

                    }))
                     
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result or ""
                    })
                    
                    session.save("tool", json.dumps({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result or ""
                    }))

asyncio.run(start())