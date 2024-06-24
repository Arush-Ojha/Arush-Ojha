import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error, connect

# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Jain.mysql.12",  
            database="education"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return None

# Function to create necessary tables if they do not exist
def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS instructor (
                instructor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(20),
                bio TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                credit_hours INT,
                instructor_id INT,
                FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(20)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deleted_records (
                record_id INT AUTO_INCREMENT PRIMARY KEY,
                table_name VARCHAR(50) NOT NULL,
                deleted_id INT,
                deletion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        print("Tables created successfully.")
    except Error as e:
        print(f"Error creating tables: {e}")

# Function to insert an instructor into the database
def insert_instructor(connection, name, email, phone, bio):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO instructor (name, email, phone, bio)
            VALUES (%s, %s, %s, %s)
        """, (name, email, phone, bio))
        connection.commit()
        print("Instructor added successfully.")
    except Error as e:
        print(f"Error adding instructor: {e}")

# Function to delete an instructor from the database
def delete_instructor(connection, instructor_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM instructor
            WHERE instructor_id = %s
        """, (instructor_id,))
        connection.commit()
        print(f"Instructor with ID {instructor_id} deleted successfully.")
        # Log the deletion in the deleted_records table
        cursor.execute("""
            INSERT INTO deleted_records (table_name, deleted_id)
            VALUES ('instructor', %s)
        """, (instructor_id,))
        connection.commit()
    except Error as e:
        print(f"Error deleting instructor: {e}")

# Function to restore a deleted instructor from the database
def restore_instructor(connection, record_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name, deleted_id FROM deleted_records
            WHERE record_id = %s
        """, (record_id,))
        deleted_record = cursor.fetchone()
        if deleted_record:
            table_name = deleted_record[0]
            deleted_id = deleted_record[1]
            if table_name == 'instructor':
                cursor.execute("""
                    INSERT INTO instructor (instructor_id, name, email, phone, bio)
                    SELECT instructor_id, name, email, phone, bio
                    FROM deleted_records dr
                    JOIN instructor i ON dr.deleted_id = i.instructor_id
                    WHERE dr.record_id = %s
                """, (record_id,))
                connection.commit()
                print(f"Instructor with ID {deleted_id} restored successfully.")
                # Delete the entry from deleted_records after restoration
                cursor.execute("""
                    DELETE FROM deleted_records
                    WHERE record_id = %s
                """, (record_id,))
                connection.commit()
    except Error as e:
        print(f"Error restoring instructor: {e}")

# Function to insert a course into the database
def insert_course(connection, name, description, credit_hours, instructor_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO course (name, description, credit_hours, instructor_id)
            VALUES (%s, %s, %s, %s)
        """, (name, description, credit_hours, instructor_id))
        connection.commit()
        print("Course added successfully.")
    except Error as e:
        print(f"Error adding course: {e}")

# Function to delete a course from the database
def delete_course(connection, course_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM course
            WHERE course_id = %s
        """, (course_id,))
        connection.commit()
        print(f"Course with ID {course_id} deleted successfully.")
        # Log the deletion in the deleted_records table
        cursor.execute("""
            INSERT INTO deleted_records (table_name, deleted_id)
            VALUES ('course', %s)
        """, (course_id,))
        connection.commit()
    except Error as e:
        print(f"Error deleting course: {e}")

# Function to restore a deleted course from the database
def restore_course(connection, record_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name, deleted_id FROM deleted_records
            WHERE record_id = %s
        """, (record_id,))
        deleted_record = cursor.fetchone()
        if deleted_record:
            table_name = deleted_record[0]
            deleted_id = deleted_record[1]
            if table_name == 'course':
                cursor.execute("""
                    INSERT INTO course (course_id, name, description, credit_hours, instructor_id)
                    SELECT course_id, name, description, credit_hours, instructor_id
                    FROM deleted_records dr
                    JOIN course c ON dr.deleted_id = c.course_id
                    WHERE dr.record_id = %s
                """, (record_id,))
                connection.commit()
                print(f"Course with ID {deleted_id} restored successfully.")
                # Delete the entry from deleted_records after restoration
                cursor.execute("""
                    DELETE FROM deleted_records
                    WHERE record_id = %s
                """, (record_id,))
                connection.commit()
    except Error as e:
        print(f"Error restoring course: {e}")

# Function to insert a student into the database
def insert_student(connection, name, email, phone):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO student (name, email, phone)
            VALUES (%s, %s, %s)
        """, (name, email, phone))
        connection.commit()
        print("Student added successfully.")
    except Error as e:
        print(f"Error adding student: {e}")

# Function to delete a student from the database
def delete_student(connection, student_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM student
            WHERE student_id = %s
        """, (student_id,))
        connection.commit()
        print(f"Student with ID {student_id} deleted successfully.")
        # Log the deletion in the deleted_records table
        cursor.execute("""
            INSERT INTO deleted_records (table_name, deleted_id)
            VALUES ('student', %s)
        """, (student_id,))
        connection.commit()
    except Error as e:
        print(f"Error deleting student: {e}")

