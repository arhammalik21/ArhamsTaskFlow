from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for tasks (we’ll use a database later)
tasks = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_content = request.form.get("task")
        if task_content:
            tasks.append(task_content)
        return redirect(url_for("home"))
    return render_template("index.html", tasks=tasks)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

