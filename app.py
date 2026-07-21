from flask import Flask, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "ilm_ai_secret_key"


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return """
    <h1>Welcome to Ilm+AI</h1>

    <p>Education in Service to Allah Through Humanity</p>

    <hr>

    <h2>Student Portal</h2>

    <a href="/register">Student Registration</a>

    <br><br>

    <a href="/login">Student Login</a>

    <hr>

    <h2>Teacher Portal</h2>

    <a href="/teacher_login">Teacher Login</a>
    """


# ============================================================
# STUDENT REGISTRATION
# ============================================================

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
            """, (
                name,
                student_class,
                username,
                password
            ))

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

        <br>

        <a href="/login">Proceed to Login</a>
        """

    return """
    <h1>Student Registration</h1>

    <form method="POST">

        Name:<br>
        <input type="text" name="name" required>

        <br><br>

        Class:<br>
        <input type="text" name="class" required>

        <br><br>

        Username:<br>
        <input type="text" name="username" required>

        <br><br>

        Password:<br>
        <input type="password" name="password" required>

        <br><br>

        <input type="submit" value="Register">

    </form>

    <br>

    <a href="/">Back Home</a>
    """


# ============================================================
# STUDENT LOGIN
# ============================================================

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
        """, (
            username,
            password
        ))

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
        <input type="text" name="username" required>

        <br><br>

        Password:<br>
        <input type="password" name="password" required>

        <br><br>

        <input type="submit" value="Login">

    </form>

    <br>

    <a href="/">Back Home</a>
    """


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:

        return redirect("/login")

    return f"""
    <h1>Student Dashboard</h1>

    <p>Welcome {session['name']}</p>

    <p>Class: {session['class_name']}</p>

    <hr>

    <ul>

        <li>
        <a href="/courses">
        My Courses
        </a>
        </li>

        <br>

        <li>
        <a href="/assignments">
        My Assignments
        </a>
        </li>

        <br>

        <li>
        <a href="/cbt">
        Take CBT Test
        </a>
        </li>

        <br>

        <li>
        <a href="/results">
        My Results
        </a>
        </li>

    </ul>

    <hr>

    <a href="/logout">
    Logout
    </a>
    """


# ============================================================
# STUDENT COURSES
# ============================================================

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

    <br>

    <a href="/dashboard">
    Back Dashboard
    </a>
    """


# ============================================================
# STUDENT ASSIGNMENTS
# ============================================================

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

    <br>

    <a href="/dashboard">
    Back Dashboard
    </a>
    """


# ============================================================
# STUDENT CBT
# ============================================================

@app.route("/cbt", methods=["GET", "POST"])
def cbt():

    if "username" not in session:

        return redirect("/login")

    if request.method == "POST":

        score = 0

        # Question 1
        if request.form.get("q1") == "Abuja":
            score += 1

        # Question 2
        if request.form.get("q2") == "4":
            score += 1

        # Question 3
        if request.form.get("q3") == "Python":
            score += 1

        # Question 4
        if request.form.get("q4") == "Allah":
            score += 1

        # Question 5
        if request.form.get("q5") == "Robot":
            score += 1

        total = 5

        percentage = (score / total) * 100

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
            total
        ))

        conn.commit()

        conn.close()

        return f"""
        <h1>CBT Result</h1>

        <p>Your Score: {score}/{total}</p>

        <p>Percentage: {percentage}%</p>

        <br>

        <a href="/results">
        View My Results
        </a>

        <br><br>

        <a href="/cbt">
        Take Test Again
        </a>

        <br><br>

        <a href="/dashboard">
        Back Dashboard
        </a>
        """

    return """
    <h1>Ilm+AI CBT Test</h1>

    <form method="POST">

    <h3>1. What is the capital of Nigeria?</h3>

    <input type="radio"
    name="q1"
    value="Lagos">

    Lagos

    <br>

    <input type="radio"
    name="q1"
    value="Abuja">

    Abuja

    <br>

    <input type="radio"
    name="q1"
    value="Kano">

    Kano

    <br><br>


    <h3>2. What is 2 + 2?</h3>

    <input type="radio"
    name="q2"
    value="3">

    3

    <br>

    <input type="radio"
    name="q2"
    value="4">

    4

    <br>

    <input type="radio"
    name="q2"
    value="5">

    5

    <br><br>


    <h3>
    3. Which programming language are we learning?
    </h3>

    <input type="radio"
    name="q3"
    value="Java">

    Java

    <br>

    <input type="radio"
    name="q3"
    value="Python">

    Python

    <br>

    <input type="radio"
    name="q3"
    value="C++">

    C++

    <br><br>


    <h3>
    4. Who should always come first
    according to Ilm+AI philosophy?
    </h3>

    <input type="radio"
    name="q4"
    value="Technology">

    Technology

    <br>

    <input type="radio"
    name="q4"
    value="Money">

    Money

    <br>

    <input type="radio"
    name="q4"
    value="Allah">

    Allah

    <br><br>


    <h3>
    5. Which of these is used in Robotics?
    </h3>

    <input type="radio"
    name="q5"
    value="Robot">

    Robot

    <br>

    <input type="radio"
    name="q5"
    value="Tree">

    Tree

    <br>

    <input type="radio"
    name="q5"
    value="River">

    River

    <br><br>


    <input type="submit"
    value="Submit CBT">

    </form>

    <br>

    <a href="/dashboard">
    Back Dashboard
    </a>
    """


