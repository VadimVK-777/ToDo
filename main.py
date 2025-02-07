from datetime import datetime
import os
from pickle import GLOBAL

# <class 'datetime.date'> - str
# TODO handle "next friday"
# TODO добавить типизацию
# TODO 1. переписать недостающие части, 2. добавить типизацию. 3. изучаем ооп
# TODO убрать секунды
# 1. загрузка данных => данные уже в приложении
# 2. работа с данными которые в приложении
# 3. сохранение данных из приложения в файл

TODO_DB_FILE = "myfile.txt"
list_data = []

def update_data() -> list:
    if os.path.exists(TODO_DB_FILE):
        with open(TODO_DB_FILE, 'r', encoding='utf-8') as f:
            list1 = f.readlines()
            for line in list1:
                list_str = []
                record = line.strip().split(' ', maxsplit=2)
                date_time = datetime.strptime(f'{record[0]} {record[1]}', "%Y-%m-%d %H:%M:%S")
                list_str.append(date_time)
                list_str.append(record[2])
                list_data.append(list_str)
                list_data.sort()
    else:
        with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
            print("Приложение запущено.")
    return list_data

def help1() -> None:
    print('\nВыбери необходимое действие:\n1 - Добавить заметку\n'
          '2 - Посмотреть все заметки\n3 - Посмотреть заметку на дату\n'
          '4 - Посмотреть заметку на дату и время\n'
          '5 - Посмотреть заметки в диапазоне дат\n'
          '6 - Удалить запись')

def add_todo(list_data: list) -> list: #TODO проверка правильности ввода данных юзером
    date_1 = input('Введите дату в формате: "2023-10-01" - ') # Дата события
    time_1 = input('Введите дату в формате: "14:15" - ')  # Время события
    date_todo = datetime.strptime(date_1, "%Y-%m-%d").date()
    time_todo = datetime.strptime(time_1, "%H:%M").time()
    my_time = datetime.combine(date_todo, time_todo)
    ask_todo = input('Введите дату в формате: "Встреча с командой" - ') # Текст события
    new_string = []
    new_string.extend([my_time, ask_todo])
    list_data.append(new_string)
    list_data.sort()
    print(list_data)
    return list_data

def data_show(list_data: list) -> None:
    for line in list_data:
        print(*line)

def read_todo_day(date1: datetime) -> list:
    list_day = []
    for i in list_data:
        if i[0].date() == date1.date():
            list_day.append(i)
    return list_day

def read_todo_day_time(time2: datetime) -> list:
    list_time = []
    for i in list_data:
        if i[0] == time2:
            list_time.append(i)
    return list_time

def read_todo_diapazon(start_date: datetime, finish_date: datetime) -> list:
    list_diapazon = []
    for i in list_data:
        # print(i[0])
        # print(start_date)
        # print(finish_date)
        if start_date <= i[0] <= finish_date:
            list_diapazon.append(i)
    return list_diapazon

def del_todo(del_list: list) -> None:
    global list_data
    result = [item for item in list_data if item not in del_list]
    list_data = result


