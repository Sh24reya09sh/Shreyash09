import tkinter as tk 
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import hashlib

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="exam_app"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register for user
def register():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username:
        messagebox.showerror("Registration", "Username cannot be empty!")
        return
    if not password:
        messagebox.showerror("Registration", "Password cannot be empty!")
        return
    
    db = connect_db()
    if not db:
        return

    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
        db.commit()
        messagebox.showinfo("Registration", "Registration successful!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Registration", "Username already exists! Please choose another.")
    except Exception as e:
        messagebox.showerror("Registration", f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        db.close()

    clear_entries()

# Login User
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Login", "Username and password cannot be empty!")
        return
    
    db = connect_db()
    if not db:
        return

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hash_password(password)))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login", f"Login successful! Welcome, {username}")
        clear_entries()
        show_student_info_form(username)
    else:
        messagebox.showerror("Login", "Invalid credentials")

    cursor.close()
    db.close()

# Clear Entry Fields
def clear_entries():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# Show Student Information Form
def show_student_info_form(username):
    student_info_window = tk.Toplevel(root)
    student_info_window.title("Student Information")
    student_info_window.configure(bg="#f0f8ff")

    tk.Label(student_info_window, text="Full Name", font=("Arial", 14), fg="#333").grid(row=0, column=0, padx=10, pady=10)
    entry_full_name = tk.Entry(student_info_window, font=("Arial", 14))
    entry_full_name.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(student_info_window, text="Date of Birth (DD-MM-YYYY)", font=("Arial", 14), fg="#333").grid(row=1, column=0, padx=10, pady=10)
    entry_dob = tk.Entry(student_info_window, font=("Arial", 14))
    entry_dob.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(student_info_window, text="Gender", font=("Arial", 14), fg="#333").grid(row=2, column=0, padx=10, pady=10)
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(student_info_window, text="Male", variable=gender_var, value="Male", bg="#f0f8ff").grid(row=2, column=1, sticky='w')
    tk.Radiobutton(student_info_window, text="Female", variable=gender_var, value="Female", bg="#f0f8ff").grid(row=2, column=1, sticky='e')

    tk.Label(student_info_window, text="Contact Details", font=("Arial", 14), fg="#333").grid(row=3, column=0, padx=10, pady=10)
    entry_contact = tk.Entry(student_info_window, font=("Arial", 14))
    entry_contact.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(student_info_window, text="Email Address", font=("Arial", 14), fg="#333").grid(row=4, column=0, padx=10, pady=10)
    entry_email = tk.Entry(student_info_window, font=("Arial", 14))
    entry_email.grid(row=4, column=1, padx=10, pady=10)

    tk.Button(student_info_window, text="Next", command=lambda: save_student_info(
        username, entry_full_name.get(), entry_dob.get(), gender_var.get(), entry_contact.get(), entry_email.get()
    ), font=("Arial", 14), bg="#4caf50", fg="white").grid(row=5, column=0, columnspan=2, pady=20)

# Save Student Info
def save_student_info(username, full_name, dob, gender, contact, email):
    if not full_name or not dob or not contact or not email:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    try:
        dob = datetime.strptime(dob, '%d-%m-%Y').date()
    except ValueError:
        messagebox.showerror("Error", "Date must be in DD-MM-YYYY format.")
        return

    db = connect_db()
    if not db:
        return

    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO student_info (username, full_name, dob, gender, contact, email, has_taken_exam) VALUES (%s, %s, %s, %s, %s, %s, FALSE)",
            (username, full_name, dob, gender, contact, email)
        )
        db.commit()
        messagebox.showinfo("Success", "Student information saved successfully!")
        show_language_selection(username)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        db.close()

