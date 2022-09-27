from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {"todo1":"test"}

class TodoSimple(Resource):
    def get(self):
        return {"data":"hello world"}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/helloworld')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')