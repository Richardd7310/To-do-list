from app.database import get_db_connection

conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Database initialized!")