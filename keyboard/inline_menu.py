from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tvshows_titles import getTitles
from parsesite import Episodes, Seasons

# Создаем CallbackData-объекты, которые будут нужны для работы с меню
menu_cd = CallbackData("show_menu", "level", "titles", "seasons", "episodes")

def make_callback_data(level, titles=[], seasons=[], episodes=[]):
    return menu_cd.new(level=level, titles=titles, seasons=seasons, episodes=episodes)

async def title_keyboard():
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup()

    for i in getTitles():

        button_text = i['title']

        callback_data =  make_callback_data(level=CURRENT_LEVEL + 1, titles=i['link'].split(":")[1])
        
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return markup
    

async def seasons_keyboard(title):
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup()

    for i in Seasons(title):
        try:
            button_text = i.split('=')[1]
            callback_data =  make_callback_data(level=CURRENT_LEVEL + 1, titles=title, seasons=button_text)
            markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
        except:
            pass
        
        
    return markup

async def episodes_keyboard(title, season):
    markup = InlineKeyboardMarkup()

    for i in Episodes(season, title):

        button_text=i['episode']
        
        markup.insert(
            InlineKeyboardButton(text=button_text, url=i['link'])
        )
    return markup