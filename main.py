from datetime import datetime
import os
from pickle import GLOBAL

# TODO handle "next friday"
# TODO изучаем ооп
# TODO убрать секунды
# TODO сделать одну функцию на вывод по одной дате + диапазон
# TODO выборку записей по всем выходным текущего месяца
# TODO сделать одну функцию для вывода диапазона, по дате , по времени

TODO_DB_FILE = "myfile.txt"
list_data = []

def update_data() -> list:
    if os.path.exists(TODO_DB_FILE):
        with open(TODO_DB_FILE, 'r', encoding='utf-8') as f:
            strings_file = f.readlines()
            for line in strings_file:
                list_str = []
                record = line.strip().split(' ', maxsplit=3)
                date_time = datetime.strptime(f'{record[0]} {record[1]}', "%Y-%m-%d %H:%M:%S")
                list_str.append(date_time)
                list_str.append(record[2])
                list_str.append(record[3])
                list_data.append(list_str)
                list_data.sort()
            return list_data

    else:
        with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
            print("Приложение запущено.")
            return list_data

def start_help() -> None:
    print('\nВыбери необходимое действие:\n1 - Добавить заметку\n'
          '2 - Посмотреть все заметки\n3 - Посмотреть заметку на дату\n'
          '4 - Посмотреть заметку на дату и время\n'
          '5 - Посмотреть заметки в диапазоне дат\n'
          '6 - Удалить запись')

def add_todo(date_time, note, daily) -> list: #TODO проверка правильности ввода данных юзером
    new_string = []
    new_string.extend([date_time, daily, note])
    list_data.append(new_string)
    list_data.sort()
    return list_data

def data_show(list_data: list) -> None:
    for index,line in enumerate(list_data, 1):
        if bool(int(line[1])):
            print(f'{index}. {line[0].date()} - заметка на весь день - {line[2]}')
        else:
            print(f'{index}. {line[0]} - {line[2]}')

# TODO сделать короткий вывод
def data_show_short(list_data: list) -> None:
    for line in list_data:
        if line[1]:
            print(f'{line[0].date()} - заметка на весь день - {line[2]}')
        else:
            print(f'{line[0]} - {line[2]}')

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

def read_todo_daytime_or_diapazon(start_date: datetime, finish_date: datetime=None) -> list:
    res_list = []
    print(start_date)
    if finish_date is None:
        for i in list_data:
            if i[0] == start_date:
                res_list.append(i)
        return res_list
    else:
        for i in list_data:
            if start_date <= i[0] <= finish_date:
                res_list.append(i)
        return res_list

def del_todo(del_list: list) -> None:
    global list_data
    result = [item for item in list_data if item not in del_list]
    list_data = result

def main() -> None:
    esc1 = '1'
    update_data()
    while esc1 != '0':
        start_help()
        comm1 = int(input('Введите номер операции: '))
        if comm1 == 1:
            date_1 = input('Введите дату в формате: "2023-10-01" - ')  # Дата события
            daily = input('Если задача на весь день, напишите 1. Если нет, напишите 0')
            if daily == '1':
                date_todo = datetime.strptime(date_1, "%Y-%m-%d")
                print(date_todo)
                ask_todo = input('Введите дату в формате: "Встреча с командой" - ')  # Текст события
                add_todo(date_todo, ask_todo, daily)
            elif daily == '0':
                date_todo = datetime.strptime(date_1, "%Y-%m-%d").date()
                time_1 = input('Введите дату в формате: "14:15" - ')  # Время события
                time_todo = datetime.strptime(time_1, "%H:%M").time()
                my_time = datetime.combine(date_todo, time_todo)
                ask_todo = input('Введите дату в формате: "Встреча с командой" - ')  # Текст события
                add_todo(my_time, ask_todo, daily)
        elif comm1 == 2:
            data_show(list_data)
        elif comm1 == 3:
            date1 = input('Введите дату в формате: "2023-10-01 - ')
            date_todo = datetime.strptime(date1, "%Y-%m-%d")
            print(date_todo)
            data_show(read_todo_day(date_todo))
        elif comm1 == 4:
            date2 = input('Введите дату записи в формате: "2023-10-01 - ')
            time2 = input('Введите время записи в формате: "14:30" - ')
            date_time = datetime.strptime(f'{date2} {time2}', "%Y-%m-%d %H:%M:%S")
            data_show(read_todo_daytime_or_diapazon(date_time))
            # print(*read_todo_day_time(time2, read_todo_day(date2)), sep='')
        elif comm1 == 5:
            start1 = input('Введите дату начала диапазона в формате: "2023-10-01 - ')
            finish1 = input('Введите дату конца диапазона в формате: "2023-10-01 - ')
            start_date = datetime.strptime(start1, "%Y-%m-%d")
            end_date = datetime.strptime(finish1, "%Y-%m-%d")
            data_show(read_todo_daytime_or_diapazon(start_date, end_date))
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
    print(list_data)
    with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
        for string in list_data:
            f.write(f'{string[0]} {string[1]} {string[2]}' + '\n')

if __name__ == "__main__":
    main()