# Show Language Selection Page
def show_language_selection(username):
    db = connect_db()
    if not db:
        return

    cursor = db.cursor()
    cursor.execute("SELECT has_taken_exam FROM student_info WHERE username=%s", (username,))
    result = cursor.fetchone()
    
    if result and result[0]:
        messagebox.showinfo("Information", "You have already taken one exam. You can only take one exam.")
        return

    language_window = tk.Toplevel(root)
    language_window.title("Select Language")
    language_window.configure(bg="#f0f8ff")

    tk.Label(language_window, text="Please select a programming language\nYou can take only one language exam\nBest of luck!", font=("Arial", 20), fg="#333", bg="#f0f8ff").pack(pady=(10, 20))

    button_frame = tk.Frame(language_window, bg="#f0f8ff")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="HTML", font=("Arial", 18), width=20, bg="#4caf50", fg="white", command=lambda: show_questions("HTML", username)).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Java", font=("Arial", 18), width=20, bg="#4caf50", fg="white", command=lambda: show_questions("Java", username)).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(button_frame, text="Python", font=("Arial", 18), width=20, bg="#4caf50", fg="white", command=lambda: show_questions("Python", username)).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="C Programming", font=("Arial", 18), width=20, bg="#4caf50", fg="white", command=lambda: show_questions("C", username)).grid(row=1, column=1, padx=10, pady=10)

# Show Questions for Selected Language
def show_questions(language, username):
    questions_window = tk.Toplevel(root)
    questions_window.title(f"{language} Questions")
    questions_window.configure(bg="#f0f8ff")

    tk.Label(questions_window, text=f"{language} Questions", font=("Arial", 24), fg="#333", bg="#f0f8ff").pack(pady=20)

    questions = []
    if language == "HTML":
        questions = [
            {"question": "What does HTML stand for?", "choices": ["Hyper Text Markup Language", "High Text Markup Language"], "answer": "Hyper Text Markup Language"},
            {"question": "Which HTML tag is used to define an internal style sheet?", "choices": ["<style>", "<css>", "<script>"], "answer": "<style>"},
            {"question": "What is the correct HTML element for inserting a line break?", "choices": ["<break>", "<br>", "<lb>"], "answer": "<br>"},
            {"question": "Which of the following elements is a block element?", "choices": ["<span>", "<div>", "<a>"], "answer": "<div>"},
            {"question": "What is the correct syntax for referring to an external script called 'script.js'?", "choices": ["<script src='script.js'>", "<script href='script.js'>", "<script link='script.js'>"], "answer": "<script src='script.js'>"},
        ]
    elif language == "Java":
        questions = [
            {"question": "What is the extension of Java files?", "choices": [".js", ".java", ".class"], "answer": ".java"},
            {"question": "Which of the following is not a Java feature?", "choices": ["Dynamic", "Architecture Neutral", "Use of pointers"], "answer": "Use of pointers"},
            {"question": "What is the default value of a boolean variable in Java?", "choices": ["true", "false", "0"], "answer": "false"},
            {"question": "Which keyword is used to create a class in Java?", "choices": ["class", "create", "define"], "answer": "class"},
            {"question": "What is the main method signature in Java?", "choices": ["public void main(String args[])", "public static void main(String[] args)", "void main(String args[])"], "answer": "public static void main(String[] args)"},
        ]
    elif language == "Python":
        questions = [
            {"question": "What is the correct file extension for Python files?", "choices": [".py", ".python", ".pt"], "answer": ".py"},
            {"question": "Which keyword is used to create a function in Python?", "choices": ["function", "def", "create"], "answer": "def"},
            {"question": "What is the output of print(type(5)) in Python?", "choices": ["<class 'int'>", "int", "5"], "answer": "<class 'int'>"},
            {"question": "How do you insert comments in Python?", "choices": ["# This is a comment", "// This is a comment", "/* This is a comment */"], "answer": "# This is a comment"},
            {"question": "Which of the following is a mutable data type in Python?", "choices": ["Tuple", "String", "List"], "answer": "List"},
        ]
    elif language == "C":
        questions = [
            {"question": "Which is a correct way to declare a variable in C?", "choices": ["int 1x = 10;", "int x = 10;", "int x = '10';"], "answer": "int x = 10;"},
            {"question": "What does C stand for?", "choices": ["Computer", "Compiler", "C Programming Language"], "answer": "C Programming Language"},
            {"question": "Which of the following is used for comments in C?", "choices": ["// This is a comment", "/* This is a comment */", "Both of the above"], "answer": "Both of the above"},
            {"question": "Which function is used to print output in C?", "choices": ["print()", "printf()", "echo()"], "answer": "printf()"},
            {"question": "What is the correct way to create a function in C?", "choices": ["function myFunction() {}", "void myFunction() {}", "create myFunction() {}"], "answer": "void myFunction() {}"},
        ]

    selected_answers = []

    for q in questions:
        frame = tk.Frame(questions_window, bg="#f0f8ff")
        frame.pack(pady=10)

        # Display the question
        tk.Label(frame, text=q["question"], font=("Arial", 14), fg="#333", bg="#f0f8ff").pack()

        var = tk.StringVar(value="")
        for choice in q["choices"]:
            tk.Radiobutton(frame, text=choice, variable=var, value=choice, font=("Arial", 12), fg="darkorange", bg="#f0f8ff").pack(anchor='w')

        selected_answers.append(var)

    # Submit button
    submit_button = tk.Button(questions_window, text="Submit", command=lambda: submit_exam(selected_answers, questions, questions_window, username), font=("Arial", 12), bg="#4caf50", fg="white")
    submit_button.pack(pady=20)

