import json

def get(session):
    messages_history = session.get_back_messages_history()
    messages = []
    for item in messages_history:
        
        role = item.get("role")
        messages.append(   
            { "role": role, "content": item.get("message") }
        )
        
    new_history  = []
    for message in messages:
        if (message["role"] == "assistant" and message["content"] != ""):
            content = message["content"]
            tools_calls = None
            
            try:
                print(json.loads(message["content"]))
                tools_calls = json.loads(message["content"])["tool_calls"]
                content = ""
            except Exception as e:
                print("")

            new_history.append({
                "role": "assistant",
                "content": content,
                "tool_calls": tools_calls
            })
        elif (message["role"] == "tool" and message["content"] != ""):
            content = message["content"]
            tools_info = None
            
            try:
                print(json.loads(message["content"]))
                tools_info = json.loads(message["content"])
                content = tools_info["content"]
            except Exception as e:
                print("")

            new_history.append({
                "role": "tool",
                "content": content,
                **tools_info
            })
        else:
            new_history.append(message)
    
    return new_history
        