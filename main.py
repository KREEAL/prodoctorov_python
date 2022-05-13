import os

import requests
import json
from datetime import datetime

users_response = requests.get("https://json.medrating.org/users")
tasks_response = requests.get("https://json.medrating.org/todos")

data = json.loads(users_response.text)
tasks = json.loads(tasks_response.text)


# persons=словарь людей

def format_title(title):
    if len(str(title)) > 48:
        formatted_string = "%.48s" % title
        return str.strip(formatted_string) + "..."
    else:
        return title


def get_tasks_by_id(person_id):
    goodl = list()
    badl = list()
    for task in tasks:
        if task['id'] < 201:  # проверка на валидность джсона
            if task['userId'] == person_id:
                formatted_title = format_title(task['title'])
                if task['completed']:
                    goodl.append(formatted_title)
                else:
                    badl.append(formatted_title)
    return goodl, badl


def create_file(name):
    if not (os.path.exists("./tasks")):
        os.mkdir("./tasks")
    f = open(f"./tasks/{name}.txt", mode='w')
    return f


def form_report():
    formed_report = """"""
    for person in data:
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
            " %d.%m.%Y %H:%M") + "\n" + f"Всего задач: {(len(tasks_titles[0]) + len(tasks_titles[1]))}" + "\n\n" + f"Завершенные задачи ({len(tasks_titles[0])}):" + list_completed + "\n\n" + f"Оставшиеся задачи ({len(tasks_titles[1])}):" + list_uncompleted

        file = create_file(person['name'])
        file.write(formed_report)
        formed_report = """"""

def main():
    form_report()


if __name__ == '__main__':
    main()
