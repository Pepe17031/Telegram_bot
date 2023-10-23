import telebot
import psycopg2 as pg

bot = telebot.TeleBot("6726984732:AAFU2iMO880Zdp9T4wBGWiZew0F36xtC7AM", parse_mode=None)

conn = pg.connect(
    host='postgres', # CHANGE TO
    database='django_db',
    port=5432,
    user='user',
    password='password'
)
cur = conn.cursor()
print("Подключение к postgres установленно.")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.chat)

    bot.reply_to(message, "Вы успешно подписались на рассылку. Аналитика будет приходить каждый час.")

    cur.execute(
        "INSERT INTO api_telegramusers (chat_id, username) VALUES (%s, %s) ON CONFLICT (username) DO UPDATE SET (chat_id) = ROW(EXCLUDED.chat_id)",
        (message.chat.id, message.chat.username)
    )
    conn.commit()


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
