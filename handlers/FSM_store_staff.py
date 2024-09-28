from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import staff
from db import db_main
import buttons

from aiogram.types import ReplyKeyboardRemove


# from db import db_main


class FSM_Store_staff(StatesGroup):
    name_products = State()
    category = State()
    size = State()
    price = State()
    product_id = State()
    photo_products = State()
    submit = State()



async def is_employee(user_id):
    return user_id in staff



async def start_fsm(message: types.Message):
    await message.answer('Write a name of product: ', reply_markup=buttons.cancel_button)
    await FSM_Store_staff.name_products.set()

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_products'] = message.text

    await message.answer('Put a product category: ')
    await FSM_Store_staff.next()

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await message.answer('Put a product size: ')
    await FSM_Store_staff.next()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Put a product price: ')
    await FSM_Store_staff.next()


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await message.answer('Write an article of product (it should be unique) : ')
    await FSM_Store_staff.next()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await message.answer('Send photo: ')
    await FSM_Store_staff.next()


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await message.answer('Is data correct?')
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Product name: {data["name_products"]}\n'
                f'Category: {data["category"]}\n'
                f'Size: {data["size"]}\n'
                f'Price: {data["price"]}\n'
                f'Product_id: {data["product_id"]}\n',
        reply_markup=buttons.submit_button)

    await FSM_Store_staff.next()


async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Yes':
        async with state.proxy() as data:
          await message.answer('Data in base!', reply_markup=kb)
          await db_main.sql_insert_products(
            name_products=data['name_products'],
            category=data['category'],
            size=data['size'],
            price=data['price'],
            product_id=data['product_id'],
            photo_products=data['photo_products']
        )

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

    dp.register_message_handler(start_fsm, commands=['products'])
    dp.register_message_handler(load_name, state=FSM_Store_staff.name_products)
    dp.register_message_handler(load_category, state=FSM_Store_staff.category)
    dp.register_message_handler(load_size, state=FSM_Store_staff.size)
    dp.register_message_handler(load_price, state=FSM_Store_staff.price)
    dp.register_message_handler(load_product_id, state=FSM_Store_staff.product_id)
    dp.register_message_handler(load_photo, state=FSM_Store_staff.photo_products, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_Store_staff.submit)