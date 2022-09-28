from ast import Delete
from dataclasses import fields
from email.policy import strict
import marshal
from os import strerror
from xmlrpc.client import boolean
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

get_args = reqparse.RequestParser()
get_args.add_argument("id", type=str, help="Reqparse help: You need to send a id of the todo")

post_args = reqparse.RequestParser()
post_args.add_argument("name", type=str, help="Reqparse help: You need to send a name of the todo", required=True)

delete_args = reqparse.RequestParser()
delete_args.add_argument("id", type=str, help="Reqparse help: You need to send a id of the todo", required=True)

put_args = reqparse.RequestParser()
put_args.add_argument("id", type=int, help="Reqparse help: You need to send a name of the todo", required=True)
put_args.add_argument("name", type=str, help="Reqparse help: You need to send a name of the todo")
put_args.add_argument("done", type=bool, help="Reqparse help: You need to send a name of the todo")

serializing = {
    "id": fields.Integer,
    "name": fields.String,
    "done": fields.Boolean
}

class TodosApi(Resource):
    
    @marshal_with(serializing)
    def get(self):
        args = get_args.parse_args()
        if args["id"] == "":
            return Todos.query.all()
        else:
            new_todo = Todos.query.filter_by(id=args["id"]).first()
            return new_todo     

    def post(self):
        args = post_args.parse_args()
        new_todo = Todos(name=args["name"])
        if args["name"] == "":
            return {"message":"You need to send a name of the todo"}
        else:
            db.session.add(new_todo)
            db.session.commit()
            return {"message":"todo added"}
       

    def delete(self, id):
        args = delete_args.parse_args()
        new_todo = Todos.query.filter_by(id=args["id"]).first()
        if new_todo:
            db.session.delete(new_todo)
            db.session.commit()
            return {"message":"todo deleted"}
        else:
            abort(404, message="Could not find todo")
        
        
    
    def put(self):
        args = put_args.parse_args()
        new_todo = Todos.query.filter_by(id=args["id"]).first()
        if new_todo:
            if args["name"] == "":
                return {"message":"You need to send a name of the todo"}
            else:
                new_todo.name = args["name"]
                db.session.commit()
            return {"message":"todo updated"}
        else:
            abort(404, message="Could not find todo")
        

api.add_resource(TodosApi, '/Todos/','/Todos/<String: id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')