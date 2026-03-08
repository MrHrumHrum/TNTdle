import customtkinter as ctk
import sqlite3



class AutoCompleteEntry(ctk.CTkFrame):
    def __init__(self, parent, v, **kwargs):
        super().__init__(parent, **kwargs)
        connection = sqlite3.connect("characters.db")
        cursor = connection.cursor()

        cursor.execute(
            f"SELECT name FROM characters")
        self.values = [row[0] for row in cursor.fetchall()]
        print(self.values)
        self.entry = ctk.CTkEntry(self, width=400, placeholder_text='Введите имя персонажа...',
                                       text_color='white', bg_color='#212121')
        self.entry.pack(fill="x", padx=5, pady=(5, 0))

        # Контейнер для списка предложений (прокручиваемый)
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            width=self.entry.cget("width"),
            height=100,
            corner_radius=8
        )
        self.list_frame.pack_forget()  # Скрываем изначально

        # Храним кнопки списка для управления
        self.suggestion_buttons = []

        # Связываем события
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<FocusOut>", self.hide_listbox)
        self.entry.bind("<Down>", self.show_listbox)

    def on_key_release(self, event):
        text = self.entry.get().lower()

        if not text:
            self.hide_listbox()
            return

        # Фильтруем подходящие варианты
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

    def insert(self, index, string):
        self.entry.insert(index, string)

    def delete(self, first, last=None):
        self.entry.delete(first, last)


# Пример использования
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("AutoComplete Entry")
    app.geometry("400x300")

    suggestions = [
        "Москва",
        "Санкт-Петербург",
        "Новосибирск",
        "Екатеринбург",
        "Казань",
        "Нижний Новгород",
        "Челябинск",
        "Самара",
        "Омск",
        "Ростов-на-Дону"
    ]

    auto_entry = AutoCompleteEntry(app, v = suggestions)
    print(auto_entry)
    auto_entry.pack(pady=20, padx=20, fill="x")

    app.mainloop()
