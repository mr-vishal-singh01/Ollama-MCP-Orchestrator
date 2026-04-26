# Ollama MCP Orchestrator (Autonomous Agent)

This repository contains an advanced Python orchestrator that connects a local Ollama model to multiple Model Context Protocol (MCP) servers simultaneously.

## Features
- **Multi-Server Hub:** Automatically loads all MCP servers configured in `z/.gemini/settings.json`.
- **Autonomous AUTO Mode:** Optionally allows the FI core to chain tool calls without manual confirmation.
- **Context Protection:** Smart truncation of large CLI outputs (Nmap, Nuclei, etc.) to prevent memory overflow.
- **Safety First:** Includes a maneual confirmation loop for all system commands.

## Requirements
- **Ollama:** Running locally with a tool-calling model (e.g., Qwen 2.5).
- **MCP Servers:** Any standard MCP servers (shell, filesystem, nmap, etc.)

## Usage
``shbash
cd Ollama-MCP-Orchestrator
python agent.py
```


*Developed on Kali Linux.*