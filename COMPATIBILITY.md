# 🔌 GracefulOS: Complete Compatibility & Supported Systems Guide

Welcome to the compatibility guide for **GracefulOS**. Because GracefulOS sits at the **Windows Operating System and Kernel layer**, it is universally compatible with almost any AI tool, local model runner, framework, and language you run on Windows 11.

---

## 💻 1. Operating Systems & Hardware

1. **Windows 11** (Home, Pro, Enterprise, Education, and Workstations)
2. **Windows 10** (Version 1903 / 64-bit and newer)
3. **Windows Server 2022 & Windows Server 2025**
4. **Intel (x64), AMD (x64), and ARM64 Windows Devices** (Laptops, Desktops, Surface, Qualcomm Snapdragon PCs)

---

## 🧠 2. AI Models & Brains (Local & Cloud)

5. **Hermes Series** (Nous Hermes 2, Hermes 3, OpenHermes)
6. **OpenClaw & OpenCode Models**
7. **Qwen & Qwen-Coder** (Qwen 2.5, Qwen 2.5 Coder 7B, 14B, 32B, 72B)
8. **DeepSeek** (DeepSeek-V3, DeepSeek-R1, DeepSeek-Coder)
9. **Meta Llama** (Llama 3, Llama 3.1, Llama 3.2, Llama 3.3, CodeLlama)
10. **Mistral & Mixtral** (Mistral 7B, Mixtral 8x7B, Devstral, Codestral)
11. **Anthropic Claude** (Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus)
12. **OpenAI GPT & Codex** (GPT-4o, GPT-4o-mini, o1, o3-mini, Codex)
13. **Google Gemini** (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0)
14. **Custom Weights** (Any local GGUF, SafeTensors, or fine-tuned model)

---

## 🖥️ 3. Local Model Runners & Inference Engines

15. **Ollama** (Runs offline local models via `http://127.0.0.1:11434`)
16. **LM Studio** (Local OpenAI-compatible API on port `1234`)
17. **llama.cpp** (Fast C/C++ inference engine)
18. **vLLM** (High-throughput local LLM server)
19. **Jan.ai / LocalAI / Text-Generation-WebUI**

---

## ⌨️ 4. AI Coding & "Vibe Coding" Tools & IDEs

20. **Claude CLI & Claude Code** (Anthropic's terminal agent)
21. **Codex CLI & OpenAI CLI tools**
22. **Cursor & Windsurf IDEs**
23. **Aider** (AI pair programming terminal)
24. **Continue.dev** (VS Code and JetBrains extension)
25. **Cline / Roo-Cline** (Autonomous coding in VS Code)
26. **GPT-Pilot / Pythagora / OpenCodeInterpreter / Goose**

---

## 🤖 5. Autonomous Agent Frameworks & SDKs

27. **OpenClaw**
28. **AutoGPT**
29. **CrewAI**
30. **LangChain & LangGraph Agents**
31. **Microsoft AutoGen & Semantic Kernel**
32. **LlamaIndex Agents**
33. **Custom Python, Node.js, Go, or Rust AI scripts**

---

## 🔌 6. Protocols, Tool Interfaces & Standards

34. **Model Context Protocol (MCP)** (Anthropic's open tool-use standard)
35. **Windows PowerShell** (Desktop 5.1 & PowerShell 7.x)
36. **Windows Command Prompt (`cmd.exe`)**
37. **Standard REST API / HTTP Tool Calling** (`http://127.0.0.1:7777/api/v1/tools/invoke`)
38. **Windows Named Pipe IPC** (`\\.\pipe\GracefulOS`)
39. **Local Filesystem & Git Repositories** (Protected via NTFS ACL sandboxing)

---

## 🛠️ 7. Programming Languages & Development Stacks

40. **Python** (3.10, 3.11, 3.12, 3.13, 3.14+)
41. **JavaScript & TypeScript** (Node.js, Bun, Deno)
42. **Rust, Go, C/C++, and C# (.NET)**

---

## 🚀 How to Run Any Tool with GracefulOS
You can run and protect any AI script or tool automatically using:

```powershell
# Run GracefulOS control plane
.\RUN_ME.bat

# Launch and protect any tool or script:
python graceful.py run claude
python graceful.py run codex
python graceful.py run python my_agent.py
```
