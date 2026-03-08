import customtkinter as ctk

# Настройка внешнего вида
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title("Динамическое добавление виджетов")

        # Кнопка добавления
        self.btn_add = ctk.CTkButton(self, text="Добавить виджет", command=self.add_widget)
        self.btn_add.pack(pady=10)

        # Контейнер с прокруткой для новых виджетов
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=350, height=250)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.widget_counter = 0

    def add_widget(self):
        self.widget_counter += 1
        # Создаем новый виджет внутри скролл-фрейма
        new_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=f"Виджет №{self.widget_counter}",
            fg_color="gray",
            corner_radius=6
        )
        # Укладываем виджет один за другим
        new_label.pack(pady=5, padx=5, fill="x")

if __name__ == "__main__":
    app = App()
    app.mainloop()
