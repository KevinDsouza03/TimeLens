from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Dict
from datetime import datetime
import pandas as pd

app = FastAPI()

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "focus.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/program-insights")
async def get_program_insights():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM program_insights", conn)
    conn.close()
    
    # Convert timedelta strings to minutes for easier visualization
    df['total_time'] = pd.to_timedelta(df['total_time']).dt.total_seconds() / 60
    df['average_time'] = pd.to_timedelta(df['average_time']).dt.total_seconds() / 60
    
    return df.to_dict(orient='records')

@app.get("/api/focus-logs/today")
async def get_today_focus_logs():
    conn = get_db_connection()
    today = datetime.now().strftime("%m/%d/%Y")
    df = pd.read_sql_query(
        "SELECT * FROM focus_logs WHERE date = ? ORDER BY time",
        conn,
        params=(today,)
    )
    conn.close()
    return df.to_dict(orient='records')

@app.get("/api/focus-logs/timeline")
async def get_focus_timeline():
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT date, program, 
               COUNT(*) as switches,
               COUNT(DISTINCT program) as unique_programs
        FROM focus_logs 
        GROUP BY date
        ORDER BY date
    """, conn)
    conn.close()
    return df.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)