import sqlite3


class Table:
    def __init__(self, db, table, columns):
        self.db = db
        self.cursor = self.db.cursor()
        self.table = table

        self.query = f"CREATE TABLE {self.table} ({columns})"
        self.cursor.execute(self.query)

    def insert_values(self, columns: tuple, values: list):
        query = f"INSERT INTO {self.table} {str(columns) if len(columns)>1 else '('+columns[0]+')'} VALUES ({','.join(['?' for _ in range(len(columns))])})"
        self.cursor.executemany(query, values)
        self.db.commit()


# Insert values
db = sqlite3.connect("server.db")

clients = Table(db, "Clients", "id_users INTEGER, user_name TEXT, PRIMARY KEY(id_users)")
clients.insert_values(("user_name",), [("Иван",), ("Константин",), ("Дмитрий",), ("Александр",)])

products = Table(db, "Products", "id_product INTEGER, product_name TEXT, price INTEGER, PRIMARY KEY(id_product)")
products.insert_values(("product_name", "price"), [("Мяч",299.99),
                                                   ("Ручка",18),
                                                   ("Кружка",159.87),
                                                   ("Монитор",18000),
                                                   ("Телефон",9999.9),
                                                   ("Кофе",159)])

orders_rows = [(2,2),(2,5),(2,1),(1,1),(1,3),(1,6),(1,2),(4,5),(3,6),(3,3),(1,5)]
orders = Table(db, "Orders", "id_Order INTEGER, id_users TEXT, id_product INTEGER, Order_name TEXT, PRIMARY KEY(id_Order)")
orders.insert_values(("id_users", "id_product", "Order_name"),[(*j, "Заказ {}".format(i+1)) for i,j in enumerate(orders_rows)])

# Queries
cursor = db.cursor()

## Список клиентов с общей суммой их покупок
query = 'SELECT Clients.user_name AS "Клиент", sum(Products.price) AS "Общая сумма покупок" FROM Clients JOIN Orders ON Clients.id_users = Orders.id_users JOIN Products ON Products.id_product = Orders.id_product GROUP BY Clients.user_name;'
print(cursor.execute(query).fetchall())

## Список клиентов, которые купили телефон
query = 'SELECT Clients.user_name AS "Клиент" FROM Clients JOIN Orders ON Clients.id_users = Orders.id_users JOIN Products ON Products.id_product = Orders.id_product WHERE Products.product_name=="Телефон";'
print(cursor.execute(query).fetchall())

## Список товаров с количеством их заказов
query = 'SELECT Products.product_name as "Товар", count(Orders.id_product) FROM Products JOIN Orders ON Products.id_product=Orders.id_product GROUP BY Orders.id_product;'
print(cursor.execute(query).fetchall())
