import random
import sqlite3
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
        # self.data = {
        #     'rights_1': 0,
        #     'tries_1': 0
        # }

        for F in (MainMenu, LevelClassic, LevelQuote, Results):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name, attempts=None):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == 'LevelClassic' or page_name == 'LevelQuote':
            if hasattr(frame, 'add_scrollable_frame'):
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
        self.toplevel_window = None

        top_container = ctk.CTkFrame(self, fg_color='#212121')
        top_container.pack(pady=(0, 0))

        image = Image.open("assets/logo_2.png")
        photo = ctk.CTkImage(image, size=(400, 150))
        image_label = ctk.CTkLabel(top_container, image=photo, text="", bg_color='#212121', width=800)
        image_label.grid(row=2, pady=(20, 0))

        label1 = ctk.CTkLabel(top_container, text="TNTdle", text_color='white',
                              bg_color='#212121', font=title_font, width=800)
        label1.grid(row=0, column=0, sticky="ew", pady=(20, 0))

        label2 = ctk.CTkLabel(top_container, text='Легендарная игра-угадайка\nпо сериалам с телеканала ТНТ',
                              text_color='white', bg_color='#212121', font=text_1_font)
        label2.grid(row=1, column=0, sticky="ew")

        bottom_container = ctk.CTkFrame(self, fg_color='#212121')
        bottom_container.pack(side="bottom", pady=63, fill="y", expand=True)

        play_1 = ctk.CTkButton(bottom_container, text="Угадать по\nхарактеристикам",
                               command=lambda: self.controller.show_frame("LevelClassic"), fg_color="#007AFF",
                               hover_color="#0064D1", bg_color='#212121',
                               width=170, height=170, font=description_font)
        play_1.grid(row=0, column=0)

        play_2 = ctk.CTkButton(bottom_container, text="Угадать по\nцитате",
                               command=lambda: self.controller.show_frame("LevelQuote"), fg_color="#F10C21",
                               # command=play_sound_event,
                               hover_color="#C90A1C", width=170, height=170, font=description_font)
        play_2.grid(row=0, column=1, padx=(50, 50))
        characters = ctk.CTkButton(bottom_container, text="Все\nперсонажи",
                                   command=self.open_toplevel,
                                   fg_color="#007AFF",
                                   # command=play_sound_event,
                                   hover_color="#0064D1", width=170, height=170, font=description_font)
        characters.grid(row=0, column=2)

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AllChars(self, self)
        else:
            self.toplevel_window.focus()


