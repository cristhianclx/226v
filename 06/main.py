from flask import Flask, request
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///raw.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
           
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

api = Api(app)


class Enterprise(db.Model):
    __tablename__ = "enterprises"
    id = db.Column(
        db.String(11),
        primary_key=True,
        index=True,
        nullable=False,
    )
    name = db.Column(
        db.Text,
        nullable=False,
    )
    state = db.Column(
        db.Text,
        nullable=False,
    )
    condition = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<Enterprise id={self.id}>"
    

class EnterpriseSchema(ma.Schema):
    class Meta:
        model = Enterprise
        field = (
            "id",
            "name",
            "state",
            "condition",
        )


enterprise_schema = EnterpriseSchema()
enterprises_schema = EnterpriseSchema(many = True)

class PINGResource(Resource):
    def get(self):
        return {
            "message": "pong"
        }


class RUCResource(Resource):
    def get(self, id):
        enterprise = db.session.query(Enterprise).filter_by(id=id).first()
        return {
            "id": enterprise.id,
            "name": enterprise.name,
            "state": enterprise.state,
            "condition": enterprise.condition,
        }


api.add_resource(PINGResource, "/ping")
api.add_resource(RUCResource, "/RUC/<id>")