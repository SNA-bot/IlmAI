from flask import Flask, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "ilm_ai_secret_key"


@app.route("/")
def home():
    return """
    <h1>Welcome to Ilm+AI</h1>

    <a href="/register">Student Registration</a>

    <br><br>

    <a href="/login">Student Login</a>

    <br><br>

    <a href="/teacher_login">Teacher Login</a>
    """


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        student_class = request.form["class"]
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("ilm_ai.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO students
            (name, class_name, username, password)
            VALUES (?, ?, ?, ?)
            """, (name, student_class, username, password))

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()

            return """
            <h1>Registration Failed</h1>

            <p>This username already exists.</p>

            <a href="/register">Try Again</a>
            """

        conn.close()

        return f"""
        <h1>Registration Successful!</h1>

        <p>Welcome {name}.</p>

        <p>You have been registered as a {student_class} student.</p>

        <p>Your username is: {username}</p>

        <a href="/login">Proceed to Login</a>
        """

    return """
    <h1>Student Registration</h1>

    <form method="POST">

        Name:<br>
        <input type="text" name="name"><br><br>

        Class:<br>
        <input type="text" name="class"><br><br>

        Username:<br>
        <input type="text" name="username"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <input type="submit" value="Register">

    </form>

    <br>

    <a href="/">Back Home</a>
    """


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("ilm_ai.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE username=? AND password=?
        """, (username, password))

        student = cursor.fetchone()

        conn.close()

        if student:

            session["username"] = username
            session["name"] = student[1]
            session["class_name"] = student[2]

            return redirect("/dashboard")

        else:
            return """
            <h1>Login Failed</h1>

            <p>Invalid username or password.</p>

            <a href="/login">Try Again</a>
            """

    return """
    <h1>Student Login</h1>

    <form method="POST">

        Username:<br>
        <input type="text" name="username"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <input type="submit" value="Login">

    </form>

    <br>

    <a href="/">Back Home</a>
    """


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    return f"""
    <h1>Student Dashboard</h1>

    <p>Welcome {session['name']}</p>

    <p>Class: {session['class_name']}</p>

    <ul>
        <li><a href="/courses">My Courses</a></li>
        <li><a href="/assignments">My Assignments</a></li>
        <li><a href="/cbt">Take CBT Test</a></li>
        <li><a href="/results">My Results</a></li>
    </ul>

    <a href="/logout">Logout</a>
    """


@app.route("/courses")
def courses():

    if "username" not in session:
        return redirect("/login")

    return """
    <h1>My Courses</h1>

    <ul>
        <li>Mathematics</li>
        <li>English Language</li>
        <li>Physics</li>
        <li>Chemistry</li>
        <li>Programming with Python</li>
    </ul>

    <a href="/dashboard">Back Dashboard</a>
    """


@app.route("/assignments")
def assignments():

    if "username" not in session:
        return redirect("/login")

    return """
    <h1>My Assignments</h1>

    <ul>
        <li>Mathematics Assignment 1</li>
        <li>English Essay</li>
        <li>Python Programming Exercise</li>
    </ul>

    <a href="/dashboard">Back Dashboard</a>
    """


@app.route("/cbt", methods=["GET", "POST"])
def cbt():

    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":

        score = 0

        if request.form["q1"] == "Abuja":
            score += 1

        if request.form["q2"] == "4":
            score += 1

        if request.form["q3"] == "Python":
            score += 1

        if request.form["q4"] == "Allah":
            score += 1

        if request.form["q5"] == "Robot":
            score += 1

        percentage = (score / 5) * 100

        conn = sqlite3.connect("ilm_ai.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO results
        (username, subject, score, total)
        VALUES (?, ?, ?, ?)
        """, (
            session["username"],
            "General Knowledge",
            score,
            5
        ))

        conn.commit()
        conn.close()

        return f"""
        <h1>CBT Result</h1>

        <p>Your Score: {score}/5</p>

        <p>Percentage: {percentage}%</p>

        <a href="/results">View My Results</a>

        <br><br>

        <a href="/cbt">Take Test Again</a>
        """

    return """
    <h1>Ilm+AI CBT Test</h1>

    <form method="POST">

    <h3>1. What is the capital of Nigeria?</h3>
    <input type="radio" name="q1" value="Lagos"> Lagos<br>
    <input type="radio" name="q1" value="Abuja"> Abuja<br>
    <input type="radio" name="q1" value="Kano"> Kano<br><br>

    <h3>2. What is 2 + 2?</h3>
    <input type="radio" name="q2" value="3"> 3<br>
    <input type="radio" name="q2" value="4"> 4<br>
    <input type="radio" name="q2" value="5"> 5<br><br>

    <h3>3. Which programming language are we learning?</h3>
    <input type="radio" name="q3" value="Java"> Java<br>
    <input type="radio" name="q3" value="Python"> Python<br>
    <input type="radio" name="q3" value="C++"> C++<br><br>

    <h3>4. Who should always come first according to Ilm+AI philosophy?</h3>
    <input type="radio" name="q4" value="Technology"> Technology<br>
    <input type="radio" name="q4" value="Money"> Money<br>
    <input type="radio" name="q4" value="Allah"> Allah<br><br>

    <h3>5. Which of these is used in Robotics?</h3>
    <input type="radio" name="q5" value="Robot"> Robot<br>
    <input type="radio" name="q5" value="Tree"> Tree<br>
    <input type="radio" name="q5" value="River"> River<br><br>

    <input type="submit" value="Submit CBT">

    </form>
    """


@app.route("/results")
def results():

    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("ilm_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject, score, total
    FROM results
    WHERE username=?
    """, (session["username"],))

    results_data = cursor.fetchall()

    conn.close()

    html = "<h1>My Results</h1>"

    if results_data:
        for result in results_data:
            html += f"<p>{result[0]} : {result[1]}/{result[2]}</p>"
    else:
        html += "<p>No results available yet.</p>"

    html += '<br><br><a href="/dashboard">Back Dashboard</a>'

    return html


@app.route("/logout")
def logout():

    session.clear()

    return """
    <h1>You have been logged out successfully.</h1>

    <a href="/login">Login Again</a>
    """
@app.route("/teacher_login", methods=["GET", "POST"])
def teacher_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("ilm_ai.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM teachers
        WHERE username=? AND password=?
        """, (username, password))

        teacher = cursor.fetchone()

        conn.close()

        if teacher:

            session["teacher_username"] = username
            session["teacher_name"] = teacher[1]
            session["teacher_subject"] = teacher[2]

            return redirect("/teacher_dashboard")

        return """
        <h1>Teacher Login Failed</h1>

        <p>Invalid username or password.</p>

        <a href="/teacher_login">Try Again</a>
        """

    return """
    <h1>Teacher Login</h1>

    <form method="POST">

        Username:<br>
        <input type="text" name="username"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <input type="submit" value="Login">

    </form>

    <br>

    <a href="/">Back Home</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
