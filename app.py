import tkinter as tk
from tkinter import messagebox

# Базовое хранилище пользователей (позже заменим на файл или БД)
users_db = {}
current_user = None

root = tk.Tk()
root.title("Мой Мессенджер - Авторизация")
root.geometry("400x500")
root.config(bg="#1e1e1e")

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Главное окно чата (появляется после входа)
def open_chat_window():
    clear_window()
    root.title(f"Мой Мессенджер — {current_user}")
    
    # Чат-бокс
    chat_box = tk.Text(root, bg="#2d2d2d", fg="white", font=("Arial", 11), state="disabled")
    chat_box.pack(expand=True, fill="both", padx=10, pady=10)

    # Поле ввода
    user_input = tk.Entry(root, font=("Arial", 12), bg="#3d3d3d", fg="white", insertbackground="white")
    user_input.pack(fill="x", padx=10, pady=5)

    def send_message(event=None):
        text = user_input.get()
        if text:
            chat_box.config(state="normal")
            chat_box.insert(tk.END, f"{current_user}: {text}\n")
            chat_box.config(state="disabled")
            user_input.delete(0, tk.END)

    send_btn = tk.Button(root, text="Отправить", command=send_message, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
    send_btn.pack(pady=10)
    user_input.bind("<Return>", send_message)

# Окно регистрации
def show_register():
    clear_window()
    root.title("Регистрация")

    tk.Label(root, text="Создать аккаунт", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)

    tk.Label(root, text="Почта:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
    email_entry = tk.Entry(root, font=("Arial", 12), width=25)
    email_entry.pack(pady=5)

    tk.Label(root, text="Пароль:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
    pass_entry = tk.Entry(root, show="*", font=("Arial", 12), width=25)
    pass_entry.pack(pady=5)

    def register_user():
        email = email_entry.get().strip()
        password = pass_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Ошибка", "Заполни все поля!")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Ошибка", "Введи реальную почту (должна содержать @ и .)")
            return
        if email in users_db:
            messagebox.showerror("Ошибка", "Такая почта уже зарегистрирована!")
            return

        # Сохраняем пользователя
        users_db[email] = password
        messagebox.showinfo("Успех", "Регистрация прошла успешно! Теперь войди.")
        show_login()

    tk.Button(root, text="Зарегистрироваться", command=register_user, bg="#28a745", fg="white", font=("Arial", 11, "bold"), width=20).pack(pady=15)
    tk.Button(root, text="Уже есть аккаунт? Войти", command=show_login, bg="#444", fg="white", font=("Arial", 9), width=20).pack(pady=5)

# Окно входа (Главный экран)
def show_login():
    clear_window()
    root.title("Вход в мессенджер")

    tk.Label(root, text="Вход", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white").pack(pady=30)

    tk.Label(root, text="Почта:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
    email_entry = tk.Entry(root, font=("Arial", 12), width=25)
    email_entry.pack(pady=5)

    tk.Label(root, text="Пароль:", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack()
    pass_entry = tk.Entry(root, show="*", font=("Arial", 12), width=25)
    pass_entry.pack(pady=5)

    def login_user():
        global current_user
        email = email_entry.get().strip()
        password = pass_entry.get().strip()

        if email in users_db and users_db[email] == password:
            current_user = email
            open_chat_window()
        else:
            messagebox.showerror("Ошибка", "Неверная почта или пароль!")

    tk.Button(root, text="Войти", command=login_user, bg="#007acc", fg="white", font=("Arial", 11, "bold"), width=20).pack(pady=15)
    tk.Button(root, text="Создать аккаунт", command=show_register, bg="#444", fg="white", font=("Arial", 9), width=20).pack(pady=5)

# Запускаем приложение с экрана входа
show_login()
root.mainloop()