def main() -> None:
    esc1 = '1'
    update_data()
    while esc1 != '0':
        help1()
        comm1 = int(input('Введите номер операции: '))
        if comm1 == 1:
            add_todo(list_data)
        elif comm1 == 2:
            data_show(list_data)
        elif comm1 == 3:
            date1 = input('Введите дату в формате: "2023-10-01 - ')
            date_todo = datetime.strptime(date1, "%Y-%m-%d")
            data_show(read_todo_day(date_todo))
        elif comm1 == 4:
            date2 = input('Введите дату записи в формате: "2023-10-01 - ')
            time2 = input('Введите время записи в формате: "14:30" - ')
            date_time = datetime.strptime(f'{date2} {time2}', "%Y-%m-%d %H:%M:%S")
            data_show(read_todo_day_time(date_time))
            # print(*read_todo_day_time(time2, read_todo_day(date2)), sep='')
        elif comm1 == 5:
            start1 = input('Введите дату начала диапазона в формате: "2023-10-01 - ')
            finish1 = input('Введите дату конца диапазона в формате: "2023-10-01 - ')
            start_date = datetime.strptime(start1, "%Y-%m-%d")
            end_date = datetime.strptime(finish1, "%Y-%m-%d")
            data_show(read_todo_diapazon(start_date, end_date))
        elif comm1 == 6:
            date2 = input('Введите дату записи, которую нужно удалить в формате: "2023-10-01 - ')
            time2 = input('Введите время записи, которую нужно удалить в формате: "14:30" - ')
            date_time = datetime.strptime(f'{date2} {time2}', "%Y-%m-%d %H:%M:%S")
            data_show(read_todo_day_time(date_time))
            del1 = input('Если хотите удалить эти данные, напишите y\n'
                         'В противном случае, напишите n')
            if del1 == 'y':
                del_todo(read_todo_day_time(date_time))
        esc1 = input('\nДля продолжения работы программы нажмите Enter.\nДля завершения напишите 0')
    with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
        for i in list_data:
            f.write(f'{i[0]} {i[1]}' + '\n')

if __name__ == "__main__":
    main()














