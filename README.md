# webcrawler

A small web crawler service implemented in Python. This README explains how to set up a local dev environment and run the app.

## Prerequisites
- Python 3.11 installed
- pip
- (optional) Docker for containerized runs

## 1. Create a virtual environment
Use a project-local venv (recommended):
```bash
python3.11 -m venv .venv
```

## 2. Activate the virtual environment
```bash
# macOS / Linux (bash/zsh)
source .venv/bin/activate

# Windows (PowerShell)
. .venv/Scripts/Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat
```

If activation fails, run: python -m venv .venv then try again, and ensure execution policy allows scripts on Windows PowerShell (`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`).

## 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment variables
Create a `.env` or set PORT directly. Example `.env`:
```
PORT=8000
```

## 5. Run the app (development)
Linux / macOS:
```bash
export PORT=8000
uvicorn main:app --host 0.0.0.0 --port $PORT --reload
```

Windows (PowerShell):
```powershell
$env:PORT = "8000"
uvicorn main:app --host 0.0.0.0 --port $env:PORT --reload
```

Notes:
- Use `--host 0.0.0.0` when running inside a container or wanting external access.
- Remove `--reload` in production.

## 6. Architecture & design docs
For design considerations for handling a large number of URLs (scalability, deduplication, queueing, sharding, rate limiting) see:
- docs/design_docs.md
- docs/part3.md (POC and execution plan)

## Troubleshooting
- If dependency installation fails, ensure you are using the virtual environment's pip: `python -m pip install -r requirements.txt`.
- If ports are in use, pick an available PORT or stop the conflicting service.
