from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class ShowSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'title',
            'created_at',
        )
        model = Show
        datetimeformat = "%Y-%m-%d %H:%M:%S"


show_schema = ShowSchema()
shows_schema = ShowSchema(many = True)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())


class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"))
    show = db.relationship("Show", backref="show")

    likes = db.Column(db.Integer, nullable=True, default=0)
    dislikes = db.Column(db.Integer, nullable=True, default=0)


class JokeSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'event_name',
            'duration',
            'show_id',
            'likes',
            'dislikes',
        )
        model = Joke


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many=True)


class ShowsResource(Resource):
    def get(self):
        shows = Show.query.all()
        return shows_schema.dump(shows)

    def post(self):
        data = request.get_json()
        show = Show(**data)
        db.session.add(show)
        db.session.commit()
        return show_schema.dump(show), 201


class ShowIDResource(Resource):
    def get(self, id):
        show = Show.query.get_or_404(id)
        return show_schema.dump(show)

    def patch(self, id):
        show = Show.query.get_or_404(id)
        data = request.get_json()
        show.title = data.get("title", show.title)
        db.session.add(show)
        db.session.commit()
        return show_schema.dump(show)

    def delete(self, id):
        show = Show.query.get_or_404(id)
        db.session.delete(show)
        db.session.commit()
        return {}, 204


class JokeResource(Resource):
    def get(self, id):
        instance = Joke.query.get_or_404(id)
        return joke_schema.dump(instance)


class JokeLikeResource(Resource):
    def post(self, id):
        instance = Joke.query.get_or_404(id)
        if not instance.likes:
            instance.likes = 1
        else:
            instance.likes = instance.likes + 1
        db.session.add(instance)
        db.session.commit()
        return {}, 204


class JokeDislikeResource(Resource):
    def post(self, id):
        instance = Joke.query.get_or_404(id)
        if not instance.dislikes:
            instance.dislikes = 1
        else:
            instance.dislikes = instance.dislikes + 1
        db.session.add(instance)
        db.session.commit()
        return {}, 204


class JokesBestResource(Resource):
    def get(self):
        jokes = db.session.query(Joke).order_by(Joke.likes.desc()).limit(3).all()
        return jokes_schema.dump(jokes)


class JokesWorstResource(Resource):
    def get(self):
        jokes = db.session.query(Joke).order_by(Joke.dislikes.desc()).limit(3).all()
        return jokes_schema.dump(jokes)


api.add_resource(ShowsResource, "/shows") # GET, POST
api.add_resource(ShowIDResource, "/shows/<int:id>") # GET, PATCH, DELETE
api.add_resource(JokesBestResource, "/jokes/best")
api.add_resource(JokesWorstResource, "/jokes/worst")
api.add_resource(JokeResource, "/jokes/<int:id>")
api.add_resource(JokeLikeResource, "/jokes/<int:id>/like")
api.add_resource(JokeDislikeResource, "/jokes/<int:id>/dislike")


# /jokes: CRUD
# /artists: CRUD
# /shows: CRUD