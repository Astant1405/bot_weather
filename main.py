import telebot
import requests
from config import open_weather_token
from translate import Translator

bot = telebot.TeleBot('5910627376:AAGYCqGX3vvBpLy1fCrDNbthYCwGXdUXFQI')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name} я бот показывающий погоду. Введи ' \
           f'название города если хочешь узнать погоду '
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler()
def get_weather(message):
    try:
        translator = Translator(from_land='en', to_lang='ru')
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
        data = r.json()
        city = data['name']
        temperature = round(data['main']['temp'])
        feels = round(data['main']['feels_like'])
        press = data['main']['pressure']
        press1 = round(int(press) * 100 / 133.32)
        hum = data['main']['humidity']
        des = data['weather'][0]['description']
        trans_des = translator.translate(des)
        wind = round(data['wind']['speed'])

        mess_weather = (f'Погода в городе: {city}\nТемпература: {temperature}°C\n'
                        f'Ощущается как: {feels}°C\nОписание: {trans_des}\n'
                        f'Давление: {press1} мм.рт.ст.\nВлажность: {hum}%\n'
                        f'Скорость ветра: {wind} м/с\n')
        bot.send_message(message.chat.id, mess_weather, parse_mode='html')

    except Exception:
        error = 'Проверьте название города'
        bot.send_message(message.chat.id, error, parse_mode='html')


bot.polling(none_stop=True)
