# Домашка 11.4 Конструктор __init__ и работа с несколькими классами

class Student:
    def __init__(self, fio, group, ocenki):
        self.fio = fio
        self.group = group
        self.ocenki = ocenki
        self.avg_score = self.score()


    def score(self):
        return sum(self.ocenki) / len(self.ocenki)

    def __gt__(self, other):
        return self.score > other.score

    def print_info(self):
        print(f'Fio: {self.fio}\n'
              f'Group: {self.group}\n'
              f'Ocenki: {self.ocenki}\n'
              f'Score: {self.score()}')


def main():
    student1 = Student('petrov', 123, [3, 1, 5, 4, 4])
    student1.print_info()
    student1.ocenki = [3, 15, 5, 4, 6]
    student1.print_info()


    #
    # student2 = Student('sidirov', 124, [3, 3, 1, 4, 4])
    # student3 = Student('serggev', 125, [3, 3, 5, 1, 4])
    # student4 = Student('ivanov', 129, [3, 2, 5, 4, 4])
    # student5 = Student('zaharov', 183, [3, 3, 5, 1, 1])
    # my_list = [student1, student2, student3, student4, student5]
    #
    # my_list_sort = sorted(my_list, key=lambda student: student.score, reverse=True)
    # print(my_list_sort)
    # for student in my_list_sort:
    #     print()
    #
    #
    # student1.print_info()
    # student2.print_info()
    # student3.print_info()
    # student4.print_info()
    # student5.print_info()



if __name__ == '__main__':
    main()





from random import randint as R

# esc1 = 1
#
# class Voin:
#     def __init__(self, name, health):
#         self.name = name
#         self.healf = health
#
#     def print_info(self):
#         print(f'Name: {self.name}\n'
#               f'Healf: {self.healf}\n')
#
#     def damage(self):
#         global esc1
#         self.healf -= 20
#         if self.healf <= 0:
#             print(f'Атаковал Воин2, Воин1 убит')
#             esc1 = 0
#         else:
#             print(f'Атаковал Воин2, у Война1 осталось {self.healf} здоровья')
#
# def main():
#
#     voin1 = Voin('MAG', 80)
#     voin2 = Voin('VOIN', 80)
#     voin1.print_info()
#     voin2.print_info()
#
# if __name__ == '__main__':
#     main()


#
# my_list = [voin1.damage, voin2.damage]
# count1 = 1
# while esc1 != 0:
#     print(f'Шаг номер {count1}\n')
#     count1 += 1
#     step = R(0, 1)
#     my_list[step]()

# from random import randint as R
#
#
# class Warrior:
#     def __init__(self, name, health):
#         self.name = name
#         self.health = health
#
#     def print_info(self):
#         print(f'Name: {self.name}\nHealth: {self.health}\n')
#
#     def damage(self):
#         self.health -= 20
#         if self.health <= 0:
#             print(f'{self.name} убит!')
#             return False  # Возвращаем False, если воин убит
#         else:
#             print(f'{self.name} получил урон, осталось {self.health} здоровья')
#             return True  # Возвращаем True, если воин жив
#
#
# def main():
#     voin1 = Warrior("MAG", 100)
#     voin2 = Warrior("ORK", 100)
#
#
#     voin1.print_info()
#     voin2.print_info()
#
#     warriors = [voin1, voin2]
#     count = 1
#
#     while all(w.health > 0 for w in warriors):  # Проверяем, что оба воина живы
#         print(f'Шаг номер {count}\n')
#         count += 1
#         attacker = warriors[R(0, 1)]  # Случайный выбор атакующего
#         defender = warriors[1] if attacker == warriors[0] else warriors[0]  # Определяем защитника
#
#         if not defender.damage():  # Если защитник убит
#             break
#
#
# if __name__ == "__main__":
#     main()




# class Employee:
#     def __init__(self, name, salary):
#         self.name = name
#         self.salary = salary
#
#     def print_info(self):
#         print(f'Name: {self.name}\n'
#               f'Salary: {self.salary}')
#
# emp_1 = Employee('Tom', 10000)
# emp_2  = Employee('Bob', 20000)
# emp_1.print_info()
# emp_2.print_info()






