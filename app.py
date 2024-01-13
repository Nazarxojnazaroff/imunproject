from flask import Flask, render_template, request, redirect
import psycopg2
import telebot
from telebot import types

app = Flask(__name__)

# Подключение к базе данных
conn = psycopg2.connect(
    host="104.236.64.26",
    database="imunpharma",
    user="postgres",
    password="fatEk(3obE"
)

# Создание курсора
cur = conn.cursor()

telegram_token = "6496605986:AAEZINXEHEsFX5dqQ3h0yjcy2uV5k7ZcHj4"
bot = telebot.TeleBot(telegram_token)
chat_id = "5825015061"


# Маршрут для добавления формы
@app.route('/add_form', methods=['POST'])
def add_form():
    name = request.form.get('name')
    numberphone = request.form.get('numberphone')
    comment = request.form.get('comment')

    # Запрос на добавление записи в таблицу form
    insert_query = "INSERT INTO form (name, numberphone, comment) VALUES (%s, %s, %s) RETURNING id"
    values = (name, numberphone, comment)

    cur.execute(insert_query, values)
    inserted_id = cur.fetchone()[0]
    conn.commit()

    # Отправка сообщения с использованием телеграм-бота
    message = f"ID опроса: {inserted_id}\nИмя покупателя: {name}\nНомер телефона: {numberphone}\nКомментарий: {comment}"
    bot.send_message(chat_id, message)

    return redirect('/')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(chat_id, 'Привет, я бот!')


@bot.message_handler(commands=['start'])
def handle_start(message):
    # Создание кнопки "Получить данные"
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn_get_data = types.KeyboardButton('Получить данные')
    markup.add(btn_get_data)

    # Отправка приветственного сообщения и кнопки
    bot.send_message(chat_id, "Привет, я бот! Нажми кнопку 'Получить данные', чтобы получить информацию.",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Получить данные':
        # Запрос на выборку всех записей из таблицы form
        cur.execute("SELECT * FROM form")
        rows = cur.fetchall()

        # Создание форматированного текста с данными
        text = "Данные из таблицы form:\n\n"
        for row in rows:
            text += f"ID: {row[0]}\nИмя: {row[1]}\nНомер телефона: {row[2]}\nКомментарий: {row[3]}\n\n"

        # Отправка сообщения с данными
        bot.send_message(chat_id, text)


# Маршрут для отображения главной страницы
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    bot.polling()
