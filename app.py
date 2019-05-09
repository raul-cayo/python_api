# Python libraries
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
# Own libraries
from resources.user import UserRegister, User, UserLogin, TokenRefresh
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


# Cuztomazing callbacks and responses
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "The token has expired",
        "error": "xpired_token"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        "description": "Signature verification failed",
        "error": "invalid_token"
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback():
    return jsonify({
        "description": "Mising access token",
        "error": "unauthorized"
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        "description": "The token is not fresh",
        "error": "needs_fresh_token"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked",
        "error": "revoked_token"
    }), 401


# Adding the RESOURCES to the API
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")

# Run the API with displaying errors on HTML for debugging
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
