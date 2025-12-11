# from itertools import chain
from tkinter import *
from tkinter import ttk, messagebox
from random import randint
import glob
from time import sleep
from tkinter.messagebox import showinfo

# from PyQt6.uic.pyuic import preview
# from winsound import Beep
from PIL import Image, ImageTk

# Метод при нажатии клавиш


def pressKey(event):
    # print(f"Клавиша: {event.keycode}, сивол: {event.char.upper()}")
    # Подсказка
    # if (playGame):
    # 	return 0
    # if (event.keycode == 32):
    #     startNewRound()
    pass

# Очистка поля


def resetField():
    global data_play_model, playGame  # , emptyCells

    possible_moves[:] = []
    playGame = False

    for i in range(cells_count):
        for j in range(cells_count):
            data_play_model[i][j] = countPlayers
            cell_lebel_set_image(i, j)
            possible_moves.append([i, j])  # Создаем список координат пустых ячеек

    switch_all_buttons()
    startButton.focus_set()

def cutEmptyCells(x: int, y: int) -> None:
    """ Удаляет один ход из списка возможных ходов
    """
    for i in range(len(possible_moves)):
        if (possible_moves[i][0] == x and possible_moves[i][1] == y):
            del possible_moves[i]
            return


def drawTest() -> bool:
    """Тест на ничью"""
    for L in range(countPlayers):
        listTest = []  # Список для проверки

        for i in range(cells_count):
            listTest.append([])
            for j in range(cells_count):
                if (data_play_model[i][j] == countPlayers):
                    listTest[i].append(L)
                else:
                    listTest[i].append(data_play_model[i][j])
        for row in possible_moves:
            win = win_check(listTest, row[0], row[1], L)
            if (win):
                return False
    return True


# Тест на победу
def win_check(list2d, x, y, number):
    def start_range(idx, chain):
        if idx - chain < 0:
            return 0
        else:
            return idx + 1 - chain

    def stop_range(idx, chain, n):
        if idx + chain < n:
            return idx + chain
        else:
            return n

    win = 0
    n = len(list2d)

    x_start = start_range(x, chain)
    x_stop = stop_range(x, chain, n)
    y_start = start_range(y, chain)
    y_stop = stop_range(y, chain, n)
    print(x_start, x_stop, y_start, y_stop)

    for i in range(x_start, x_stop):
        if (list2d[i][y] == number):
            win += 1
            if (win == chain):
                return True
        else:
            win = 0
    win = 0

    for i in range(y_start, y_stop):
        if (list2d[x][i] == number):
            win += 1
            if (win == chain):
                return True
        else:
            win = 0
    win = 0

    # Проверка по направлению главной диагонали
    spin = x - y
    if spin != x_start - y_start:
        if x_start < y_start + spin:
            x_start = y_start + spin
        else:
            y_start = x_start - spin

    if spin != x_stop - y_stop:
        if x_stop > y_stop + spin:
            x_stop = y_stop + spin
        else:
            y_stop = x_stop - spin
    if (x_stop - x_start >= chain and y_stop - y_start >= chain):
        for i in range(x_start, x_stop):
            if list2d[i][i - spin] == number:
                win += 1
                if win == chain:
                    return True
            else:
                win = 0
    win = 0

    x_start = start_range(x, chain)
    x_stop = stop_range(x, chain, n)

    spin = x + y
    if spin - x_start > n - 1:
        x_start = spin - n + 1
    if spin - x_stop < -1:
        x_stop = spin

    print(f"{x_start=} {y_start=} = {x_start + y_start} ")
    print(f"{x_stop=} {y_stop=} = {x_stop + y_stop}")

    if x_stop - x_start >= chain:
        for i in range(x_start, x_stop):
            if list2d[i][spin - i] == number:
                win += 1
                if win == chain:
                    return True
            else:
                win = 0
        win = 0

    return False

# Ход бота

def smart_bot(matrix:list, moves_left, turn:int, replay=0):
    """ Логика работы умного компьютера
    """
    n = len(matrix)
    pass


def bot():
    global data_play_model
    if (diffCombobox.current() == 0):
        i = randint(0, len(possible_moves) - 1)
        move(possible_moves[i][0], possible_moves[i][1])
    elif (diffCombobox.current() == 1):
        for l in range(countPlayers):
            for i in range(len(possible_moves)):
                data_play_model[possible_moves[i][0]][possible_moves[i][1]] = (
                                                                              player_turn + l) % countPlayers
                if (win_check(data_play_model, possible_moves[i][0], possible_moves[i][1], (player_turn + l) % countPlayers)):
                    move(possible_moves[i][0], possible_moves[i][1])
                    return 0
                else:
                    data_play_model[possible_moves[i][0]
                                    ][possible_moves[i][1]] = countPlayers
        i = randint(0, len(possible_moves) - 1)
        move(possible_moves[i][0], possible_moves[i][1])
    elif (diffCombobox.current() == 2):
        smart_bot(data_play_model, possible_moves, player_turn, 3)

