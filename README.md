# Ollama MCP Orchestrator (Autonomous Agent)

This repository contains an advanced Python orchestrator that connects a local Ollama model to multiple Model Context Protocol (MCP) servers simultaneously. It bridges the gap between AI and over 200+ professional Kali Linux security tools.

## Features
- **Multi-Server Hub:** Automatically loads all MCP servers configured in your environment.
- **Autonomous AUTO Mode:** Optionally allows the AI core to chain tool calls indefinitely without manual confirmation.
- **Context Protection:** Smart truncation of extremely large CLI outputs (e.g., from Nmap, Nuclei, Masscan) to prevent ELM memory overflow.
- **Safety First:** Includes a manual confirmation loop for all system commands to ensure safe execution.

## Hardware Requirements & Performance

Running an autonomous AI agent locally requires significant computational resources depending on the intelligence level you expect. This project can be run in two different hardware tiers:

### 1. The "Super-Agent" Tier (Requirements my system CANNOT handle)
To have a highly intelligent agent capable of autonomously finding bugs, writing exploits, and chaining complex tools without mistakes, you need a larger model (7B to 32B parameters).
- **RAM:** 16GB to 32GB+ DDR4/DDR5
- **GPU:** Dedicated NVIDIA GPU with 8GB to 24GB+ VRAM (e.g., RTX 3060, RTX 4090) or an Apple Silicon Mac with high Unified Memory.
- **Storage:** NVMe SSD (Crucial for fast tool output reading).
- **Model:** `qwen2.5:7b`, `llama3.1:8b`, or larger.

*Note: Older hardware (like Intel i3 laptops with 4GB RAM) cannot run this tier. The system will swap memory to the hard drive, causing extreme lag and potential crashes.*

### 2. The "Testing/Minimal" Tier (Requirements my system CAN handle)
You can still test and run this architecture on older, low-end hardware by using a highly compressed, tiny "nano" model. While the AI won't be exceptionally smart, it proves that the MCP integration and Python orchestrator work flawlessly.
- **CPU:** Older processors (e.g., Intel Core i3)
- **RAM:** 4GB Total RAM
- **GPU:** Integrated Graphics (No dedicated VRAM required)
- **Model:** `qwen2.5:0.5b` or `qwen2.5:1.5b` (Uses very little RAM).

## Usage
1. Make sure Ollama is running (`systemctl start ollama`).
2. Pull your chosen model (e.g., `ollama pull qwen2.5:0.5b`).
3. Update the `MODEL` variable in `agent.py` to match your downloaded model.
4. Run the agent:

``bash
cd Ollama-MCP-Orchestrator
python3 agent.py
```

*Developed and tested on Kali Linux.*