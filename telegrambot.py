import logging
import telegram
import requests
import json
import get_covid_city_stats as gccs
import api_key
import call_openai
from datetime import datetime
from random import randrange
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram import InputMediaPhoto

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
reply = False

def covid_city_stats(update, context):
    global reply
    #if(reply == True):
    try:
        aux = update.message.text
        city_stats_cmd = aux.split()
        city = city_stats_cmd[1]
        city_stats = gccs.get_covid_city_stats(city)

        for i in city_stats:
                judet = 'Judet: {} \n'.format(i['Judet'])
                localitate = 'Localitate: {} \n'.format(i['Localitate'])
                populatie = 'Populatie: {} \n'.format(i['Populatie'])
                cazuri = 'Cazuri: {} \n'.format(i['Cazuri'])
                incidenta = 'Incidenta: {} \n'.format(i['Incidenta'])
                last_updated = "Ultima actualizare: {} \n".format(i['last_updated'])
                stats = incidenta + localitate + judet + populatie + cazuri  + last_updated
                update.message.reply_text(stats)
    finally:
        log_action(
            update.message.chat.id,
            update.message.chat.title,
            update.message.chat.type,
            update.message.from_user.id,
            update.message.from_user.username,
            update.message.from_user.first_name,
            update.message.from_user.last_name, city
            )

def openai_jokes(update, context):
    global reply
    #if(reply == True):
    try:
        aux = update.message.text
        text = aux.split(' ',1)[1]
        completion = call_openai.req_openai(text)
        update.message.reply_text(completion)
    finally:
        print("TODO:To add logging")

def log_action(chat_id, title, chat_type, user_id , username, first_name, last_name, city):
    n0w = datetime.now()
    log = {"chat_id": None, "chat_name": None, "chat_type": None, "user_id": None, "username": None, "first_name": None, 'last_name': None, "city": None, "datetime": None}
    log['chat_id'] = chat_id
    log['chat_name'] = title
    log['chat_type'] = chat_type
    log['user_id'] = user_id
    log['username'] = username
    log['first_name'] = first_name
    log['last_name'] = last_name
    log['city'] = city.upper()
    log['datetime'] = str(n0w)
    logs = json.dumps(log)
    f = open("covid_city_stats.log","a")
    f.write(logs + "\n")
    f.close()


def main():
    #TEST
    #updater = Updater(api_key.test(), use_context=True)

    #PROD
    updater = Updater(api_key.prod(), use_context=True)

    updater.dispatcher.add_handler(CommandHandler('city', covid_city_stats))
    updater.dispatcher.add_handler(CommandHandler('openai', openai_jokes))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
