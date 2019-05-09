# Python libraries
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
# Own libraries
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# Initializing the app whit a secret_key for JTW to encode
# and the information of the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('JAWSDB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = 'cayo'  # app.config["JWT_SECRET_KEY"]
api = Api(app)

# adds '/auth' endpoint to return a token when login in
jwt = JWTManager(app)


@jwt.user_claims_loader
# identity is taken from create_access_token
def add_claims_to_jwt(identity):
    # This should read from a database not hardcoding
    if identity == 4:
        return {"is_admin": True}
    return {"is_admin": False}


# Adding the RESOURCES to the API
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

# Run the API with displaying errors on HTML for debugging
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
