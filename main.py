import random
import sqlite3
# from random import *
from random import randint
import customtkinter as ctk
from PIL import Image

# from playsound import playsound

lvl1_list = []
lvl2_list = []

color = 'green'
hover_color1 = '#135E28'


# def play_sound_event():
#    playsound('medic.wav')


# 50 title_font - для названия приложения в начале (?)
# 40 header_font - для заголовков
# 35 big_space_font - для больших промежутков (?)
# 30 text_1_font - для стандартных текстов
# 25 text_2_font - для небольших текстов
# 20 description_font - для описаний (маленьких текстов)

##292929

# Класс приложения
class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TNTdle - угадайка по сериалам с ТНТ")
        self.iconbitmap('assets/i.ico')
        self.geometry("800x600")
        self.resizable(False, False)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme("dark-blue")
        self.configure(bg='#000200')

        self.frames = {}
        self.data = {
            'rights_1': 0,
            'tries_1': 0
        }

        for F in (MainMenu, Guide, CharOut, Level_1_Choice, Results):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name, attempts=None):
        frame = self.frames[page_name]
        frame.tkraise()
        # if page_name == 'Level_1_Choice' or page_name == 'Level_2_Write':
        # frame.reset_lvl()
        # frame.widgets()
        # if page_name == 'Results':
        #    frame.widgets(result)
        if page_name == 'Level_1_Choice':
            if hasattr(frame, 'widgets'):
                frame.add_scrollable_frame()
        if hasattr(frame, 'show'):
            frame.show(attempts)


# Главное меню
class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title_font = ctk.CTkFont(family="Impact", size=50)
        big_space_font = ctk.CTkFont(family="Impact", size=35)
        text_1_font = ctk.CTkFont(family="Impact", size=30)
        description_font = ctk.CTkFont(family="Impact", size=20)

        top_container = ctk.CTkFrame(self, fg_color='#212121')
        top_container.pack(pady=(0, 0))

        image = Image.open("assets/logo_2.png")
        photo = ctk.CTkImage(image, size=(400, 180))
        image_label = ctk.CTkLabel(top_container, image=photo, text="", bg_color='#212121', width=800)
        image_label.grid(row=2, pady=(20, 0))

        label1 = ctk.CTkLabel(top_container, text="TNTdle", text_color='white',
                              bg_color='#212121', font=title_font, width=800)
        label1.grid(row=0, column=0, sticky="ew", pady=(20, 0))

        label2 = ctk.CTkLabel(top_container, text='Легендарная игра-угадайка\nпо сериалам с телеканала ТНТ',
                              text_color='white',
                              bg_color='#212121', font=text_1_font)
        label2.grid(row=1, column=0, sticky="ew")

        bottom_container = ctk.CTkFrame(self, fg_color='#212121')
        bottom_container.pack(side="bottom", pady=63, fill="y", expand=True)

        play_1 = ctk.CTkButton(bottom_container, text="Угадать по\nхарактеристикам",
                               command=lambda: self.controller.show_frame("Level_1_Choice"), fg_color="#007AFF",
                               hover_color="#0064D1", bg_color='#212121',
                               width=170, height=170, font=description_font)
        play_1.grid(row=0, column=0)

        play_2 = ctk.CTkButton(bottom_container, text="Угадать по\nцитате",
                               # command=lambda: self.controller.show_frame("Guide"),
                               fg_color="#F10C21",
                               # command=play_sound_event,
                               hover_color="#C90A1C",
                               width=170, height=170, font=description_font)
        play_2.grid(row=0, column=1, padx=(50, 50))
        characters = ctk.CTkButton(bottom_container, text="Все\nперсонажи",
                                   # command=lambda: self.controller.show_frame("Guide"),
                                   fg_color="#007AFF",
                                   # command=play_sound_event,
                                   hover_color="#0064D1",
                                   width=170, height=170, font=description_font)
        characters.grid(row=0, column=2)


# Справочник
class Guide(ctk.CTkFrame):
    def __init__(self, parent, controller):
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
        bottom_container.pack(side="bottom", pady=(0, 700))

        back = ctk.CTkButton(bottom_container, text="Назад",
                             command=lambda: controller.show_frame("MainMenu"), fg_color=color,
                             hover_color=hover_color1,
                             width=350, height=50, font=text_1_font)
        back.grid(row=0, column=0, sticky="ewsn")


# CharOut
class CharOut(ctk.CTkFrame):
    def __init__(self, parent, controller):
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
        bottom_container.pack(side="bottom", pady=(0, 700))

        back = ctk.CTkButton(bottom_container, text="Назад",
                             command=lambda: controller.show_frame("MainMenu"), fg_color=color,
                             hover_color=hover_color1,
                             width=350, height=50, font=text_1_font)
        back.grid(row=0, column=0, sticky="ewsn")

    def char_output(self):
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()

        cursor.execute(f"SELECT name FROM Nouns WHERE id = 1")
        word1 = cursor.fetchall()
        # lvl1_list.extend([word1[0][0], word2[0][0], word3[0][0], word4[0][0], wordru, right_id])


