import asyncio
import json
import os
from contextlib import AsyncExitStack
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
MODEL = "qwen2.5:0.5b"
OLLAMA_URL = "http://localhost:11434/v1"
SETTINGS_PATH = os.path.expanduser("~/.gemini/settings.json")
client = AsyncOpenAI(base_url=OLLAMA_URL, api_key="ollama")
SYSTEM_PROMPT = "You are an advanced, autonomous AI assistant. Break down problems, use tools extensively, and chain commands together autonomously."
def load_mcp_configs():
    if not os.path.exists(SETTINGS_PATH):
        return {}
    with open(SETTINGS_PATH, "r") as f:
        return json.load(f).get("mcpServers", {})
async def main():
    print("[*] Starting Advanced Autonomous Ollama Agent")
    mcp_configs = load_mcp_configs()
    if not mcp_configs: return
    all_ollama_tools = []
    tool_to_session = {}
    exit_stack = AsyncExitStack()
    async with exit_stack:
        print(f"[*] Initializing {len(mcp_configs)} MCP servers...")
        for name, config in mcp_configs.items():
            try:
                env = os.environ.copy()
                if "env" in config: env.update(config["env"])
                params = StdioServerParameters(command=config["command"], args=config.get("args", []), env=env)
                transport = await exit_stack.enter_async_context(stdio_client(params))
                session = await exit_stack.enter_async_context(ClientSession(transport[0], transport[1]))
                await session.initialize()
                for tool in (await session.list_tools()).tools:
                    all_ollama_tools.append({"type": "function", "function": {"name": tool.name, "description": tool.description, "parameters": tool.inputSchema}})
                    tool_to_session[tool.name] = session
                print(f"    [+] {name} online")
            except Exception as e: print(f"    [!] Failed to load {name}: {e}")
        auto_mode = input("\nEnable AUTO mode? (y/N): ").strip().lower() == "y"
        chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        while True:
            try:
                user_input = input("\n[You]: ")
                if user_input.lower() in ["exit", "quit"]: break
                chat_history.append({"role": "user", "content": user_input})
                while True:
                    response = await client.chat.completions.create(model=MODEL, messages=chat_history, tools=all_ollama_tools if all_ollama_tools else None)
                    message = response.choices[0].message
                    if not message.tool_calls:
                        print(f"\n[Agent]: {message.content}")
                        chat_history.append({"role": "assistant", "content": message.content})
                        break
                    chat_history.append(message)
                    for tool_call in message.tool_calls:
                        f_name = tool_call.function.name
                        f_args = json.loads(tool_call.function.arguments)
                        print(f"\n[⚙️ Action]: {f_name}")
                        if not auto_mode and input("Proceed? (y/n): ").lower() != "y":
                            chat_history.append({"role": "tool", "tool_call_id": tool_call.id, "name": f_name, "content": "User denied."})
                            continue
                        session = tool_to_session.get(f_name)
                        if session:
                            try:
                                r = await session.call_tool(f_name, arguments=f_args)
                                r_text = "\n".join([c.text for c in r.content if c.type == "text"])
                                if len(r_text) > 8000: r_text = r_text[:4000] + "\n...[TRUNCATED]...\n" + r_text[-4000:]
                                chat_history.append({"role": "tool", "tool_call_id": tool_call.id, "name": f_name, "content": r_text})
                                print("    [+] Completed.")
                            except Exception as e: chat_history.append({"role": "tool", "tool_call_id": tool_call.id, "name": f_name, "content": str(e)})
            except KeyboardInterrupt: continue
if __name__ == "__main__": asyncio.run(main())
