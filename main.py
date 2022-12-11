import requests
import random
import telebot
from bs4 import BeautifulSoup as b

URL = 'https://www.anekdot.ru/last/good/'
API_KEY = '5467543677:AAGVl5y1Tu0XroxjFnEMdaB2TejTbLGsi2g'


def parser(url):
    r = requests.get(url)
    # print(r.status_code)
    # print(r.text)
    soup = b(r.text, 'html.parser')  # отправляем текст и запускаем парсер
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]


list_of_jokes = parser(URL)
random.shuffle(list_of_jokes)

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вас приветствует внезапный смех. Отправь любую цифру:')

@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id, 'Введите любую цифру от 1 до 10:')

bot.polling()
