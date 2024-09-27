from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "123456"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "cibertec" or password != "test":
        return {"msg": "Bad username or password"}, 401
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}


@app.route("/non-protected", methods=["GET"])
def non_protected():
    return {"status": "non-protected"}


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {"status": "protected", "user": current_user}