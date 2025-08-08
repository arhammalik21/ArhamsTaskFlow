from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for tasks (we’ll use a database later)
tasks = []
next_id = 1


@app.route("/", methods=["GET", "POST"])
def home():
    global next_id
    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            tasks.append({"id": next_id, "text": task_text})
            next_id += 1
        return redirect(url_for('home'))

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for('home'))



@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