def submit_exam(selected_answers, questions, questions_window, username):
    score = 0
    total_questions = len(questions)

    for i, q in enumerate(questions):
        if selected_answers[i].get() == q["answer"]:
            score += 1

    percentage = (score / total_questions) * 100
    grade = calculate_grade(percentage)

    # Show the results
    messagebox.showinfo("Result", f"You scored {score}/{total_questions}!\nPercentage: {percentage:.2f}%\nGrade: {grade}")

    # Update the has_taken_exam status in the database
    db = connect_db()
    if not db:
        return

    cursor = db.cursor()
    cursor.execute(
        "UPDATE student_info SET has_taken_exam = TRUE WHERE username=%s",
        (username,)
    )
    db.commit()
    cursor.close()
    db.close()

    # Close the current questions window
    questions_window.destroy()

    # Show the certificate
    show_certificate(username, score, percentage, grade)

def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'

def show_certificate(username, score, percentage, grade):
    cert_window = tk.Toplevel(root)
    cert_window.title("Certificate of Completion")
    cert_window.configure(bg="#f0f8ff")

    # Display the certificate information
    tk.Label(cert_window, text="Certificate of Completion", font=("Arial", 24, "bold"), fg="purple", bg="#f0f8ff").pack(pady=20)
    tk.Label(cert_window, text=f"This certifies that {username}", font=("Arial", 18), fg="#333", bg="#f0f8ff").pack(pady=10)
    tk.Label(cert_window, text=f"Score: {score}", font=("Arial", 18), fg="#333", bg="#f0f8ff").pack(pady=5)
    tk.Label(cert_window, text=f"Percentage: {percentage:.2f}%", font=("Arial", 18), fg="#333", bg="#f0f8ff").pack(pady=5)
    tk.Label(cert_window, text=f"Grade: {grade}", font=("Arial", 18), fg="#333", bg="#f0f8ff").pack(pady=5)

    # Exit button
    tk.Button(cert_window, text="Exit", command=cert_window.destroy, font=("Arial", 14), bg="#4caf50", fg="white").pack(pady=20)

# Main Window
root = tk.Tk()
root.title("Exam Application")
root.configure(bg="#f0f8ff")

# Maximize the main window
root.state('zoomed')

# Sign In Label
sign_in_label = tk.Label(root, text="| Sign in to your account |", font=("Arial", 30), fg="#333", bg="#f0f8ff")
sign_in_label.pack(pady=(10, 20))

# Create login and register frames
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(pady=20)

tk.Label(frame, text="Username", font=("Arial", 20), fg="#333", bg="#f0f8ff").grid(row=0, column=0, padx=10)
entry_username = tk.Entry(frame, font=("Arial", 20))
entry_username.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Password", font=("Arial", 20), fg="#333", bg="#f0f8ff").grid(row=1, column=0, padx=10)
entry_password = tk.Entry(frame, show="*", font=("Arial", 20))
entry_password.grid(row=1, column=1, padx=10)

tk.Button(frame, text="Login", command=login, font=("Arial", 20), bg="#4caf50", fg="white").grid(row=2, column=0, pady=10)
tk.Button(frame, text="Register", command=register, font=("Arial", 20), bg="#4caf50", fg="white").grid(row=2, column=1)

root.mainloop()
