import os
import pymysql
from fastapi import FastAPI

app = FastAPI()


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", ""),  # 💡 Fallback to empty string resolves the Type Error
        database=os.getenv("DB_NAME", "appdb"),
        cursorclass=pymysql.cursors.DictCursor
    )



@app.get("/")
def home():
    return {"message": "FastAPI is running with Docker!"}


@app.get("/db-check")
def check_database():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION() AS version")
            result = cursor.fetchone()

        return {
            "database": "connected",
            "mysql_version": result["version"] if result is not None else None
        }
    finally:
        connection.close()


@app.get("/health")
def health():
    return {"status": "healthy"}