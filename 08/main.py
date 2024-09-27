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


class Conversation(db.Model):
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Conversation {self.id}>"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    importance = db.Column(db.String(10), nullable=True, default="low")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id"))
    conversation = db.relationship("Conversation", backref="conversation")

    def __repr__(self):
        return f"<Message {self.id}>"
    

class MessageSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "nickname",
            "message",
            "importance",
            "created_at",
        )
        model = Message
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/")
def index():
    return {}


@app.route("/conversations/<id>")
def conversations(id):
    conversation = Conversation.query.filter_by(id = id).first()
    if not conversation:
        conversation = Conversation(id = id)
        db.session.add(conversation)
        db.session.commit()
    messages = Message.query.filter_by(conversation = conversation)
    return render_template("conversations.html", id=id, messages=messages)


@socketio.on("welcome")
def handle_welcome(data):
    print("receive data on welcome: {}".format(data))


@socketio.on("messages")
def handle_messages(data):
    print("receive data on message: {}".format(data))
    message = Message(**data)
    db.session.add(message)
    db.session.commit()
    socketio.emit("messages-responses-{}".format(message.conversation_id), message_schema.dump(message))