import argparse
from datetime import datetime
import os
from collections import defaultdict
from pickle import GLOBAL
from pprint import pprint as pp
import csv


# TODO handle "next friday"
# TODO изучаем ооп
# TODO сделать одну функцию на вывод по одной дате + диапазон
# TODO выборку записей по всем выходным текущего месяца
# TODO сделать одну функцию для вывода диапазона, по дате , по времени

# TODO_DB_FILE = "myfile.txt"
TODO_DB_FILE = "myfile.csv"

def update_data() -> dict:
    database = {}
    if os.path.exists(TODO_DB_FILE):
        with open(TODO_DB_FILE, 'r', encoding='utf-8') as f:
            strings_file = f.readlines()
            tags_list = strings_file[0].strip().split('-')
            database['tags'] = tags_list
            records = []
            for i in range(1, len(strings_file)):
                record_data = strings_file[i].strip().split(' ', maxsplit=4)
                record = {}
                date_time = datetime.strptime(f'{record_data[0]} {record_data[1]}', "%Y-%m-%d %H:%M")
                record['date'] = date_time
                record['daily'] = bool(int(record_data[2]))
                record['tags'] = record_data[3].split('/')
                record['task'] = record_data[4]
                records.append(record)
            database['records'] = records
            return database
    else:
        with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
            print("Приложение запущено.")
            return database

def sort_database(database: dict) -> tuple:
    return database['date'].date(), database['daily'], database['date'].time()

def start_help() -> None:
    print('\nВыбери необходимое действие:\n1 - Добавить заметку\n'
          '2 - Посмотреть все заметки(long)\n'
          '3 - Посмотреть все заметки(compact)\n'
          '4 - Посмотреть все заметки(short)\n'
          '5 - Посмотреть заметки на день\n'
          '6 - Посмотреть заметки в диапазоне дат\n'
          '7 - Удалить запись\n'
          '8 - Посмотреть все заметки(table)')


def add_todo(database: dict, date, time, note, daily) -> list:  # TODO проверка правильности ввода данных юзером
    date_time = datetime.strptime(f'{date} {time}', "%Y-%m-%d %H:%M")
    record = {}
    record['date'] = date_time
    record['daily'] = bool(int(daily))
    record['task'] = note
    record['tags'] = ['0']
    database['records'].append(record)
    return database

def read_todo_day(database: dict, date_todo: datetime) -> dict:
    tags = database['tags']
    records = []
    for i in database['records']:
        record = {}
        if i['date'] == date_todo:
            # date_time = datetime.strptime(f'{record_data[0]} {record_data[1]}', "%Y-%m-%d %H:%M")
            record['date'] = i['date']
            record['daily'] = i['daily']
            record['tags'] = i['tags']
            record['task'] = i['task']
            records.append(record)
        database = {}
        database['tags'] = tags
        database['records'] = records
    return database

def my_records(dictionary: dict) -> dict:
    record = {}
    record['date'] = dictionary['date']
    record['daily'] = dictionary['daily']
    record['tags'] = dictionary['tags']
    record['task'] = dictionary['task']
    return record

def read_todo_daytime_or_diapazon(database: dict, daily=0, start_date: datetime = None, finish_date: datetime = None) -> dict:
    records = []
    tags = database['tags']
    if finish_date is None and daily == 1:
        for i in database['records']:
            if i['date'].date() == start_date.date():
                records.append(my_records(i))
    elif finish_date is None and daily == 0:
        for i in database['records']:
            if i['date'] == start_date:
                records.append(my_records(i))
    elif finish_date:
        for i in database['records']:
            if start_date <= i['date'] <= finish_date:
                records.append(my_records(i))
    database = {}
    database['tags'] = tags
    database['records'] = records
    return database

def show_compact(database: dict) -> None:
    # Создаем словарь для группировки по датам
    grouped_data = defaultdict(list)
    # Группируем данные по дате (без учета времени)
    for entry in database['records']:
        date_key = entry['date'].date()  # Получаем только дату
        grouped_data[date_key].append(entry)
    # Преобразуем обратно в список вложенных списков
    result = list(grouped_data.values())
    for list_day in result:
        list_task_daily = [x for x in list_day if x['daily'] is True]
        # list_task_daily1 = list(filter(lambda x: x[1] == '1', list_day))
        list_task_time = [x for x in list_day if x['daily'] is False]
        # list_task_time = list(filter(lambda x: x[0] == '1', list_day))
        print(f'[{list_day[0]['date'].date()}]\n============')
        if list_task_daily:
            for line in list_task_daily:
                print(f'* {line["task"]}')
        print('------------')
        if list_task_time:
            for line in list_task_time:
                print(f'{line["date"].time()} - {line["task"]}')
        print('.............\n')

