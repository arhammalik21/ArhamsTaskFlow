from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
task_id_counter = 1

@app.route("/", methods=["GET", "POST"])
def index():
    global task_id_counter
    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            tasks.append({"id": task_id_counter, "text": task_text, "completed": False})
            task_id_counter += 1
        return redirect(url_for("index"))
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = not t["completed"]   # toggle complete/undo
            break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

