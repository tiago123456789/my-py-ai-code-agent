## ABOUT

- The project is AI code agent created by me to understand how tools like Codex, Claude, OpenCode works under the hood.

## FEATURES
- Code agent que receive many instructions at once and will understand execute one by one
- Support tools. PS: you can create your tools add a file on folder **tools**
- Support MCP servers. PS: you need to provide the file in json format.

## HOW TO USE

- Clone the project
- Create a file .env with the following variables:
  - OPENAI_API_KEY=your_api_key
- Create virtual environment using venv: python -m venv .venv
- Activate virtual environment: source .venv/bin/activate
- Install dependencies: pip install -r requirements.txt
- Run the project: python main.py. PS: to run the project on specific folder **WF=absolute_folder_path_here python main.py** , to use the MCP servers **MCP_FILE=absolute_path_json_file_here python main.py** or to use both **WF=absolute_folder_path_here MCP_FILE=absolute_path_json_file_here python main.py**

## EXTRA INFO

- You can see a example of mcp.json on root of project, file named **mcp.json**
- The folders todo-app and todo-app-react are project I created used this AI code agent.
