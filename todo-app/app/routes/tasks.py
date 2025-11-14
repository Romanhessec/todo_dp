from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.task import Task
from app.utils.storage import load_tasks, save_tasks

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def index():
    filter_status = request.args.get('filter', 'all')  # Get filter parameter, default to 'all'
    tasks = load_tasks()
    
    # Filter tasks based on status
    if filter_status == 'pending':
        tasks = [task for task in tasks if task['status'] == 'pending']
    elif filter_status == 'completed':
        tasks = [task for task in tasks if task['status'] == 'completed']
    # If 'all', show all tasks (no filtering needed)
    
    return render_template('index.html', tasks=tasks, current_filter=filter_status)

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

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            # Toggle status between pending and completed
            task['status'] = 'completed' if task['status'] == 'pending' else 'pending'
            save_tasks(tasks)
            return redirect(url_for('tasks.index'))
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task_post(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task_form(task_id):
    tasks = load_tasks()
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break
    if task:
        return render_template('edit_task.html', task=task)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['POST'])
def edit_task_submit(task_id):
    data = request.form
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['description'] = data.get('description', task['description'])
            save_tasks(tasks)
            return redirect(url_for('tasks.index'))
    return redirect(url_for('tasks.index'))