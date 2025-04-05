from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
app = Flask(__name__)

CORS(app,
     origins=["https://flask-to-do-kcw6.onrender.com"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# model
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200),nullable = False)
    done =db.Column(db.Boolean,default=False)
# table creation
with app.app_context():
    db.create_all()

# Routes and functions

@app.route('/todos',methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    print(todos)
    return jsonify([{"id": t.id, "task": t.task, "done": t.done} for t in todos])

@app.route('/todos',methods=['POST'])
def add_todos():
    data = request.json
    print(data)
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message":"To do added"})

@app.route('/todos/<int:id>',methods=['DELETE'])
def delete_todos(id):
    print(id)
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message":"Task deleted"})
    return jsonify({"error":"Task not found"}),404

@app.route('/todos/<int:id>',methods = ['PUT'])
def update_todo(id):
    print('this is id',id)
    todo = Todo.query.get(id)
    if todo:
        todo.done =  request.json.get('done',todo.done)
        db.session.commit()
        return jsonify({"message":"Task Updated"})
    return jsonify({"error":"Task not Found"}),404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)