# import sqlite3
#
# print('Это приложение ToDo для заметок')
#
# # Используем менеджер контекста для работы с базой данных
# with sqlite3.connect('todolist.db') as conn:
#     # Создаем курсор
#     cursor = conn.cursor()
#     # Создаем таблицу
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS todolist (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         date_todo DATE NOT NULL,
#         time_todo TIME NOT NULL,
#         task_todo TEXT NOT NULL
#     )
#     ''')
#     # Сохраняем изменения
#     conn.commit()
#
# def add_todo():
#     with sqlite3.connect('todolist.db') as conn:
#         # Создаем курсор
#         cursor = conn.cursor()
#         # Пример данных для добавления
#         date_todo = input('Введите дату в формате: "2023-10-01" - ') # Дата события
#         time_todo = input('Введите время в формате: "14:30" - ') # Время события
#         task_todo = input('Введите дату в формате: "Встреча с командой" - ') # Текст события
#
#         # Выполняем запрос для вставки новой записи
#         cursor.execute('''
#             INSERT INTO todolist (date_todo, time_todo, task_todo)
#             VALUES (?, ?, ?)
#             ''', (date_todo, time_todo, task_todo))
#
#         # Сохраняем изменения
#         conn.commit()
#
#     print("Запись успешно добавлена в таблицу 'todolist'!")
#
# def read_todo():
#     # Используем менеджер контекста для работы с базой данных
#     with sqlite3.connect('todolist.db') as conn:
#         # Создаем курсор
#         cursor = conn.cursor()
#
#         # Выполняем запрос для выборки всех данных из таблицы events
#         cursor.execute('SELECT * FROM todolist')
#
#         # Получаем все строки результата
#         rows = cursor.fetchall()
#
#         # Проверяем, есть ли данные и выводим их
#         if rows:
#             for row in rows:
#                 print(*row, sep=' -- ')  # Выводим каждую строку
#         else:
#             print("Таблица пуста.")
#
# def read_todo_day(date1):
#     # Используем менеджер контекста для работы с базой данных
#     with sqlite3.connect('todolist.db') as conn:
#         # Создаем курсор
#         cursor = conn.cursor()
#
#         # Выполняем запрос для выборки всех данных из таблицы todolist
#         sql = f'SELECT * FROM todolist WHERE date_todo = "{date1}"'
#
#         cursor.execute(sql)
#
#         # Получаем все строки результата
#         rows = cursor.fetchall()
#
#         # Проверяем, есть ли данные и выводим их
#         if rows:
#             for row in rows:
#                 print(*row, sep=' -- ')  # Выводим каждую строку
#         else:
#             print("Таблица пуста.")
#
# def read_todo_day_time(date2, time2):
#     # Используем менеджер контекста для работы с базой данных
#     with sqlite3.connect('todolist.db') as conn:
#         # Создаем курсор
#         cursor = conn.cursor()
#
#         # Выполняем запрос для выборки всех данных из таблицы todolist
#         sql = f'SELECT * FROM todolist WHERE date_todo = "{date2}" AND time_todo = "{time2}"'
#
#         cursor.execute(sql)
#
#         # Получаем все строки результата
#         rows = cursor.fetchall()
#
#         # Проверяем, есть ли данные и выводим их
#         if rows:
#             for row in rows:
#                 print(*row, sep=' -- ')  # Выводим каждую строку
#         else:
#             print("Нет записей по вашим условиям")
#
# def read_todo_diapazon(start_date, finish_date):
#     # Используем менеджер контекста для работы с базой данных
#     with sqlite3.connect('todolist.db') as conn:
#         # Создаем курсор
#         cursor = conn.cursor()
#
#         # Выполняем запрос для выборки всех данных из таблицы todolist
#         sql = f'SELECT * FROM todolist WHERE date_todo BETWEEN "{start_date}" AND "{finish_date}" ORDER BY date_todo ASC'
#
#         cursor.execute(sql)
#
#         # Получаем все строки результата
#         rows = cursor.fetchall()
#
#         # Проверяем, есть ли данные и выводим их
#         if rows:
#             for row in rows:
#                 print(*row, sep=' -- ')  # Выводим каждую строку
#         else:
#             print("Таблица пуста.")
#
# def del_todo(date2, time2):
#     # Используем менеджер контекста для работы с базой данных
#     with sqlite3.connect('todolist.db') as conn:
#         # Создаем курсор
#         cursor = conn.cursor()
#
#         # Выполняем запрос для выборки всех данных из таблицы todolist
#         sql = f'DELETE FROM todolist WHERE date_todo = "{date2}" AND time_todo = "{time2}"'
#
#         cursor.execute(sql)
#
#         # Получаем все строки результата
#         rows = cursor.fetchall()
#
#         # Проверяем, есть ли данные и выводим их
#         print(f"Удалено записей: {cursor.rowcount}")
#
# def help1():
#     print('\nВыбери необходимое действие:\n1 - Добавить заметку\n'
#           '2 - Посмотреть все заметки\n3 - Посмотреть заметку на дату\n'
#           '4 - Посмотреть заметку на дату и время\n'
#           '5 - Посмотреть заметки в диапазоне дат\n'
#           '6 - Удалить запись')
#
# def main():
#     esc1 = '1'
#     while esc1 != '0':
#
#         help1()
#
#         comm1 = int(input('Введите номер операции: '))
#
#         if comm1 == 1:
#             add_todo()
#         elif comm1 == 2:
#             read_todo()
#         elif comm1 == 3:
#             date1 = input('Введите дату в формате: "2023-10-01 - ')
#             read_todo_day(date1)
#         elif comm1 == 4:
#             date2 = input('Введите дату записи в формате: "2023-10-01 - ')
#             time2 = input('Введите время записи в формате: "14:30" - ')
#             read_todo_day_time(date2, time2)
#         elif comm1 == 5:
#             start_date = input('Введите дату начала диапазона в формате: "2023-10-01 - ')
#             finish_date = input('Введите дату конца диапазона в формате: "2023-10-01 - ')
#             read_todo_diapazon(start_date, finish_date)
#         elif comm1 == 6:
#             date2 = input('Введите дату записи, которую нужно удалить в формате: "2023-10-01 - ')
#             time2 = input('Введите время записи, которую нужно удалить в формате: "14:30" - ')
#             read_todo_day_time(date2, time2)
#             del1 = input('Если хотите удалить эти данные, напишите y\n'
#                          'В противном случае, напишите n')
#             if del1 == 'y':
#                 del_todo(date2, time2)
#         esc1 = input('\nДля продолжения работы программы нажмите Enter.\nДля завершения напишите 0')
#
#
# if __name__ == "__main__":
#     main()






