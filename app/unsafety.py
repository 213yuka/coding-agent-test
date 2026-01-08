
import subprocess
import os
from fastapi import APIRouter, Query
from sqlalchemy import text
from app.database import engine
import ast

router = APIRouter()

@router.get("/unsafe/cmd")
def unsafe_command(cmd: str = Query("echo hello")):
    # NG例: shell=Trueでユーザー入力を直接渡す（コマンドインジェクション）
    out = subprocess.check_output(cmd, shell=True)
    return {"out": out.decode()}

@router.get("/unsafe/eval")
def run_eval(user_code: str = Query("1+1")):
    # NG例: evalでユーザー入力を評価（任意コード実行）
    result = eval(user_code)
    return {"result": result}

@router.get("/unsafe/sql")
def unsafe_sql(task_id: str = Query("1")):
    # NG例: SQLインジェクション（ユーザー入力を直接クエリに埋め込み）
    query = text(f"SELECT * FROM tasks WHERE id = {task_id}")
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = [dict(row._mapping) for row in result]
    return {"tasks": rows}

@router.get("/unsafe/file")
def read_file_unsafe(filename: str = Query("data.txt")):
    # NG例: パストラバーサル（ユーザー入力でファイルパスを構築）
    filepath = os.path.join("/var/data", filename)
    with open(filepath, "r") as f:
        content = f.read()
    return {"content": content}

@router.get("/unsafe/exec")
def unsafe_exec(code: str = Query("'hello'")):
    # safer example: evaluate only Python literals instead of executing arbitrary code
    try:
        result = ast.literal_eval(code)
    except (ValueError, SyntaxError):
        return {"error": "Invalid expression"}
    return {"result": result}
