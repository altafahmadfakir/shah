import streamlit as st
import sqlite3
import pandas as pd

# ---------------- Page Config ----------------

st.set_page_config(
    page_title="Student Management",
    page_icon="🎓",
    layout="wide"
)
# ---------------- Session ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
# ---------------- Database ----------------
conn = sqlite3.connect("student.db",
    check_same_thread=False
)
cursor = conn.cursor()
# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    gender TEXT,
    mobile TEXT,
    username TEXT UNIQUE,
    password TEXT
)
""")
# Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT,
    email TEXT,
    phone TEXT
)
""")
conn.commit()
# ---------------- Functions ----------------
def signup(name, gender, mobile, username, password):
    try:
        cursor.execute("""
        INSERT INTO users
        (name, gender, mobile, username, password)
        VALUES(?,?,?,?,?)
        """,
        (name, gender, mobile, username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
def login(username, password):
    cursor.execute("""
    SELECT *
    FROM users
    WHERE username=? AND password=?
    """,
    (username, password))
    return cursor.fetchone()
def add_student(name, age, course, email, phone):
    cursor.execute("""
    INSERT INTO students
    (name, age, course, email, phone)
    VALUES(?,?,?,?,?)
    """,
    (name, age, course, email, phone))
    conn.commit()
def view_students():
    cursor.execute(
        "SELECT * FROM students"
    )
    return cursor.fetchall()
def update_student(id, name, age, course, email, phone):
    cursor.execute("""
    UPDATE students
    SET name=?,
        age=?,
        course=?,
        email=?,
        phone=?
    WHERE id=?
    """,
    (name, age, course, email, phone, id))
    conn.commit()
def delete_student(id):
    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )
    conn.commit()
# ---------------- Login System ----------------
if not st.session_state.logged_in:
    st.title("🎓 Student Management System")
    option = st.radio(
        "Choose",
        ["Login","Sign Up"]
    )
    # -------- Signup --------
    if option == "Sign Up":
        st.subheader("📝 Create Account")
        name = st.text_input("Full Name")
        gender = st.selectbox("Gender",["Male","Female","Other"])
        mobile = st.text_input("Mobile Number")
        username = st.text_input("Username")
        password = st.text_input("Password",type="password")
        confirm = st.text_input("Confirm Password",type="password" )
        if st.button("Create Account"):
            if password != confirm:
                st.error("Password not matched")
            elif not name or not mobile or not username or not password:
                st.warning("Fill all fields")
            else:
                if signup(name,gender,mobile, username,password):
                    st.success("Account Created Successfully")
                else:
                    st.error("Username already exists")
    # -------- Login --------
    else:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password",type="password")
        if st.button("Login"):
            user = login(username,password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid Login")
    st.stop()
# ---------------- Dashboard ----------------
st.title("🎓 Student Management Dashboard")
st.sidebar.success(
    f"Welcome {st.session_state.username}"
)
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
menu = st.sidebar.selectbox("Menu",
    ["Add Student","View Students","Update Student","Delete Student"])
# ---------------- Add Student ----------------
if menu == "Add Student":
    st.subheader("➕ Add Student")
    name = st.text_input("Student Name")
    age = st.number_input("Age",1,100)
    course = st.selectbox("Course",["BCA","BSc CSIT","BIT","BIM","BBS","BBA","MBA"])
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    if st.button("Save Student"):
        if name:
            add_student(name,age,course,email,phone)
            st.success("Student Added")
        else:
            st.warning("Enter student name")
# ---------------- View ----------------
elif menu == "View Students":
    st.subheader("📋 Student List")
    data = view_students()
    if data:
        df = pd.DataFrame(
            data,
            columns=["ID","Name","Age","Course","Email","Phone"]
        )
        search = st.text_input("Search")
        if search:
            df = df[
                df["Name"]
                .str.contains(
                    search,
                    case=False
                )
            ]
        st.dataframe(df,use_container_width=True)
    else:
        st.info("No records found")
# ---------------- Update ----------------
elif menu == "Update Student":
    st.subheader("✏ Update Student")
    id = st.number_input("Student ID",1)
    name = st.text_input("Name")
    age = st.number_input("Age",1,100)
    course = st.text_input("Course")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    if st.button("Update"):
        update_student(id,name,age,course,email,phone)
        st.success("Updated Successfully")
# ---------------- Delete ----------------
elif menu == "Delete Student":
    st.subheader("🗑 Delete Student")
    id = st.number_input("Student ID",1)
    if st.button("Delete"):
        delete_student(id)
        st.success("Deleted Successfully")