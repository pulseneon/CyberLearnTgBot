import types
from telebot import types
from user import User

def notify_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Проходить тесты', url='http://26.170.53.65:5173')
    markup.add(btn_my_site)

    return markup

def main_keyboard():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="Профиль", callback_data=f'profile:open'))
    markup.add(types.InlineKeyboardButton(text='Тесты', url='http://26.170.53.65:5173'))
    markup.add(types.InlineKeyboardButton("Аналитика", callback_data=f'stats:main'))
    markup.add(types.InlineKeyboardButton("Рейтинг", callback_data=f'rating:open'))
    markup.add(types.InlineKeyboardButton("Настройки", callback_data=f'open_settings:profile'))

    return markup

def profile_keyboard():
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="📊 Статистика", callback_data=f'stats:main'))
    markup.add(types.InlineKeyboardButton(text="◀️ Назад", callback_data=f'back:open'))
    return markup

def back_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="◀️ Назад", callback_data=f'back:open'))
    return markup

def get_emoji(value) -> str:
    if value:
        return '🟢'
    else:
        return '🔴'

def settings_keyboard(user: User):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(text="Симуляция атак " + get_emoji(user.attacks_enable), callback_data=f'settings:attacks'))
    markup.add(types.InlineKeyboardButton(text="Ежедневные подсказки " + get_emoji(user.everyday_enable), callback_data=f'settings:everyday'))
    markup.add(types.InlineKeyboardButton(text="Оповещение новых угроз " + get_emoji(user.new_enable), callback_data=f'settings:new'))
    markup.add(types.InlineKeyboardButton(text="Напоминания о тестах " + get_emoji(user.notifications_enable), callback_data=f'settings:notify'))
    markup.add(types.InlineKeyboardButton(text="◀️ Назад", callback_data=f'back:open'))

    return markup