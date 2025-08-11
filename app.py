from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production!
csrf = CSRFProtect(app)

class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])

tasks = []
next_id = 1  # Unique task ID for every new task

@app.route("/", methods=["GET", "POST"])
def index():
    global next_id
    form = TaskForm()
    if form.validate_on_submit():
        task_name = form.task.data.strip()
        tasks.append({
            "id": next_id,
            "name": task_name,
            "completed": False
        })
        next_id += 1
        flash("Task added!", "success")
        return redirect(url_for("index"))
    return render_template("index.html", tasks=tasks, form=form)

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            flash("Task marked as complete!", "info")
            break
    else:
        abort(404)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        abort(404)  # Task not found, show 404 page
    tasks = updated_tasks
    flash("Task deleted.", "warning")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

