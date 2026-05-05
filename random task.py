import tkinter as tk
from tkinter import messagebox
import json
import random

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("800x600")
        
        self.tasks_file = "tasks.json"
        self.history_file = "task_history.json"
        
        # Predefined tasks
        self.tasks = [
            {"task": "Прочитать главу книги", "Тип": "Учеба"},
            {"task": "Сделай 10 отжиманий", "Тип": "Спорт"},
            {"task": "Написать отзыв о коде", "Тип": "Работа"},
            {"task": "Выучите новое слово", "Тип": "Учеба"},
            {"task": "Прогуляйтесь 15 минут", "Тип": "Спорт"},
            {"task": "Проверьте письма", "Тип": "Работа"},
            {"task": "Решить задачу по программированию", "Тип": "Учеба"},
            {"task": "Потянитесь в течение 5 минут", "Тип": "Спорт"},
            {"task": "Спланировать расписание на завтра", "Тип": "Работа"},
            {"task": "Медитируйте 5 минут", "Тип": "Здоровье"}
        ]
        
        self.history = self.load_history()
        self.setup_ui()
        self.refresh_history()
        
    def setup_ui(self):
        # Task display
        self.task_frame = tk.LabelFrame(self.root, text="Текущая задача", font=("Arial", 10, "bold"))
        self.task_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.task_text = tk.Text(self.task_frame, height=4, width=60, font=("Arial", 14))
        self.task_text.pack(padx=10, pady=10)
        
        # Generate button
        tk.Button(self.root, text="Сгенерировать случайное задание", command=self.generate_task, 
                  bg="lightblue", font=("Arial", 12)).pack(pady=10)
        
        # Add new task frame
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу")
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(add_frame, text="Описание задания:").grid(row=0, column=0, padx=5, pady=5)
        self.new_task_text = tk.Entry(add_frame, width=40)
        self.new_task_text.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Тип задания:").grid(row=0, column=2, padx=5, pady=5)
        self.new_type_var = tk.StringVar(value="Учеба")
        types = ["Учеба", "Спорт", "Работа", "Здоровье", "Личный"]
        self.type_menu = tk.OptionMenu(add_frame, self.new_type_var, *types)
        self.type_menu.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(add_frame, text="Добавить задачу", command=self.add_task).grid(row=0, column=4, padx=10, pady=5)
        
        # Filter frame
        filter_frame = tk.LabelFrame(self.root, text="История фильтров")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(filter_frame, text="Фильтровать по типу:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type = tk.StringVar(value="Все")
        filter_types = ["Все", "Учеба", "Спорт", "Работа", "Здоровье", "Личный"]
        tk.OptionMenu(filter_frame, self.filter_type, *filter_types, command=self.refresh_history).grid(row=0, column=1, padx=5)
        
        tk.Button(filter_frame, text="Показать все", command=self.clear_filter).grid(row=0, column=2, padx=10, pady=5)
        
        # History display
        history_frame = tk.LabelFrame(self.root, text="История задач")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollable listbox
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=10)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Clear history button
        tk.Button(self.root, text="Очистить историю", command=self.clear_history).pack(pady=5)
        
    def generate_task(self):
        if self.tasks:
            task = random.choice(self.tasks)
            self.task_text.delete(1.0, tk.END)
            self.task_text.insert(tk.END, f"{task['task']}\n\nType: {task['Тип']}")
            
            # Add to history
            self.history.append(task)
            self.save_history()
            self.refresh_history()
        else:
            messagebox.showwarning("Нет задач. Задачи отсутствуют. Пожалуйста, добавьте несколько задач.")
            
    def add_task(self):
        task_desc = self.new_task_text.get().strip()
        
        if not task_desc:
            messagebox.showwarning("Ошибка ввода", "Описание задачи не может быть пустым")
            return
            
        new_task = {
            "task": task_desc,
            "type": self.new_type_var.get()
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        
        # Clear input
        self.new_task_text.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Задача успешно выполнена")
        
    def refresh_history(self, *args):
        self.history_listbox.delete(0, tk.END)
        
        filtered = self.history.copy()
        
        # Filter by type
        if self.filter_type.get() != "All":
            filtered = [t for t in filtered if t["type"] == self.filter_type.get()]
        
        for task in reversed(filtered):  # Show newest first
            self.history_listbox.insert(tk.END, f"{task['task']} [{task['type']}]")
            
    def clear_filter(self):
        self.filter_type.set("All")
        self.refresh_history()
            
    def clear_history(self):
        if messagebox.askyesno("Подтвердить", "Очистить всю историю задач?"):
            self.history = []
            self.save_history()
            self.refresh_history()
            messagebox.showinfo("Готово", "История очищена.")
            
    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except:
            return []
            
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
            
    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()