# from random import randint as R
#
# class Toyota:
#     color = "red"
#     price = 1000000
#     max_speed = 200
#     now_speed = 0
#
#     def car_info(self):
#         print(f'Color: {self.color}\n'
#               f'Price: {self.price}\n'
#               f'Max speed: {self.max_speed}\n'
#               f'Now speed: {self.now_speed}\n')
#
#     def write_speed(self, speed):
#         self.now_speed = speed
#
#
#
# car_1 = Toyota()
#
# car_1.car_info()
#
# car_1.write_speed(100)
#
# car_1.car_info()





# class Family:
#     surname = 'Common family'
#     money = 1000000
#     have_a_house = False
#
#     def info(self):
#         print(f'Family name: {self.surname}\n'
#               f'Money: {self.money}\n'
#               f'have_a_house: {self.have_a_house}\n')
#
#     def earn_money(self, amount):
#         self.money += amount
#         print(f'Earned {amount} money! Current value: {self.money}')
#
#     def buy_house(self, house_price, discount=0):
#         house_price -= house_price * discount / 100
#         if self.money >= house_price:
#             self.money -= house_price
#             self.have_a_house = True
#             print(f'House purchased! Current mone: {self.money}$\n')
#         else:
#             print(f'Not enough money! Current value: {self.money}$\n')
#
# my_family = Family()
#
# my_family.info()
#
# print('Try to buy a house')
# my_family.buy_house(10**6)
# if not my_family.have_a_house:
#     my_family.earn_money(800000)
#     print('Try to buy a house again')
#     my_family.buy_house(10 ** 6, 10)
#
# my_family.info()


# from random import randint as R
#
# class Monitor:
#     monitor_name = "Brand"
#     monitor_matrix = 'Type'
#     monitor_res = 'VGA'
#     monitor_freq = 60
#     count = []
#
#     def print_info(self):
#         print(f'Brand: {self.monitor_name}\n'
#               f'Matrix: {self.monitor_matrix}\n'
#               f'Resolution: {self.monitor_res}\n'
#               f'Freqrunce:{self.monitor_freq}')
#
#     def add_count(self, count):
#         self.count.append(count)
#
#
#
#
# class Headphones:
#     headphones_name = 'Brand'
#     headphones_sensitivity = 100
#     availability = False
#
# headphones_1 = Headphones()
# headphones_1.headphones_name = 'Sony'
# headphones_1.headphones_sensitivity = 108
# headphones_1.availability = False
#
# headphones_2 = Headphones()
# headphones_2.headphones_name = 'Sony'
# headphones_2.headphones_sensitivity = 108
# headphones_2.availability = True
#
# headphones_3 = Headphones()
# headphones_3.headphones_name = 'Sony'
# headphones_3.headphones_sensitivity = 108
# headphones_3.availability = True
#
# monitor_1 = Monitor()
# monitor_1.monitor_name = 'Samsung'
# monitor_1.monitor_matrix = 'VA'
# monitor_1.monitor_res = 'WQHD'
# monitor_1.monitor_freq = 60
#
# monitor_2 = Monitor()
# monitor_2.monitor_name = 'Samsung'
# monitor_2.monitor_matrix = 'VA'
# monitor_2.monitor_res = 'WQHD'
# monitor_2.monitor_freq = 144
#
# monitor_3 = Monitor()
# monitor_2.monitor_name = 'Samsung'
# monitor_2.monitor_matrix = 'VA'
# monitor_2.monitor_res = 'WQHD'
# monitor_2.monitor_freq = 70
#
# monitor_4 = Monitor()
# monitor_1.monitor_name = 'Samsung'
# monitor_1.monitor_matrix = 'VA'
# monitor_1.monitor_res = 'WQHD'
# monitor_1.monitor_freq = 60
#
# monitor_1.add_count('1')
# print(monitor_1.count)


# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __lt__(self, other):
#         return self.age < other.age
#
#     def __le__(self, other):
#         return self.age <= other.age
#
#     def __gt__(self, other):
#         return self.age > other.age
#
#     def __ge__(self, other):
#         return self.age >= other.age
#
#     def __eq__(self, other):
#         return self.age == other.age
#
#     def __ne__(self, other):
#         return self.age != other.age
#
#     def __repr__(self):
#         return f"Person(name={self.name}, age={self.age})"
#
# # Создаем список объектов
# people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]
#
# # Сортируем список по возрасту
# sorted_people = sorted(people)
# print(sorted_people)  # Вывод: [Person(name=Bob, age=25), Person(name=Alice, age=30), Person(name=Charlie, age=35)]

