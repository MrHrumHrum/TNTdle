import random
import sqlite3
from PIL import Image, ImageTk
from linecache import cache

import customtkinter as ctk

# Настройка внешнего вида
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        global lvl1_list
        lvl1_list = []
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM characters")
        count = cursor.fetchone()[0]
        rcount = random.randint(1, count)
        # rcount = random.randint(1, 20)

        cursor.execute(
            f"SELECT id, name, series, gender, role, height, membership, profession, first_date, family_statuus FROM characters WHERE id = {rcount}")
        # true_char = cursor.fetchall()
        # self.true_char = true_char[0][0]
        # print(true_char)
        # print(true_char[0])
        # print(true_char[0][0])
        # print(true_char)
        # print(true_char[0])
        # print(true_char[0][1])
        true_char = cursor.fetchall()
        print(true_char)
        print(true_char[0])
        self.true_char_id = true_char[0][0]
        self.true_char_name = true_char[0][1]
        self.true_char_series = true_char[0][2]
        self.true_char_gender = true_char[0][3]
        self.true_char_role = true_char[0][4]
        self.true_char_height = true_char[0][5]
        self.true_char_membership = true_char[0][6]
        self.true_char_profession = true_char[0][7]
        self.true_char_first_date = true_char[0][8]
        self.true_char_family_status = true_char[0][9]

        self.geometry("400x400")
        self.title("Динамическое добавление виджетов")

        # Кнопка добавления
        self.btn_add = ctk.CTkButton(self, text="Добавить виджет", command=self.add_widget)
        self.btn_add.pack(pady=10)
        self.entry_name = ctk.CTkEntry(self,
                                       text_color='black', bg_color='#212121')
        self.entry_name.pack(pady=10)

        # Контейнер с прокруткой для новых виджетов
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=350, height=250)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

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
            self.char_first_date = nigga[0][6]
            self.char_family_statuus = nigga[0][7]
            print(self.char_id)
            print(self.char_name)
            self.widget_counter += 1

            if text != self.true_char_name:
                image = Image.open(f"characters/{self.char_id}.png")
                photo = ctk.CTkImage(image, size=(80, 80))
                image_label = ctk.CTkLabel(self.scrollable_frame, image=photo, text="", bg_color='#212121', width=80,
                                           height=80)
                image_label.grid(row=self.widget_counter, column=0)

                name_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Виджет №{self.true_char_name}",
                    fg_color="gray",
                    corner_radius=6
                )
                # Укладываем виджет один за другим
                name_label.grid(row=self.widget_counter, column=1)

                name_label2 = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_name}",
                    fg_color="gray",
                    corner_radius=6
                )
                # Укладываем виджет один за другим
                name_label2.grid(row=self.widget_counter, column=2)

                series_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_series}",
                    fg_color="green",
                    corner_radius=6
                )
                series_label.grid(row=self.widget_counter, column=3)

                gender_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_gender}",
                    fg_color="green",
                    corner_radius=6
                )
                gender_label.grid(row=self.widget_counter, column=4)

                role_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_role}",
                    fg_color="green",
                    corner_radius=6
                )
                role_label.grid(row=self.widget_counter, column=5)

                height_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_height}",
                    fg_color="green",
                    corner_radius=6
                )
                height_label.grid(row=self.widget_counter, column=6)

                membership_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_membership}",
                    fg_color="green",
                    corner_radius=6
                )
                membership_label.grid(row=self.widget_counter, column=7)

                profession_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_profession}",
                    fg_color="green",
                    corner_radius=6
                )
                profession_label.grid(row=self.widget_counter, column=8)

                date_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_first_date}",
                    fg_color="green",
                    corner_radius=6
                )
                date_label.grid(row=self.widget_counter, column=9)

                family_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"{self.char_family_statuus}",
                    fg_color="green",
                    corner_radius=6
                )
                family_label.grid(row=self.widget_counter, column=10)

                if self.char_series != self.true_char_series:
                    series_label.configure(fg_color="red")
                if self.char_gender != self.true_char_gender:
                    gender_label.configure(fg_color="red")
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
                    height_label.configure(text="Чрезвычайно низкий")
                elif current_height == 2:
                    height_label.configure(text="Низкий")
                elif current_height == 3:
                    height_label.configure(text="Средний")
                elif current_height == 4:
                    height_label.configure(text="Высокий")
                elif current_height == 5:
                    height_label.configure(text="Гигант из клещ рояля")
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
                new_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Виджет №ПОБЕДА",
                    fg_color="gray",
                    corner_radius=6
                )
                # Укладываем виджет один за другим
                new_label.grid(row=self.widget_counter, column=0)
                new_label2 = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Виджет №{self.widget_counter}",
                    fg_color="gray",
                    corner_radius=6
                )
                # Укладываем виджет один за другим
                new_label2.grid(row=self.widget_counter, column=1)
        except:
            self.entry_name.delete(0, "end")  # Удаляем от 0 до конца
            self.entry_name.insert(0, "Новый текст")  # Вставляем новый

        # lvl1_list = []
        # connection = sqlite3.connect("characters.db")
        # cursor = connection.cursor()
        #
        # cursor.execute("SELECT COUNT(*) FROM characters")
        # count = cursor.fetchone()[0]
        # rcount = random.randint(1, count)
        #
        # cursor.execute(
        #     f"SELECT name, series, gender, role, height, membership, profession, first_date, family_statuus FROM characters WHERE id = {rcount}")
        # true_char = cursor.fetchall()
        # Создаем новый виджет внутри скролл-фрейма


if __name__ == "__main__":
    app = App()
    app.mainloop()
