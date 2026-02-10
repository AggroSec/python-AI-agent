# Python AI Agent

A custom AI agent built in Python using the **Google Gemini API** as part of the Boot.dev "Build an AI Agent with Python" course. The agent follows a **ReAct-style reasoning loop** (Reason → Act → Observe) to complete tasks by calling tools, processing results, and iterating until a final answer is reached.

**Important – Educational Use Only**

This is a **learning project** from the Boot.dev AI Agent course.

- **Not production-ready** — lacks full security hardening, input sanitization, rate limiting, authentication, robust error recovery, and safety features.
- **Do NOT deploy publicly**, run in untrusted environments, or share for others to use without significant review and improvements.
- Built for educational purposes only. Use at your own risk.
- See the course warning: "Do not give this program to others for them to use! It doesn't have all the security and safety features that a production AI agent would have."

Feel free to view, fork for personal learning, or reference — but please **do not** run it as-is in any real or shared context.

## How It Works

The agent implements a classic **ReAct loop**:

1. **User prompt** → sent to Gemini with a system instruction and tool definitions.
2. **Model response** → either:
   - Final text answer (done)
   - Function/tool call(s) → agent executes them via `call_function()`
3. **Tool results** → fed back as new "user" messages in the conversation history.
4. **Repeat** until no more tool calls are needed → final answer returned.

### Key Features Implemented

- **Tool/Function Calling** — defined via Gemini's `FunctionDeclaration` schema (with correct `items` for array parameters).
- **Conversation History Management** — accumulates messages properly to avoid repetition loops.
- **Path Security** — prevents directory traversal and restricts writes to the allowed working directory using `os.path.commonpath`.
- **Verbose Mode** — shows token usage, function calls, and results for debugging.
- **Error Handling** — catches API and runtime errors, returns user-friendly messages.

### Tech Stack

- Python 3.13
- Google Gemini API (via `google-generativeai` SDK)
- `dotenv` for API key management
- `argparse` for CLI interface
- `os` / `pathlib` for safe file/directory handling
- ReAct-style agent loop with history persistence

## Setup & Running

1. Clone the repo:
   ```bash
   git clone https://github.com/AggroSec/python-AI-agent.git
   cd python-AI-agent
   ```
2. Install dependencies:
```bash
uv sync #needs uv project management, see https://github.com/astral-sh/uv?tab=readme-ov-file#installation
```
3. Create a .env file in the root:
```text
GEMINI_API_KEY=your-api-key-here
```
4. Run the agent:
```bash
uv run main.py "Explain how the calculator renders the result to the console"
uv run main.py "Explain how the calculator renders the result to the console" --verbose # verbose used to see more information like token usage, and full function calls with parameters
```

## License

MIT License

See LICENSE for full text.

Made with curiosity, persistence, and a lot of debugging — for learning purposes only.

Built while working through Boot.dev's AI Agent curriculum.
