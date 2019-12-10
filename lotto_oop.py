import random
import numpy as np
import sys
import copy


def separator(symbol, count=55):
    return symbol * count


class Player:
    def __init__(self, name, category, score):
        self.name = name
        self.category = category
        self.score = score

    @staticmethod
    def failure():
        print(separator('*', 35))
        print('ИГРА ЗАКОНЧЕНА')
        raise SystemExit('НЕВНИМАТЕЛЬНОСТЬ')

    def __str__(self):
        return f'Игрок {self.name} : набрано {self.score} очков'

    def __eq__(self, other):
        return self.name == other.name


class Lototron:
    def __init__(self, kegs_count=90):
        self.kegs_count = kegs_count
        self.kegs = [_i for _i in range(1, kegs_count + 1)]
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
            return 0

    def __str__(self):
        s = 'Инициализация лототрона:'
        s = f'{s}\n'
        count = len(self.kegs) // 10
        for _i in range(count):
            for _j in range(_i*10, (_i+1)*10):
                s = f'{s} {str(self.kegs[_j])}'
            s = f'{s}\n'
        return s

    def __eq__(self, other):
        return len(self.kegs) == len(other.kegs)

    def __ne__(self, other):
        return len(self.kegs) != len(other.kegs)

    def __getitem__(self, item):
        return self.kegs[item]

    def __len__(self):
        return len(self.kegs)


class Card:
    def __init__(self, name, kegs_count=90, rows=3, cols=5):
        self.position = []
        self.name = name
        self.card_cfg = random.randint(1, 10000)
        _card = [_i for _i in range(1, kegs_count + 1)]
        random.shuffle(_card)
        self.card = np.sort(np.reshape(np.array(random.sample(_card, rows*cols)), (rows, cols))).flatten()

    def __str__(self, rows=3, cols=5):
        random.seed(self.card_cfg)
        card = np.reshape(self.card, (rows, cols)).tolist()
        card_appearance = '{:-^31}\n'.format(self.name)
        for row in card:
            r = row[:]
            for _j in range(len(r)):
                if r[_j] == 0:
                    r[_j] = '><'
            for _i in range(4, 8):
                r.insert(random.randint(0, _i), '')
            card_appearance += '{:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2} {:>2}'.format(*r) + '\n'
        card_appearance += '-' * 31
        return card_appearance

    def show(self):
        print(self)

    def update(self, item):
        self.card[item] = 0

    def check(self, keg):
        self.position = np.where(self.card == keg)[0]
        self.position = list(self.position)
        return True if keg in self.card else False

    def __eq__(self, other, rows=3, cols=5):
        return (int(rows * cols) - np.count_nonzero(self.card)) == (int(rows * cols) - np.count_nonzero(other.card))

    def __ne__(self, other, rows=3, cols=5):
        return (int(rows * cols) - np.count_nonzero(self.card)) != (int(rows * cols) - np.count_nonzero(other.card))


if __name__ == '__main__':
    sep_count = 35
    game_status = False
    computers = ['Cray CS-Storm', 'Vulcan', 'Juqueen', 'Stampede', 'Piz Daint', 'Mira', 'K Computer', 'Sequoia', 'Titan',
                 'Tianhe-2']
    cards = []
    print('------------ Игра лото ------------')
    print(separator('-', sep_count))
    print('В игре могут принимать участие:')
    print('>> 1. Игроки / Компьютеры')
    print('>> 2. Игроки / Игроки')
    print('>> 3. Компьютеры / Компьютеры')
    print('>> 4. Press any key to EXIT')
    game_type = int(input('Выберите тип игры (1, 2 или 3): '))
    if game_type in (1, 2):
        players = list(input('Введите имена игроков через запятую (max=10): ').split(',')[:10])
        for i, n in enumerate(players):
            n = n.strip()
            players[i] = Player(n, True, 0)
            cards.append(Card(n))
        if len(players) > 1:
            for _ii in players:
                for _jj in players[1:]:
                    if _ii == _j:
                        print('Введены одинаковые имена игроков...')
                        sys.exit('ИМЕНА ИГРОКОВ ДОЛЖНЫ БЫТЬ РАЗНЫМИ! ИГРА TERMINATED...')
        if game_type == 1:
            n = int(input('Введите количество играющих компьютеров (max=10): '))
            computers = random.sample(computers, n if n <= 10 else 10)
            for i, n in enumerate(computers):
                computers[i] = Player(n, False, 0)
                cards.append(Card(n))
        else:
            computers.clear()
        players = players + computers
        del computers
    elif game_type == 3:
        n = int(input('Введите количество компьютеров (max=10): '))
        computers = random.sample(computers, n if n <= 10 else 10)
        for i, n in enumerate(computers):
            computers[i] = Player(n, False, 0)
            cards.append(Card(n))
        players = copy.deepcopy(computers)
        del computers
    else:
        print('Введена цифра 4 или что-то другое...')
        sys.exit('ИГРА TERMINATED')
    print(separator('-', sep_count), '\n')

    print('*' * 8 + ' ИГРА НАЧАЛАСЬ ' + '*' * 8)
    bag = Lototron()
    print(bag)
    for i, player in enumerate(players):
        print(f'Карточка игрока {player.name}')
        cards[i].show()
    while True:
        new_keg = bag.get_keg()
        print()
        if not game_status:
            print(f'>>>>>>>>>> Раунд {90 - bag.kegs_count} <<<<<<<<<<')
            print(f'Новый бочонок: {new_keg} (осталось {bag.kegs_count})')
        for i, player in enumerate(players):
            if player.score == 15:
                game_status = True
                print(player)
                print(f'Игрок {player.name} ВЫИГРАЛ!!!')
                print(separator('*', sep_count))
                sys.exit('ИГРА ЗАКОНЧЕНА')
            if len(bag) == 0:
                game_status = True
                for p in players:
                    print(p)
                print(separator('*', sep_count))
                sys.exit('ИГРА ЗАКОНЧЕНА')
            if player.category:
                answer = input(f'{player.name}, эачеркнуть цифру? (y/n) ').lower()
                if answer == 'y':
                    if cards[i].check(new_keg):
                        player.score += 1
                        if player.score == 15:
                            game_status = True
                        cards[i].update(cards[i].position)
                    else:
                        print(f'Игрок {player.name} ПРОИГРАЛ!!!')
                        print(player)
                        player.failure()
                elif answer == 'n':
                    if cards[i].check(new_keg):
                        print(f'Игрок {player.name} ПРОИГРАЛ!!!')
                        print(player)
                        player.failure()
                else:
                    print('Неверный ответ на вопрос! Должно быть y/n')
                    sys.exit('ИГРА TERMINATED')
            else:
                if cards[i].check(new_keg):
                    player.score += 1
                    if player.score == 15:
                        game_status = True
                    cards[i].update(cards[i].position)
        for i, player in enumerate(players):
            cards[i].show()