def show_short1(database: dict) -> None:
    # Создаем словарь для группировки по датам
    grouped_data = defaultdict(list)
    # Группируем данные по дате (без учета времени)
    for entry in database['records']:
        date_key = entry['date'].date()  # Получаем только дату
        grouped_data[date_key].append(entry)
    # Преобразуем обратно в список вложенных списков
    result = list(grouped_data.values())
    for list_day in result:
        list_task_daily = [x for x in list_day if x['daily'] is True]
        # list_task_daily1 = list(filter(lambda x: x[1] == '1', list_day))
        list_task_time = [x for x in list_day if x['daily'] is False]
        # list_task_time = list(filter(lambda x: x[0] == '1', list_day))
        print(f'{list_day[0]['date'].date()}')
        if list_task_time:
            for line in list_task_time:
                print(f'{str(line["date"].strftime("%H:%M")):>10} | {line["task"]}')
        if list_task_daily:
            for line in list_task_daily:
                print(f'{"*":>6} {"|":>5} {line["task"]}')

def show_table(database: dict, len_task=40, len_daily=40) -> None:
    def truncate_task(task: str, max_length: int) -> str:
        """Обрезает задачу, если она превышает max_length, добавляя многоточие."""
        if len(task) > max_length:
            return task[:max_length - 3] + '...'
        return task
    # Создаем словарь для группировки по датам
    grouped_data = defaultdict(list)
    # Группируем данные по дате (без учета времени)
    header = f"+------------+{'-' * (len_task + 2)}+{'-' * (len_daily + 2)}+"
    date_row = f"|  Date      |{' ' * (len_task // 2)}Task{' ' * (len_task - (len_task // 2) - 2)}|{' ' * (len_daily // 2 - 4)}Daily Task{' ' * (len_daily - (len_daily // 2) - 4)}|"
    time_row = f"|     Time   |  {' ' * (len_task)}|  {' ' * (len_daily)}|"
    print(f'{header}\n{date_row}\n{time_row}\n{header}')
    for entry in database['records']:
        date_key = entry['date'].date()  # Получаем только дату
        grouped_data[date_key].append(entry)
    # Преобразуем обратно в список вложенных списков
    result = list(grouped_data.items())
    for date_key, list_day in result:
        # Задачи с daily: False
        list_task_time = [x for x in list_day if x['daily'] is False]
        # Задачи с daily: True
        list_task_daily = [x for x in list_day if x['daily'] is True]
        # Выводим дату
        print(f'| {date_key} |  {"":>{len_task}}|  {"":>{len_daily}}|')
        # Определяем максимальное количество задач в день
        max_length = max(len(list_task_time), len(list_task_daily))
        for i in range(max_length):
            time_task = list_task_time[i] if i < len(list_task_time) else {'date': None, 'task': ''}
            daily_task = list_task_daily[i] if i < len(list_task_daily) else {'task': ''}
            time_str = time_task['date'].strftime("%H:%M") if time_task['date'] else ''
            task_str = truncate_task(time_task["task"], len_task)  # Обрезаем задачу
            daily_str = truncate_task(daily_task["task"], len_daily)  # Обрезаем ежедневную задачу
            print(f'| {time_str:>10} | {task_str:<{len_task}} | {daily_str:<{len_daily}} |')
            # print(f'| 1-{len(time_str)} | 2-{len(task_str)} | 3-{len(daily_str)} |')
        print(header)

def show_long(database: dict) -> None:
    # Создаем словарь для группировки по датам
    grouped_data = defaultdict(list)
    # Группируем данные по дате (без учета времени)
    for entry in database['records']:
        date_key = entry['date'].date()  # Получаем только дату
        grouped_data[date_key].append(entry)
    # Преобразуем обратно в список вложенных списков
    result = list(grouped_data.values())
    for list_day in result:
        list_task_daily = [x for x in list_day if x['daily'] is True]
        # list_task_daily1 = list(filter(lambda x: x[1] == '1', list_day))
        list_task_time = [x for x in list_day if x['daily'] is False]
        # list_task_time = list(filter(lambda x: x[0] == '1', list_day))
        print(f'{list_day[0]['date'].date()}', end=' ')
        if list_task_time and list_task_daily:
            print(f'{list_task_time[0]["date"].strftime("%H:%M")} - {list_task_time[0]["task"]}')
            for line in list_task_time:
                print(f'{str(line["date"].strftime("%H:%M")):>16} - {line["task"]}')
            for line in list_task_daily:
                print(f'{"*":>12} {line["task"]}')
        elif list_task_daily:
            for line in list_task_daily:
                print(f'* {line["task"]}')
        else:
            for line in list_task_time:
                print(f'{line["date"].strftime("%H:%M")} - {line["task"]}')