class AllChars(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.geometry("800x800+1000+0")
        self.title("Димка")

        header_font = ctk.CTkFont(family="Impact", size=40)
        text_1_font = ctk.CTkFont(family="Impact", size=30)
        text_2_font = ctk.CTkFont(family="Impact", size=25)

        self.top_container = ctk.CTkFrame(self)
        self.top_container.pack(pady=(0, 0))

        connection = sqlite3.connect("characters.db")
        self.cursor = connection.cursor()

        self.cursor.execute("SELECT COUNT(*) FROM characters")
        count = self.cursor.fetchone()[0]
        for i in range(1, count):
            self.new_char(i, count)

    def new_char(self, index, count):
        mexican_border = int(round(count / 3, 0))
        rage_of_the_usa = 0
        column_buff = 0
        if index >= mexican_border * 2:
            column_buff += 4
            rage_of_the_usa = mexican_border * 2 - 1
        elif index >= mexican_border:
            column_buff += 2
            rage_of_the_usa = mexican_border - 1
        self.cursor.execute(
            f"SELECT id, name, series FROM characters WHERE id = {index}")
        self.char = self.cursor.fetchall()
        self.char_id = self.char[0][0]
        self.char_name = self.char[0][1]
        self.char_series = self.char[0][2]
        image = Image.open(f"characters/{self.char_id}.png")
        photo = ctk.CTkImage(image, size=(80, 80))
        image_label = ctk.CTkLabel(self.top_container, image=photo, text="", bg_color='#212121',
                                   width=80, height=80)
        print(0 + column_buff)
        image_label.grid(row=(index - rage_of_the_usa), column=(0 + column_buff))
        text_label = ctk.CTkLabel(
            self.top_container,
            text=f"{self.char_name}\n{self.char_series}",
            height=80,
            width=80
        )
        text_label.grid(row=(index - rage_of_the_usa), column=(1 + column_buff))

# Всплывающая подсказка
class AutoCompleteEntry(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._escape_pressed = False
        db_path = "characters.db"
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        # Получаем данные из БД
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM characters")
            self.values = [row[0] for row in cursor.fetchall()]
            connection.close()
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            self.values = []

        # Поле ввода
        self.entry = ctk.CTkEntry(self, width=400,
                                   placeholder_text='Введите имя персонажа...',
                                   text_color='white', bg_color='#212121',
                                   font=self.text_1_font)
        self.entry.pack(fill="x", padx=5, pady=5)

        self.entry.bind("<Escape>", self.on_escape)

        self.entry.bind("<Escape>", lambda e: self.hide_listbox())
        # Контейнер для списка предложений
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            width=400,
            height=150,
            corner_radius=8,
            fg_color="#2B2B2B"
        )
        self.list_frame.pack_forget()

        # Храним кнопки списка
        self.suggestion_buttons = []

        # Связываем события
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<FocusOut>", self.hide_listbox)
        self.entry.bind("<Down>", self.show_listbox)

    def on_escape(self, event):
        self.hide_listbox()
        self._escape_pressed = True
        self.after(100, lambda: setattr(self, '_escape_pressed', False))

    def on_key_release(self, event):
        if self._escape_pressed:
            return

            # Скрытие списка при нажатии стрелок
        if event.keysym in ('Up', 'Down'):
            self.hide_listbox()
            return

        text = self.entry.get().lower()
        if not text:
            self.hide_listbox()
            return

        matches = [
            item for item in self.values
            if text in item.lower()
        ]
        if matches:
            self.show_listbox(matches)
        else:
            self.hide_listbox()

    def show_listbox(self, matches=None):
        # Очищаем старые кнопки
        for btn in self.suggestion_buttons:
            btn.destroy()
        self.suggestion_buttons.clear()

        if matches:
            # Создаём кнопки для каждого варианта
            for item in matches:
                btn = ctk.CTkButton(
                    self.list_frame,
                    text=item,
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("#D3D3D3", "#404040"),
            anchor="w",
            command=lambda x=item: self.insert_suggestion(x)
        )
                btn.pack(fill="x", padx=2, pady=1)
                self.suggestion_buttons.append(btn)

            # Показываем контейнер
            self.list_frame.pack(
                fill="x",
                padx=5,
                pady=(0, 5)
            )
        else:
            self.hide_listbox()

    def hide_listbox(self, event=None):
        self.list_frame.pack_forget()

    def insert_suggestion(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self.hide_listbox()

    def get(self):
        return self.entry.get()

    def delete(self, first, last=None):
        self.entry.delete(first, last)



class LevelClassic(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.text_2_font = ctk.CTkFont(family="Impact", size=25)
        self.description = ctk.CTkFont(family="Impact", size=20)
        self.features = ctk.CTkFont(family="Impact", size=13)
        self.toplevel_window = None
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

        ctk.CTkLabel(self.scrollable_frame, text=f"Фото\nперсонажа",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=0, column=0)
        ctk.CTkLabel(self.scrollable_frame, text=f"Сериал",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=1)
        ctk.CTkLabel(self.scrollable_frame, text=f"Пол",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=2)
        ctk.CTkLabel(self.scrollable_frame, text=f"Роль",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=3)
        ctk.CTkLabel(self.scrollable_frame, text=f"Рост",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=4)
        ctk.CTkLabel(self.scrollable_frame, text=f"Семья",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=5)
        ctk.CTkLabel(self.scrollable_frame, text=f"Профессия",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=6)
        ctk.CTkLabel(self.scrollable_frame, text=f"Первое\nпоявление",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=7)
        ctk.CTkLabel(self.scrollable_frame, text=f"Семейное\nположение",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=self.widget_counter, column=8)

    def widgets(self):
        self.true_char_choice()

        self.top_container = ctk.CTkFrame(self, fg_color='#212121')
        self.top_container.pack(pady=(0, 0))
        self.button_exit = ctk.CTkButton(self, text='X', command=lambda: self.controller.show_frame("MainMenu"),
                                         text_color='black',
                                         fg_color="#F10C21", hover_color="#C90A1C",
                                         width=50, height=50,
                                         font=self.text_2_font, corner_radius=10)
        self.button_exit.place(x=730, y=20)
        self.button_chars = ctk.CTkButton(self, text='?', command=lambda: AllChars(self, self), text_color='black',
                                          fg_color='#ffdfa7', hover_color='#ae6f12',
                                          width=50, height=50,
                                          font=self.text_2_font, corner_radius=10)
        self.button_chars.place(x=730, y=80)

        self.title = ctk.CTkLabel(self.top_container, text="Угадывание персонажа по его\nХАРАКТЕРИСТИКАМ",
                                  text_color='white', font=self.text_1_font)
        self.title.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        self.entry_name = AutoCompleteEntry(self.top_container,)
        self.entry_name.grid(row=2, column=0, pady=20)

        self.button_accept = ctk.CTkButton(self.top_container, text='Проверить догадку',
                                           command=self.add_widget, fg_color="#007AFF",
                                           hover_color="#0064D1", bg_color='#212121', width=400,
                                           height=30, font=self.text_2_font)
        self.button_accept.grid(row=3, column=0)
        self.error_msg = ctk.CTkLabel(self.top_container, text="",
                                      text_color='white', font=self.text_1_font)
        self.error_msg.grid(row=4, column=0, sticky="nsew", pady=(10, 0))

        # self.add_scrollable_frame()

        self.widget_counter = 0

    def add_widget(self):
        text = self.entry_name.get()
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT id, name, series, gender, role, height, membership, profession, first_date, family_statuus FROM characters WHERE name = '{text}'")
            nigga = cursor.fetchall()
            char_id = nigga[0][0]
            char_name = nigga[0][1]
            char_series = nigga[0][2]
            char_gender = nigga[0][3]
            char_role = nigga[0][4]
            char_height = nigga[0][5]
            char_membership = nigga[0][6]
            char_profession = nigga[0][7]
            char_first_date = nigga[0][8]
            char_family_statuus = nigga[0][9]
            print(char_id)
            print(char_name)
            self.widget_counter += 1

            if text != self.true_char_name:
                image = Image.open(f"characters/{char_id}.png")
                photo = ctk.CTkImage(image, size=(80, 80))
                image_label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="", bg_color='#212121',
                                           width=80, height=80)
                image_label.grid(row=self.widget_counter, column=0)
                print(self.true_char_name)
                series_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_series}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                series_label.grid(row=self.widget_counter, column=1)

                gender_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_gender}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                gender_label.grid(row=self.widget_counter, column=2)

                role_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_role}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                role_label.grid(row=self.widget_counter, column=3)

                height_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_height}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                height_label.grid(row=self.widget_counter, column=4)

                membership_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_membership}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                membership_label.grid(row=self.widget_counter, column=5)

                profession_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_profession}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                profession_label.grid(row=self.widget_counter, column=6)

                date_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_first_date}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                date_label.grid(row=self.widget_counter, column=7)

                family_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_family_statuus}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                family_label.grid(row=self.widget_counter, column=8)

                if char_series != self.true_char_series:
                    series_label.configure(fg_color="red")
                if char_gender != self.true_char_gender:
                    gender_label.configure(fg_color="red")
                current_gender = gender_label.cget("text")
                if current_gender == "М":
                    gender_label.configure(text="Мужской")
                elif current_gender == "Ж":
                    gender_label.configure(text="Женский")
                if (self.true_char_role == "Главная" and (
                        char_role == "Основная" or char_role == "Втор.")) or (
                        self.true_char_role == "Основная" and char_role == "Втор."):
                    role_label.configure(fg_color="red", text=f"{char_role} ⬆")
                elif (self.true_char_role == "Втор." and (
                        char_role == "Основная" or char_role == "Главная")) or (
                        self.true_char_role == "Основная" and char_role == "Главная"):
                    role_label.configure(fg_color="red", text=f"{char_role} ⬇")

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
                if char_height > self.true_char_height:
                    new_text = height_label.cget("text") + " ⬇"
                    height_label.configure(text=new_text)
                    height_label.configure(fg_color="red")
                elif char_height < self.true_char_height:
                    new_text = height_label.cget("text") + " ⬆"
                    height_label.configure(text=new_text)
                    height_label.configure(fg_color="red")

                if char_membership != self.true_char_membership:
                    membership_label.configure(fg_color="red")
                if char_profession != self.true_char_profession:
                    profession_label.configure(fg_color="red")

                if char_first_date > self.true_char_first_date:
                    date_label.configure(fg_color="red", text=f"{char_first_date} ⬇")
                elif char_first_date < self.true_char_first_date:
                    date_label.configure(fg_color="red", text=f"{char_first_date} ⬆")

                if char_family_statuus == 1:
                    if char_gender == "М":
                        family_label.configure(text="Женат")
                    else:
                        family_label.configure(text="Замужем")
                else:
                    if char_gender == "М":
                        family_label.configure(text="Не женат")
                    else:
                        family_label.configure(text="Не замужем")
                if char_family_statuus != self.true_char_family_status:
                    family_label.configure(fg_color="red")

            else:
                self.true_char_choice()
                # self.scrollable_frame.destroy()
                self.scrollable_frame.pack_forget()
                self.entry_name.delete(0, "end")
                self.controller.show_frame("Results", self.widget_counter)
                self.widget_counter = 0

        except Exception as e:
            print(e)
            self.error_msg.configure(text='Введите верное имя (можно подглядеть по кнопке "?")')
            self.entry_name.delete(0, "end")


