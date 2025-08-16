# Import necessary modules
from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from datetime import date

# ----- Initialize Flask and CSRF protection -----
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production!
csrf = CSRFProtect(app)            # Enable CSRF protection for secure forms

# ----- Define the form for creating/editing tasks -----
class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])  # Task name input
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[], default=None)  # Optional due date
    category = SelectField('Category', choices=[
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Study', 'Study'),
        ('Other', 'Other')
    ])  # Dropdown for Category

# ----- In-memory data storage for tasks and unique IDs -----
tasks = []      # List to store all tasks
next_id = 1     # Counter for assigning unique IDs to tasks

# ----- Homepage: add new tasks and show all tasks -----
@app.route("/", methods=["GET", "POST"])
def index():
    global next_id
    form = TaskForm()
    if form.validate_on_submit():  # If user submitted the form and it's valid
        # Get data from the form fields
        task_name = form.task.data.strip()
        due_date = form.due_date.data
        category = form.category.data
        # Create new task and add to list
        tasks.append({
            "id": next_id,
            "name": task_name,
            "completed": False,
            "due_date": due_date,
            "category": category
        })
        next_id += 1
        flash("Task added!", "success")
        return redirect(url_for("index"))  # Prevent duplicate form submission on reload
    # Show tasks list: pass tasks, form, and today's date to template
    return render_template("index.html", tasks=tasks, form=form, current_date=date.today())

# ----- Edit an individual task using its ID -----
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # Find the right task by ID
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404)
    form = TaskForm(obj=task)  # Pre-fills the form with current task data
    if request.method == "POST" and form.validate_on_submit():
        task["name"] = form.task.data.strip()
        task["due_date"] = form.due_date.data
        task["category"] = form.category.data
        flash("Task updated!", "info")
        return redirect(url_for("index"))
    return render_template("edit.html", form=form, task=task)

# ----- Mark a task as complete (no longer incomplete) -----
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

# ----- Delete a task by ID -----
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    updated_tasks = [task for task in tasks if task["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        abort(404)  # No task deleted, ID not found
    tasks = updated_tasks
    flash("Task deleted.", "warning")
    return redirect(url_for("index"))

# ----- Entry point -----
if __name__ == "__main__":
    app.run(debug=True)  # Start app for development (auto-reloads on changes)
