#! /opt/miniconda3/bin/python3
'''
tracker is an app that maintains a list of personal
financial transactions.

It uses Object Relational Mappings (ORM)
to abstract out the database operations from the
UI/UX code.

The ORM, Category, will map SQL rows with the schema
  (rowid, category, description)
to Python Dictionaries as follows:

(5,'rent','monthly rent payments') <-->

{rowid:5,
 category:'rent',
 description:'monthly rent payments'
 }

Likewise, the ORM, Transaction will mirror the database with
columns:
amount, category, date (yyyymmdd), description

In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/tracker.db

Note the actual implementation of the ORM is hidden and so it
could be replaced with PostgreSQL or Pandas or straight python lists

'''

from transactions import Transaction
from category import Category

transactions = Transaction('tracker.db')
category = Category('tracker.db')


# here is the menu for the tracker app

menu = '''
0. quit
1. show categories
2. add category
3. modify category
4. show transactions
5. add transaction
6. delete transaction
7. summarize transactions by date
8. summarize transactions by month
9. summarize transactions by year
10. summarize transactions by category
11. print this menu
'''



def process_choice(choice):
    ''' processes the user's choice '''
    if choice=='0':
        return
    elif choice=='1':
        cats = category.select_all()
        print_categories(cats)
    elif choice=='2':
        name = input("category name: ")
        desc = input("category description: ")
        cat = {'name':name, 'desc':desc}
        category.add(cat)
    elif choice=='3':
        print("modifying category")
        rowid = int(input("rowid: "))
        name = input("new category name: ")
        desc = input("new category description: ")
        cat = {'name':name, 'desc':desc}
        category.update(rowid,cat)
    elif choice == '4':
        print('showing transactions')
        trans = transactions.select_all()
        print_transactions(trans)
    elif choice =='5':
        item_no = input("Name the transaction: ")
        desc = input("Give a description to the transaction: ")
        amount = float((input("Enter in price: ")))
        categ = input("Enter category of: ")
        date = (input("Enter the date of the transaction: "))
        tran = {'item #':item_no, 'amount': amount , 'category': categ , 'date':date, 'description':desc}
        transactions.add(tran)
    elif choice == '6':
        row = input('Row id to delete: ')
        transactions.delete(row)
    elif choice == '7':
        trans = transactions.summarize()
        print("%-10s %-10s"%('amount','date'))
        print('-'*40)
        for tran in trans:
            values = tuple(tran.values())
            print("%-10d %-10s"%values)
    elif choice == '8':
        trans = transactions.summarize_month()
        print("%-10s %-10s"%('amount','Month'))
        print('-'*40)
        for tran in trans:
            values = tuple(tran.values())
            print("%-10d %-10s"%values)
    elif choice == '9':
        trans = transactions.summarize_year()
        print("%-10s %-10s"%('amount','Year'))
        print('-'*40)
        for tran in trans:
            values = tuple(tran.values())
            print("%-10d %-10s"%values)
    elif choice == '10':
        trans = transactions.summarize_category()
        print("%-10s %-10s"%('amount','category'))
        print('-'*40)
        for tran in trans:
            values = tuple(tran.values())
            print("%-10d %-10s"%values)
    elif choice == '11':
        print(menu)

    else:
        print("choice",choice,"not yet implemented")
    choice = input("> ")
    return choice

def toplevel():
    ''' handle the user's choice, read the command args and process them'''
    print(menu)
    choice = input("> ")
    while choice !='0' :
        choice = process_choice(choice)
    print('bye')

#
# here are some helper functions
#

def print_transactions(items):
    ''' print the transactions '''
    if len(items)==0:
        print('no items to print')
        return
    print('\n')
    print("%-3s %-10s %-10s %-10s %-10s %-30s"%(
       'id', 'item #','amount','category','date','description'))
    print('-'*40)
    for item in items:
        values = tuple(item.values())
        print("%-3d %-10s %-10d %-10s %-10s %-30s"%values)

def print_category(cat):
    '''prints the categories'''
    print("%-3d %-10s %-30s"%(cat['rowid'],cat['name'],cat['desc']))

def print_categories(cats):
    '''prints the categories'''
    print("%-3s %-10s %-30s"%("id","name","description"))
    print('-'*45)
    for cat in cats:
        print_category(cat)


# here is the main call!

toplevel()
