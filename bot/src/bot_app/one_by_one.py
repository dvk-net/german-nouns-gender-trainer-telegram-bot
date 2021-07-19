from aiogram import types

from bot_app.states import GameStates
from aiogram.dispatcher import FSMContext
from . app import dp, bot
from . keyboards import inline_kb
from . data_fetcher import get_random, get_next

@dp.message_handler(commands='train_all', state="*")
async def train_all(message: types.Message, state: FSMContext):
    await GameStates.all_words.set()
    res = await get_next(0)
    if not res:
        await GameStates.start.set()
        await message.reply('All is done!!!')
        return
    async with state.proxy() as data:
        data['step'] = 1
        data['pk'] = 1
        data['answer'] = res.get('gender')
        data['word'] = res.get('word')

        await message.reply(f"{ data['step'] }. Das wort ist { data['word'] }", reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data in ['das', 'die', 'der'], state=GameStates.all_words)
async def button_click_call_back_all(callback_query: types.CallbackQuery, state:FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        if answer == data.get('answer'):
            await bot.send_message(callback_query.from_user.id, 'Ya\n')
            res = await get_next(data.get('pk'))
            if res:
                data['step'] += 1
                data['answer'] = res.get('gender')
                data['word'] = res.get('word')
                data['pk'] = res.get('pk')
                await bot.send_message(callback_query.from_user.id, f"{ data['step'] }. Das wort ist { data['word'] }", reply_markup=inline_kb)
            else:
                await bot.send_message(callback_query.from_user.id, "The game is over!!!" )
                await GameStates.start.set()
        else:
            await bot.send_message(callback_query.from_user.id, f'Nein\n', reply_markup=inline_kb) 