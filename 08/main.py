from flask import Flask, request, render_template, redirect, url_for
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
    name = db.Column(db.String(50))
    persons = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    messages = db.relationship("Message", back_populates="conversation")

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
    conversations = Conversation.query.all()
    data = []
    for c in conversations:
        participants = len(db.session.query(Message.nickname, db.func.count(Message.nickname)).filter(Message.conversation_id == c.id).group_by(Message.nickname).all())
        data.append({
            "conversation": c,
            "participants": participants,
        })
    return render_template("index.html", data=data)


@app.route("/conversations/create", methods=["GET", "POST"])
def conversations_create():
    if request.method == "GET":
        return render_template("conversations-create.html")
    if request.method == "POST":
        conversation = Conversation(
            id = request.form["id"],
            name = request.form["name"],
            persons = request.form["persons"],
        )
        db.session.add(conversation)
        db.session.commit()
        return redirect(url_for('conversations', id=conversation.id))


@app.route("/conversations/<id>")
def conversations(id):
    conversation = Conversation.query.filter_by(id = id).first()
    participants = len(db.session.query(Message.nickname, db.func.count(Message.nickname)).filter(Message.conversation_id == conversation.id).group_by(Message.nickname).all())
    if conversation.persons <= participants:
        return redirect(url_for('index'))
    messages = Message.query.filter_by(conversation = conversation)
    return render_template("conversations.html", conversation=conversation, id=id, messages=messages)


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