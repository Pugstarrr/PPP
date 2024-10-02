import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
import telegram
import asyncio

# Укажите свои данные
EMAIL_ADDRESS = 'keampunols@web.de'
EMAIL_PASSWORD = 'GcczKqVt522'
TELEGRAM_TOKEN = '6086581648:AAFAB7-2BZ-fw572P8ungc_mlNJTI7cjEEI'
CHAT_ID = '5616095464'

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send_email(name, email, message):
    subject = "Обратная связь от {}".format(name)
    msg = MIMEText("Имя: {}\nEmail: {}\nСообщение: {}".format(name, email, message))
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        # Используем SMTP-сервер web.de
        with smtplib.SMTP_SSL('smtp.web.de', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email отправлен успешно.")  # Отладочное сообщение
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")

async def send_telegram_message(name, email, message):
    text = "Имя: {}\nEmail: {}\nСообщение: {}".format(name, email, message)
    await bot.send_message(chat_id=CHAT_ID, text=text)

def submit_form():
    name = name_entry.get()
    email = email_entry.get()
    message = message_entry.get("1.0", tk.END)

    if name and email and message:
        send_email(name, email, message)

        # Запускаем асинхронную функцию для отправки в Telegram
        asyncio.run(send_telegram_message(name, email, message))

        messagebox.showinfo("Успех", "Ваше сообщение отправлено!")
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")

# Создание основного окна
root = tk.Tk()
root.title("Форма обратной связи")

# Поля ввода
tk.Label(root, text="Имя:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

tk.Label(root, text="Сообщение:").pack(pady=5)
message_entry = tk.Text(root, height=10, width=30)
message_entry.pack(pady=5)

# Кнопка отправки
submit_button = tk.Button(root, text="Отправить", command=submit_form)
submit_button.pack(pady=20)

# Запуск главного цикла
root.mainloop()
