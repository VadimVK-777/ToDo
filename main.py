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
                date_time = datetime.strptime(f'{record[0]} {record[1]}', "%Y-%m-%d %H:%M")
                list_str.append(date_time)
                list_str.append(record[2])
                list_str.append(record[3])
                list_data.append(list_str)
            list_data.sort(key=lambda x: (x[0].date(), x[1]))
            # print(list_data)
            return list_data

    else:
        with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
            print("Приложение запущено.")
            return list_data

def start_help() -> None:
    print('\nВыбери необходимое действие:\n1 - Добавить заметку\n'
          '2 - Посмотреть все заметки\n'
          '3 - Посмотреть все заметки, коротко на дату\n'
          '4 - Посмотреть заметку на дату\n'
          '5 - Посмотреть заметку на дату и время\n'
          '6 - Посмотреть заметки в диапазоне дат\n'
          '7 - Удалить запись\n'
          '8 - Короткий вывод')

def add_todo(date_time, note, daily) -> list: #TODO проверка правильности ввода данных юзером
    new_string = []
    new_string.extend([date_time, daily, note])
    list_data.append(new_string)
    list_data.sort()
    return list_data

def data_show(list_data: list) -> None:
    for index,line in enumerate(list_data, 1):
        if bool(int(line[1])):
            print(f'{index}. [{line[0].date()} --:--] - {line[2]}')
        else:
            print(f'{index}. [{line[0].strftime("%Y-%m-%d %H:%M")}] - {line[2]}')

def read_todo_day(date1: datetime) -> list:
    list_day = []
    for i in list_data:
        if i[0].date() == date1.date():
            list_day.append(i)
    return list_day

def show_short(list_day: list) -> None:
    list_task_daily = [x for x in list_day if x[1] == '1']
    # list_task_daily1 = list(filter(lambda x: x[1] == '1', list_day))
    list_task_time = [x for x in list_day if x[1] == '0']
    # list_task_time = list(filter(lambda x: x[0] == '1', list_day))
    print(f'[{list_task_daily[0][0].date()}]\n============')
    for i in list_task_daily:
        print(f'* {i[2]}')
    print('------------')
    for i in list_task_time:
        print(f'{list_task_time[0][0].time()} - {i[2]}')

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
        # TODO доделать ввод времени
        if comm1 == 1:
            # Получаем текущую дату
            default_date = datetime.now()
            # Запрашиваем ввод пользователя
            user_input = input(f"Введите дату в формате '{default_date.date()}'. Если запись на сегодня, нажмите Enter: ")
            # Если пользователь не ввел ничего, используем текущую дату
            if not user_input:
                user_date = default_date
            else:
                # Пробуем преобразовать введенную дату в объект datetime
                try:
                    user_date = datetime.strptime(user_input, "%Y-%m-%d").date()
                except ValueError:
                    print("Некорректный формат даты. Используйте 'YYYY-MM-DD'.")
                    user_date = default_date  # Используем значение по умолчанию в случае ошибки
            # date_1 = input('Введите дату в формате: "2023-10-01" - ')  # Дата события
            time_todo = input('Если задача на весь день, нажмите Enter. Если нет, напишите время в форматe "12:00": ')
            if not time_todo:
                ask_todo = input('Введите дату в формате: "Встреча с командой" - ')  # Текст события
                add_todo(user_date, ask_todo, 1)
            else:
                time_todo = datetime.strptime(time_todo, "%H:%M").time()
                my_time = datetime.combine(user_date, time_todo)
                ask_todo = input('Введите дату в формате: "Встреча с командой" - ')  # Текст события
                add_todo(my_time, ask_todo, 0)
        elif comm1 == 2:
            data_show(list_data)
        elif comm1 == 3:
            date1 = input('Введите дату в формате: "2023-10-01 - ')
            date_todo = datetime.strptime(date1, "%Y-%m-%d")
            print(date_todo)
            show_short(read_todo_day(date_todo))
        elif comm1 == 4:
            date1 = input('Введите дату в формате: "2023-10-01 - ')
            date_todo = datetime.strptime(date1, "%Y-%m-%d")
            print(date_todo)
            data_show(read_todo_day(date_todo))
        elif comm1 == 5:
            date2 = input('Введите дату записи в формате: "2023-10-01 - ')
            time2 = input('Введите время записи в формате: "14:30" - ')
            date_time = datetime.strptime(f'{date2} {time2}', "%Y-%m-%d %H:%M")
            data_show(read_todo_daytime_or_diapazon(date_time))
        elif comm1 == 6:
            start1 = input('Введите дату начала диапазона в формате: "2023-10-01 - ')
            finish1 = input('Введите дату конца диапазона в формате: "2023-10-01 - ')
            start_date = datetime.strptime(start1, "%Y-%m-%d")
            end_date = datetime.strptime(finish1, "%Y-%m-%d")
            data_show(read_todo_daytime_or_diapazon(start_date, end_date))
        elif comm1 == 7:
            date2 = input('Введите дату записи, которую нужно удалить в формате: "2023-10-01 - ')
            time2 = input('Введите время записи, которую нужно удалить в формате: "14:30" - ')
            date_time = datetime.strptime(f'{date2} {time2}', "%Y-%m-%d %H:%M")
            data_show(read_todo_day_time(date_time))
            del1 = input('Если хотите удалить эти данные, напишите y\n'
                         'В противном случае, напишите n')
            if del1 == 'y':
                del_todo(read_todo_day_time(date_time))
        elif comm1 == 8:
            pass
        esc1 = input('\nДля продолжения работы программы нажмите Enter.\nДля завершения напишите 0')
    print(list_data)
    with open(TODO_DB_FILE, 'w', encoding='utf-8') as f:
        for string in list_data:
            f.write(f'{string[0].strftime("%Y-%m-%d %H:%M")} {string[1]} {string[2]}' + '\n')

if __name__ == "__main__":
    main()