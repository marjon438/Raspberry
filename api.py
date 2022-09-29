
from dataclasses import fields
from flask import Flask
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort, inputs
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)

#db.create_all()

get_args = reqparse.RequestParser()
get_args.add_argument("id", type=int, help="Reqparse help: You need to send a id of the todo")

post_args = reqparse.RequestParser()
post_args.add_argument("title", type=str, help="Reqparse help: You need to send a title of the todo", required=True)

delete_args = reqparse.RequestParser()
delete_args.add_argument("id", type=int, help="Reqparse help: You need to send a id of the todo", required=True)

put_args = reqparse.RequestParser()
put_args.add_argument("id", type=int, help="Reqparse help: You need to send a title of the todo", required=True)
put_args.add_argument("title", type=str, help="Reqparse help: You need to send a title of the todo")
put_args.add_argument("done", type=inputs.boolean, help="Reqparse help: You need to send a title of the todo")

serializing = {
    "id": fields.Integer,
    "title": fields.String,
    "done": fields.Boolean
}

class TodosApi(Resource):
    
    @marshal_with(serializing)
    def get(self):
        return Todos.query.all()

    @marshal_with(serializing)
    def post(self):
        args = post_args.parse_args()
        new_todo = Todos(title=args["title"])
        db.session.add(new_todo)
        db.session.commit()
        return Todos.query.all()
       
    @marshal_with(serializing)
    def delete(self):
        args = delete_args.parse_args()
        new_todo = Todos.query.filter_by(id=args["id"]).first()
        if new_todo:
            db.session.delete(new_todo)
            db.session.commit()
            return Todos.query.all()
        else:
            abort(404, message="Could not find todo")
        
    @marshal_with(serializing)
    def put(self):
        args = put_args.parse_args()
        new_todo = Todos.query.filter_by(id=args["id"]).first()
        if new_todo:
            if args["id"] == "":
                return {"message":"You need to send a id of the todo"}
            else:
                if args["title"] == "" or args["done"] == "":
                    return {"message":"You need to send a title and done of the todo"}
                else:
                    new_todo.done = args["done"]
                    new_todo.title = args["title"]
                    db.session.commit()
                return Todos.query.all()
        else:
            abort(404, message="Could not find todo")
        

api.add_resource(TodosApi, '/Todos/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')