import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True,
                        help="Enter a username, cannot be blank")
    parser.add_argument("password", type=str, required=True,
                        help="Enter a password, cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]) is not None:
            # The user is already existing
            return {"message": "User already exists"}, 400
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (NULL,?,?)"
            cursor.execute(query, (data["username"], data["password"]))
            connection.commit()
            # connection.close()
            return {"message": "User created sucessfully"}, 201
