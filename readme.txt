SQLGenie - SQL Optimizer App
===========================

An app for data engineers to analyze and optimize SQL queries for better performance.

---

## Features
- Paste or type a SQL query and get an optimized version.
- Detects anti-patterns like SELECT *, unnecessary DISTINCT, and missing WHERE clauses.
- Provides suggestions for query improvements.
- Simple web interface (FastAPI backend, HTML/JS frontend).
- Auto-commit and push changes to GitHub every 5 minutes (optional).

---

## Setup Instructions

1. **Clone the repository**
   (If not already cloned)
   ```
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```
   uvicorn main:app --reload
   ```
   - The app will be available at: http://127.0.0.1:8000/

4. **Use the app**
   - Paste your SQL query in the textarea.
   - Click "Optimize SQL".
   - View the optimized query and suggestions below.

---

## Auto Git Push (Optional)

To automatically commit and push changes every 5 minutes:

1. Make sure your git remote is set and authentication is configured.
2. Run:
   ```
   python auto_git_push.py
   ```

---

## Tech Stack
- Python (FastAPI, sqlparse)
- Uvicorn (ASGI server)
- HTML, CSS, JavaScript (frontend)

---

## Future Features
- AI-powered SQL optimization (GPT-4, Claude, etc.)
- EXPLAIN plan upload and analysis
- Support for multiple SQL dialects
- Schema-aware suggestions

---

## License
MIT (or specify your license) 