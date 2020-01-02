import sqlite3


class ItemModel():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM items WHERE name=?"
            result = cursor.execute(query, (name,))
            row = result.fetchone()
            if row is not None:
                return cls(*row)

    def insert(self):
        with sqlite3.connect("data.db") as connection:
            cursor = connection. cursor()
            query = "INSERT INTO items VALUES (?,?)"
            cursor.execute(query, (self.name, self.price))
            connection.commit()

    def update(self):
        with sqlite3.connect("data.db") as connection:
            cursor = connection. cursor()
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (self.price, self.name))
            connection.commit()
