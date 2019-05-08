# Python libraries
import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# Own libraries
from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Initializing the app whit a secret_key for JTW to encode
# and the information of the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('JAWSDB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = 'cayo'
api = Api(app)

# adds '/auth' endpoint to return a token when login in
jwt = JWT(app, authenticate, identity)

# Adding the RESOURCES to the API
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")

# Run the API with displaying errors on HTML for debugging
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
