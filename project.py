import json
from getpass import getpass
import re
import datetime

email_regex = r'^[A-Za-z0-9._]+@[A-Za-z0-9.]+\.[A-Za-z]{2,}$'
phone_regex = r'^01[0-2]\d{8}$'
date_regex = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def write_users(users):
    with open("users.json", "w") as file_users:
        json.dump(users, file_users)

def read_users():
    try:
        with open("users.json", "r") as file_users:
            return json.load(file_users)
    except FileNotFoundError:
        return {}
    
def write_projects(projects):
    with open("projects.json", "w") as file_projects:
        json.dump(projects, file_projects, cls=DateTimeEncoder)

def read_projects():
    try:
        with open("projects.json", "r") as file_projects:
            return json.load(file_projects)
    except FileNotFoundError:
        return []

def registeration(users):
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    while not re.match(email_regex, email):
        print('Please enter valid email.')
        email = input("Email: ")
    if email in users:
        print("Email already registered")
        return
    password = getpass("password: ")
    while not password.strip():
        print("Password can't be empty")
        password = getpass("password: ")
    confirm_password = getpass("Confirm Password: ")
    while password != confirm_password:
        print("Passwords don't match")
        password = getpass("password: ")
        confirm_password = getpass("Confirm Password: ")
    phone = input("Phone: ")
    while not re.match(phone_regex, phone):
        print('Please enter valid phone number.')
        phone = input("Phone: ")

    users[email] = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'mobile_phone': phone
    }

    write_users(users)
    print("Registration successful.")

def login(users):
    email = input("Email: ")
    password = getpass("Password: ")
    if email in users and users[email]['password'] == password:
        print("Login successful.")
        return email
    else:
        print("Invalid email or password.")
        return None



def create_project(current_user_email):
    if current_user_email is None:
        print("Please log in before creating a project.")
        return
    
    title = input("Enter project title: ")
    while not title.strip():
        print("Title can't be empty.")
        title = input("Enter project title: ")

    details = input("Enter project details: ")
    while not details.strip():
        print("Details can't be empty.")
        details = input("Enter project details: ")

    while True:
        total_target_contain = input("Enter total target: ")
        if total_target_contain.strip():
            try:
                total_target = float(total_target_contain)
                break
            except ValueError:
                print("Invalid total target. Please enter a valid number")
        else:
            print("Total target can't be empty.")

    start_time = input("Enter start time: ")
    while not start_time.strip():
        print("Start time can't be empty.")
        start_time = input("Enter start time: ")

    end_time = input("Enter end time: ")
    while not end_time.strip():
        print("End time can't be empty.")
        end_time = input("Enter end time: ")

    while not re.match(date_regex, start_time) or not re.match(date_regex, end_time):
        print("Please Enter valid date.")
        start_time = input("Enter start time: ")
        end_time = input("Enter end time: ")

    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")

    if start_time >= end_time:
        print("Start time should be before End time.")
        return
    
    project = {
        "title": title,
        "details": details,
        "total_target": total_target,
        "start_time": start_time,
        "end_time": end_time,
        "user_email": current_user_email
    }

    projects.append(project)
    write_projects(projects)

    print("Project created successfully.")



def view_projects(current_user_email):
    if not projects:
        print("No projects available.")
    else:
        index = 1
        for project in projects:
            if project['user_email'] == current_user_email:

                print(f"Project {index}:")
                print(f"""
                    Title: {project['title']}
                    Details: {project['details']}
                    Total Target: {project['total_target']} EGP
                    Start Time: {project['start_time']}
                    End Time: {project['end_time']}
                    """)
            else:
                print(f"You don't have permission to view project {index}.")
            index += 1



def delete_project(current_user_email):
    index = int(input("Enter the index of the project you want to delete: ")) - 1

    while index < 0 or index >= len(projects):
        print("Please enter valid project index.")
        index = int(input("Please enter the index of the project you want to delete: ")) - 1

    if projects[index]['user_email'] == current_user_email:
        del projects[index]
        write_projects(projects)
        print("Project deleted successfully.")
    else:
        print(f"You don't have permission to delete project {index}.")



def edit_project(current_user_email):
    index = int(input("Enter the index of the project you want to edit: ")) - 1

    while index < 0 or index >= len(projects):
        print("Please enter valid project index.")
        index = int(input("Please enter the index of the project you want to edit: ")) - 1
    
    project = projects[index]

    if project['user_email'] != current_user_email:
        print(f"You do not have permission to edit project {index}.")
        return

    title = input("Enter new project title (If you want to edit it): ")
    details = input("Enter new project details (If you want to edit it): ")
    total_target = input("Enter new total target (If you want to edit it): ")
    start_time = input("Enter new start time (If you want to edit it): ")
    end_time = input("Enter new end time (If you want to edit it): ")

    if title:
        project['title'] = title
    if details:
        project['details'] = details
    if total_target:
        project['total_target'] = float(total_target)
    if start_time:
        while not re.match(date_regex, start_time):
            print("Please Enter valid date.")
            start_time = input("Enter new start time (If you want to edit it): ")

        project['start_time'] = start_time
    if end_time:
        while not re.match(date_regex, end_time):
            print("Please Enter valid date.")
            end_time = input("Enter new end time (If you want to edit it): ")

        project['end_time'] = end_time
    
    write_projects(projects)
    print("Project edited successfully.")






users = read_users()
projects = read_projects()

current_user_email = None

while True:
    print("1. Register")
    print("2. Login")
    print("3. Create Project")
    print("4. View Projects")
    print("5. Edit Project")
    print("6. Delete Project")
    print("7. Exit")

    choice = input("Choose: ")

    if choice == '1':
        registeration(users)
    elif choice == '2':
        current_user_email = login(users)
    elif choice == '3':
        create_project(current_user_email)
    elif choice == '4':
        view_projects(current_user_email)
    elif choice == '5':
        edit_project(current_user_email)
    elif choice == '6':
        delete_project(current_user_email)
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please choose from 1 to 7.")