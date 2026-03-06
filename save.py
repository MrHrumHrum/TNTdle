import customtkinter as ctk
from PIL import Image
import sqlite3
from random import *
import random

lvl1_list = []
lvl2_list = []

color = 'green'
hover_color1 = '#135E28'

#50 title_font - для названия приложения в начале (?)
#40 header_font - для заголовков
#35 big_space_font - для больших промежутков (?)
#30 text_1_font - для стандартных текстов
#25 text_2_font - для небольших текстов
#20 description_font - для описаний (маленьких текстов)

##292929

# Класс приложения
class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Во Все Испанские")
        self.iconbitmap('spain_icon.ico')
        self.geometry("800x600")
        self.resizable(False, False)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("dark-blue")
        self.configure(bg='#000200')

        my_font = ctk.CTkFont(family="Impact", size=25)

        self.frames = {}
        self.data = {
            'rights_1': 0,
            'tries_1': 0
        }

        for F in (StartMenu, MainMenu, Guide, LevelSelect, Level_1_Choice, Level_2_Write, Results):
            page_name = F.__name__
            frame = F(parent=self, controller=self, data=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartMenu")
        #self.show_frame("Results")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == 'Level_1_Choice' or page_name == 'Level_2_Write':
            frame.reset_lvl()
        if hasattr(frame, 'show'):
            frame.show()


# Стартовое окно
class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller

        title_font = ctk.CTkFont(family="Impact", size=50)
        text_1_font = ctk.CTkFont(family="Impact", size=30)

        top_container = ctk.CTkFrame(self)
        top_container.pack(pady=(0, 0))

        image = Image.open("hola.png")
        photo = ctk.CTkImage(image, size=(550, 350))
        image_label = ctk.CTkLabel(top_container, image=photo, text="")
        image_label.grid(row=3)

        label1 = ctk.CTkLabel(top_container, text="Добро пожаловать в приложение", text_color='white',
                              bg_color='#212121', font=text_1_font)
        label1.grid(row=0, column=0, sticky="nsew")

        label2 = ctk.CTkLabel(top_container, text='"Во Все Испанские"', text_color='white',
                              bg_color='#212121', font=title_font)
        label2.grid(row=1, column=0, sticky="nsew")

        space = ctk.CTkLabel(top_container, text='', text_color='white',
                              bg_color='#212121', font=text_1_font)
        space.grid(row=2, column=0, sticky="nsew")


        bottom_container = ctk.CTkFrame(self)
        bottom_container.pack(side="bottom", pady=63, fill="both", expand=True)

        button = ctk.CTkButton(bottom_container, text="Войти в приложение",
                               command=lambda: controller.show_frame("MainMenu"), fg_color=color, hover_color=hover_color1,
                               width=800, height=50, font=text_1_font)
        button.grid(row=0, column=0, sticky="ewsn")


# Главное меню
class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller

        global color
        header_font = ctk.CTkFont(family="Impact", size=40)
        big_space_font = ctk.CTkFont(family="Impact", size=35)

        top_container = ctk.CTkFrame(self)
        top_container.pack(pady=(0, 0))
        menu_label = ctk.CTkLabel(top_container, text="Во Все Испанские\nГлавное меню", text_color='white',
                                  bg_color='#212121', font=header_font)
        menu_label.grid(row=0, column=0, sticky="nsew")

        bottom_container = ctk.CTkFrame(self)
        bottom_container.pack(side="bottom", pady=(20, 600))

        play = ctk.CTkButton(bottom_container, text="Выбрать уровень",
                             command=lambda: self.controller.show_frame("LevelSelect"), fg_color=color, hover_color=hover_color1,
                             width=500, height=100, font=header_font)
        play.grid(row=0, column=0, sticky="ewsn")
        space = ctk.CTkLabel(bottom_container, text="                 ", text_color='white', bg_color='#212121',
                             font=big_space_font)
        space.grid(row=1, column=0, sticky="nsew")
        guide = ctk.CTkButton(bottom_container, text="Справочник",
                              command=lambda: self.controller.show_frame("Guide"), fg_color=color, hover_color=hover_color1,
                              width=500, height=100, font=header_font)
        guide.grid(row=2, column=0, sticky="ewsn")


class Guide(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller

        header_font = ctk.CTkFont(family="Impact", size=40)
        text_1_font = ctk.CTkFont(family="Impact", size=30)
        text_2_font = ctk.CTkFont(family="Impact", size=25)

        top_container = ctk.CTkFrame(self)
        top_container.pack(pady=(0, 0))

        name_label = ctk.CTkLabel(top_container, text='Справочник', text_color='white',
                                       bg_color='#212121', font=header_font)
        name_label.grid(row=0, column=0, sticky="nsew")

        space = ctk.CTkLabel(top_container, text='      ', text_color='white',
                                  bg_color='#212121', font=header_font)
        space.grid(row=1, column=0, sticky="nsew")

        text = ctk.CTkLabel(top_container,
                                 text='1. Все слова пишутся с маленькой буквы.\n2. Испанские слова пишутся без диакритических знаков.\n2. Испанские слова пишутся без диакритических знаков.\n3. В русских словах вместо "ё" пишется "е".',
                                 text_color='white',
                                 bg_color='#212121', font=text_1_font, justify='left')
        text.grid(row=2, column=0, sticky="nsew")

        bottom_container = ctk.CTkFrame(self)
        bottom_container.pack(side="bottom", pady=(20, 550))

        back = ctk.CTkButton(bottom_container, text="Назад",
                                  command=lambda: controller.show_frame("MainMenu"), fg_color=color, hover_color=hover_color1,
                                  width=350, height=50, font=text_2_font)
        back.grid(row=1, column=0, sticky="ewsn")


# Выбор уровня
class LevelSelect(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller

        header_font = ctk.CTkFont(family="Impact", size=40)
        text_2_font = ctk.CTkFont(family="Impact", size=25)
        description_font = ctk.CTkFont(family="Impact", size=20)

        top_container = ctk.CTkFrame(self)
        top_container.pack(pady=(0, 0))

        label0 = ctk.CTkLabel(top_container, text="Выберите тип тренажёра:", text_color='white', bg_color='#212121',
                              font=header_font)
        label0.grid(row=0, column=0, sticky="nsew")

        bottom_container = ctk.CTkFrame(self)
        bottom_container.pack(side="bottom", pady=(20, 600))

        label11 = ctk.CTkLabel(bottom_container, text="Тип №1:",
                               text_color='white', bg_color='#212121',
                               font=text_2_font)
        label11.grid(row=1, column=0, sticky="nsew")
        button1 = ctk.CTkButton(bottom_container, text="Выбор правильного перевода",
                                command=lambda: controller.show_frame("Level_1_Choice"), fg_color=color, hover_color=hover_color1,
                                width=300, height=50, font=text_2_font)
        button1.grid(row=2, column=0, sticky="ewsn")
        label12 = ctk.CTkLabel(bottom_container, text="Выберите правильный перевод слова из 4-х представленных",
                               text_color='white', bg_color='#212121',
                               font=description_font)
        label12.grid(row=3, column=0, sticky="nsew")
        label_space = ctk.CTkLabel(bottom_container, text="                                 ", bg_color='#212121',
                                   font=description_font)
        label_space.grid(row=4, column=0, sticky="nsew")
        label21 = ctk.CTkLabel(bottom_container, text="Тип №2:",
                               text_color='white', bg_color='#212121',
                               font=text_2_font)
        label21.grid(row=5, column=0, sticky="nsew")
        button2 = ctk.CTkButton(bottom_container, text="Ввод правильного перевода",
                                command=lambda: controller.show_frame("Level_2_Write"), fg_color=color, hover_color=hover_color1,
                                width=600, height=50, font=text_2_font)
        button2.grid(row=6, column=0, sticky="ewsn")
        label22 = ctk.CTkLabel(bottom_container, text="Введите с помощью клавиатуры перевод слова", text_color='white',
                               bg_color='#212121',
                               font=description_font)
        label22.grid(row=7, column=0, sticky="nsew")
        label_space_2 = ctk.CTkLabel(bottom_container, text="                                 ", bg_color='#212121',
                                     font=header_font)
        label_space_2.grid(row=8, column=0, sticky="nsew")
        back = ctk.CTkButton(bottom_container, text="Вернуться в главное меню",
                             command=lambda: self.controller.show_frame("MainMenu"), fg_color=color, hover_color=hover_color1,
                             width=350, height=50, font=text_2_font)
        back.grid(row=9, column=0, sticky="wesn")


# Уровень "Выбор"
class Level_1_Choice(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.text_2_font = ctk.CTkFont(family="Impact", size=25)
        self.description = ctk.CTkFont(family="Impact", size=20, weight="bold")

        self.lvl1()
        self.widgets()

    def widgets(self):
        self.top_container = ctk.CTkFrame(self)
        self.top_container.pack(pady=(0, 0))

        self.title_1 = ctk.CTkLabel(self.top_container, text=f"Задание {self.controller.data['tries_1'] + 1}",
                                    text_color='white',
                                    bg_color='#212121',
                                    font=self.header_font)
        self.title_1.grid(row=0, column=0, sticky="nsew")
        self.title_2 = ctk.CTkLabel(self.top_container, text=f"Выберите перевод русского слова на испанский:",
                                    text_color='white', bg_color='#212121',
                                    font=self.text_1_font)
        self.title_2.grid(row=1, column=0, sticky="nsew")

        self.space_0 = ctk.CTkLabel(self.top_container,
                                    text="                                                         ",
                                    bg_color='#212121',
                                    font=self.text_1_font)
        self.space_0.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.lable_ru = ctk.CTkLabel(self.top_container, text='',
                                     text_color='white', bg_color='#212121',
                                     font=self.text_1_font)
        self.lable_ru.grid(row=3, column=0, sticky="nsew")

        self.bottom_container = ctk.CTkFrame(self)
        self.bottom_container.pack(side="bottom", pady=(20, 700))

        self.button1 = ctk.CTkButton(self.bottom_container, text='', command=lambda: self.check1(0),
                                     fg_color=color, hover_color=hover_color1, width=200,
                                     height=50, font=self.text_2_font)
        self.button1.grid(row=4, column=0, sticky="ewsn")
        self.space_1_2 = ctk.CTkLabel(self.bottom_container, text="       ", bg_color='#212121',
                                      font=self.header_font)
        self.space_1_2.grid(row=4, column=1, sticky="nsew")
        self.button2 = ctk.CTkButton(self.bottom_container, text='',
                                     command=lambda: self.check1(1),
                                     fg_color=color, hover_color=hover_color1, width=200,
                                     height=50, font=self.text_2_font)
        self.button2.grid(row=4, column=2, sticky="ewsn")
        self.space_12_34 = ctk.CTkLabel(self.bottom_container,
                                        text="                                                         ",
                                        bg_color='#212121',
                                        font=self.header_font)
        self.space_12_34.grid(row=5, column=0, columnspan=3, sticky="nsew")
        self.button3 = ctk.CTkButton(self.bottom_container, text='',
                                     command=lambda: self.check1(2),
                                     fg_color=color, hover_color=hover_color1, width=200,
                                     height=50, font=self.text_2_font)
        self.button3.grid(row=6, column=0, sticky="ewsn")
        self.space_3_4 = ctk.CTkLabel(self.bottom_container, text="       ",
                                      bg_color='#212121',
                                      font=self.header_font)
        self.space_3_4.grid(row=6, column=1, sticky="nsew")
        self.button4 = ctk.CTkButton(self.bottom_container, text='',
                                     command=lambda: self.check1(3),
                                     fg_color=color, hover_color=hover_color1, width=200,
                                     height=50, font=self.text_2_font)
        self.button4.grid(row=6, column=2, sticky="ewsn")
        self.space_after = ctk.CTkLabel(self.bottom_container, text="       ",
                                        bg_color='#212121',
                                        font=self.header_font)
        self.space_after.grid(row=7, columnspan=3, sticky="nsew")
        self.label_result = ctk.CTkLabel(self.bottom_container, text='',
                                         text_color='white', bg_color='#212121',
                                         font=self.text_1_font)
        self.label_result.grid(row=8, columnspan=3, sticky="nsew")
        self.update_widgets(0, '')

    def update_widgets(self, x, word):
        if x == 1:
            result_text = 'Правильно!'
        elif x == 2:
            result_text = f'Неправильно!\nПравильный ответ: {word}'
        else:
            result_text = ''

        self.label_result.configure(text=result_text)

        # self.title_1.configure(text=f"Задание {self.controller.data['tries_1'] + 1}")
        # self.lable_ru.configure(text='', text_color='gray')
        for btn in [self.button1, self.button2, self.button3, self.button4]:
            # btn.configure(text='', state='disabled')
            btn.configure(state='disabled')

        if x in (1, 2) and self.controller.data['tries_1'] < 10:
            self.after(3000, self.show_new_question)
        elif x == 0:
            self.show_new_question()

    def show_new_question(self):
        self.label_result.configure(text='')
        self.lable_ru.configure(text=lvl1_list[4])
        self.title_1.configure(text=f"Задание {self.controller.data['tries_1'] + 1}")

        self.button1.configure(text=lvl1_list[0], state='normal')
        self.button2.configure(text=lvl1_list[1], state='normal')
        self.button3.configure(text=lvl1_list[2], state='normal')
        self.button4.configure(text=lvl1_list[3], state='normal')

    def lvl1(self):
        global lvl1_list
        lvl1_list = []
        tralaleo = list(range(1, 9))
        random.shuffle(tralaleo)
        tralala = tralaleo[:4]
        connection = sqlite3.connect("Words.db")
        cursor = connection.cursor()

        cursor.execute(f"SELECT word_es  FROM Nouns WHERE id = {tralala[0]}")
        word1 = cursor.fetchall()
        cursor.execute(f"SELECT word_es  FROM Nouns WHERE id = {tralala[1]}")
        word2 = cursor.fetchall()
        cursor.execute(f"SELECT word_es  FROM Nouns WHERE id = {tralala[2]}")
        word3 = cursor.fetchall()
        cursor.execute(f"SELECT word_es FROM Nouns WHERE id = {tralala[3]}")
        word4 = cursor.fetchall()
        right_id = random.randint(0, 3)
        cursor.execute(f"SELECT word_ru FROM Nouns WHERE id = {tralala[right_id]}")
        wordru0 = cursor.fetchall()
        wordru = wordru0[0][0]
        lvl1_list.extend([word1[0][0], word2[0][0], word3[0][0], word4[0][0], wordru, right_id])

    def check1(self, es):
        if es == lvl1_list[5]:
            self.controller.data['rights_1'] += 1
            print("Правильный ответ!", self.controller.data['tries_1'])
            i = 1
            word = ''
        else:
            print("Неправильный ответ!", self.controller.data['tries_1'])
            i = 2
            word = lvl1_list[lvl1_list[5]]
        self.controller.data['tries_1'] += 1

        self.update_widgets(i, word)
        self.lvl1()
        print(lvl1_list)

        if self.controller.data['tries_1'] >= 10:
            print(self.controller.data['tries_1'])
            # self.controller.data['tries_1'] = 0
            self.after(3000, self.lvL1_end)

    def lvL1_end(self):
        print("Тест завершен!", self.controller.data['rights_1'])
        self.controller.data['tries_1'] = 0
        self.controller.show_frame("Results")

    def reset_lvl(self):
        self.controller.data['tries_1'] = 0
        self.controller.data['rights_1'] = 0
        self.lvl1()
        self.update_widgets(0, '')


# Уровень "Письменный ответ"
class Level_2_Write(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.text_2_font = ctk.CTkFont(family="Impact", size=25)
        self.lvl2()
        self.widgets()

    def widgets(self):
        self.top_container = ctk.CTkFrame(self)
        self.top_container.pack(pady=(0, 0))

        self.title_1 = ctk.CTkLabel(self.top_container, text=f"Задание {self.controller.data['tries_1'] + 1}",
                                    text_color='white',
                                    bg_color='#212121',
                                    font=self.header_font)
        self.title_1.grid(row=0, column=0, sticky="nsew")
        self.title_2 = ctk.CTkLabel(self.top_container, text=f"Напишите русский перевод испанского слова:",
                                    text_color='white', bg_color='#212121',
                                    font=self.text_1_font)
        self.title_2.grid(row=1, column=0, sticky="nsew")

        self.space_0 = ctk.CTkLabel(self.top_container,
                                    text="                                                         ",
                                    bg_color='#212121',
                                    font=self.text_1_font)
        self.space_0.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.lable_es = ctk.CTkLabel(self.top_container, text='',
                                     text_color='white', bg_color='#212121',
                                     font=self.text_1_font)
        self.lable_es.grid(row=3, column=0, sticky="nsew")

        self.bottom_container = ctk.CTkFrame(self)
        self.bottom_container.pack(side="bottom", pady=(20, 700))

        self.entry = ctk.CTkEntry(self.bottom_container, font=self.text_2_font, placeholder_text='Введите перевод...')
        self.entry.grid(row=0, column=0, sticky="nsew")

        self.space_en_bt = ctk.CTkLabel(self.bottom_container, text="       ",
                                        bg_color='#212121',
                                        font=self.header_font)
        self.space_en_bt.grid(row=1, columnspan=3, sticky="nsew")

        self.button1 = ctk.CTkButton(self.bottom_container, text='Подтвердить ответ',
                                     command=lambda: self.check1(lvl2_list[0]),
                                     fg_color=color, hover_color=hover_color1, width=400,
                                     height=50, font=self.text_2_font)
        self.button1.grid(row=2, column=0, sticky="ewsn")
        self.space_after = ctk.CTkLabel(self.bottom_container, text="       ",
                                        bg_color='#212121',
                                        font=self.header_font)
        self.space_after.grid(row=3, columnspan=3, sticky="nsew")
        self.label_result = ctk.CTkLabel(self.bottom_container, text='',
                                         text_color='white', bg_color='#212121',
                                         font=self.text_1_font)
        self.label_result.grid(row=4, columnspan=3, sticky="nsew")
        self.update_widgets(0, '')

    def update_widgets(self, x, word):
        if x == 1:
            result_text = 'Правильно!'
        elif x == 2:
            result_text = f'Неправильно!\nПравильный ответ: {word}'
        else:
            result_text = ''

        self.label_result.configure(text=result_text)

        for btn in [self.button1]:
            btn.configure(state='disabled')

        if x in (1, 2) and self.controller.data['tries_1'] < 10:
            self.after(3000, self.show_new_question)
        elif x == 0:
            self.show_new_question()

    def show_new_question(self):
        self.label_result.configure(text='')
        self.lable_es.configure(text=lvl2_list[0])
        self.title_1.configure(text=f"Задание {self.controller.data['tries_1'] + 1}")
        # self.button1.configure(text=lvl2_list[0], state='normal')
        self.button1.configure(state='normal')

    def lvl2(self):
        global lvl2_list
        lvl2_list = []
        tralaleo = list(range(1, 9))
        random.shuffle(tralaleo)
        connection = sqlite3.connect("Words.db")
        cursor = connection.cursor()

        cursor.execute(f"SELECT word_es  FROM Nouns WHERE id = {tralaleo[0]}")
        word_es = cursor.fetchall()
        cursor.execute(f"SELECT word_ru FROM Nouns WHERE id = {tralaleo[0]}")
        word_ru = cursor.fetchall()
        lvl2_list.extend([word_es[0][0], word_ru[0][0]])

    def check1(self, es):
        answer = self.entry.get()
        if answer == lvl2_list[1]:
            self.controller.data['rights_1'] += 1
            print("Правильный ответ!", self.controller.data['tries_1'])
            i = 1
            word = ''
        else:
            print("Неправильный ответ!", self.controller.data['tries_1'])
            i = 2
            word = lvl2_list[1]
        self.controller.data['tries_1'] += 1

        self.update_widgets(i, word)
        self.lvl2()
        print(lvl2_list)

        if self.controller.data['tries_1'] >= 10:
            print(self.controller.data['tries_1'])
            # self.controller.data['tries_1'] = 0
            self.after(3000, self.lvL2_end)

    def lvL2_end(self):
        print("Тест завершен!", self.controller.data['rights_1'])
        self.controller.data['tries_1'] = 0
        self.controller.show_frame("Results")

    def reset_lvl(self):
        self.controller.data['tries_1'] = 0
        self.controller.data['rights_1'] = 0
        self.lvl2()
        self.update_widgets(0, '')


class Results(ctk.CTkFrame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.widgets()

    def widgets(self):
        self.top_container = ctk.CTkFrame(self)
        self.top_container.pack(pady=(0, 0))

        self.title = ctk.CTkLabel(self.top_container, text="Поздравляем с завершением теста!", text_color='white',
                                  bg_color='#212121',
                                  font=self.header_font)
        self.title.grid(row=0, column=0, sticky="nsew")

        self.result = ctk.CTkLabel(self.top_container, text='', text_color='white',
                                   bg_color='#212121',
                                   font=self.text_1_font)
        self.result.grid(row=1, column=0, sticky="nsew")

        self.space = ctk.CTkLabel(self.top_container, text='', text_color='white',
                                   bg_color='#212121',
                                   font=self.text_1_font)
        self.space.grid(row=2, column=0, sticky="nsew")

        self.image = Image.open("felicidades.png")
        self.photo = ctk.CTkImage(self.image, size=(625, 350))
        self.image_label = ctk.CTkLabel(self.top_container, image=self.photo, text="")
        self.image_label.grid(row=3)

        self.bottom_container = ctk.CTkFrame(self)
        self.bottom_container.pack(side="bottom", pady=(20, 600))

        self.button = ctk.CTkButton(self.bottom_container, text="Вернуться в главное меню",
                                    command=lambda: self.controller.show_frame("MainMenu"), fg_color=color, hover_color=hover_color1,
                                    width=600, height=50, font=self.text_1_font)
        self.button.grid(row=3, column=0, sticky="ewsn")


    def show(self):
        rights = self.controller.data['rights_1']
        self.result.configure(
            text=f"Количество правильных ответов: {rights}"
        )


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
