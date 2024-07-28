import streamlit as st
import mysql.connector
from mysql.connector import Error

# Establish a connection to the MySQL database
def create_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # use your own password
            database="college",
        )
        if mydb.is_connected():
            return mydb
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

mydb = create_connection()
mycursor = mydb.cursor(buffered=True) if mydb else None

def create_student(name, age, gender, major, gpa):
    query = "INSERT INTO students (name, age, gender, major, gpa) VALUES (%s, %s, %s, %s, %s)"
    values = (name, age, gender, major, gpa)
    try:
        mycursor.execute(query, values)
        mydb.commit()
        st.success("Student added successfully.")
    except Error as e:
        st.error(f"Error adding student: {e}")

def read_students():
    mycursor.execute("SELECT * FROM students")
    return mycursor.fetchall()

# def update_student(name, age, gender, major, gpa, student_id):
#     if not mydb or not mycursor:
#         st.error("Database connection is not established.")
#         return False
#
#     if 0 <= age <= 100:
#         query = "UPDATE students SET name=%s, age=%s, gender=%s, major=%s, gpa=%s WHERE student_id=%s"
#         values = (name, age, gender, major, gpa, student_id)
#         try:
#             st.write(f"Executing update query: {query} with values {values}")
#             mycursor.execute(query, values)
#             mydb.commit()
#             if mycursor.rowcount > 0:
#                 st.success("Update successful, commit completed.")
#                 return True
#             else:
#                 st.error("Update failed: No rows affected. Please check if the student ID exists.")
#                 return False
#         except Error as e:
#             st.error(f"Error updating student: {e}")
#             return False
#     else:
#         st.error("Age must be between 0 and 100")
#         return False

def delete_student(student_id):
    query = "DELETE FROM students WHERE student_id=%s"
    try:
        mycursor.execute(query, (student_id,))
        mydb.commit()
        if mycursor.rowcount > 0:
            st.success("Student deleted successfully.")
        else:
            st.error("Delete failed: No rows affected. Please check if the student ID exists.")
    except Error as e:
        st.error(f"Error deleting student: {e}")

def main():
    if mydb is None:
        st.error("Failed to connect to the database. Please check your connection settings.")
        return

    st.title("College Student Management System")

    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create":
        st.subheader("Add New Student")
        with st.form(key='create_form'):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=1, max_value=100)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            major = st.text_input("Major")
            gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, step=0.1)
            submit_button = st.form_submit_button(label="Add Student")

            if submit_button:
                create_student(name, age, gender, major, gpa)

    elif choice == "Read":
        st.subheader("View Students")
        students = read_students()
        for student in students:
            st.write(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Gender: {student[3]}, Major: {student[4]}, GPA: {student[5]}")

    # elif choice == "Update":
    #     st.subheader("Update Student Information")
    #     student_id = st.number_input("Enter Student ID", min_value=1)
    #     if st.button("Fetch Student Data"):
    #         mycursor.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
    #         student = mycursor.fetchone()
    #         if student:
    #             st.success(f"Fetched student data: {student}")
    #             with st.form(key='update_form'):
    #                 name = st.text_input("Name", value=student[1])
    #                 age = st.number_input("Age", min_value=1, max_value=100, value=student[2])
    #                 gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(student[3]))
    #                 major = st.text_input("Major", value=student[4])
    #                 gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, step=0.1, value=student[5])
    #                 submit_button = st.form_submit_button(label="Update Student")
    #
    #                 if submit_button:
    #                     success = update_student(name, age, gender, major, gpa, student_id)
    #                     if success:
    #                         st.success(f"Student ID {student_id} updated successfully")
    #                     else:
    #                         st.error("Failed to update student data.")

    elif choice == "Delete":
        st.subheader("Delete Student")
        student_id = st.number_input("Enter Student ID to Delete", min_value=1)
        if st.button("Delete Student"):
            delete_student(student_id)

if __name__ == "__main__":
    main()
