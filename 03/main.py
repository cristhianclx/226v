from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:sistemas@127.0.0.1:5432/cibertec"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message {}>".format(self.id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    users_data = User.query.all()
    return render_template("users.html", users=users_data)


@app.route("/users/add", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        user = User(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            age=request.form["age"],
            city=request.form["city"],
        )
        db.session.add(user)
        db.session.commit()
        return render_template("users-add.html", message="User added")


@app.route("/users/<int:id>")
def users_by_id(id):
    user_data =User.query.get_or_404(id)
    return render_template("users-detail.html", user=user_data)


@app.route("/users/edit/<int:id>", methods=["GET", "POST"])
def users_edit_by_id(id):
    user_data =User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-edit.html", user=user_data)
    if request.method == "POST":
        user_data.first_name = request.form["first_name"]
        user_data.last_name = request.form["last_name"]
        user_data.age = request.form["age"]
        user_data.city = request.form["city"]
        db.session.add(user_data)
        db.session.commit()
        return render_template("users-edit.html", user=user_data, message="User updated")


@app.route("/users/delete/<int:id>", methods=["GET", "POST"])
def users_delete_by_id(id):
    user_data = User.query.get_or_404(id)
    if request.method == "GET":
        return render_template("users-delete.html", user=user_data)
    if request.method == "POST":
        db.session.delete(user_data)
        db.session.commit()
        return redirect(url_for('users'))