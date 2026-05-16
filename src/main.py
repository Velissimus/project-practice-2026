import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")


class TextEditor:

    def __init__(self, root):
        self.root = root
        root.title("Nebula Notes")
        root.geometry("1200x800")

        self.dark_theme = True
        self.current_file = None

        # ФОНЫ

        self.dark_bg = ImageTk.PhotoImage(
            Image.open("assets/milkyway.jpg").resize((1400, 900))
        )

        self.light_bg = ImageTk.PhotoImage(
            Image.open("assets/sky.jpg").resize((1400, 900))
        )

        self.background = tk.Label(
            root,
            image=self.dark_bg,
            border=0
        )

        self.background.place(
            x=0, y=0,
            relwidth=1,
            relheight=1
        )

        # ПАНЕЛЬ

        self.toolbar = ctk.CTkFrame(
            root,
            fg_color="#222225",
            corner_radius=0,
            height=75,
            border_width=0
        )

        self.toolbar.pack(
            fill="x",
            padx=50,
            pady=35
        )

        self.toolbar.pack_propagate(False)

        # Внутренний контейнер для отступов
        self.toolbar_inner = ctk.CTkFrame(
            self.toolbar,
            fg_color="transparent"
        )

        self.toolbar_inner.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )


        # ФАЙЛ МЕНЮ


        self.file_menu = ctk.CTkOptionMenu(
            self.toolbar_inner,
            values=[
                "Файл",
                "Создать",
                "Открыть",
                "Сохранить",
                "Сохранить как",
                "Выход"
            ],
            command=self.handle_file,
            width=130,
            height=45,
            corner_radius=15,
            fg_color="#2f2f34",
            button_color="#2f2f34",
            button_hover_color="#4a4a52",
            text_color="white"
        )

        self.file_menu.set("Файл")
        self.file_menu.pack(side="left", padx=10)


        # КНОПКИ


        self.buttons = []

        buttons_config = [
            ("𝐁", self.bold_text, "Bold"),
            ("𝘐", self.italic_text, "Italic"),
            ("U̲", self.underline_text, "Underline"),
            ("🎨", self.change_color, "Text Color"),
            ("🖍", self.highlight_text, "Highlight"),
            ("🌙", self.toggle_theme, "Theme")
        ]

        for text, cmd, tooltip in buttons_config:
            btn = ctk.CTkButton(
                self.toolbar_inner,
                text=text,
                command=cmd,
                width=60,
                height=45,
                corner_radius=15,
                fg_color="#2f2f34",
                hover_color="#4a4a52",
                text_color="white",
                font=("Arial", 16, "bold")
            )

            btn.pack(side="left", padx=8)
            self.buttons.append(btn)


        # ОБЛАСТЬ ТЕКСТА


        self.editor = ctk.CTkFrame(
            root,
            fg_color="#222225",
            corner_radius=0,
            border_width=0
        )

        self.editor.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=(0, 40)
        )

        # Контейнер для текста
        self.text_container = ctk.CTkFrame(
            self.editor,
            fg_color="transparent",
            corner_radius=0
        )

        self.text_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # Текстовое поле
        self.text = tk.Text(
            self.text_container,
            bg="#222225",
            fg="white",
            insertbackground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            undo=True,
            font=("Consolas", 14),
            padx=25,
            pady=25,
            wrap="word",
            selectbackground="#4a4a52",
            selectforeground="white"
        )

        self.text.pack(fill="both", expand=True)
        self.text.bind("<KeyRelease>", self.check_empty)


        # ПУСТОЙ ЭКРАН


        self.empty_img = ImageTk.PhotoImage(
            Image.open("assets/cat.png").resize((360, 180))
        )

        self.empty_label = tk.Label(
            self.editor,
            image=self.empty_img,
            text="\n\nНачните писать...",
            compound="top",
            font=("Arial", 18),
            fg="#888888",
            bg="#222225",
            border=0
        )

        self.empty_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )


        # СТАТУС


        self.status = ctk.CTkLabel(
            root,
            text="Готово",
            height=35,
            corner_radius=0,
            fg_color="#222225",
            text_color="white"
        )

        self.status.pack(
            fill="x",
            padx=50,
            pady=(0, 25)
        )


        # ГОРЯЧИЕ КЛАВИШИ


        root.bind("<Control-s>", lambda e: self.save_file())
        root.bind("<Control-o>", lambda e: self.open_file())
        root.bind("<Control-n>", lambda e: self.new_file())
        root.bind("<Control-b>", lambda e: self.bold_text())
        root.bind("<Control-i>", lambda e: self.italic_text())
        root.bind("<Control-u>", lambda e: self.underline_text())


    # ФОРМАТИРОВАНИЕ


    def get_selection(self):
        try:
            return self.text.index("sel.first"), self.text.index("sel.last")
        except:
            return None, None

    def bold_text(self):
        s, e = self.get_selection()
        if s:
            self.text.tag_add("bold", s, e)
            self.text.tag_config("bold", font=("Consolas", 14, "bold"))

    def italic_text(self):
        s, e = self.get_selection()
        if s:
            self.text.tag_add("italic", s, e)
            self.text.tag_config("italic", font=("Consolas", 14, "italic"))

    def underline_text(self):
        s, e = self.get_selection()
        if s:
            self.text.tag_add("underline", s, e)
            self.text.tag_config("underline", underline=True)

    def highlight_text(self):
        s, e = self.get_selection()
        if s:
            self.text.tag_add("highlight", s, e)
            self.text.tag_config(
                "highlight",
                background="#FFD54F",
                foreground="#000000"
            )

    def change_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста")[1]
        s, e = self.get_selection()

        if color and s:
            tag = f"color_{color.replace('#', '')}"
            self.text.tag_add(tag, s, e)
            self.text.tag_config(tag, foreground=color)


    # ПУСТОЙ ЭКРАН


    def check_empty(self, event=None):
        content = self.text.get("1.0", "end-1c").strip()

        if content:
            self.empty_label.place_forget()
        else:
            self.empty_label.place(relx=0.5, rely=0.5, anchor="center")


    # ПЕРЕКЛЮЧЕНИЕ ТЕМЫ


    def toggle_theme(self):
        self.dark_theme = not self.dark_theme

        if self.dark_theme:
            # Тёмная тема
            bg = "#222225"
            fg = "white"
            img = self.dark_bg

            btn_fg = "#2f2f34"
            btn_hover = "#4a4a52"
            btn_text = "white"

            status_text = "white"
            empty_fg = "#888888"

        else:
            # Светлая тема
            bg = "#f5f5f5"
            fg = "#000000"
            img = self.light_bg

            btn_fg = "#e0e0e0"
            btn_hover = "#c8c8c8"
            btn_text = "#000000"

            status_text = "#000000"
            empty_fg = "#666666"

        # Применение фона
        self.background.configure(image=img)

        # Редактор
        self.editor.configure(fg_color=bg)
        self.text.configure(
            bg=bg,
            fg=fg,
            insertbackground=fg,
            selectbackground="#4a4a52" if self.dark_theme else "#b8d4ff"
        )
        self.empty_label.configure(bg=bg, fg=empty_fg)

        # Статус
        self.status.configure(fg_color=bg, text_color=status_text)

        # Панель инструментов
        self.toolbar.configure(fg_color=bg)

        # Меню файлов
        self.file_menu.configure(
            fg_color=btn_fg,
            button_color=btn_fg,
            button_hover_color=btn_hover,
            text_color=btn_text
        )

        # Все кнопки
        for btn in self.buttons:
            btn.configure(
                fg_color=btn_fg,
                hover_color=btn_hover,
                text_color=btn_text
            )


    # РАБОТА С ФАЙЛАМИ


    def handle_file(self, choice):
        if choice == "Создать":
            self.new_file()
        elif choice == "Открыть":
            self.open_file()
        elif choice == "Сохранить":
            self.save_file()
        elif choice == "Сохранить как":
            self.save_as()
        elif choice == "Выход":
            self.root.quit()

        self.file_menu.set("Файл")

    def new_file(self):
        self.text.delete("1.0", tk.END)
        self.current_file = None
        self.check_empty()
        self.status.configure(text="Новый файл")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )

        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()

                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", content)
                self.current_file = path
                self.check_empty()

                import os
                self.status.configure(text=f"Открыт: {os.path.basename(path)}")

            except Exception as e:
                self.status.configure(text=f"Ошибка: {str(e)}")

    def save_file(self):
        if not self.current_file:
            self.save_as()
            return

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))

            import os
            self.status.configure(text=f"✓ Сохранено: {os.path.basename(self.current_file)}")

            # Возврат к "Готово" через 3 секунды
            self.root.after(3000, lambda: self.status.configure(text="Готово"))

        except Exception as e:
            self.status.configure(text=f"Ошибка сохранения: {str(e)}")

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )

        if path:
            self.current_file = path
            self.save_file()


# ЗАПУСК ПРИЛОЖЕНИЯ


if __name__ == "__main__":
    root = ctk.CTk()
    app = TextEditor(root)
    root.mainloop()
