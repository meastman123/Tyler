import sqlite3

#def create_order_table():
#    conn = sqlite3.connect('shoes_shop.db')
#    cursor = conn.cursor()


#    cursor.execute('''
#               CREATE TABLE orders (
#                   id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   orderNum INTEGER NOT NULL,
#                   userId INTEGER NOT NULL,
#                   email TEXT NOT NULL,
#               )
#           ''')

# Insert test order
#    cursor.execute( "INSERT INTO orders (orderNum, userId, email) VALUES (?, ?, ?)",
#                    ('0', '0','test@email.com'))


# Create the user table and the admin user
#    conn.commit()
#    conn.close()



#create_order_table()


def create_order_table():
    conn = sqlite3.connect('shoes_shop.db')
    cursor = conn.cursor()

    # Create the users table if it does not exist

    cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orders INTEGER NOT NULL,
                user TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

    # Insert the admin user
    cursor.execute("INSERT INTO orders (orders, user, email) VALUES (?, ?, ?)",
                   ('admin', 'admin', 'admin@admin.com'))

    conn.commit()
    conn.close()

create_order_table()