def move(x:int, y:int):
    """Ход игрока или бота и их последствия
    """
    global data_play_model, player_turn

    data_play_model[x][y] = player_turn
    cell_lebel_set_image(x, y)
    cutEmptyCells(x, y)

    win = win_check(data_play_model, x, y, player_turn)
    if (win):
        insertText(f"Победил {player_turn + 1} игрок")
        messagebox.showinfo(f"Победил {player_turn + 1} игрок!",
                            f"Для продолжения нажмите ОК")
        resetField()
    elif (drawTest()):
        insertText(f"Ничья! Дальнейшая победа невозможна")
        messagebox.showinfo("НИЧЬЯ!",
                            f"Для продолжения нажмите ОК")
        resetField()
    player_turn = (player_turn + 1) % countPlayers
    battle()


# Ход игрока
def go(x, y):
    print(x, y)

    if (playGame and data_play_model[x][y] == countPlayers):
        move(x, y)
    # battle()


# Игра запущена
def battle():
    if (playGame):
        insertText(f"Ходит {player_turn + 1} игрок")
    else:
        insertText("Для начала игры нажмите ПРОБЕЛ или кнопку СТАРТ")

    if (not player.get() and player_turn == 1 and playGame):
        bot()


def switch_all_buttons():
    """ Активация/декзактивация всех кнопок и переключателей в зависимости
    от фазы игры
    """
    if playGame:
        # Блокируем переключатели
        for i in range(countPlayers):
            skinCombobox[i]["state"] = DISABLED
        radio01["state"] = DISABLED
        radio02["state"] = DISABLED
        diffCombobox["state"] = DISABLED
        startButton["state"] = DISABLED
        cells_count_combobox["state"] = DISABLED
    else:
        # Активируем переключатели
        for i in range(countPlayers):
            skinCombobox[i]["state"] = "readonly"
        radio01["state"] = NORMAL
        radio02["state"] = NORMAL
        diffCombobox["state"] = "readonly"
        startButton["state"] = NORMAL
        cells_count_combobox["state"] = NORMAL


# Кнопка СТАРТ
def startNewRound():
    global playGame, player_starts_round, player_turn

    playGame = True
    player_turn = player_starts_round
    player_starts_round = (player_starts_round + 1) % countPlayers
    textDiary.delete("1.0", END)
    insertText("Новый раунд!")
    switch_all_buttons()
    battle()

def chain_change():
	global chain
	chain = int(chain_combobox.get())
	print(chain)

def get_chain_values():
	return [i for i in range(3, cells_count + 1)]

