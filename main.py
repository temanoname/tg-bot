import telebot
import requests
from config import API_TOKEN, WEATHER_API_KEY

bot = telebot.TeleBot(API_TOKEN)

start_txt = '''Привет! Я бот прогноза погоды. 
Отправьте название города, и я скажу, какая там температура и как она ощущается.'''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, start_txt)


@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text.strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={WEATHER_API_KEY}'

    try:
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code == 200:
            temperature = round(weather_data['main']['temp'])
            temperature_feels = round(weather_data['main']['feels_like'])

            w_now = f'Сейчас в городе {city.capitalize()} {temperature} °C'
            w_feels = f'Ощущается как {temperature_feels} °C'

            bot.send_message(message.chat.id, w_now)
            bot.send_message(message.chat.id, w_feels)
        else:
            bot.send_message(message.chat.id, f"Не удалось получить данные о погоде для города: {city}.")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при получении данных о погоде.")
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f' Исключение: {e}')
