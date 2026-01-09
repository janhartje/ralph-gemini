Ralph - Gemini CLI Edition

![Ralph](ralph.webp)

Ralph is an autonomous AI agent loop that runs **Gemini CLI** repeatedly until all PRD items are complete. Each iteration is a fresh instance with clean context. Memory persists via git history, `progress.txt`, and `prd.json`.

Based on [Geoffrey Huntley's Ralph pattern](https://ghuntley.com/ralph/).

## Prerequisites

- [Gemini CLI](https://github.com/google/gemini-cli-experimental) installed and authenticated
  - `npm install -g gemini-chat-cli` (or similar depending on distribution)
  - `gemini login` or `GOOGLE_API_KEY` set
- `jq` installed (`brew install jq` on macOS)
- A git repository for your project
- Python 3 installed (for the wrapper)

## Setup

### Option 1: Copy to your project

Copy the ralph files into your project:

```bash
# From your project root
mkdir -p scripts/ralph
cp /path/to/ralph/ralph.sh scripts/ralph/
cp /path/to/ralph/ralph_gemini.py scripts/ralph/
cp /path/to/ralph/prompt.md scripts/ralph/
chmod +x scripts/ralph/ralph.sh
```

## Workflow

### 1. Create a PRD

Use a tool or manual process to create a `prd.json` file. See `prd.json.example` for the required format.

### 2. Run Ralph

```bash
./scripts/ralph/ralph.sh [max_iterations]
```

Default is 10 iterations.

Ralph will:
1.  Read the context (`prd.json`, `progress.txt`, `prompt.md`)
2.  Spawn a `gemini` CLI instance using the Python wrapper.
3.  **Autonomous Execution**: Gemini uses native tools (File Read/Write, Shell Execution) to:
    *   Pick the next task.
    *   Implement code changes.
    *   Run tests/checks.
    *   Commit changes using `git`.
4.  Repeat until all stories pass or max iterations reached.

## Key Files

| File | Purpose |
|------|---------|
| `ralph.sh` | Main entry point loop. |
| `ralph_gemini.py` | Python wrapper that orchestrates the `gemini` CLI in YOLO mode. |
| `prompt.md` | System instructions for the agent (using Native Tools). |
| `prd.json` | User stories with `passes` status (the task list). |
| `progress.txt` | Append-only learnings for future iterations. |

## Critical Concepts

### Native Tools (YOLO Mode)

Ralph now runs in **YOLO Mode**, meaning the agent has full, unprompted access to:
*   **File System**: Reading and writing files directly.
*   **Shell**: executing `git` commands, running tests, etc.

### Each Iteration = Fresh Context

Each iteration spawns a **new Gemini context**. The only memory between iterations is:
- Git history (commits from previous iterations)
- `progress.txt` (learnings and context)
- `prd.json` (which stories are done)

### Stop Condition

When all stories have `passes: true`, Ralph outputs `RALPH_COMPLETE` and the loop exits.

## References

- [Geoffrey Huntley's Ralph article](https://ghuntley.com/ralph/)
- [Gemini CLI Documentation](https://github.com/google/gemini-cli-experimental)
