MACROMATE - SCRIPT DOCUMENTATION
===============================

Overview
--------
MacroMate is an interactive command-line assistant for macroeconomic research.
The main script, agent.py, uses a local Ollama model through LangChain, Tavily
for web searches, JSON for research notes, and SQLite for conversation memory.
It covers topics such as inflation, GDP, interest rates, monetary and fiscal
policy, unemployment, and economic growth.

Requirements
------------
- Python 3 and pip, with versions compatible with requirements.txt.
- Ollama installed and running locally.
- The Ollama model configured in agent.py: gemma4:e2b.
- A Tavily API key and an internet connection for web searches.
- Write access to the project directory for notes and conversation history.

Python dependencies are listed in requirements.txt. Their versions are not
pinned, so compatibility can vary between installations.

Setup
-----
1. Open a terminal in the project directory.

2. Create and activate a virtual environment:

   macOS / Linux:
     python3 -m venv .venv
     source .venv/bin/activate

   Windows PowerShell:
     py -m venv .venv
     .venv\Scripts\Activate.ps1

3. Install the dependencies:

     python -m pip install -r requirements.txt

4. Start Ollama using its application or, in a separate terminal:

     ollama serve

   If Ollama is already running, use the existing instance.

5. Download the configured model:

     ollama pull gemma4:e2b

   If that model tag is unavailable in your Ollama installation, choose an
   available model that supports tool calling, download it, and update the
   model argument in agent.py to match its exact tag.

6. Create a file named .env beside agent.py containing:

     TAVILY_API_KEY=your_tavily_api_key_here

   Use your own key in place of the placeholder. Keep this file private.
   The script exits at startup if TAVILY_API_KEY is missing. An existing
   environment variable can also supply the key.

Run the assistant
-----------------
With the virtual environment activated, run:

  python agent.py

Enter a question at the "You:" prompt. The assistant prints its response after
processing the question and any tool calls. Empty input is ignored.
Type quit or exit to end the session; these commands are case-insensitive.

Example prompts:
  Explain how higher interest rates affect inflation.
  Find the latest euro area inflation release and include its source.
  Save a note titled "Interest rates" summarizing your explanation.
  Show my saved research notes.

The assistant is instructed to search for recent statistics and news, prefer
official sources, distinguish observations from forecasts, and include source
URLs and publication dates when available. These are model instructions, so
check the cited sources when accuracy matters.

Tools and saved data
--------------------
Web search:
  TavilySearch uses basic search and requests up to three results per search.
  Search queries are sent to the external Tavily service. Model inference runs
  through local Ollama; the complete workflow is not offline.

Save note:
  save_note(title, content) appends a note to notes.json. Each note contains
  title, content, and saved_at (a UTC timestamp). The assistant is instructed
  to save only when explicitly asked. The file is created on the first save.

Read notes:
  read_notes() returns the contents of notes.json, or reports that no notes
  have been saved if the file does not exist.

Conversation memory:
  conversation.sqlite stores LangGraph checkpoints. Every session uses the
  fixed thread ID "macro-study", allowing follow-up conversations across
  restarts. The script provides no separate-user or separate-session selector.
  SQLite may also create conversation.sqlite-wal and conversation.sqlite-shm.

All data paths are relative to agent.py, regardless of the terminal's current
directory. Notes and conversation history are stored locally without
application-level encryption. The current .gitignore excludes .env and .venv,
but does not exclude notes.json or the SQLite files; check what you commit.

Configuration
-------------
Edit agent.py to change these settings:

  ChatOllama model     gemma4:e2b
  temperature         0
  num_ctx             4096 tokens
  Tavily max_results  3
  search_depth        basic
  thread_id           macro-study
  recursion_limit     15 graph execution steps per invocation

SYSTEM_PROMPT controls the assistant's research behavior. Its date is taken
from the computer's local date when the script starts. format_response()
converts string responses or text content blocks into printable terminal text.

Troubleshooting
---------------
Missing TAVILY_API_KEY in .env:
  Add the key to .env beside agent.py or set the environment variable, then
  restart the script.

Cannot connect to Ollama:
  Start Ollama and check that its local service is accessible. Run ollama list
  to confirm that the configured model is installed.

Model missing or tool calls fail:
  Check the exact model tag and its tool-calling support. If you change models,
  update agent.py as well. The optional test_gemma.py script tests a basic
  model response with python test_gemma.py; it does not test tools or Tavily.

Web search fails:
  Check your internet connection, Tavily key, and account limits.

Import errors:
  Activate the virtual environment and reinstall requirements.txt. Confirm
  that the installed package versions support the imports used by agent.py.

Invalid notes.json or file errors:
  Back up the file before editing it. save_note expects notes.json to contain
  a valid JSON list and rewrites that list when adding a note. Check write
  permissions and avoid running multiple instances that save simultaneously.

Execution limit reached:
  Try a narrower question. recursion_limit limits graph steps, not elapsed
  time. Review the agent's behavior before increasing it.

Errors during agent invocation are printed and the input loop continues.
Startup errors and interrupted terminal input are not handled by that loop.

Project files
-------------
agent.py             Main assistant script.
requirements.txt     Python dependencies.
.env                 Local Tavily credentials (create during setup).
notes.json           Research notes (created on first save).
conversation.sqlite  Persistent conversation checkpoints.
test_gemma.py        Optional basic Ollama model check, if present locally.
README.txt           This documentation.
