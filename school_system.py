import sqlite3
import hashlib

connection = sqlite3.connect('students.db')
c = connection.cursor()


#STUDENT DATABASE
c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_year INTEGER NOT NULL,
        birth_month INTEGER NOT NULL,
        birth_day INTEGER NOT NULL
        )''')


#TEACHER DATABASE
c.execute('''CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_year INTEGER NOT NULL,
        birth_month INTEGER NOT NULL,
        birth_day INTEGER NOT NULL
        )''')

#PASSWORD HASHING
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#ACCOUNT of STUDENT
def add_student(email, password, first_name, last_name, birth_year, birth_month, birth_day):
    try:
        with connection:
            hashed_password = hash_password(password)
            c.execute("INSERT INTO students (email, password, first_name, last_name, birth_year, birth_month, birth_day) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                                                (email,
                                                                           hashed_password,
                                                                           first_name,
                                                                           last_name,
                                                                           birth_year,
                                                                           birth_month,
                                                                           birth_day))
        return True
    except sqlite3.IntegrityError:
        return False

#ACCOUNT of TEACHER
def add_teacher(email, password, first_name, last_name, birth_year, birth_month, birth_day):
    try:
        with connection:
            hashed_password = hash_password(password)
            c.execute("INSERT INTO teachers (email, password, first_name, last_name, birth_year, birth_month, birth_day) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                                                (email,
                                                                           hashed_password,
                                                                           first_name,
                                                                           last_name,
                                                                           birth_year,
                                                                           birth_month,
                                                                           birth_day))
        return True
    except sqlite3.IntegrityError:
        return False

#AUTHENTICATE STUDENT
def authenticate_student(email, password):
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM students WHERE email = ? and password = ?", (email, hashed_password))
    return c.fetchone()

#AUTHENTICATE TEACHER
def authenticate_teacher(email, password):
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM teachers WHERE email = ? and password = ?", (email, hashed_password))
    return c.fetchone()


# SIGNing-up STUDENT
def sign_up_student():
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    birth_year = int(input('Enter your birth year: '))
    birth_month = int(input('Enter your birth month: '))
    birth_day = int(input('Enter your birth day: '))

    if add_student(email, password, first_name, last_name, birth_year, birth_month, birth_day):
        print("Student is signed up!")
    else:
        print("Incorrect email or password. Try again.")


# LOGGing-in STUDENT
def log_in_student():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    student_data = authenticate_student(email, password)
    if student_data:
        print("Student is logged in successfully!")
        show_data = input("Would you like to see your data? (Y/N): ")
        if show_data == "Y":
            print(f"Email: {student_data[1]}")
            print(f"Full name: {student_data[3]} {student_data[4]}")
            print(f"Date of birth: {student_data[5]}/{student_data[6]}/{student_data[7]}")
    else:
        print("Incorrect email or password. Try again.")


# SIGNing-up TEACHER
def sign_up_teacher():
    email = input('Enter your email: ')
    if not email.endswith("@teacher.com"):
        print("This is not a teacher's email.")
        print("Please use the one that ends with '@teacher.com'")
    password = input('Enter your password: ')
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    birth_year = int(input('Enter your birth year: '))
    birth_month = int(input('Enter your birth month: '))
    birth_day = int(input('Enter your birth day: '))
    if add_teacher(email, password, first_name, last_name, birth_year, birth_month, birth_day):
        print("Teacher is signed up!")
    else:
        print("Incorrect email or password. Try again.")

# LOGGing-in TEACHER
def log_in_teacher():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    teacher_data = authenticate_teacher(email, password)
    if teacher_data:
        print("Student is logged in successfully!")
        show_data = input("Would you like to see your data? (Y/N): ")
        if show_data == "Y":
            print(f"Email: {teacher_data[1]}")
            print(f"Full name: {teacher_data[3]} {teacher_data[4]}")
            print(f"Date of birth: {teacher_data[5]}/{teacher_data[6]}/{teacher_data[7]}")
    else:
        print("Incorrect email or password. Try again.")

def main():
    while True:
        print("FOR STUDENTS: Type '1' to sign up and type '2' to login.")
        print("FOR TEACHERS: Type '3' to sign up and type '4' to login.")
        print("Type 'Q' to quit")
        decision = input("Enter your choice: ")
        if decision == '1':
            sign_up_student()
        elif decision == '2':
            log_in_student()
        elif decision == '3':
            sign_up_teacher()
        elif decision == '4':
            log_in_teacher()
        elif decision == 'Q':
            print("Thank you for using School System!")
            break

if __name__ == '__main__':
    main()

connection.close()