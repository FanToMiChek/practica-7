import tkinter as tk
from tkinter import ttk

from game import CircuitGame


class SettingsApp:
    """
    Окно Tkinter с двумя вкладками (Задача №1):
      1) «Настройки» — ползунок Scale для толщины курсора-проводника (5..20 px)
      2) «Игра» — запуск игры Pygame с выбранной толщиной заряда
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Электрическая цепь — Настройки")
        self.root.geometry("380x220")
        self.root.resizable(False, False)

        self.thickness_var = tk.IntVar(value=10)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_settings = ttk.Frame(notebook)
        self.tab_game = ttk.Frame(notebook)

        notebook.add(self.tab_settings, text="Настройки")
        notebook.add(self.tab_game, text="Игра")

        self._build_settings_tab()
        self._build_game_tab()

    def _build_settings_tab(self):
        label = ttk.Label(self.tab_settings, text="Толщина курсора-проводника (px):")
        label.pack(pady=(20, 5))

        scale = ttk.Scale(
            self.tab_settings,
            from_=5, to=20,
            orient="horizontal",
            variable=self.thickness_var,
            command=self._on_scale_move,
            length=250,
        )
        scale.pack(pady=5)

        self.value_label = ttk.Label(
            self.tab_settings, text=f"Текущее значение: {self.thickness_var.get()} px"
        )
        self.value_label.pack(pady=5)

    def _on_scale_move(self, value):
        rounded = round(float(value))
        self.thickness_var.set(rounded)
        self.value_label.config(text=f"Текущее значение: {rounded} px")

    def _build_game_tab(self):
        info = ttk.Label(
            self.tab_game,
            text="Проведите заряд от старта к финишу,\nне касаясь стенок провода.",
            justify="center",
        )
        info.pack(pady=(25, 15))

        start_btn = ttk.Button(self.tab_game, text="Играть", command=self._launch_game)
        start_btn.pack(pady=5)

    def _launch_game(self):
        thickness = self.thickness_var.get()
        self.root.withdraw()  # прячем окно настроек на время игры
        game = CircuitGame(thickness=thickness)
        game.run()
        self.root.deiconify()  # возвращаем окно настроек после выхода из игры


def main():
    root = tk.Tk()
    SettingsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()