import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

def load_tasks():
    response = supabase.table("tasks").select("*").order("created_at").execute()
    return response.data

def task_to_dict(task):
    return {
        "name": task["name"],
        "priority": task["priority"],
        "notes": task["notes"],
        "completed": task["completed"]
    }

@app.route("/")
def index():
    tasks = [task_to_dict(t) for t in load_tasks()]
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    supabase.table("tasks").insert({
        "name": data["task"],
        "priority": "medium",
        "notes": "",
        "completed": False
    }).execute()
    tasks = [task_to_dict(t) for t in load_tasks()]
    return jsonify({"success": True, "tasks": tasks})

@app.route("/remove", methods=["POST"])
def remove_task():
    data = request.get_json()
    tasks = load_tasks()
    task_id = tasks[data["index"]]["id"]
    supabase.table("tasks").delete().eq("id", task_id).execute()
    tasks = [task_to_dict(t) for t in load_tasks()]
    return jsonify({"success": True, "tasks": tasks})

@app.route("/complete", methods=["POST"])
def complete_task():
    data = request.get_json()
    tasks = load_tasks()
    task_id = tasks[data["index"]]["id"]
    supabase.table("tasks").update({"completed": True}).eq("id", task_id).execute()
    tasks = [task_to_dict(t) for t in load_tasks()]
    return jsonify({"success": True, "tasks": tasks})

@app.route("/undo", methods=["POST"])
def undo_task():
    data = request.get_json()
    tasks = load_tasks()
    task_id = tasks[data["index"]]["id"]
    supabase.table("tasks").update({"completed": False}).eq("id", task_id).execute()
    tasks = [task_to_dict(t) for t in load_tasks()]
    return jsonify({"success": True, "tasks": tasks})

@app.route("/update", methods=["POST"])
def update_task():
    data = request.get_json()
    tasks = load_tasks()
    task_id = tasks[data["index"]]["id"]
    supabase.table("tasks").update({
        "priority": data["priority"],
        "notes": data["notes"]
    }).eq("id", task_id).execute()
    tasks = [task_to_dict(t) for t in load_tasks()]
    return jsonify({"success": True, "tasks": tasks})

if __name__ == "__main__":
    app.run(debug=True)