import datetime
from json import loads
import json
import math
import types
import numpy as np

import keyboards
import matplotlib.pyplot as plt

import api_service
from settings import users

class Callback:
    def __init__(self, bot, call) -> None:
        self.arg = None
        self.data = call
        self.bot = bot

        self.parse()

    def parse(self):
        command = self.data.data.split(':')[0]
        self.arg = self.data.data.split(':')[1]

        exists = False

        for user in users:
            if user.telegram_token == self.data.from_user.id:
                exists = True

        if (not exists):
            msg = self.bot.send_message(self.data.from_user.id, f'Авторизуйтесь /login')
            return

        match command:
            case "back": # назад
                self._handle_back()
            case 'profile': # профиль
                self._handle_profile()
            case 'open_settings':
                self._handle_open_settings()
            case 'rating':
                self._handle_rating()
            case 'settings':
                self._handle_settings()
            case 'stats': # статистика
                self._handle_stats()

    def _handle_back(self):
        self.bot.delete_message(self.data.from_user.id, self.data.message.id)
        self.bot.send_message(chat_id=self.data.from_user.id, text="Вы вернулись назад", reply_markup = keyboards.main_keyboard())

    def _handle_stats(self):
        self.bot.delete_message(self.data.from_user.id, self.data.message.id)
        
        user = next(filter(lambda x: x.telegram_token == self.data.from_user.id, users))
        response = api_service.get_history(user.api_token)['response']

        days = dict()

        for result in response:
            dt_object = datetime.datetime.strptime(result['date'], "%Y-%m-%dT%H:%M:%S.%f%z")
            formatted_date = dt_object.strftime("%d.%m")

            if (dt_object.date() - datetime.datetime.now().date()).days > 5:
                continue
            
            if formatted_date in days and result['is_correct'] is 1:
                days[formatted_date] += 1
            elif result['is_correct']:
                days[formatted_date] = 1

        days = dict(sorted(days.items(), key=lambda item: item[0]))

        keys = list(days.keys())
        values = list(days.values())

        # Plot the histogram
        plt.bar(keys, values)

        plt.xlabel('Дни')
        plt.ylabel('Число правильных ответов')
        plt.title('История ответов на вопросы')

        plt.savefig(f'{str(self.data.from_user.id)}.png')

        with open(f'{str(self.data.from_user.id)}.png', 'rb') as photo:
            self.bot.send_photo(self.data.from_user.id, photo)
        self.bot.send_message(chat_id=self.data.from_user.id, text="Статистика ваших последних ответов: ", reply_markup = keyboards.back_keyboard())

    def _handle_open_settings(self):
        user = next(filter(lambda x: x.telegram_token == self.data.from_user.id, users))
        self.bot.delete_message(self.data.from_user.id, self.data.message.id)
        self.bot.send_message(chat_id=self.data.from_user.id, text="Ваши настройки", reply_markup = keyboards.settings_keyboard(user))

    def _handle_settings(self):
        user = next(filter(lambda x: x.telegram_token == self.data.from_user.id, users))

        match self.arg:
            case "attacks":
                user.reverse_attacks()
            case "everyday":
                user.reverse_everyday()
            case 'new':
                user.reverse_new()
            case 'notify':
                user.reverse_notifications()

        self.bot.delete_message(self.data.from_user.id, self.data.message.id)
        self.bot.send_message(chat_id=self.data.from_user.id, text="Пункт настроек изменен", reply_markup = keyboards.settings_keyboard(user))

    def _handle_rating(self):
        response = api_service.get_rating()['users']

        i = 1
        text = '<b>Список лучших пользователей:</b>\n\n'

        for result in response:
            if i == 10:
                self.bot.send_message(chat_id=self.data.from_user.id, text=text, parse_mode = 'html', reply_markup = keyboards.back_keyboard())
                return

            text += f'<b>{i}. {result["first_name"]} {result["last_name"]}</b> — {round(result["experience"]/100)} уровень\n' 
            i+=1
        
        self.bot.send_message(chat_id=self.data.from_user.id, text=text, parse_mode = 'html', reply_markup = keyboards.back_keyboard())

    def _handle_profile(self):
        user = next(filter(lambda x: x.telegram_token == self.data.from_user.id, users))
        
        response = api_service.get_profile(user.api_token)

        user_info = response['user']
        first_name = user_info['first_name']
        last_name = user_info['last_name']
        exp = user_info['experience']
        photo_url = user_info['photo']

        lvl = math.floor(exp/100)
        exp_lines = round(((exp - (exp//100)*100))/10)
        need = 100 - (exp - (exp//100)*100)
        progress = ''

        for i in range(10):
            if (exp_lines > 0):
                progress += '🟩'
                exp_lines-=1
            else:
                progress += '⬜️'

        text_message = f"👤 Ваш профиль: <b>{first_name} {last_name}</b>\n\n🔰 Ваш уровень: {lvl}\nПрогресс до следующего уровня: {progress}\n<i>(не хватает {need} опыта)</i>"
        
        self.bot.delete_message(self.data.from_user.id, self.data.message.id)
        self.bot.send_message(chat_id=self.data.from_user.id, text=text_message, parse_mode = 'html', reply_markup = keyboards.profile_keyboard())