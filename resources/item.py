# Python libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
# Own libraries
from models.item import ItemModel


# Creating a Resource with the HTTP calls that can access it
class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be empty!"
    )

    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    # This decorator requires the HTTP call to have a token on the headers
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with "
                    "name '{}' already exists".format(name)}, 400

        data = self.parser.parse_args()
        # **data | price=data["price"], store_id=data["store_id"]
        item = ItemModel(name, **data)

        try:  # Should do this with every instruction to the database
            item.save_to_db()
        except Exception:
            # Internal server error
            return {"message": "An error ocurred inserting the item"}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin priviliges required"}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "Item not found"}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            # Lambda Function would be:
            #   list(map(lambda item: item.json(), ItemModel.query.all()))
            # List Comprehension is:
            return {"items": items}, 200
        return {
            "items": [item["name"] for item in items],
            "message": "More data available if you log in"
        }, 200
