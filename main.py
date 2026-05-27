import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()

        self.setup_ui()

    def setup_ui(self):
        # Форма ввода
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="w")
        self.type_entry = ttk.Entry(input_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w")
        self.duration_entry = ttk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Button(input_frame, text="Добавить тренировку",
                 command=self.add_training).grid(row=3, column=0, columnspan=2, pady=5)

        # Фильтры
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация")
        filter_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(filter_frame, text="Тип:").grid(row=0, column=0, sticky="w")
        self.filter_type = ttk.Combobox(filter_frame, values=["Все", "Кардио", "Силовая", "Йога", "Бег"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="Дата:").grid(row=0, column=2, sticky="w")
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(filter_frame, text="Применить фильтр",
                 command=self.apply_filter).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить",
                 command=self.reset_filter).grid(row=0, column=5, padx=5)

        # Таблица
        columns = ("Дата", "Тип", "Длительность")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Обновление таблицы
        self.update_table()

    def validate_input(self):
        """Проверка корректности ввода"""
        try:
            date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
            return False

        try:
            duration = float(self.duration_entry.get())
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        if not self.type_entry.get():
            messagebox.showerror("Ошибка", "Тип тренировки не может быть пустым")
            return False

        return True

    def add_training(self):
        """Добавление тренировки"""
        if self.validate_input():
            training = {
                "date": self.date_entry.get(),
                "type": self.type_entry.get(),
                "duration": float(self.duration_entry.get())
            }
            self.trainings.append(training)
            self.save_data()
            self.update_table()
            # Очистка полей ввода
            self.date_entry.delete(0, tk.END)
            self.type_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)

    def update_table(self, data=None):
        """Обновление таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_data = data if data is not None else self.trainings
        for training in display_data:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']} мин"
            ))

    def apply_filter(self):
        """Применение фильтров"""
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        filtered = self.trainings

        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]

        if filter_date:
            filtered = [t for t in filtered if filter_date in t["date"]]

        self.update_table(filtered)

    def reset_filter(self):
        """Сброс фильтров"""
        self.filter_type.set("Все")
        self.filter_date.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        """Сохранение данных в JSON"""
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, indent=2, ensure_ascii=False)

    def load_data(self):
        """Загрузка данных из JSON"""
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
