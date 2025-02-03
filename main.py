import sqlite3


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


def help1():
    print('Это приложение ToDo для заметок\nВыбери необходимое действие:')
    print('1 - Добавить заметку\n2 - Посмотреть все заметки\n3 - Посмотреть заметку на дату\n4 - Посмотреть заметки в диапазоне дат')
    return None

def add_todo():
    with sqlite3.connect('todolist.db') as conn:
        # Создаем курсор
        cursor = conn.cursor()
        # Пример данных для добавления
        date_todo = input('Введите дату в формате: "2023-10-01" - ') # Дата события
        time_todo = input('Введите дату в формате: "14:30:00" - ') # Время события
        task_todo = input('Введите дату в формате: "Встреча с командой" - ') # Текст события

        # Выполняем запрос для вставки новой записи
        cursor.execute('''
            INSERT INTO todolist (date_todo, time_todo, task_todo)
            VALUES (?, ?, ?)
            ''', (date_todo, time_todo, task_todo))

        # Сохраняем изменения
        conn.commit()

    print("Запись успешно добавлена в таблицу 'todolist'!")


def main():
    help1()

    comm1 = int(input('Введите номер операции: '))

    if comm1 == 1:
        add_todo()
    elif comm1 == 2:
        read_todo()
    elif comm1 == 3:
        print('3')
    elif comm1 == 4:
        print('4')


if __name__ == "__main__":
    main()






