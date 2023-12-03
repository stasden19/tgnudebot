import asyncio

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters.command import CommandStart, Command
from aiogram.types.message import ContentType

from core.handlers import generate_photo
from core.handlers.basic import get_start, get_account_info, agree_term_use, send_instruction_command, help_command, \
    dont_understand, dont_agree_term
from core.handlers.callback import accept_terms, send_instruction, send_instruction_cmd
from core.handlers.pay import order, pre_check_out_query, succesful_payment, order_1, order_2, order_5, order_10, \
    order_50, order_100, order_200, order_command
from core.settings import settings
from core.utils.check_database import UserInDatabaseFilter
from core.utils.commands import set_command


async def start_bot(bot: Bot):
    await set_command(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот успешно запущен')


async def start():
    bot = Bot(settings.bots.bot_token)
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.message.register(get_start, CommandStart())
    dp.message.register(dont_agree_term, ~UserInDatabaseFilter())
    dp.message.register(generate_photo.selected_gender, (F.content_type.in_({ContentType.PHOTO})))
    # dp.callback_query.register(generate_photo.selected_gender, StatesPhoto.SELECT_GENDER)
    dp.callback_query.register(send_instruction, F.data.startswith('send_photo'))
    dp.message.register(send_instruction_cmd, Command('send_photo'))
    dp.callback_query.register(accept_terms, F.data.startswith('agree_term'))
    dp.callback_query.register(order, F.data.startswith('replenishment'))
    dp.callback_query.register(order_1, F.data == 'order_1')
    dp.callback_query.register(order_2, F.data == 'order_2')
    dp.callback_query.register(order_5, F.data == 'order_5')
    dp.callback_query.register(order_10, F.data == 'order_10')
    dp.callback_query.register(order_50, F.data == 'order_50')
    dp.callback_query.register(order_100, F.data == 'order_100')
    dp.callback_query.register(order_200, F.data == 'order_200')
    dp.pre_checkout_query.register(pre_check_out_query)
    dp.message.register(succesful_payment, F.content_type.in_({ContentType.SUCCESSFUL_PAYMENT}))
    dp.message.register(get_account_info, Command('account'))
    dp.message.register(agree_term_use, Command('terms_of_use'))
    dp.message.register(send_instruction_command, Command('instructions'))
    dp.message.register(order_command, Command('top_up_balance'))
    dp.message.register(help_command, Command('help'))
    dp.message.register(dont_understand)

    try:
        await dp.start_polling(bot, skip_updates=True)

    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
