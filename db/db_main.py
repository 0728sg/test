import sqlite3

from db import queries

db= sqlite3.connect('db/store.sqlite3.1')
cursor = db.cursor()


async def sql_create():
    if db:
        print("Data base is connected")

        cursor.execute(queries.CREATE_TABLE_PRODUCTS)
        db.commit()

async def sql_insert_products(name_product, category, size, price, product_id, photo):
    with sqlite3.connect('db/store.sqlite') as db_with:
        cursor = db.cursor()
        cursor.execute(queries.INSERT_PRODUCTS_QUERY, (
            name_product,
            category,
            size,
            price,
            product_id,
            photo
        ))
        db_with.commit()
