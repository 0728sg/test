from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import staff
from db import db_main
import buttons

from aiogram.types import ReplyKeyboardRemove


# from db import db_main


class FSM_Store_client(StatesGroup):
    product_id = State()
    count = State()
    size = State()
    phone_number = State()
    submit = State()



async def start_fsm(message: types.Message):
    await message.answer('Write a product id: ', reply_markup=buttons.cancel_button)
    await FSM_Store_client.product_id.set()

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await message.answer('Write a count of products: ')
    await FSM_Store_client.next()

async def load_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count'] = message.text

    await message.answer('Put a product size: ')
    await FSM_Store_client.next()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Write your phone number: ')
    await FSM_Store_client.next()


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text



    await message.answer('Is data correct?')
    await message.answer(
        caption=f'Product_id: {data["product_id"]}\n'
                f'Count: {data["count"]}\n'
                f'Size: {data["size"]}\n'
                f'Phone_number: {data["phone_number"]}\n',
        reply_markup=buttons.submit_button)

    await FSM_Store_client.next()


async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Yes':
        async with state.proxy() as data:
          await message.answer('Data in base!', reply_markup=kb)
          await db_main.sql_insert_products(
            Product_id =data['product_id'],
            Count=data['count'],
            size=data['size'],
            phone_number=data['phone_number']
        )

          await state.finish()

        for staff_id in staff:
                try:
                    await message.bot.send_photo(
                        chat_id=staff_id,
                        caption=f'New product was added:\n\n'
                                f'Product_id: {data["product_id"]}\n'
                                f'Sizze: {data["size"]}\n'
                                f'Phone_number: {data["phone_number"]}\n'
                    )
                except Exception as e:
                    await message.answer(f"Error occured with sending {staff}: {e}")

        await state.finish()


    elif message.text == 'No':
        await message.answer('Filling a blank is over!', reply_markup=kb)
        await state.finish()

    else:
        await message.answer('Choose "Yes" или "No"')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Cancelled!', reply_markup=kb)

def register_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Cancel', ignore_case=True), state="*")

    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(load_product_id, state=FSM_Store_client.product_id)
    dp.register_message_handler(load_count, state=FSM_Store_client.count)
    dp.register_message_handler(load_size, state=FSM_Store_client.size)
    dp.register_message_handler(load_phone_number, state=FSM_Store_client.phone_number)
    dp.register_message_handler(submit, state=FSM_Store_client.submit)