# ============================================================
# STUDENT RESULTS
# ============================================================

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
    """, (
        session["username"],
    ))

    results_data = cursor.fetchall()

    conn.close()

    html = """
    <h1>My Results</h1>
    """

    if results_data:

        html += """
        <table border="1"
        cellpadding="10">

        <tr>
            <th>Subject</th>
            <th>Score</th>
            <th>Total</th>
        </tr>
        """

        for result in results_data:

            html += f"""
            <tr>

                <td>{result[0]}</td>

                <td>{result[1]}</td>

                <td>{result[2]}</td>

            </tr>
            """

        html += """
        </table>
        """

    else:

        html += """
        <p>No results available yet.</p>
        """

    html += """
    <br><br>

    <a href="/dashboard">
    Back Dashboard
    </a>
    """

    return html


# ============================================================
# STUDENT LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return """
    <h1>You have been logged out successfully.</h1>

    <a href="/login">
    Student Login
    </a>

    <br><br>

    <a href="/">
    Back Home
    </a>
    """


# ============================================================
# TEACHER LOGIN
# ============================================================

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
        """, (
            username,
            password
        ))

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

        <a href="/teacher_login">
        Try Again
        </a>
        """

    return """
    <h1>Teacher Login</h1>

    <form method="POST">

        Username:<br>

        <input type="text"
        name="username"
        required>

        <br><br>

        Password:<br>

        <input type="password"
        name="password"
        required>

        <br><br>

        <input type="submit"
        value="Login">

    </form>

    <br>

    <a href="/">
    Back Home
    </a>
    """


# ============================================================
# TEACHER DASHBOARD
# ============================================================

@app.route("/teacher_dashboard")
def teacher_dashboard():

    if "teacher_username" not in session:

        return redirect("/teacher_login")

    return f"""
    <h1>Teacher Dashboard</h1>

    <p>
    Welcome {session["teacher_name"]}
    </p>

    <p>
    Subject: {session["teacher_subject"]}
    </p>

    <hr>

    <h2>Teacher Menu</h2>

    <ul>

        <li>
        <a href="/view_students">
        View Students
        </a>
        </li>

        <br>

        <li>
        <a href="/view_all_results">
        View All Student Results
        </a>
        </li>

        <br>

        <li>
        <a href="/add_question">
        Add CBT Question
        </a>
        </li>

        <br>

        <li>
        <a href="/upload_assignment">
        Upload Assignment
        </a>
        </li>

    </ul>

    <hr>

    <a href="/teacher_logout">
    Teacher Logout
    </a>
    """


# ============================================================
# VIEW ALL STUDENTS
# ============================================================

@app.route("/view_students")
def view_students():

    if "teacher_username" not in session:

        return redirect("/teacher_login")

    conn = sqlite3.connect("ilm_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, class_name, username
    FROM students
    ORDER BY name
    """)

    students = cursor.fetchall()

    conn.close()

    html = """
    <h1>Registered Students</h1>

    <table border="1"
    cellpadding="10">

    <tr>

        <th>Name</th>

        <th>Class</th>

        <th>Username</th>

    </tr>
    """

    if students:

        for student in students:

            html += f"""
            <tr>

                <td>{student[0]}</td>

                <td>{student[1]}</td>

                <td>{student[2]}</td>

            </tr>
            """

    else:

        html += """
        <tr>

            <td colspan="3">
            No students registered yet.
            </td>

        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/teacher_dashboard">
    Back Teacher Dashboard
    </a>
    """

    return html


