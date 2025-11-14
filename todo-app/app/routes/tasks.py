from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.task import Task
from app.utils.storage import load_tasks, save_tasks

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.form
    new_task = Task(title=data['title'], description=data.get('description', ''), status='pending')
    tasks = load_tasks()
    tasks.append(new_task.to_dict())
    save_tasks(tasks)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    data = request.json
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['description'] = data.get('description', task['description'])
            save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return jsonify({'message': 'Task deleted'}), 200