#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
from peewee import *
import pandas as pd

db = SqliteDatabase('inventory.db')


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Product(Model):
    """Create Product model"""
    product_id = IntegerField(primary_key=True)
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


def initialize():
    """Initialize Sqlite database"""
    db.connect()
    db.create_tables([Product], safe=True)


def menu_loop():
    """Create a Menu to make selections"""
    choice = None

    while choice != 'q':
        clear_screen()
        print('-' * 20)
        print('Store-Inventory Menu')
        print('-' * 20)
        for key, value, in menu.items():
            print('{} {}'.format(key, value.__doc__))
        print('-' * 20)
        print("Enter 'q' to quit.")
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()
    print('')


def add_product_from_csv():
    """Add the data from CSV into the database"""
    data = pd.read_csv('./store-inventory/inventory.csv')
    product_list = []

    for i in data.index:
        product_dict = {'product_id': i, 'product_name': data['product_name'][i],
                        'product_price': int(data['product_price'][i].replace('.', '').strip('$')),
                        'product_quantity': int(data['product_quantity'][i]),
                        'date_updated': datetime.datetime.strptime(data['date_updated'][i], '%m/%d/%Y')}
        product_list.append(product_dict)

    try:
        Product.insert_many(product_list).execute()

    except IntegrityError as ex:
        print(ex)
        db.rollback()


def show_product_detail(product):
    print('-' * 20)
    print('product_id: {}'.format(product.product_id))
    print('product_name: {}'.format(product.product_name))
    print('product_price: ${}'.format(product.product_price / 100))
    print('product_quantity: {}'.format(product.product_quantity))
    print('date_updated: {}'.format(product.date_updated.strftime('%m/%d/%Y')))
    print('-' * 20)


def view_product_detail(query=None):
    """View the details of a single product in the database"""
    if query is None:
        for product in Product.select().order_by(Product.date_updated.desc()):
            show_product_detail(product)
            print('n) next product detail')
            print('q) return to main menu')

            next_action = input('Action: [N/q]').lower().strip()
            if next_action != 'n':
                break

    else:
        for product in Product.select().where(Product.product_id == query):
            show_product_detail(product)
            print('s) search again')
            print('q) return to main menu')

            next_action = input('Action: [S/q]').lower().strip()
            if next_action == 's':
                search_product_by_id()


def search_product_by_id():
    """Search and display a product by its ID"""
    query = None

    while query is None:
        try:
            query = int(input('Enter product id: '))
        except ValueError:
            print('Invalid input.. please enter a number.')

    view_product_detail(query=query)


def add_new_product():
    """Add a new product to the database"""
    new_product_name = ''
    new_product_price = None
    new_product_quantity = None

    while not new_product_name:
        new_product_name = str(input('Enter product name: '))
        if not new_product_name:
            print('Invalid input.. please enter a product name.')

    while new_product_price is None:
        try:
            new_product_price = float(input('Enter product price in $: '))
            new_product_price *= 100
        except ValueError:
            print('Invalid input.. please enter a number.')

    while new_product_quantity is None:
        try:
            new_product_quantity = int(input('Enter product quantity: '))
        except ValueError:
            print('Invalid input.. please enter a number.')

    if input('Save Entry? [Y/n] ').lower() != 'n':
        Product.create(
            product_name=new_product_name,
            product_price=new_product_price,
            product_quantity=new_product_quantity
        )
        print('Save successfully!')
        input('Press ENTER to continue.. ')

    else:
        print('Discard changes.')
        input('Press ENTER to continue.. ')


def backup_database():
    """Make a backup of the entire contents of the database"""
    product_list = []
    for product in Product.select().order_by(Product.date_updated.desc()):
        product_dict = {'product_id': product.product_id,
                        'product_name': product.product_name,
                        'product_price': product.product_price / 100,
                        'product_quantity': product.product_quantity,
                        'date_updated': product.date_updated.strftime('%m/%d/%Y')}
        product_list.append(product_dict)

    data = pd.DataFrame(product_list)
    data = data.set_index('product_id')
    data = data.sort_index()[['product_name',
                              'product_price',
                              'product_quantity',
                              'date_updated']]
    data.to_csv('./store-inventory/inventory_{}.csv'.format(datetime.datetime.now().strftime('%m%d%Y')),
                index=False)
    print('Successfully export csv file!')
    input('Press ENTER to continue.. ')


menu = OrderedDict([
    ('v', view_product_detail),
    ('s', search_product_by_id),
    ('a', add_new_product),
    ('b', backup_database)
])


if __name__ == "__main__":
    initialize()
    add_product_from_csv()
    menu_loop()
