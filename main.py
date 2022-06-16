from aiogram import(
    Bot,
    Dispatcher,
    executor,
    types
)

import config
from quiz import Quiz

bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

quiz_db = {} # Quiz info
quiz_owners = {} # Quiz owners info

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    """Start command handler"""
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(
        text='Создать тест',
        request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)
    ))
    poll_keyboard.add(types.KeyboardButton(text='Отмена'))
    await message.answer('Нажмите на кпопку и создайте тест!',
                        reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == 'Отмена')
async def action_cancel(message: types.Message) -> None:
    """Cancel action handler"""
    await message.answer('Действие отменено. Введите /start, чтобы начать заново',
        reply_markup=types.ReplyKeyboardMarkup())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
