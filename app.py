import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    tasks = load_tasks()
    tasks.append({
        "name": data["task"],
        "priority": "medium",
        "notes": "",
        "completed": False
    })
    save_tasks(tasks)
    return jsonify({"success": True, "tasks": tasks})

@app.route("/remove", methods=["POST"])
def remove_task():
    data = request.get_json()
    tasks = load_tasks()
    tasks.pop(data["index"])
    save_tasks(tasks)
    return jsonify({"success": True, "tasks": tasks})

@app.route("/complete", methods=["POST"])
def complete_task():
    data = request.get_json()
    tasks = load_tasks()
    tasks[data["index"]]["completed"] = True
    save_tasks(tasks)
    return jsonify({"success": True, "tasks": tasks})

@app.route("/undo", methods=["POST"])
def undo_task():
    data = request.get_json()
    tasks = load_tasks()
    tasks[data["index"]]["completed"] = False
    save_tasks(tasks)
    return jsonify({"success": True, "tasks": tasks})

@app.route("/update", methods=["POST"])
def update_task():
    data = request.get_json()
    tasks = load_tasks()
    index = data["index"]
    tasks[index]["priority"] = data["priority"]
    tasks[index]["notes"] = data["notes"]
    save_tasks(tasks)
    return jsonify({"success": True, "tasks": tasks})

if __name__ == "__main__":
    app.run(debug=True)