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


def form_report():
    for person in data:
        tasks_titles = get_tasks_by_id(int(person['id']))
        print("Отчёт для " + person['company']['name'])
        print(person['name'] + f" <{person['email']}>"+datetime.now().strftime(" %d.%m.%Y %H:%M"))
        print(f"Всего задач: {(len(tasks_titles[0])+len(tasks_titles[1]))}")
        print()
        print(f"Завершенные задачи ({len(tasks_titles[0])}):")
        for item in tasks_titles[0]:
            print(item)
        print()
        print(f"Оставшиеся задачи ({len(tasks_titles[1])}):")
        for item in tasks_titles[1]:
            print(item)
        print()


def main():
    form_report()


if __name__ == '__main__':
    main()
