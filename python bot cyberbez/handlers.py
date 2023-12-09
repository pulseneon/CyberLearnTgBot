from commands import Commands
from callbacks import Callback
from settings import users
import keyboards

class Handlers:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.commands = Commands(bot)

        # user handlers list
        bot.message_handler(commands=['start'])(self.commands.start)
        bot.message_handler(commands=['login'])(self.commands.login)

        @bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            Callback(bot, call)

        # default handler
        bot.message_handler(content_types=["text"])(self._default_answer)
        bot.message_handler(content_types=['photo'])(self._default_answer)

    def _default_answer(self, message):
        exists = False

        for user in users:
            if user.telegram_token == message.chat.id:
                exists = True

        if (exists):
            msg = self.bot.send_message(message.chat.id, f'Воспользуйтесь клавиатурой ниже для работы',
                                        reply_markup=keyboards.main_keyboard())
            
        else:
            msg = self.bot.send_message(message.chat.id, text=f'Авторизуйтесь. Используйте <i>/login</i>', parse_mode='html')