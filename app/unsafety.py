
import subprocess
import os
from fastapi import APIRouter, Query, HTTPException
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
    # 安全な例: ユーザー入力は Python リテラルとしてのみ評価し、任意コード実行を防止
    try:
        result = ast.literal_eval(user_code)
    except (ValueError, SyntaxError):
        raise HTTPException(status_code=400, detail="Invalid expression")
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
    # 安全な例: 正規化とベースディレクトリチェックでパストラバーサルを防止
    base_path = "/var/data"
    filepath = os.path.normpath(os.path.join(base_path, filename))
    # ベースディレクトリ外へのアクセスを拒否
    if os.path.commonpath([base_path, filepath]) != base_path:
        raise HTTPException(status_code=400, detail="Invalid file path")
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
