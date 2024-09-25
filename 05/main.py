from flask import Flask, request
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

api = Api(app)


class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    city = db.Column(db.String(120))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User {}>".format(self.id)
    

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))
    priority = db.Column(db.String(1))
    importance = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.id)


class UserForTableSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
        )
        model = User


user_for_table_schema = UserForTableSchema()
users_for_table_schema = UserForTableSchema(many = True)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "age",
            "city",
            "created_at",
        )
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class PINGResource(Resource):

    def get(self):
        return {
            "message": "pong"
        }
    

class UsersForTableResource(Resource):
    def get(self):
        users = User.query.all()
        return users_for_table_schema.dump(users)


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
    
    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class UserIDResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.dump(user)
    
    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.age = data.get("age", user.age)
        user.city = data.get("city", user.city)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
    
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204


api.add_resource(PINGResource, "/ping")
api.add_resource(UsersForTableResource, "/users-for-table")
api.add_resource(UsersResource, "/users")
api.add_resource(UserIDResource, "/users/<int:id>")


# GET /messages 
# POST /messages 
# GET /messages/<int:id> 
# PATCH /messages/<int:id> 
# DELETE /messages/<int:id>

# GET /messages-by-user/<int:user_id> 