"""
== GEEKBRAINS.RU ==
Факультет - Geek University Искусственного интеллекта
1-я четверть / Основы языка Python
18/05/2019

== Игра Лото ==
Правила игры в лото.
Игра ведется с помощью специальных карточек, на которых отмечены числа,
и фишек (бочонков) с цифрами.
Количество бочонков — 90 штук с цифрами от 1 до 90. (В жизни они обычно достаются из мешка,
чтобы можно было вытянуть случайно)
Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:
--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------
В игре 2 игрока: пользователь и компьютер (*так же может быть 2 пользователя или 2 компьютера).
Каждому в начале выдается случайная карточка.
Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.
Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.

Побеждает тот, кто первый закроет все числа на своей карточке.
Пример одного хода:
Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87
      16 49    55 77    88
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)
Подсказка: каждый следующий случайный бочонок из мешка удобно получать
с помощью функции-генератора.
Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html
"""

import random
import sys

__author__ = 'Alexander Nikolaev'


def fill_bag(kegs_):
    return random.sample(range(1, kegs_ + 1), kegs_)


def get_one_keg(bag_):
    _keg = bag_.pop(random.randint(0, len(bag_) - 1))
    print(f'-' * 31)
    print(f'Новый бочонок: {_keg} (осталось {len(bag_)})')
    return _keg


def set_card(bag_, rows_, fill_cols_):
    card = random.sample(bag_, rows_ * fill_cols_)
    for item in card:
        bag_.remove(item)
    return [sorted(card[:5]), sorted(card[5:10]), sorted(card[10:])]


def get_card(__card, name_, seed):
    random.seed(seed)
    card_view = '{:-^31}\n'.format(name_)
    for row in __card:
        r = row[:]
        for i in range(4, 8):
            r.insert(random.randint(0, i), '')
        card_view += '{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}'.format(*r) + '\n'
    card_view += '-' * 31
    print(card_view)


def check_keg(card_, new_keg_):
    index = None
    for i in range(len(card_)):
        try:
            j = card_[i].index(new_keg_)
            index = [i, j]
            break
        except ValueError:
            index = False
    return index


def update_card(index_, card_):
    card_[index_[0]][index_[1]] = '><'


def failure():
    print('*' * 7 + ' ИГРА ЗАКОНЧЕНА! ' + '*' * 7)
    print('-' * 3 + ' ВЫ ОШИБЛИСЬ И ПРОИГРАЛИ ' + '-' * 3)
    sys.exit('НЕВНИМАТЕЛЬНОСТЬ')


kegs = 90
rows = 3
fill_cols = 5
n1 = 'Ваша карточка'
n2 = 'Карточка компьютера'
bag = fill_bag(kegs)
card1_cfg = random.randint(1, 50)
card2_cfg = random.randint(50, 100)
card1 = set_card(bag, rows, fill_cols)
card2 = set_card(bag, rows, fill_cols)
print('*' * 8 + ' ИГРА НАЧАЛАСЬ ' + '*' * 8)
print('* Завешить игру - press any key')
bag = fill_bag(kegs)
score1 = 0
score2 = 0
for new_keg in bag:
    if score1 == 15:
        print('*' * 5 + ' УРА!!! ВЫ ПОБЕДИЛИ! ' + '*'*5)
    elif score2 == 15:
        print('*' * 5 + ' КОМПЬЮТЕР ПОБЕДИЛ! ' + '*' * 5)
    else:
        kegs -= 1
        print(f'-' * 31)
        print(f'Новый бочонок: {new_keg} (осталось {kegs})')
        index1 = check_keg(card1, new_keg)
        index2 = check_keg(card2, new_keg)
        if index2:
            update_card(index2, card2)
            score2 += 1
        get_card(card1, n1, card1_cfg)
        get_card(card2, n2, card2_cfg)
        answer = input('Зачеркнуть цифру? (y/n) ').lower()
        if answer == 'y':
            if index1:
                update_card(index1, card1)
                score1 += 1
                continue
            else:
                failure()
        elif answer == 'n':
            if index1:
                failure()
            else:
                continue
        else:
            sys.exit('ИГРА TERMINATED')
        if kegs == 0:
            print('* В мешке больше нет боченков ')
            print('*' * 7 + ' ИГРА ЗАКОНЧЕНА! ' + '*' * 7)
            sys.exit('МЕШОК ПУСТ')
