from settings import TOKEN
from handlers import Handlers
import threading
import notificator
import telebot
import sys
import simulate

try:    
    bot = telebot.TeleBot(TOKEN)
except Exception as e:
    sys.exit(1)

def main(): 
    Handlers(bot)

    threadReminder = threading.Thread(target=notificator.notify_reminder_loop, args=(bot,))
    threadAlert = threading.Thread(target=notificator.notify_alert_timer, args=(bot,))
    threadSimulate = threading.Thread(target=notificator.simulate_attack)
    threadBot = threading.Thread(target=simulate.polling)

    threadReminder.start()
    threadAlert.start()
    threadSimulate.start()
    threadBot.start()
    bot.polling(none_stop=True)     
    
if __name__ == "__main__":
    main()