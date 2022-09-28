from ast import Delete
from dataclasses import fields
from email.policy import strict
import marshal
from os import strerror
from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)

db.create_all()

put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="Reqparse help: You need to send a name of the todo")


serializing = {
    "id": fields.Integer,
    "name": fields.String,
    "done": fields.Boolean
}

class TodosApi(Resource):
    
    @marshal_with(serializing)
    def get(self):
        args = put_args.parse_args()
        if args["id"] == "":
            return Todos.query.all()
        else:
            new_todo = Todos.query.filter_by(id=args["id"]).first()
            return new_todo
            
        

    def post(self):
        args = put_args.parse_args()
        new_todo = Todos(name=args["name"])
        if args["name"] == "":
            return {"message":"You need to send a name of the video"}
        else:
            db.session.add(new_todo)
            db.session.commit()
            return {"message":"Video added"}
            

        

    def delete(self):
        args = delete_args.reqparse.RequestParser()
        delete_args.add_argument("id", type=str, help="Reqparse help: You need to send id of the video", required = True)
        args = delete_args.parse_args()
        new_todo = Todos.query.filter_by(id=args["id"]).first()
        if new_todo:
            db.session.delete(new_todo)
            db.session.commit()
            return {"message":"Video deleted"}
        else:
            abort(404, message="Could not find video")
        
        
    
    def put(self):
        args = put_args.parse_args()
        new_todo = Todos.query.filter_by(id=args["id"]).first()
        if new_todo:
            if args["name"] == "":
                return {"message":"You need to send a name of the video"}
            else:
                new_todo.name = args["name"]
                db.session.commit()
            return {"message":"Video updated"}
        else:
            abort(404, message="Could not find video")
        

api.add_resource(TodoSimple, '/helloworld/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')