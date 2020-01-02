from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask import request
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True,
                        help="This field cannot be left blank")

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404
        # item = next(filter(lambda x: x["name"] == name, items), None)
        # # for item in items:
        # #     if item["name"] == name:
        # #         # with flask_restful, there is no need to use jsonify
        # #         return item
        # return {"item": item}, 200 if item else 404

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM items WHERE name=?"
            result = cursor.execute(query, (name,))
            row = result.fetchone()
            if row is not None:
                return {"item": {"name": row[0], "price": row[1]}}

    def post(self, name):
        if Item.find_by_name(name) is not None:
            return {"error": f"an item with name '{name}' already exists"}, 400
        # if next(filter(lambda x: x["name"] == name, items), None):

        # force=true, when passed to get_json does not process the header. It forces the request to be json
        request_data = Item.parser.parse_args()
        item = {"name": name, "price": request_data["price"]}
        try:
            Item.insert(item)
        except:
            return {"message": "An error occured inserting the item"}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        with sqlite3.connect("data.db") as connection:
            cursor = connection. cursor()
            query = "INSERT INTO items VALUES (?,?)"
            cursor.execute(query, (item["name"], item["price"]))
            connection.commit()

    @classmethod
    def update(cls, item):
        with sqlite3.connect("data.db") as connection:
            cursor = connection. cursor()
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (item["price"], item["name"]))
            connection.commit()

    def delete(self, name):
        with sqlite3.connect("data.db") as connection:
            cursor = connection. cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
        # Tell python that items variable is the global variable that we should use
        # global items
        # items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {"name": name, "price": request_data["price"]}
        # item = next(filter(lambda x: x["name"] == name, items), None)
        try:
            if item is None:
                # item = {"name": name, "price": request_data["price"]}
                # items.append(item)
                Item.insert(updated_item)
            else:
                Item.update(updated_item)
        except:
            return {"message": "an error occurred during db operation"}, 500
        return updated_item


class ItemList(Resource):
    def get(self):
        with sqlite3.connect("data.db") as connection:
            cursor = connection. cursor()
            query = "SELECT * FROM items"
            result = cursor.execute(query)
            items = []
            for row in result:
                items.append({"name": row[0], "price": row[1]})
            connection.commit()
            return {"items": items}
