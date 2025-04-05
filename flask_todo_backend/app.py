from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

# Environment config (optional for local dev)
# from dotenv import load_dotenv
# load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS setup (you can add localhost for dev too)
CORS(app, resources={r"/todos*": {"origins": [
    "https://flask-to-do-kcw6.onrender.com",
    "http://localhost:3000"
]}})

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Create DB table
with app.app_context():
    db.create_all()

# Root route (optional)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Flask ToDo API"}), 200

# Todos route
@app.route('/todos', methods=['GET', 'POST', 'OPTIONS'])
def todos():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'GET':
        todos = Todo.query.all()
        return jsonify([{"id": t.id, "task": t.task, "done": t.done} for t in todos])

    if request.method == 'POST':
        data = request.json
        new_todo = Todo(task=data['task'])
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"message": "To do added", "id": new_todo.id})

# Delete route
@app.route('/todos/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete_todo(id):
    if request.method == 'OPTIONS':
        return '', 200

    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

# Update route
@app.route('/todos/<int:id>', methods=['PUT', 'OPTIONS'])
def update_todo(id):
    if request.method == 'OPTIONS':
        return '', 200

    todo = Todo.query.get(id)
    if todo:
        todo.done = request.json.get('done', todo.done)
        db.session.commit()
        return jsonify({"message": "Task Updated"})
    return jsonify({"error": "Task not Found"}), 404

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)