def read_todo_day_time(time2: datetime, database: dict) -> list:
    list_time = []
    for i in range(1, len(database['records']) - 1):
        pp(time2)
        pp(type(time2))
        pp(database['records'][i]['date'])
        pp(type(database['records'][i]['date']))
        if database['records'][i]['date'] == time2:
            list_time.append(i)
    return list_time

def del_todo(database, del_dict: dict) -> None:
    tags = database['tags']
    result = [item for item in database['records'] if item not in del_dict['records']]
    database = {}
    database['tags'] = tags
    database['records'] = result
    return database

def save_to_file(database: dict) -> None:
    with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
        print('-'.join(database['tags']), file=f)
        for string in database['records']:
            f.write(
                f'{string['date'].strftime("%Y-%m-%d %H:%M")} {int(string['daily'])} {'/'.join(string['tags'])} {string['task']}' + '\n')

def interactive_mode() -> None:
    esc1 = '1'
    database = update_data()
    while esc1 != '0':
        start_help()
        database['records'] = sorted(database['records'], key=sort_database)
        # pp(database)
        comm1 = int(input('Введите номер операции: '))
        # TODO доделать ввод времени
        if comm1 == 1:
            # Получаем текущую дату
            default_date = datetime.now()
            # Запрашиваем ввод пользователя
            user_input = input(
                f"Введите дату в формате '{default_date.date()}'. Если запись на сегодня, нажмите Enter: ")
            # Если пользователь не ввел ничего, используем текущую дату
            if not user_input:
                user_date = default_date.strftime("%Y-%m-%d")
            else:
                user_date = user_input
            time_todo = input('Если задача на весь день, нажмите Enter. Если нет, напишите время в форматe "12:00": ')
            if not time_todo:
                ask_todo = input('Введите дату в формате: "Встреча с командой" - ')  # Текст события
                date1 = user_date
                time1 = '00:00'
                database = add_todo(database, date1, time1, ask_todo, '1')
            else:
                date1 = user_date
                time1 = time_todo
                ask_todo = input('Введите дату в формате: "Встреча с командой" - ')  # Текст события
                database = add_todo(database, date1, time1, ask_todo, '0')
        elif comm1 == 2:
            show_long(database)
        elif comm1 == 3:
            show_compact(database)
        elif comm1 == 4:
            show_short1(database)
        elif comm1 == 5:
            date2 = input('Введите дату записи в формате: "2023-10-01 - ')
            date_time = datetime.strptime(f'{date2}', "%Y-%m-%d")
            show_table(read_todo_daytime_or_diapazon(database, 1, date_time))
        elif comm1 == 6:
            start1 = input('Введите дату начала диапазона в формате: "2023-10-01 - ')
            finish1 = input('Введите дату конца диапазона в формате: "2023-10-01 - ')
            start_date = datetime.strptime(start1, "%Y-%m-%d")
            end_date = datetime.strptime(finish1, "%Y-%m-%d")
            show_table(read_todo_daytime_or_diapazon(database, 1, start_date, end_date))
        elif comm1 == 7:
            date2 = input('Введите дату записи, которую нужно удалить в формате: "2023-10-01 - ')
            time2 = input('Введите время записи, которую нужно удалить в формате: "14:30" - ')
            date_time = datetime.strptime(f'{date2} {time2}', "%Y-%m-%d %H:%M")
            show_table(read_todo_day(database, date_time))
            del1 = input('Если хотите удалить эти данные, напишите y\n'
                         'В противном случае, напишите n')
            if del1 == 'y':
                database = del_todo(database, read_todo_day(database, date_time))
        elif comm1 == 8:
            show_table(database)
        esc1 = input('\nДля продолжения работы программы нажмите Enter.\nДля завершения напишите 0')
    save_to_file(database)


def popit(args):
    args.pop(0)
    args.pop(0)

def del_todo2(database, day, task) -> None:
    tags = database['tags']
    pp(database)
    result = [item for item in database['records'] if item['task'] != task or item['date'].date() != day]
    database = {}
    database['tags'] = tags
    database['records'] = result
    pp(database)
    return database

def date_10(str10: str) -> datetime:
    return datetime.strptime(str10, "%Y-%m-%d")

def date_16(str16: str) -> datetime:
    return datetime.strptime(f'{str16[:10]} {str16[-5:]}', "%Y-%m-%d %H:%M")

