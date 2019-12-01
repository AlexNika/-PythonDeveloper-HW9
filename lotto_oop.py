import random
import numpy as np
import sys


def separator(symbol, count=55):
    return symbol * count


class Player:
    def __init__(self, name, category, score):
        self.name = name
        self.category = category
        self.score = score

    def failure(self):
        print(f'Игрок {self.name} ПРОИГРАЛ!!!')
        print(separator('*', sep_count))
        print('ИГРА ЗАКОНЧЕНА')
        sys.exit('НЕВНИМАТЕЛЬНОСТЬ')


class Lototron:
    def __init__(self, kegs_count=90):
        self.kegs_count = kegs_count
        self.kegs = [i for i in range(1, kegs_count + 1)]
        random.shuffle(self.kegs)
        self.keg = 0

    def get_keg(self):
        if self.kegs:
            random.shuffle(self.kegs)
            self.keg = self.kegs.pop()
            self.kegs_count -= 1
            return self.keg
        else:
            print('Лототрон пуст!')

    def is_empty(self):
        return True if self.kegs else False


class Card:
    def __init__(self, name, kegs_count=90, rows=3, cols=5):
        self.position = []
        self.name = name
        self.card_cfg = random.randint(1, 10000)
        __ = [i for i in range(1, kegs_count + 1)]
        random.shuffle(__)
        self.card = np.sort(np.reshape(np.array(random.sample(__, rows*cols)), (rows, cols))).flatten()

    def appearance(self, rows=3, cols=5):
        random.seed(self.card_cfg)
        card = np.reshape(self.card, (rows, cols)).tolist()
        card_appearance = '{:-^31}\n'.format(self.name)
        for row in card:
            r = row[:]
            for j in range(len(r)):
                if r[j] == 0:
                    r[j] = '><'
            for i in range(4, 8):
                r.insert(random.randint(0, i), '')
            card_appearance += '{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}'.format(*r) + '\n'
        card_appearance += '-' * 31
        return card_appearance

    def show(self):
        print(self.appearance())

    def update(self, index):
        self.card[index] = 0

    def check(self, keg):
        self.position = np.where(self.card == keg)[0]
        return True if keg in self.card else False


sep_count = 35
game_status = False
print('------------ Игра лото ------------')
print(separator('-', sep_count))
print('В игре могут принимать участие:')
print('>> 1. Игрок / Компьютер')
print('>> 2. Игрок / Игрок')
print('>> 3. Компьютер / Компьютер')
print('>> 4. Press any key to EXIT')
game_type = input('Выберите тип игры (1, 2 или 3): ')
print(separator('-', sep_count), '\n')
if game_type == '1':
    player1 = input('Введите имя игрока: ')
    card1 = Card(player1)
    player1 = Player(player1, 'Human', 0)
    player2 = 'Tiny Cray CS-Storm'
    card2 = Card(player2)
    player2 = Player(player2, 'AI', 0)
elif game_type == '2':
    player1 = input('Введите имя игрока №1: ')
    card1 = Card(player1)
    player1 = Player(player1, 'Human', 0)
    player2 = input('Введите имя игрока №2: ')
    card2 = Card(player2)
    player2 = Player(player2, 'Human', 0)
elif game_type == '3':
    player1 = 'Tiny Cray CS-Storm'
    card1 = Card(player1)
    player1 = Player(player1, 'AI', 0)
    player2 = 'Tiny Tianhe-2'
    card2 = Card(player2)
    player2 = Player(player2, 'AI', 0)
else:
    sys.exit('ИГРА TERMINATED')
print('*' * 8 + ' ИГРА НАЧАЛАСЬ ' + '*' * 8)
print(f'Карточка игрока {player1.name}')
card1.show()
print(f'Карточка игрока {player2.name}')
card2.show()
bag = Lototron()
while True:
    new_keg = bag.get_keg()
    print()
    if not game_status:
        print(f'>>>>>>>>>> Роунд {90 - bag.kegs_count} <<<<<<<<<<')
    if not game_status:
        print(f'Новый бочонок: {new_keg} (осталось {bag.kegs_count})')
    if player1.score == 15:
        game_status = True
        print(f'Игрок {player1.name} ВЫИГРАЛ!!!')
        print(separator('*', sep_count))
        sys.exit('ИГРА ЗАКОНЧЕНА')
    elif player2.score == 15:
        game_status = True
        print(f'Игрок {player2.name} ВЫИГРАЛ!!!')
        print(separator('*', sep_count))
        sys.exit('ИГРА ЗАКОНЧЕНА')
    else:
        if not bag.is_empty():
            if player1.score == player2.score:
                game_status = True
                print('Ничья!!! Игроки закрыли одинаковое количество чисел на карточках')
                print(separator('*', sep_count+29))
                sys.exit('ИГРА ЗАКОНЧЕНА')
            elif player1.score > player2.score:
                game_status = True
                print(f'Игрок {player1.name} ВЫИГРАЛ!!!')
                print(separator('*', sep_count))
                sys.exit('ИГРА ЗАКОНЧЕНА')
            else:
                game_status = True
                print(f'Игрок {player2.name} ВЫИГРАЛ!!!')
                print(separator('*', sep_count))
                sys.exit('ИГРА ЗАКОНЧЕНА')

        if player1.category == 'Human':
            answer = input(f'{player1.name}, эачеркнуть цифру? (y/n) ').lower()
            if answer == 'y':
                if card1.check(new_keg):
                    player1.score += 1
                    card1.update(card1.position)
                else:
                    player1.failure()
            elif answer == 'n':
                if card1.check(new_keg):
                    player1.failure()
            else:
                print('Неверный ответ на вопрос! Должно быть y/n')
                sys.exit('ИГРА TERMINATED')
        else:
            if card1.check(new_keg):
                player1.score += 1
                if player1.score == 15:
                    game_status = True
                card1.update(card1.position)
        if player2.category == 'Human':
            answer = input(f'{player2.name}, эачеркнуть цифру? (y/n) ').lower()
            if answer == 'y':
                if card2.check(new_keg):
                    player2.score += 1
                    card2.update(card2.position)
                else:
                    player2.failure()
            elif answer == 'n':
                if card2.check(new_keg):
                    player2.failure()
            else:
                print('Неверный ответ на вопрос! Должно быть y/n')
                sys.exit('ИГРА TERMINATED')

        else:
            if card2.check(new_keg):
                player2.score += 1
                if player2.score == 15:
                    game_status = True
                card2.update(card2.position)
    card1.show()
    card2.show()
