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

@dp.message_handler(content_types=['poll'])
async def msg_with_poll(message: types.Message) -> None:
    """Message with poll(quiz handler"""
    user_id = str(message.from_user.id)
    # if user is unknown
    if not quiz_db.get(user_id):
        quiz_db[user_id] = []

    # quiz type check
    if message.poll.type != 'quiz':
        await message.reply('Извините, я принимаю только тесты!')
        return

    quiz_db[user_id].append(Quiz(
        quiz_id=message.poll.id,
        question=message.poll.question,
        options=[option.text for option in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=user_id
    ))
    quiz_owners[message.poll.id] = user_id

    await message.reply(
        f'Тест сохранен. Общие количество тестов: {len(quiz_db[user_id])}'
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