class LevelQuote(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.header_font = ctk.CTkFont(family="Impact", size=40)
        self.text_1_font = ctk.CTkFont(family="Impact", size=30)
        self.text_2_font = ctk.CTkFont(family="Impact", size=25)
        self.description = ctk.CTkFont(family="Impact", size=20)
        self.features = ctk.CTkFont(family="Impact", size=13)
        self.toplevel_window = None
        self.widgets()

    def true_char_choice(self):
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        rcount = random.randint(1, count)

        cursor.execute(
            f"SELECT id, name, series, quote FROM characters WHERE id = {rcount}")
        self.true_char = cursor.fetchall()
        print(self.true_char)
        print(self.true_char[0])
        self.true_char_id = self.true_char[0][0]
        self.true_char_name = self.true_char[0][1]
        self.true_char_series = self.true_char[0][2]
        self.true_char_quote = self.true_char[0][3]

    def add_scrollable_frame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=650, height=300)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both")

        ctk.CTkLabel(self.scrollable_frame, text=f"Фото\nперсонажа",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=80).grid(row=0, column=0)
        ctk.CTkLabel(self.scrollable_frame, text=f"Имя",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=270).grid(row=self.widget_counter, column=1)
        ctk.CTkLabel(self.scrollable_frame, text=f"Сериал",
                     font=self.features, fg_color="#007AFF", corner_radius=6,
                     height=40, width=270).grid(row=self.widget_counter, column=2)

    def widgets(self):
        self.true_char_choice()

        self.top_container = ctk.CTkFrame(self, fg_color='#212121')
        self.top_container.pack(pady=(0, 0))
        self.button_exit = ctk.CTkButton(self, text='X', command=lambda: self.controller.show_frame("MainMenu"), text_color='black',
                                         fg_color="#F10C21", hover_color="#C90A1C",
                                         width=50, height=50,
                                         font=self.text_2_font, corner_radius=10)
        self.button_exit.place(x=730, y=20)
        self.button_chars = ctk.CTkButton(self, text='?', command=lambda: AllChars(self, self), text_color='black',
                                          fg_color='#ffdfa7', hover_color='#ae6f12',
                                          width=50, height=50,
                                          font=self.text_2_font, corner_radius=10)
        self.button_chars.place(x=730, y=80)


        self.title = ctk.CTkLabel(self.top_container, text="Угадай персонажа по цитате:",
                                  text_color='white', font=self.text_2_font)
        self.title.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.title = ctk.CTkLabel(self.top_container, text=self.true_char_quote,
                                  text_color='gold', font=self.text_1_font)
        self.title.grid(row=2, column=0, sticky="nsew", pady=(10, 0))

        self.entry_name = ctk.CTkEntry(self.top_container, width=400, placeholder_text='Введите имя персонажа...',
                                       text_color='white', bg_color='#212121', font=self.text_2_font)
        self.entry_name.grid(row=3, column=0, pady=20)

        self.button_accept = ctk.CTkButton(self.top_container, text='Проверить догадку',
                                           command=self.add_widget, fg_color="#007AFF",
                                           hover_color="#0064D1", bg_color='#212121', width=400,
                                           height=30, font=self.text_2_font)
        self.button_accept.grid(row=4, column=0)
        self.error_msg = ctk.CTkLabel(self.top_container, text="",
                                      text_color='white', font=self.text_2_font)
        self.error_msg.grid(row=5, column=0, sticky="nsew", pady=(10, 0))

        # self.add_scrollable_frame()

        self.widget_counter = 0

    def add_widget(self):
        text = self.entry_name.get()
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT id, name, series FROM characters WHERE name = '{text}'")
            nigga = cursor.fetchall()
            char_id = nigga[0][0]
            char_name = nigga[0][1]
            char_series = nigga[0][2]
            print(char_id)
            print(char_name)
            self.widget_counter += 1
            if self.widget_counter == 5:
                self.button_sound = ctk.CTkButton(self.top_container, text='Звуковая подсказка', fg_color="#007AFF",
                                                  # command=lambda: playsound('sfx/11.mp3'),
                                                  hover_color="#0064D1", bg_color='#212121', width=400,
                                                  height=30, font=self.text_2_font)
                self.button_sound.grid(row=6, column=0)

            if text != self.true_char_name:
                image = Image.open(f"characters/{char_id}.png")
                photo = ctk.CTkImage(image, size=(80, 80))
                image_label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="", bg_color='#212121',
                                           width=80, height=80)
                image_label.grid(row=self.widget_counter, column=0)

                name_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_name}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=80
                )
                name_label.grid(row=self.widget_counter, column=1)
                print(self.true_char_name)
                series_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{char_series}",
                    font=self.features,
                    fg_color="green",
                    corner_radius=6,
                    height=80,
                    width=270
                )
                series_label.grid(row=self.widget_counter, column=2)

                if char_series != self.true_char_series:
                    series_label.configure(fg_color="red")
                if char_name != self.true_char_name:
                    name_label.configure(fg_color="red")

            else:
                self.true_char_choice()
                # self.scrollable_frame.destroy()
                self.scrollable_frame.pack_forget()
                self.entry_name.delete(0, "end")
                self.controller.show_frame("Results", self.widget_counter)
                self.widget_counter = 0

        except Exception as e:
            print(e)
            self.error_msg.configure(text='Введите верное имя (можно подглядеть по кнопке "?")')
            self.entry_name.delete(0, "end")


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

        self.photo = ctk.CTkImage(Image.open("assets/final.png"), size=(625, 350))
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
        self.result.configure(
            text=f"Угадано с {attempts} попытки!"
        )


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
