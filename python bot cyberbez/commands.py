from json import loads
import telebot.types
import telebot
from api_service import login
from settings import users
import keyboards
from user import User

class Commands:
    def __init__(self, bot: telebot.TeleBot) -> None:
        self.bot = bot

    # /start
    def start(self, message):
        text = "Добро пожаловать в CyberLearnBot\n\nИспользуйте /login <login> <password>"
        msg = self.bot.send_message(message.chat.id, text, parse_mode='markdown')

    # /login
    def login(self, message: telebot.types.Message):
        args = message.text.split()[1:]

        if len(args) == 0:
            msg = self.bot.send_message(message.chat.id, "Вы не указали логин и пароль", parse_mode='markdown')
            return
        if len(args) == 1:
            msg = self.bot.send_message(message.chat.id, "Вы не указали пароль", parse_mode='markdown')
            return
        if len(args) > 2:
            msg = self.bot.send_message(message.chat.id, "Вы указали слишком много аргументов", parse_mode='markdown')
            return
        
        response = login(message.chat.id, args[0], args[1])

        if (response.status_code != 200):
            if (response.status_code == 401):
                self.bot.send_message(message.chat.id, "Неверный логин или пароль. Повторите авторизацию снова", parse_mode='html')
                return
            else:
                self.bot.send_message(message.chat.id, "Извините, на стороне сервиса неполадки.\n\n<b>Ожидайте возобновления работ.</b>", parse_mode='html')
            return
        
        user = User(message.chat.id, loads(response.text)['access_token'])
    
        already_exists = False

        for user in users:
            if user.telegram_token == message.chat.id:
                self.bot.send_message(message.chat.id, "Извините, вы уже авторизованы. \n\nИспользуйте: <i>/logout</i>", parse_mode='markdown')
                return

        users.append(user)

        self.bot.delete_message(message.chat.id, message.id)
        msg = self.bot.send_message(message.chat.id, f"Вы успешно авторизовались. \n\nДля навигации используйте клавиатуру", parse_mode='markdown', reply_markup=keyboards.main_keyboard())