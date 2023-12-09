import telebot

simulate_bot_token = '6899772812:AAFWWiqHSC1KuNLgCAlaK-9mkQhbzQ3RT9c'

bot = telebot.TeleBot(simulate_bot_token)
    
def polling():
    bot.polling(none_stop=True)

read_users = ()

def simulate(chat_id):
    pass

def delete_dialog(client, chat_id):
    pass

@bot.message_handler(commands=['start'])
def start(message):
    print("[simulate] sent start")
    bot.delete_message(message.from_user.id, message.id)
    print("[simulate] message deleted")