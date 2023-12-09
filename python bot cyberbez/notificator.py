from telethon import TelegramClient
import settings
import time
import random
import keyboards
import api_service
import simulate
import telebot

def notify_reminder(bot: telebot):
    with open('notify.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        random_line = random.choice(lines).strip()

    for u in settings.users:
        print(u)
        if u.notifications_enable:
            print("enable" + " " + str(u.telegram_token))
            try:
                bot.send_message(u.telegram_token, random_line, reply_markup = keyboards.notify_keyboard())
            except Exception as ex:
                print(str(ex))

def notify_alert(bot: telebot):
    alert = api_service.get_alert()

    print(alert['last_alert'])

    if (alert['last_alert'] == None):
        print("alert is null. return.")
        return

    last_alert = alert['last_alert']
    title = last_alert['title']
    desc = last_alert['description']
    id = last_alert['id']

    if (id == settings.last_alert_id):
        return

    text = f"⚠️ <b>Оповещение о новой угрозе: </b>\n\n<b>{title}</b>\n{desc}"

    for u in settings.users:
        if u.new_enable:
            bot.send_message(u.telegram_token, text, parse_mode='html')

    settings.last_alert_id = id

def notify_reminder_loop(bot: telebot):
    while True:
        print("кайфанул")
        notify_reminder(bot)
        time.sleep(24 * 60 * 60)

def notify_alert_timer(bot: telebot):
    while True:
        print("алерт кайфанул")
        notify_alert(bot)
        time.sleep(60)


def daily_alert(bot: telebot):
    pass

def daily_alert_timer(bot: telebot):
    while True:
        print("daily kaifanyl")
        daily_alert(bot)
        time.sleep(60)

def simulate_attack():
    while True:
        pass
        # time.sleep(15)
        # random_user = random.choice(settings.users)
        # print("rnd user" + random_user)

#       simulate.simulate(client=client, random_user)