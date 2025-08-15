from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from datetime import date

app = Flask(__name__)
app.secret_key = 'supersecretkey'
csrf = CSRFProtect(app)

# ----- Task Form -----
class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[], default=None)

# ----- Data -----
tasks = []
next_id = 1

# ----- Routes -----
@app.route("/", methods=["GET", "POST"])
def index():
    global next_id
    form = TaskForm()
    if form.validate_on_submit():
        task_name = form.task.data.strip()
        due_date = form.due_date.data
        tasks.append({
            "id": next_id,
            "name": task_name,
            "completed": False,
            "due_date": due_date
        })
        next_id += 1
        flash("Task added!", "success")
        return redirect(url_for("index"))
    return render_template("index.html", tasks=tasks, form=form, current_date=date.today())

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404)
    form = TaskForm(obj=task)
    if request.method == "POST" and form.validate_on_submit():
        task["name"] = form.task.data.strip()
        task["due_date"] = form.due_date.data
        flash("Task updated!", "info")
        return redirect(url_for("index"))
    return render_template("edit.html", form=form, task=task)

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
        abort(404)
    tasks = updated_tasks
    flash("Task deleted.", "warning")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