def cells_count_change():
	"""
	Изменение размера игрового поля
	"""
	global cells_count, sizeSkin
	cells_count = cells_count_combobox.current() + 3
	sizeSkin = int((sizeField) // cells_count)
	chain_values = get_chain_values()
	chain_combobox["values"] = chain_values
	if chain > max(chain_values):
		chain_combobox.current(len(chain_values) - 1)
		chain_change()

	destroy_widget(cells_lebel)
	update_data_play_model_and_labelImage()

	resetField()

def isCheckSkin():
    global activeSkin
    if (skinCombobox[1].get() == skinCombobox[0].get()):
        skinCombobox[1].current(
            (skinCombobox[0].current() + 1) % len(skinList))
    activeSkin = []
    for i in range(countPlayers):
        activeSkin.append(skinCombobox[i].current())
    activeSkin.append(-1)

def cell_lebel_set_image(x:int, y:int):
    """ Установка изображения по координатам клетки
    в зависимости от активного скина каждого игрока
    """
    global cells_lebel
    cells_lebel[x][y]["image"] = image_skin[activeSkin[data_play_model[x][y]]]

def get_image_skin_base_from_file():
    """ Загрузка изображений для значков(скинов) игрока из файла"""
    return list(Image.open(name) for name in glob.glob("skin/*.*"))

def image_resize(image, size):
    """ Изменение размера квадратной картинки
    """
    # print(f'def image_resize(image, size): {size=}')
    resized = image.resize((size, size), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized)

def get_image_skin():
    """ Возвращает список скинов с учетом их актуальных размеров
    """
    global _image_cache, sizeSkin

    # print(f"def get_image_skin(): current sizeSkin = {sizeSkin}")

    # Если для текущего размера уже есть результат — берём из кеша
    if sizeSkin in _image_cache:
        # print("Using cached images")
        return _image_cache[sizeSkin]

    # Иначе пересчитываем все изображения
    # print("Recalculating images for new size")
    image_skin = [
        image_resize(img, sizeSkin)
        for img in image_skin_base
    ]

    # Сохраняем в кеш
    _image_cache[sizeSkin] = image_skin
    return image_skin

def isCheckPlayer():
    """ Определяет кто будет играть за второго игрока
    человек или Бот
    """
    if (player.get()):
        diffCombobox["state"] = DISABLED
    else:
        diffCombobox["state"] = "readonly"

def insertText(s):
    """ Добавление строки в информационный блок
    """
    textDiary.insert(INSERT, s + "\n")
    textDiary.see(END)

def destroy_widget(widget_for_destroy):
    """
    Рекурсивно уничтожает все виджеты в структуре любой глубины вложенности.
    Args:
        widget_for_destroy: структура (список/вложенный список) с виджетами Tkinter
    """
    if not widget_for_destroy:
        return  # Если объект пуст/None — выходим

    # Проверяем, является ли текущий объект итерируемым (но не строкой)
    if hasattr(widget_for_destroy, '__iter__') and not isinstance(widget_for_destroy, (str, bytes)):
        for item in widget_for_destroy:
            destroy_widget(item)  # Рекурсивный вызов для каждого элемента
    else:
        # Базовый случай: item — это виджет
        try:
            widget_for_destroy.destroy()
        except Exception as e:
            print(f"Ошибка при удалении виджета: {e}")

    # После рекурсивного удаления обнуляем исходную структуру
    if isinstance(widget_for_destroy, list):
        widget_for_destroy[:] = []


def preview_create_label_from_image_list(image_list: list):
    """ Проверка отображения списка картинок в из списка изображений
    :param image_list:
    :return:
    """
    label_test = []
    for i in range(len(image_list)):
        label_test.append(Label(root, bg=back))
        label_test[i]["bd"] = 1
        label_test[i].place(x=3 + i * sizeSkin, y=3)
        label_test[i]["image"] = image_list[i]
    messagebox.showinfo("Проверка размера картинки",
                        f"Актуальный размер: {cells_count=} x {sizeSkin=}, {sizeField=}")
    destroy_widget(label_test)


def update_data_play_model_and_labelImage():
    """ Создание игровой модели и базовых картинок ячеек
    """
    global data_play_model, cells_lebel, image_skin

    image_skin = get_image_skin()
    isCheckSkin()
    cells_lebel = []
    data_play_model = []

    for i in range(cells_count):
        cells_lebel.append([])
        data_play_model.append([])

        for j in range(cells_count):
            # Формуля i * n + j генерирует ряд чисел 0, 1, 2...(n * m)
            data_play_model[i].append(countPlayers)

            # Создаем и настраиваем Label
            cells_lebel[i].append(Label(root, bg=back))
            cells_lebel[i][j]["bd"] = 1
            cells_lebel[i][j].place(
                x=(WIDTH - sizeField) // 2 + j * sizeSkin,
                y=(WIDTH - sizeField) // 2 + i * sizeSkin)
            # При нажатии на Label
            cells_lebel[i][j].bind("<Button-1>", lambda e, x=i, y=j: go(x, y))

            # Устанавливаем изображение
            cell_lebel_set_image(i, j)


# ============== НАЧАЛО ПРОГРАММЫ ===========
# Переменные
countPlayers = 2
""" Количество игроков удаствующих в игре
"""
playGame = False
player_turn = 0
""" Кто ходит сейчас
"""
player_starts_round = 0
""" Кто первый ходит
"""
possible_moves = []
""" Список возможных ходов"""

# Создание окна
root = Tk()
root.resizable(False, False)
root.title("Крестики-Нолики")

# Иконка
# root.iconbitmap("icon/icon.ico")

# Цвета
back = "#373737"
fore = "#AFAFAF"

# Настройка геометрии окна
WIDTH = 500  # 422     # Ширина
HEIGHT = int(1.44 * WIDTH)  # 600    # Высота

SCR_WIDTH = root.winfo_screenwidth()    # Ширина экрана в пикселях
SCR_HEIGHT = root.winfo_screenheight()  # Высота экрана в пикселях

POS_X = SCR_WIDTH // 2 - WIDTH // 2     # Координата по X
POS_Y = SCR_HEIGHT // 2 - HEIGHT // 2   # Кооридната по Y

root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

# Фоновый цвет окна
root["bg"] = back

# Кнопка СТАРТ
startButton = Button(root, text="СТАРТ")
startButton.place(x=0.03 * WIDTH, y=WIDTH, width=0.94 *
                  WIDTH, height=0.04 * HEIGHT)
startButton["command"] = startNewRound

# Выбор значка

# Список картинок
skinList = ["Крестик", "Нолик", "Ножницы", "Смайл"]

# Выпадающий список
skinCombobox = []
for i in range(countPlayers):
    # Метки значков
    Label(root, bg=back, fg=fore, text=f"Игрок {i + 1}:").place(x=0.02 * WIDTH, y=(0.75 + i * 0.05) * HEIGHT)

    skinCombobox.append(ttk.Combobox(
        root, width=20, values=skinList, state="readonly"))
    skinCombobox[i].place(x=0.15 * WIDTH, y=(0.75 + i * 0.05) * HEIGHT)
    skinCombobox[i].current(i)
    skinCombobox[i].bind("<<ComboboxSelected>>", lambda e: isCheckSkin())

# Выбор человек или Бот :)
player = BooleanVar()
player.set(False)

radio01 = Radiobutton(root, text="Человек", variable=player,
                      value=True, activebackground=back, bg=back, fg=fore)
radio02 = Radiobutton(root, text="Бот", variable=player,
                      value=False, activebackground=back, bg=back, fg=fore)

radio01["command"] = isCheckPlayer
radio02["command"] = isCheckPlayer

radio01.place(x=0.08 * WIDTH, y=0.85 * HEIGHT)
radio02.place(x=0.3 * WIDTH, y=0.85 * HEIGHT)

# Метка сложности
Label(root, bg=back, fg=fore, text="Уровень сложности Бота:").place(
    x=0.03 * WIDTH, y=0.88 * HEIGHT)

# Название степеней сложности
itemDiff = ["Нулевка", "Крези Бот", "Мегамозг"]

# Выпадающий список
diffCombobox = ttk.Combobox(root, values=itemDiff, state="readonly")
diffCombobox.place(x=0.03 * WIDTH, y=0.92 * HEIGHT, width=0.455 * WIDTH)
diffCombobox.current(1)

isCheckPlayer()


# ================= ИЗОБРАЖЕНИЯ

# Количество клеток. длина == ширине поля
cells_count = 3

# Метка количества клеток
Label(root, bg=back, fg=fore, text="Размер поля:").place(
    x=0.02 * WIDTH, y=0.95 * HEIGHT)

# Название степеней сложности
cells_count_item = ["3x3", "4x4", "5x5", "6x6", "7x7", "8x8", "9x9", "10x10"]

# Выпадающий список
cells_count_combobox = ttk.Combobox(
    root, values=cells_count_item, state="readonly")
cells_count_combobox.place(x=0.19 * WIDTH, y=0.95 * HEIGHT, width=0.1 * WIDTH)
cells_count_combobox.bind(
    "<<ComboboxSelected>>",
    lambda e: cells_count_change())
cells_count_combobox.current(0)

# Количество знаков подряд для победы (длина цепи)
chain = 3

# Метка длина цепи
Label(root, bg=back, fg=fore, text="Цепь:").place(
    x=0.29 * WIDTH, y=0.95 * HEIGHT)

# Выпадающий список
chain_combobox = ttk.Combobox(root, values=get_chain_values(), state="readonly")
chain_combobox.place(x=0.382 * WIDTH, y=0.95 * HEIGHT, width=0.1 * WIDTH)
chain_combobox.bind("<<ComboboxSelected>>",
					lambda e: chain_change())
chain_combobox.current(0)
chain_change()

# Размер поля
sizeField = WIDTH * 0.95

# Ширина и высота скина
sizeSkin = int((sizeField) // cells_count)

# Глобальный кеш: храним версии для разных размеров
_image_cache = {}

# Загружаем скины из файлов
image_skin_base = get_image_skin_base_from_file()
print("image_skin_base:", image_skin_base)

# двумерный список спрайтов
image_skin = get_image_skin()

# Активные скины
activeSkin = []
for i in range(countPlayers):
    activeSkin.append(image_skin[i])
activeSkin.append(image_skin[-1])


# Метки Label
cells_lebel = []

# Математическая модель игрового поля
data_play_model = []

update_data_play_model_and_labelImage()

# Чат с информацией
textDiary = Text(wrap=WORD)
textDiary.place(x=0.51 * WIDTH, y=0.75 * HEIGHT,
                width=0.45 * WIDTH, height=0.23 * HEIGHT)

# Прокрутка текста с привязкой по оси Y
scroll = Scrollbar(command=textDiary.yview)
scroll.place(x=0.96 * WIDTH, y=0.75 * HEIGHT,
             height=0.23 * HEIGHT, width=0.01 * WIDTH)
textDiary["yscrollcommand"] = scroll.set

# Обработчик клавиш
root.bind('<Key>', pressKey)


resetField()

insertText('''Приветствуем Вас на игре Крестики-Нолики!
Перед стартом можно выбрать знак Игрока, противника Бота и его сложность
''')

root.mainloop()