# def main():
#     database = update_data()
#     while args:
#         arg = args[0]
#         if arg == '-i' or arg == '--interactive':
#             interactive_mode()
#         elif arg == '-v' or arg == '--view':
#             if args[1] == 'short':
#                 show_short1(database)
#             elif args[1] == 'compact':
#                 show_compact(database)
#             elif args[1] == 'long':
#                 show_long(database)
#             elif args[1] == 'table':
#                 show_table(database)
#         elif arg == '-r' or arg == '--remove':
#             day1 = datetime.strptime(args[1], "%Y-%m-%d").date()
#             task1 = ' '.join(args[2:])
#             save_to_file(del_todo2(database, day1, task1))
#         elif arg == '-a' or arg == '--add':
#             if len(args[1]) == 10:
#                 database = add_todo(database, args[1], '00:00', args[2], '1')
#                 save_to_file(database)
#             elif len(args[1]) == 16:
#                 database = add_todo(database, args[1][:10], args[1][-5:], args[2], '0')
#                 save_to_file(database)
#         elif arg == '-l' or arg == '--list':
#             if len(args) < 3:
#                 if len(args[1]) == 10:
#                     start_date = datetime.strptime(args[1], "%Y-%m-%d")
#                     show_table(read_todo_daytime_or_diapazon(database, 1, start_date))
#                 elif len(args[1]) == 16:
#                     start_date = datetime.strptime(f'{args[1][:10]} {args[1][-5:]}', "%Y-%m-%d %H:%M")
#                     show_table(read_todo_daytime_or_diapazon(database,0, start_date))
#             else:
#                 if len(args[1]) == 10 and len(args[2]) == 10:
#                     show_table(read_todo_daytime_or_diapazon(database, 1, date_10(args[1]), date_10(args[2])))
#                 elif len(args[1]) == 10 and len(args[2]) == 16:
#                     show_table(read_todo_daytime_or_diapazon(database, 0, date_10(args[1]), date_16(args[2])))
#                 elif len(args[1]) == 16 and len(args[2]) == 16:
#                     show_table(read_todo_daytime_or_diapazon(database, 0, date_16(args[1]), date_16(args[2])))
#                 elif len(args[1]) == 16 and len(args[2]) == 10:
#                     show_table(read_todo_daytime_or_diapazon(database, 0, date_16(args[1]), date_10(args[2])))
#
#         args.clear()

def main():
    database = update_data()
    parser = argparse.ArgumentParser(description='Пример использования argparse.')
    parser.add_argument('-i', '--interactive', action='store_true', help='Запустить интерактивный режим.', required=False)
    parser.add_argument('-v', '--view', choices=['short', 'long', 'table', 'compact'], help='Показать все записи.', required=False)
    parser.add_argument('-r', '--remove', nargs='+', help='Удалить запись.', required=False)
    parser.add_argument('-a', '--add', nargs='+', help='Добавить запись.', required=False)
    parser.add_argument('-l', '--list', nargs='+', help='Показать записи на день или в диапазоне дат', required=False)

    args = parser.parse_args()

    if args.view == 'short':
        show_short1(database)
    elif args.view == 'long':
        show_long(database)
    elif args.view == 'table':
        show_table(database)
    elif args.view == 'compact':
        show_compact(database)
    elif args.interactive:
        interactive_mode()
    elif args.remove:
        pp(args.remove[0])
        date = datetime.strptime(args.remove[0], "%Y-%m-%d").date()
        pp(date)
        message = ' '.join(args.remove[1:])  # Остальные значения - это сообщение
        pp(message)
        save_to_file(del_todo2(database, date, message))
    elif args.add:
        if len(args.add[0]) == 10:
            database = add_todo(database, args.add[0], '00:00', args.add[1], '1')
            save_to_file(database)
        elif len(args.add[0]) == 16:
            database = add_todo(database, args.add[0][:10], args.add[0][-5:], args.add[1], '0')
            save_to_file(database)
    elif args.list:
        pp(len(args.list))
        if len(args.list) < 2:
            if len(args.list[0]) == 10:
                start_date = datetime.strptime(args.list[0], "%Y-%m-%d")
                show_table(read_todo_daytime_or_diapazon(database, 1, start_date))
            elif len(args.list[0]) == 16:
                start_date = datetime.strptime(f'{args.list[0][:10]} {args.list[0][-5:]}', "%Y-%m-%d %H:%M")
                show_table(read_todo_daytime_or_diapazon(database,0, start_date))
        else:
            if len(args.list[0]) == 10 and len(args.list[1]) == 10:
                show_table(read_todo_daytime_or_diapazon(database, 1, date_10(args.list[0]), date_10(args.list[1])))
            elif len(args.list[0]) == 10 and len(args.list[1]) == 16:
                show_table(read_todo_daytime_or_diapazon(database, 0, date_10(args.list[0]), date_16(args.list[1])))
            elif len(args.list[0]) == 16 and len(args.list[1]) == 16:
                show_table(read_todo_daytime_or_diapazon(database, 0, date_16(args.list[0]), date_16(args.list[1])))
            elif len(args.list[0]) == 16 and len(args.list[1]) == 10:
                show_table(read_todo_daytime_or_diapazon(database, 0, date_16(args.list[0]), date_10(args.list[1])))












# interactive_mode()

if __name__ == "__main__":
    main()