# Function to restore a deleted student from the database
def restore_student(connection, record_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name, deleted_id FROM deleted_records
            WHERE record_id = %s
        """, (record_id,))
        deleted_record = cursor.fetchone()
        if deleted_record:
            table_name = deleted_record[0]
            deleted_id = deleted_record[1]
            if table_name == 'student':
                cursor.execute("""
                    INSERT INTO student (student_id, name, email, phone)
                    SELECT student_id, name, email, phone
                    FROM deleted_records dr
                    JOIN student s ON dr.deleted_id = s.student_id
                    WHERE dr.record_id = %s
                """, (record_id,))
                connection.commit()
                print(f"Student with ID {deleted_id} restored successfully.")
                # Delete the entry from deleted_records after restoration
                cursor.execute("""
                    DELETE FROM deleted_records
                    WHERE record_id = %s
                """, (record_id,))
                connection.commit()
    except Error as e:
        print(f"Error restoring student: {e}")

# GUI Application class
class EduSchemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Schema Application")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_student_tab()
        self.create_deleted_records_tab()

    def create_instructor_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Instructors')

        # Instructor Form
        self.instructor_id_var = tk.StringVar()
        self.instructor_name_var = tk.StringVar()
        self.instructor_email_var = tk.StringVar()
        self.instructor_phone_var = tk.StringVar()
        self.instructor_bio_var = tk.StringVar()

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.instructor_name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.instructor_email_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Phone").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.instructor_phone_var).grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame, text="Bio").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.instructor_bio_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Instructor", command=self.add_instructor).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Delete Instructor", command=self.delete_instructor_gui).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Restore Instructor", command=self.restore_instructor_gui).grid(row=4, column=2, padx=5, pady=5)

        # Instructor Listbox
        self.instructor_listbox = tk.Listbox(frame, width=80)
        self.instructor_listbox.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        self.populate_instructor_list()

    def create_course_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Courses')

        # Course Form
        self.course_id_var = tk.StringVar()
        self.course_name_var = tk.StringVar()
        self.course_description_var = tk.StringVar()
        self.course_credit_hours_var = tk.IntVar()
        self.course_instructor_id_var = tk.IntVar()

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.course_name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Description").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.course_description_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Credit Hours").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.course_credit_hours_var).grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame, text="Instructor ID").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.course_instructor_id_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Course", command=self.add_course).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Delete Course", command=self.delete_course_gui).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Restore Course", command=self.restore_course_gui).grid(row=4, column=2, padx=5, pady=5)

        # Course Listbox
        self.course_listbox = tk.Listbox(frame, width=80)
        self.course_listbox.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        self.populate_course_list()

    def create_student_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Students')

        # Student Form
        self.student_id_var = tk.StringVar()
        self.student_name_var = tk.StringVar()
        self.student_email_var = tk.StringVar()
        self.student_phone_var = tk.StringVar()

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.student_name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.student_email_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(frame, text="Phone").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.student_phone_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Student", command=self.add_student).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Delete Student", command=self.delete_student_gui).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Restore Student", command=self.restore_student_gui).grid(row=3, column=2, padx=5, pady=5)

        # Student Listbox
        self.student_listbox = tk.Listbox(frame, width=80)
        self.student_listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.populate_student_list()

    def create_deleted_records_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Deleted Records')

        # Deleted Records Listbox
        self.deleted_records_listbox = tk.Listbox(frame, width=100)
        self.deleted_records_listbox.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(frame, text="View Deleted Records", command=self.populate_deleted_records_list).grid(row=1, column=0, padx=5, pady=5)

    def populate_instructor_list(self):
        self.instructor_listbox.delete(0, tk.END)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT instructor_id, name FROM instructor")
            instructors = cursor.fetchall()
            for instructor in instructors:
                self.instructor_listbox.insert(tk.END, f"{instructor[0]} - {instructor[1]}")
            connection.close()

    def populate_course_list(self):
        self.course_listbox.delete(0, tk.END)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT course_id, name FROM course")
            courses = cursor.fetchall()
            for course in courses:
                self.course_listbox.insert(tk.END, f"{course[0]} - {course[1]}")
            connection.close()

    def populate_student_list(self):
        self.student_listbox.delete(0, tk.END)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT student_id, name FROM student")
            students = cursor.fetchall()
            for student in students:
                self.student_listbox.insert(tk.END, f"{student[0]} - {student[1]}")
            connection.close()

    def populate_deleted_records_list(self):
        self.deleted_records_listbox.delete(0, tk.END)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT record_id, table_name, deleted_id, deletion_time FROM deleted_records ORDER BY deletion_time DESC")
            deleted_records = cursor.fetchall()
            for record in deleted_records:
                self.deleted_records_listbox.insert(tk.END, f"Record ID: {record[0]}, Table: {record[1]}, Deleted ID: {record[2]}, Deletion Time: {record[3]}")
            connection.close()

    def add_instructor(self):
        name = self.instructor_name_var.get()
        email = self.instructor_email_var.get()
        phone = self.instructor_phone_var.get()
        bio = self.instructor_bio_var.get()

        connection = create_connection()
        if connection:
            insert_instructor(connection, name, email, phone, bio)
            self.populate_instructor_list()
            connection.close()

    def delete_instructor_gui(self):
        selected_item = self.instructor_listbox.curselection()
        if selected_item:
            instructor_info = self.instructor_listbox.get(selected_item)
            instructor_id = int(instructor_info.split()[0])  # Extracting ID from the listbox item
            connection = create_connection()
            if connection:
                delete_instructor(connection, instructor_id)
                self.populate_instructor_list()
                self.populate_deleted_records_list()  # Update deleted records list after deletion
                connection.close()

    def restore_instructor_gui(self):
        selected_item = self.deleted_records_listbox.curselection()
        if selected_item:
            record_info = self.deleted_records_listbox.get(selected_item)
            record_id = int(record_info.split()[2])  # Extracting record ID from the listbox item
            connection = create_connection()
            if connection:
                restore_instructor(connection, record_id)
                self.populate_instructor_list()
                self.populate_deleted_records_list()  # Update deleted records list after restoration
                connection.close()

    def add_course(self):
        name = self.course_name_var.get()
        description = self.course_description_var.get()
        credit_hours = self.course_credit_hours_var.get()
        instructor_id = self.course_instructor_id_var.get()

        connection = create_connection()
        if connection:
            insert_course(connection, name, description, credit_hours, instructor_id)
            self.populate_course_list()
            connection.close()

    def delete_course_gui(self):
        selected_item = self.course_listbox.curselection()
        if selected_item:
            course_info = self.course_listbox.get(selected_item)
            course_id = int(course_info.split()[0])  # Extracting ID from the listbox item
            connection = create_connection()
            if connection:
                delete_course(connection, course_id)
                self.populate_course_list()
                self.populate_deleted_records_list()  # Update deleted records list after deletion
                connection.close()

    def restore_course_gui(self):
        selected_item = self.deleted_records_listbox.curselection()
        if selected_item:
            record_info = self.deleted_records_listbox.get(selected_item)
            record_id = int(record_info.split()[2])  # Extracting record ID from the listbox item
            connection = create_connection()
            if connection:
                restore_course(connection, record_id)
                self.populate_course_list()
                self.populate_deleted_records_list()  # Update deleted records list after restoration
                connection.close()

    def add_student(self):
        name = self.student_name_var.get()
        email = self.student_email_var.get()
        phone = self.student_phone_var.get()

        connection = create_connection()
        if connection:
            insert_student(connection, name, email, phone)
            self.populate_student_list()
            connection.close()

    def delete_student_gui(self):
        selected_item = self.student_listbox.curselection()
        if selected_item:
            student_info = self.student_listbox.get(selected_item)
            student_id = int(student_info.split()[0])  # Extracting ID from the listbox item
            connection = create_connection()
            if connection:
                delete_student(connection, student_id)
                self.populate_student_list()
                self.populate_deleted_records_list()  # Update deleted records list after deletion
                connection.close()

    def restore_student_gui(self):
        selected_item = self.deleted_records_listbox.curselection()
        if selected_item:
            record_info = self.deleted_records_listbox.get(selected_item)
            record_id = int(record_info.split()[2])  # Extracting record ID from the listbox item
            connection = create_connection()
            if connection:
                restore_student(connection, record_id)
                self.populate_student_list()
                self.populate_deleted_records_list()  # Update deleted records list after restoration
                connection.close()

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_tables(connection)
        connection.close()
    else:
        print("Cannot connect to the database. Exiting...")
        exit()

    root = tk.Tk()
    app = EduSchemaApp(root)
    root.mainloop()