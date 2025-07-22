import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import optimizer
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SQLRequest(BaseModel):
    query: str
    use_ai: bool = False
    dialect: str = "PostgreSQL"

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return """
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <title>SQLGenie - SQL Optimizer</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f7f7fa; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px; }
            h1 { text-align: center; color: #3a3a5a; }
            textarea { width: 100%; min-height: 120px; font-size: 1em; padding: 10px; border-radius: 4px; border: 1px solid #ccc; margin-bottom: 16px; }
            button { background: #4f8cff; color: #fff; border: none; padding: 12px 24px; border-radius: 4px; font-size: 1em; cursor: pointer; transition: background 0.2s; }
            button:hover { background: #3466c2; }
            .result { margin-top: 24px; background: #f0f4ff; border-left: 4px solid #4f8cff; padding: 16px; border-radius: 4px; min-height: 40px; font-family: monospace; white-space: pre-wrap; }
            .error { color: #c00; margin-top: 16px; }
            .options { margin-bottom: 16px; }
            label { margin-right: 12px; }
        </style>
    </head>
    <body>
        <div class=\"container\">
            <h1>SQLGenie</h1>
            <div class=\"options\">
                <label><input type=\"checkbox\" id=\"useAI\"> Use AI Optimization</label>
                <label>Dialect:
                    <select id=\"dialect\">
                        <option>PostgreSQL</option>
                        <option>Snowflake</option>
                        <option>BigQuery</option>
                        <option>MySQL</option>
                    </select>
                </label>
            </div>
            <textarea id=\"sqlInput\" placeholder=\"Paste your SQL query here...\"></textarea>
            <button onclick=\"optimizeSQL()\">Optimize SQL</button>
            <div id=\"result\" class=\"result\"></div>
            <div id=\"error\" class=\"error\"></div>
        </div>
        <script>
            async function optimizeSQL() {
                document.getElementById('error').innerText = '';
                document.getElementById('result').innerText = '';
                const query = document.getElementById('sqlInput').value;
                const use_ai = document.getElementById('useAI').checked;
                const dialect = document.getElementById('dialect').value;
                try {
                    const response = await fetch('/optimize', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query, use_ai, dialect })
                    });
                    const data = await response.json();
                    if (!response.ok) {
                        document.getElementById('error').innerText = data.detail || 'Optimization failed.';
                    } else {
                        document.getElementById('result').innerText = data.optimized_sql;
                    }
                } catch (err) {
                    document.getElementById('error').innerText = 'Network or server error.';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/optimize")
async def optimize_sql_endpoint(req: SQLRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="SQL query cannot be empty.")
    if req.use_ai:
        if not OPENAI_API_KEY:
            return JSONResponse(status_code=500, content={"detail": "OpenAI API key not set on server."})
        try:
            prompt = f"Rewrite this SQL query to be optimized and more efficient for execution on {req.dialect}.\nSQL: {query}"
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful SQL optimization assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.2
            )
            ai_sql = response.choices[0].message.content.strip()
            return {"optimized_sql": ai_sql}
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": f"AI Optimization error: {str(e)}"})
    try:
        optimized = optimizer.optimize_sql(query)
        return {"optimized_sql": optimized}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Optimization error: {str(e)}"}) 