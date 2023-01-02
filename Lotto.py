from random import sample  # выбор случайного набора
from collections import defaultdict  # объявление словаря со значениями нужного типа
from faker import Faker  # объявление типа для фиксации случайных имен

class Cart:
    """
    класс для карты
    """
    def __init__(self):
        self.cart = self.create_cart()

    def create_cart(self):
        """
        Задание содержимого карточки 15 уникальных номеров от 1 до 100
        :return: задание свойства cart, как лист из 3 строк
        """
        cart = sorted(sample(list(range(1, 100)), k=15))
        app = defaultdict(list)
        for item in cart:
            app[item // 10].append(item)
        # создает словарь со значениями из трехэлементных листов из заданных цифр, а остальное добавляется символами "#"
        for i in range(10):
            if len(app[i]) > 3:
                k = len(app[i]) - 3
                app[i] = app[i][:3]
                j = 1
                bag = set(app[(i + j) % 10]) - set('#')
                while len(bag) >= 3:
                    j += 1
                    bag = set(app[(i + j) % 10]) - set('#')
                new_set = list(set(range(((i + j) * 10) % 100, ((i + j + 1) * 10) % 101)) - bag)
                app[(i + j) % 10] = list(set(app[(i + j) % 10]) - set('#')) + sample(new_set, k=k)
                k = 3 - len(app[(i + j) % 10])
                app[(i + j) % 10] += ['#'] * k
            elif len(app[i]) < 3:
                k = 3 - len(app[i])
                app[i] += ['#'] * k
        result = []
        # превращает из словаря в список по 10 элементов
        for i in range(3):
            result.append([app[key][i] for key in range(10)])
        return result

    def get_cart_numbers(self):
        """
        Возвращает множество номеров карты
        :return: множество номеров карты
        """
        numbers = set()
        for item in self.cart:
            numbers |= set(item)
        numbers = numbers - {'#', '-'}
        return sorted(numbers)

    @property
    def is_empty(self):
        """
        Проверка на отсутствие цифр в карточке
        :return: bool
        """
        return len(self.get_cart_numbers()) == 0

    def is_num_to_cart(self, num):
        """
        Проверка присутствия номера в карточке
        :param num: искомый номер
        :return: bool
        """
        return any([item.count(num) for item in self.cart])

    def cross_out(self, num):
        """
        Замена числа в карточке на символ "-"
        :param num: номер для поиска
        :return: все изменения производятся в картоке
        """
        for item in self.cart:
            if num in item:
                index = item.index(num)
                item[index] = '-'
                return True

        return False

    def out_print(self):
        """
        Подготовка карточки для вывода на экран.
        :return: стока для вывода
        """
        s = ' ' + '_' * 30 + '\n'
        for item in self.cart:
            s += '|'
            for char in item:
                s += f'{str(char):^3}'
            s += '|\n'
        s += ' ' + '-' * 30 + '\n'
        return s


class PlayerComp:
    """
    Класс для бота
    """
    def __init__(self):
        """
        Инициализируются два свойства карта игрока и его имя - генерируется автоматически
        """
        self.cart = Cart()
        self.name = Faker('ru-RU').name()
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        """
        Ход игрока
        :param num: номер бочонка
        :return: bool
        """
        print(self.cart.out_print())
        if self.cart.is_num_to_cart(num):
            self.cart.cross_out(num)
            print('Номер есть')
        else:
            print('Номера нет в карточке')
        return True


class PlayerHuman:
    """
    Ход игрока с переопределением методов.
    """
    def __init__(self):
        self.cart = Cart()
        self.name = input('Введите имя игрока: ')
        print(f'Имя игрока: {self.name}')

    def step(self, num):
        print(self.cart.out_print())
        ans = input('Зачеркнуть цифру (Д/Н)? ')
        while ans not in 'ДдНн':
            ans = input('Некорректный ввод. Зачеркнуть цифру (Д/Н)? ')
        if ans in 'Дд':
            if self.cart.is_num_to_cart(num):
                self.cart.cross_out(num)
                return True
            else:
                return False
        else:
            if self.cart.is_num_to_cart(num):
                return False
            else:
                return True


class Game:
    """
    Класс игры, свойство bag - мешок с бочонками
    """
    def __init__(self):
        """
        Инициация игроков
        """
        self.bag = list(range(1, 100))
        self.player1 = None
        self.player2 = None

    def menu(self):
        """
        Вывод меню и получение номера выбранного пункта.
        :return: номер пункта
        """
        mtext = """
        
        1. Один игрок с компьютером
        2. 2 игрока
        3. 2 Компьютера
        4. Выход
        
        """
        print(mtext)
        n = input('Введите номер пункта: ')
        while n not in '1234':
            n = input('Некорректный ввод. Введите номер пункта: ')
        return int(n)

    def init_players(self, n):
        if n == 1:
            self.player1 = PlayerHuman()
            self.player2 = PlayerComp()
        elif n == 2:
            self.player1 = PlayerHuman()
            self.player2 = PlayerHuman()
        elif n == 3:
            self.player1 = PlayerComp()
            self.player2 = PlayerComp()


    def step(self):
        number = sample(self.bag, k=1)[0]
        print(f'Выпал бочонок: {number}')
        self.bag.remove(number)
        return number

    def start(self):
        """
        Процесс игры
        """
        n = self.menu()
        if n in [1, 2, 3]:
            self.init_players(n)
        else:
            print('Выбран выход')
            return False

        number = self.step()

        while not (self.player1.cart.is_empty or self.player2.cart.is_empty):
            step1 = self.player1.step(number)
            step2 = self.player2.step(number)
            if not step1 or not step2:
                break
            number = self.step()

        if self.player1.cart.is_empty or not step1:
            winner = self.player1
            loser = self.player2
        else:
            loser = self.player1
            winner = self.player2

        print()
        print("_"*40)
        print(f"Победитель: {winner.name}")
        print("_"*40)
        print(f'{loser.name} сегодня не выиграл')
        return True


if __name__ == '__main__':
    # запуск игры
    game = Game()
    game.start()
