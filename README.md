## ABOUT

- The project is AI code agent created by me to understand how tools like Codex, Claude, OpenCode works under the hood.

## FEATURES
- Code agent can receive many instructions at once and will understand execute one by one
- Support tools. PS: you can create your tools add a file on folder **tools**
- Support MCP servers. PS: you need to provide the file in json format.
- Plan mode. PS: you can plan your code before execute it.
- Change the OpenAi model to select one you prefer or more powerful.

## HOW TO USE

- Clone the project
- Create a file .env with the following variables:
  - OPENAI_API_KEY=your_api_key
- Create virtual environment using venv: python -m venv .venv
- Activate virtual environment: source .venv/bin/activate
- Install dependencies: pip install -r requirements.txt
- Access file **config.py** and change 2 lines:
```python
WORKING_DIR="absolute_path_where_you_installed_project" // Or ./
PROJECT_FOLDER="absolute_path_where_you_installed_project"      // Or ./
```
- Run the project: python main.py. PS: to run the project on specific folder **WF=absolute_folder_path_here python main.py** , to use the MCP servers **MCP_FILE=absolute_path_json_file_here python main.py** or to use both **WF=absolute_folder_path_here MCP_FILE=absolute_path_json_file_here python main.py**

## EXTRA INFO

- Commands available: /help, /models, /set-model <model_id>, /plan, /build, /exit
 ```txt
/models - List all models available
/set-model <model_id> - Set the model to use
/plan - Enable plan mode. PS: is good to plan feature before build anything
/build - Build the plan. PS: execute the plan. Default mode when start the code agent
/exit - Exit the program
 ```
- You can see a example of mcp.json on root of project, file named **mcp.json**
- The folders todo-app and todo-app-react are project I created used this AI code agent.
