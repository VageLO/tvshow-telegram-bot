from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp
from keyboard.inline_menu import menu_cd, title_keyboard, seasons_keyboard, episodes_keyboard

@dp.message_handler(commands=['tvshows'])
async def shows(message: types.Message):
    await list_titles(message)

async def list_titles(message: CallbackQuery, **kwargs):
    markup = await title_keyboard()

    await message.answer('Мультсериалы🐨', reply_markup=markup)

async def list_seasons(callback: CallbackQuery, titles, **kwargs):
    markup = await seasons_keyboard(titles)
    await callback.message.edit_reply_markup(reply_markup=markup)

async def list_episodes(callback: CallbackQuery, seasons, titles, **kwargs):
    markup = await episodes_keyboard(titles, seasons)
    await callback.message.reply(f'https:{titles}season.php?id={seasons}')
    await callback.message.edit_reply_markup(markup)

@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
   
    current_level = callback_data.get("level")
    titles = callback_data.get("titles")
    seasons = callback_data.get("seasons")
    episodes = callback_data.get("episodes")


    levels = {
        "0": list_titles,  
        "1": list_seasons, 
        "2": list_episodes
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        titles=titles,
        seasons=seasons,
        episodes=episodes
    )