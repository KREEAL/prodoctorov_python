import os

import requests
import json
from datetime import datetime
from requests import RequestException

data = []
tasks = []

try:
    users_response = requests.get("https://json.medrating.org/users")
    tasks_response = requests.get("https://json.medrating.org/todos")

    data = json.loads(users_response.text)
    tasks = json.loads(tasks_response.text)
except RequestException:
    print("Server error")
    exit(404)
except ValueError:
    print("Data error")
    exit(500)


# validates the one task from tasks
def validate_task(task):
    if 'userId' in task.keys() and 'id' in task.keys() and 'title' in task.keys():
        return True
    else:
        return False


# format string to desired length
def format_title(title):
    if len(str(title)) > 48:
        formatted_string = "%.48s" % title
        return str.strip(formatted_string) + "..."
    elif len(str(title)) == 0:
        return "TASK WITHOUT ITLE"
    else:
        return title


# gets the time of report creation from existing file
def get_creation_time(file_path):
    with open(file_path) as file:
        lines = file.readlines()
        dt = lines[1][-17:-1]
        formed_dt = dt[6:10] + "-" + dt[0:2] + "-" + dt[3:5] + "T" + dt[-5:-3] + "-" + dt[-2:]
        return formed_dt


# getting lists of completed and not completed tasks by employee id
def get_tasks_by_id(person_id):
    goodl = list()
    badl = list()
    for task in tasks:
        if validate_task(task):
            if task['userId'] == person_id:
                formatted_title = format_title(task['title'])
                if task['completed']:
                    goodl.append(formatted_title)
                else:
                    badl.append(formatted_title)
    return goodl, badl


# just switches the time in current report if needed
def switch_datetime(person_username):
    with open(f"./tasks/{person_username}.txt", 'r') as file:
        old_data = file.read()
    lines = file.readlines()
    dt = lines[1][-17:-1]
    new_data = old_data.replace(dt, datetime.now().strftime("%d.%m.%Y %H:%M"))
    file.close()
    with open(f"./tasks/{person_username}.txt", 'w') as f:
        f.write(new_data)
    f.close()


# renaming the old reports
def rename_old_report(person_username):
    files = os.listdir("./tasks")
    if f"{person_username}.txt" in files:
        creation_time = get_creation_time(f"./tasks/{person_username}.txt")
        if f"./tasks/old_{person_username}_{creation_time}.txt" not in files:
            try:
                os.rename(f"./tasks/{person_username}.txt", f"./tasks/old_{person_username}_{creation_time}.txt")
            except FileExistsError:
                print("CAN'T RENAME FILE")
        else:
            switch_datetime(person_username)


# creates the new file and directory if needed
def create_report(person_username):
    if not (os.path.exists("./tasks")):
        os.mkdir("./tasks")
    f = open(f"./tasks/{person_username}.txt", mode='w')
    return f


# forms the text for one report
def form_report_text(person):
    formed_report = """"""
    tasks_titles = get_tasks_by_id(int(person['id']))
    list_completed = """"""
    list_uncompleted = """"""

    for item in tasks_titles[0]:
        list_completed += "\n" + item

    for item in tasks_titles[1]:
        list_uncompleted += "\n" + item

    if len(tasks_titles[0]) == 0:
        list_completed += "\nЗавершенные задачи отсутствуют"

    if len(tasks_titles[1]) == 0:
        list_uncompleted += "\nНеавершенные задачи отсутствуют"

    formed_report += "Отчёт для " + person['company']['name'] + "\n" + person[
        'name'] + f" <{person['email']}>" + datetime.now().strftime(
        " %d.%m.%Y %H:%M") + "\n" + f"Всего задач: {(len(tasks_titles[0]) + len(tasks_titles[1]))}" + "\n\n" + \
        f"Завершенные задачи ({len(tasks_titles[0])}):" + list_completed + "\n\n" + \
        f"Оставшиеся задачи ({len(tasks_titles[1])}):" + list_uncompleted

    return formed_report


# forms the all files
def form_reports():
    for person in data:
        report_text = form_report_text(person)
        rename_old_report(person['username'])
        file = create_report(person['username'])
        file.write(report_text)
        file.close()


def main():
    form_reports()


if __name__ == '__main__':
    main()
