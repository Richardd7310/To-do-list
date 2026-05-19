from flask import Blueprint, request, jsonify, render_template
from app.database import get_db_connection

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

#Get all tasks
@main.route("/tasks", methods=["GET"])
def get_tasks():

    conn = get_db_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return jsonify([
        dict(task) for task in tasks
    ])

@main.route("/tasks", methods=["POST"])
def add_tasks():

    data = request.get_json()

    title = data.get("title")

    if not title:
        return {"error": "Title is required"}, 400

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO tasks (title) VALUES (?)",
       (title,)
    )

    conn.commit()
    conn.close()


    return{"message": "Task successfully added"}, 201

@main.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (id,)
    ).fetchone()

    if not task:
        conn.close()
        return {"error": "Task not found"}, 404

    conn.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Task deleted successfully"}, 200