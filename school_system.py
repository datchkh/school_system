import sqlite3
import hashlib

connection = sqlite3.connect('students.db')
c = connection.cursor()

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

def authentication(email, password):
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM students WHERE email = ? and password = ?", (email, hashed_password))
    return c.fetchone()

def sign_up():
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

def log_in():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    student_data = authentication(email, password)
    if student_data:
        print("Student is logged in successfully!")
        show_data = input("Would you like to see your data? (Y/N): ")
        if show_data == "Y":
            print(f"Email: {student_data[1]}")
            print(f"Full name: {student_data[3]} {student_data[4]}")
            print(f"Date of birth: {student_data[5]}/{student_data[6]}/{student_data[7]}")
    else:
        print("Incorrect email or password. Try again.")
def main():
    while True:
        decision = input("Type 'S' to sign up and type 'L' to login. Type 'Q' to quit: ")
        if decision == 'S':
            sign_up()
        elif decision == 'L':
            log_in()
        elif decision == 'Q':
            print("Thank you for using School System!")
            break

if __name__ == '__main__':
    main()

connection.close()