# ============================================================
# VIEW ALL STUDENT RESULTS
# ============================================================

@app.route("/view_all_results")
def view_all_results():

    if "teacher_username" not in session:

        return redirect("/teacher_login")

    conn = sqlite3.connect("ilm_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        results.username,
        students.name,
        results.subject,
        results.score,
        results.total
    FROM results

    LEFT JOIN students
    ON results.username = students.username

    ORDER BY results.rowid DESC
    """)

    results_data = cursor.fetchall()

    conn.close()

    html = """
    <h1>All Student Results</h1>

    <table border="1"
    cellpadding="10">

    <tr>

        <th>Username</th>

        <th>Student Name</th>

        <th>Subject</th>

        <th>Score</th>

        <th>Total</th>

    </tr>
    """

    if results_data:

        for result in results_data:

            html += f"""
            <tr>

                <td>{result[0]}</td>

                <td>{result[1] or "Unknown"}</td>

                <td>{result[2]}</td>

                <td>{result[3]}</td>

                <td>{result[4]}</td>

            </tr>
            """

    else:

        html += """
        <tr>

            <td colspan="5">
            No student results available yet.
            </td>

        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/teacher_dashboard">
    Back Teacher Dashboard
    </a>
    """

    return html


# ============================================================
# ADD CBT QUESTION
# ============================================================

@app.route("/add_question", methods=["GET", "POST"])
def add_question():

    if "teacher_username" not in session:

        return redirect("/teacher_login")

    if request.method == "POST":

        subject = request.form["subject"]

        question = request.form["question"]

        option_a = request.form["option_a"]

        option_b = request.form["option_b"]

        option_c = request.form["option_c"]

        correct_answer = request.form["correct_answer"]

        conn = sqlite3.connect("ilm_ai.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO questions
        (
            question,
            option_a,
            option_b,
            option_c,
            correct_answer,
            subject
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            question,
            option_a,
            option_b,
            option_c,
            correct_answer,
            subject
        ))

        conn.commit()

        conn.close()

        return """
        <h1>Question Saved Successfully!</h1>

        <p>
        The CBT question has been saved
        to the Ilm+AI question bank.
        </p>

        <br>

        <a href="/add_question">
        Add Another Question
        </a>

        <br><br>

        <a href="/teacher_dashboard">
        Back Teacher Dashboard
        </a>
        """

    return """
    <h1>Add CBT Question</h1>

    <form method="POST">

    Subject:<br>

    <input type="text"
    name="subject"
    required>

    <br><br>


    Question:<br>

    <textarea
    name="question"
    rows="5"
    cols="50"
    required>
    </textarea>

    <br><br>


    Option A:<br>

    <input type="text"
    name="option_a"
    required>

    <br><br>


    Option B:<br>

    <input type="text"
    name="option_b"
    required>

    <br><br>


    Option C:<br>

    <input type="text"
    name="option_c"
    required>

    <br><br>


    Correct Answer:<br>

    <input type="text"
    name="correct_answer"
    placeholder="Enter the exact correct answer"
    required>

    <br><br>


    <input type="submit"
    value="Save Question">

    </form>

    <br>

    <a href="/teacher_dashboard">
    Back Teacher Dashboard
    </a>
    """


# ============================================================
# UPLOAD ASSIGNMENT - PLACEHOLDER
# ============================================================

@app.route("/upload_assignment")
def upload_assignment():

    if "teacher_username" not in session:

        return redirect("/teacher_login")

    return """
    <h1>Upload Assignment</h1>

    <p>
    The Assignment Management System
    will be added in a future version.
    </p>

    <br>

    <a href="/teacher_dashboard">
    Back Teacher Dashboard
    </a>
    """


# ============================================================
# TEACHER LOGOUT
# ============================================================

@app.route("/teacher_logout")
def teacher_logout():

    session.pop("teacher_username", None)

    session.pop("teacher_name", None)

    session.pop("teacher_subject", None)

    return """
    <h1>Teacher Logout Successful</h1>

    <p>
    You have been logged out of the Teacher Portal.
    </p>

    <br>

    <a href="/teacher_login">
    Teacher Login
    </a>

    <br><br>

    <a href="/">
    Back Home
    </a>
    """


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
