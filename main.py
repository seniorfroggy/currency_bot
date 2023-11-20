import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import telebot
from config import CBR_LINK
from constants import DELTA
from datetime import datetime
import xmltodict
import time
from sqlite import databasetrace, getdatabase
from telebot import types 
import json
import urllib
import os

TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)

def check_for_surges(result, previous_date_result):
    result = json.loads(result)
    previous_date_result = json.loads(previous_date_result)
    troubles = ''

    if previous_date_result == '["Error in parameters"]':
        return troubles
    
    for today in result[0]['Valute']:
        del today['Name']
        for yest in previous_date_result[0]['Valute']:
            if today['@ID'] == yest['@ID']:
                if yest['Value'] == 0:
                    troubles += today['CharCode'] + ''
                    break
                today['Value'] = today['Value'].replace(',', '.', 1)
                yest['Value'] = yest['Value'].replace(',', '.', 1)
                if abs(float(today['Value']) - float(yest['Value'])) / float(yest['Value']) > DELTA:
                    troubles += today['CharCode'] + ' '
                    break

    with open('docs/simple.json', 'w') as file:
        json.dump(result, file, indent=3)
    
    return troubles

def parse_results(message, result, previous_date_result, date):
    output_file = open('docs/simple.json', 'rb')
    if result == '["Error in parameters"]':
        bot.send_message(message, "Incorrect date")
        return
    
    surges = check_for_surges(result, previous_date_result)

    if surges == '':
        bot.send_document(message, output_file, caption = f'Курс за {date}', visible_file_name="CurrencyRate.json")
    else:
        bot.send_document(message, output_file, caption = f'Курс за {date} P.S: Изменились более чем на {DELTA*100}% по сравнению с предыдущим днем: {surges}', visible_file_name="CurrencyRate.json")


def get_results(date, message): 
    link = CBR_LINK + date
    input_file = urllib.request.urlopen(link)           
    result = input_file.read()
    result = json.dumps(xmltodict.parse(result))
    result = '[' + result[12:-1] + ']'
    previous_date = date
    previous_date = str(int(previous_date[:2]) - 1) + previous_date[2:]
    link = CBR_LINK + previous_date
    input_file = urllib.request.urlopen(link)      
    previous_date_result = input_file.read()
    previous_date_result = json.dumps(xmltodict.parse(previous_date_result))
    previous_date_result = '[' + previous_date_result[12:-1] + ']'
    parse_results(message, result, previous_date_result, date)

bot.set_my_commands(commands=[
        telebot.types.BotCommand("/start", "Начать работу с ботом"), telebot.types.BotCommand("/stat", "График запросов")
    ])
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 1)
    item1 = types.KeyboardButton("Курс за вчера")
    item2 = types.KeyboardButton("Курс за сегодня")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите одно из предложенного или введите дату в формате dd/MM/yyyy', parse_mode='html', reply_markup=markup)  

@bot.message_handler(commands=['stat'])
def statistics(message):
    logins, attendance = getdatabase()
    plt.bar(logins, attendance, color = 'g', width=0.25, )
    plt.xlabel('Logins', fontsize = 12)
    plt.ylabel('Attendance', fontsize = 12)
    plt.savefig('plot.jpg')
    doc = open('plot.jpg', 'rb')
    bot.send_document(message.chat.id, doc) 
    doc.close()

@bot.message_handler(content_types=['text'])
def response(message):
    databasetrace(message.from_user.username, message.date)
    if message.chat.type == 'private':

        if message.text == 'Курс за вчера':         
            t = datetime.now().strftime('%d/%m/%Y')[:10]
            t = str(int(t[:2]) - 1) + t[2:]
            get_results(t, message.chat.id)

        elif message.text == 'Курс за сегодня':           
            t = datetime.now().strftime("%d/%m/%Y")[:10]
            get_results(t, message.chat.id)

        else:
            try:
                time.strptime(message.text, "%d/%m/%Y")
            except ValueError:
                bot.send_message(message.chat.id, "Incorrect date format")
                return
            get_results(message.text, message.chat.id)
                 
bot.polling()

