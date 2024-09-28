import logging
from aiogram.utils import executor
from buttons import start_test
from config import bot, dp, staff
from handlers import commands, echo, FSM_store_staff, FSM_store_staff
from db import db_main
from handlers.FSM_store_client import FSM_Store_client


async def on_startup(_):
    for i in staff:
        await bot.send_message(chat_id=i, text="Bot activate!",
                               reply_markup=start_test)
        await db_main.sql_create()


commands.register_commands(dp)
FSM_store_staff.register_store(dp)
FSM_Store_client.register_store(dp)


# echo.register_echo(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)