# Уровень "Выбор"
class Level_1_Choice(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.text_2_font = ctk.CTkFont(family="Impact", size=25)
        self.description = ctk.CTkFont(family="Impact", size=20)
        self.features = ctk.CTkFont(family="Impact", size=13)

        # self.lvl1()
        self.widgets()
    def true_char_choice(self):
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        rcount = random.randint(1, count)

        cursor.execute(
            f"SELECT id, name, series, gender, role, height, membership, profession, first_date, family_statuus FROM characters WHERE id = {rcount}")
        self.true_char = cursor.fetchall()
        print(self.true_char)
        print(self.true_char[0])
        self.true_char_id = self.true_char[0][0]
        self.true_char_name = self.true_char[0][1]
        self.true_char_series = self.true_char[0][2]
        self.true_char_gender = self.true_char[0][3]
        self.true_char_role = self.true_char[0][4]
        self.true_char_height = self.true_char[0][5]
        self.true_char_membership = self.true_char[0][6]
        self.true_char_profession = self.true_char[0][7]
        self.true_char_first_date = self.true_char[0][8]
        self.true_char_family_status = self.true_char[0][9]

    def add_scrollable_frame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=650, height=300)
        # self.scrollable_frame.configure(height=200)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both")
        # self.scrollable_frame.grid(row=4, column=0, sticky="ewsn")
        print("scrol добавлен")

    def widgets(self):
        self.true_char_choice()

        self.top_container = ctk.CTkFrame(self, fg_color='#212121')
        self.top_container.pack(pady=(0, 0))

        self.title = ctk.CTkLabel(self.top_container, text="Угадывание персонажа по его\nхарактеристикам",
                                  text_color='white',
                                  font=self.text_1_font)
        self.title.grid(row=1, column=0, sticky="nsew", pady=(20, 0))

        self.entry_name = ctk.CTkEntry(self.top_container,
                                       text_color='white', bg_color='#212121',
                                       font=self.text_1_font)
        self.entry_name.grid(row=2, column=0, sticky="nsew", pady=20)

        self.button_accept = ctk.CTkButton(self.top_container, text='Проверить догадку',
                                           command=self.add_widget,
                                           fg_color=color, hover_color=hover_color1, width=200,
                                           height=50, font=self.text_2_font)
        self.button_accept.grid(row=3, column=0, sticky="ewsn")

        #self.add_scrollable_frame()

        self.widget_counter = 0

    def add_widget(self):
        text = self.entry_name.get()
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT id, name, series, gender, role, height, membership, profession, first_date, family_statuus FROM characters WHERE name = '{text}'")
            nigga = cursor.fetchall()
            self.char_id = nigga[0][0]
            self.char_name = nigga[0][1]
            self.char_series = nigga[0][2]
            self.char_gender = nigga[0][3]
            self.char_role = nigga[0][4]
            self.char_height = nigga[0][5]
            self.char_membership = nigga[0][6]
            self.char_profession = nigga[0][7]
            self.char_first_date = nigga[0][8]
            self.char_family_statuus = nigga[0][9]
            print(self.char_id)
            print(self.char_name)
            self.widget_counter += 1

            if text != self.true_char_name:
                image = Image.open(f"characters/{self.char_id}.png")
                photo = ctk.CTkImage(image, size=(80, 80))
                image_label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="", bg_color='#212121',
                                           width=80, height=80)
                image_label.grid(row=self.widget_counter, column=0)
                print(self.true_char_name)

                # name_label = ctk.CTkLabel(
                #     self.scrollable_frame,
                #     text=f"Виджет №{self.true_char_name}",
                #     fg_color="gray",
                #     corner_radius=6
                # )
                # name_label.grid(row=self.widget_counter, column=1)

                # name_label2 = ctk.CTkLabel(
                #     self.scrollable_frame,
                #     text=f"{self.char_name}",
                #     fg_color="gray",
                #     corner_radius=6
                # )
                # name_label2.grid(row=self.widget_counter, column=2)

                series_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_series}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                series_label.grid(row=self.widget_counter, column=3)

                gender_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_gender}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                gender_label.grid(row=self.widget_counter, column=4)

                role_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_role}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                role_label.grid(row=self.widget_counter, column=5)

                height_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_height}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                height_label.grid(row=self.widget_counter, column=6)

                membership_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_membership}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                membership_label.grid(row=self.widget_counter, column=7)

                profession_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_profession}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                profession_label.grid(row=self.widget_counter, column=8)

                date_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_first_date}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                date_label.grid(row=self.widget_counter, column=9)

                family_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_family_statuus}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                family_label.grid(row=self.widget_counter, column=10)

                if self.char_series != self.true_char_series:
                    series_label.configure(fg_color="red")
                if self.char_gender != self.true_char_gender:
                    gender_label.configure(fg_color="red")
                current_gender = gender_label.cget("text")
                if current_gender == "М":
                    gender_label.configure(text="Мужской")
                elif current_gender == "Ж":
                    gender_label.configure(text="Женский")
                if (self.true_char_role == "Главная" and (
                        self.char_role == "Основная" or self.char_role == "Втор.")) or (
                        self.true_char_role == "Основная" and self.char_role == "Втор."):
                    role_label.configure(fg_color="red", text=f"{self.char_role} ⬆")
                elif (self.true_char_role == "Втор." and (
                        self.char_role == "Основная" or self.char_role == "Главная")) or (
                        self.true_char_role == "Основная" and self.char_role == "Главная"):
                    role_label.configure(fg_color="red", text=f"{self.char_role} ⬇")

                current_height = int(height_label.cget("text"))
                if current_height == 1:
                    height_label.configure(text="Очень\nнизкий")
                elif current_height == 2:
                    height_label.configure(text="Низкий")
                elif current_height == 3:
                    height_label.configure(text="Средний")
                elif current_height == 4:
                    height_label.configure(text="Высокий")
                elif current_height == 5:
                    height_label.configure(text="Очень\nвыс.")
                if self.char_height > self.true_char_height:
                    new_text = height_label.cget("text") + " ⬇"
                    height_label.configure(text=new_text)
                    height_label.configure(fg_color="red")
                elif self.char_height < self.true_char_height:
                    new_text = height_label.cget("text") + " ⬆"
                    height_label.configure(text=new_text)
                    height_label.configure(fg_color="red")

                if self.char_membership != self.true_char_membership:
                    membership_label.configure(fg_color="red")
                if self.char_profession != self.true_char_profession:
                    profession_label.configure(fg_color="red")

                if self.char_first_date > self.true_char_first_date:
                    date_label.configure(fg_color="red", text=f"{self.char_first_date} ⬇")
                elif self.char_first_date < self.true_char_first_date:
                    date_label.configure(fg_color="red", text=f"{self.char_first_date} ⬆")

                if self.char_family_statuus == 1:
                    if self.char_gender == "М":
                        family_label.configure(text="Женат")
                    else:
                        family_label.configure(text="Замужем")
                else:
                    if self.char_gender == "М":
                        family_label.configure(text="Не женат")
                    else:
                        family_label.configure(text="Не замужем")
                if self.char_family_statuus != self.true_char_family_status:
                    family_label.configure(fg_color="red")

            else:
                self.true_char_choice()
                #self.scrollable_frame.destroy()
                self.scrollable_frame.pack_forget()
                self.entry_name.delete(0, "end")
                self.controller.show_frame("Results", self.widget_counter)
                self.widget_counter = 0

                # self.widget_counter = 0
                # new_label = ctk.CTkLabel(
                #     self.scrollable_frame,
                #     text=f"Виджет №ПОБЕДА",
                #     fg_color="gray",
                #     corner_radius=6
                # )
                # new_label.grid(row=self.widget_counter, column=0)
                #
                # new_label2 = ctk.CTkLabel(
                #     self.scrollable_frame,
                #     text=f"Виджет №{self.widget_counter}",
                #     fg_color="gray",
                #     corner_radius=6
                # )
                # new_label2.grid(row=self.widget_counter, column=1)
        except Exception as e:
            print(e)
            self.entry_name.delete(0, "end")
            self.entry_name.insert(0, "Новый текст")


class Results(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.widgets()

    def widgets(self):
        self.top_container = ctk.CTkFrame(self)
        self.top_container.pack(pady=(0, 0))

        self.title = ctk.CTkLabel(self.top_container, text="ПОБЕДА!", text_color='white',
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

        self.image = Image.open("assets/final.png")
        self.photo = ctk.CTkImage(self.image, size=(625, 350))
        self.image_label = ctk.CTkLabel(self.top_container, image=self.photo, text="")
        self.image_label.grid(row=3)

        self.bottom_container = ctk.CTkFrame(self)
        self.bottom_container.pack(side="bottom", pady=(20, 700))

        self.button = ctk.CTkButton(self.bottom_container, text="Вернуться в главное меню",
                                    command=lambda: self.controller.show_frame("MainMenu"), fg_color=color,
                                    hover_color=hover_color1,
                                    width=600, height=50, font=self.text_1_font)
        self.button.grid(row=3, column=0, sticky="ewsn")

    def show(self, attempts):
        # rights = self.controller.data['rights_1']
        self.result.configure(
            text=f"Угадано с {attempts} попытки!"
        )


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
