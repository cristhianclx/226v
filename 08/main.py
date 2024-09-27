from flask import Flask, request, render_template
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Message {self.id}>"
    

class MessageSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "nickname",
            "message",
            "created_at",
        )
        model = Message
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/")
def index():
    messages = Message.query.all()
    return render_template("index.html", messages=messages)


@socketio.on("welcome")
def handle_welcome(data):
    print("receive data on welcome: {}".format(data))


@socketio.on("messages")
def handle_messages(data):
    print("receive data on message: {}".format(data))
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    socketio.emit("messages-responses", message_schema.dump(message))


# (1) http://127.0.0.1:5000/conversations/abcde
#     # crear model Conversation
#     Message -> añadir el campo conversation
# (2) Message -> (importance), low, high, si es high mostrar una etiqueta que diga high