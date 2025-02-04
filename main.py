import sqlite3

print('Это приложение ToDo для заметок')

# Используем менеджер контекста для работы с базой данных
with sqlite3.connect('todolist.db') as conn:
    # Создаем курсор
    cursor = conn.cursor()
    # Создаем таблицу
    cursor.execute('''    
    CREATE TABLE IF NOT EXISTS todolist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_todo DATE NOT NULL,
        time_todo TIME NOT NULL,
        task_todo TEXT NOT NULL
    )
    ''')
    # Сохраняем изменения
    conn.commit()

def add_todo():
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()
        # Пример данных для добавления
        date_todo = input('Введите дату в формате: "2023-10-01" - ') # Дата события
        time_todo = input('Введите время в формате: "14:30" - ') # Время события
        task_todo = input('Введите дату в формате: "Встреча с командой" - ') # Текст события

        # Выполняем запрос для вставки новой записи
        cursor.execute('''
            INSERT INTO todolist (date_todo, time_todo, task_todo)
            VALUES (?, ?, ?)
            ''', (date_todo, time_todo, task_todo))

        # Сохраняем изменения
        conn.commit()

    print("Запись успешно добавлена в таблицу 'todolist'!")

def read_todo():
    # Используем менеджер контекста для работы с базой данных
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()

        # Выполняем запрос для выборки всех данных из таблицы events
        cursor.execute('SELECT * FROM todolist')

        # Получаем все строки результата
        rows = cursor.fetchall()

        # Проверяем, есть ли данные и выводим их
        if rows:
            for row in rows:
                print(*row, sep=' -- ')  # Выводим каждую строку
        else:
            print("Таблица пуста.")

def read_todo_day(date1):
    # Используем менеджер контекста для работы с базой данных
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()

        # Выполняем запрос для выборки всех данных из таблицы todolist
        sql = f'SELECT * FROM todolist WHERE date_todo = "{date1}"'

        cursor.execute(sql)

        # Получаем все строки результата
        rows = cursor.fetchall()

        # Проверяем, есть ли данные и выводим их
        if rows:
            for row in rows:
                print(*row, sep=' -- ')  # Выводим каждую строку
        else:
            print("Таблица пуста.")

def read_todo_day_time(date2, time2):
    # Используем менеджер контекста для работы с базой данных
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()

        # Выполняем запрос для выборки всех данных из таблицы todolist
        sql = f'SELECT * FROM todolist WHERE date_todo = "{date2}" AND time_todo = "{time2}"'

        cursor.execute(sql)

        # Получаем все строки результата
        rows = cursor.fetchall()

        # Проверяем, есть ли данные и выводим их
        if rows:
            for row in rows:
                print(*row, sep=' -- ')  # Выводим каждую строку
        else:
            print("Нет записей по вашим условиям")

def read_todo_diapazon(start_date, finish_date):
    # Используем менеджер контекста для работы с базой данных
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()

        # Выполняем запрос для выборки всех данных из таблицы todolist
        sql = f'SELECT * FROM todolist WHERE date_todo BETWEEN "{start_date}" AND "{finish_date}" ORDER BY date_todo ASC'

        cursor.execute(sql)

        # Получаем все строки результата
        rows = cursor.fetchall()

        # Проверяем, есть ли данные и выводим их
        if rows:
            for row in rows:
                print(*row, sep=' -- ')  # Выводим каждую строку
        else:
            print("Таблица пуста.")

def del_todo(date2, time2):
    # Используем менеджер контекста для работы с базой данных
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()

        # Выполняем запрос для выборки всех данных из таблицы todolist
        sql = f'DELETE FROM todolist WHERE date_todo = "{date2}" AND time_todo = "{time2}"'

        cursor.execute(sql)

        # Получаем все строки результата
        rows = cursor.fetchall()

        # Проверяем, есть ли данные и выводим их
        print(f"Удалено записей: {cursor.rowcount}")

def help1():
    print('\nВыбери необходимое действие:\n1 - Добавить заметку\n'
          '2 - Посмотреть все заметки\n3 - Посмотреть заметку на дату\n'
          '4 - Посмотреть заметку на дату и время\n'
          '5 - Посмотреть заметки в диапазоне дат\n'
          '6 - Удалить запись')

def main():
    esc1 = '1'
    while esc1 != '0':

        help1()

        comm1 = int(input('Введите номер операции: '))

        if comm1 == 1:
            add_todo()
        elif comm1 == 2:
            read_todo()
        elif comm1 == 3:
            date1 = input('Введите дату в формате: "2023-10-01 - ')
            read_todo_day(date1)
        elif comm1 == 4:
            date2 = input('Введите дату записи в формате: "2023-10-01 - ')
            time2 = input('Введите время записи в формате: "14:30" - ')
            read_todo_day_time(date2, time2)
        elif comm1 == 5:
            start_date = input('Введите дату начала диапазона в формате: "2023-10-01 - ')
            finish_date = input('Введите дату конца диапазона в формате: "2023-10-01 - ')
            read_todo_diapazon(start_date, finish_date)
        elif comm1 == 6:
            date2 = input('Введите дату записи, которую нужно удалить в формате: "2023-10-01 - ')
            time2 = input('Введите время записи, которую нужно удалить в формате: "14:30" - ')
            read_todo_day_time(date2, time2)
            del1 = input('Если хотите удалить эти данные, напишите y\n'
                         'В противном случае, напишите n')
            if del1 == 'y':
                del_todo(date2, time2)
        esc1 = input('\nДля продолжения работы программы нажмите Enter.\nДля завершения напишите 0')


if __name__ == "__main__":
    main()






