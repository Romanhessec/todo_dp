from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.task import Task
from app.utils.storage import load_tasks, save_task, delete_task, update_task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def index():
    """Display all tasks for current user"""
    filter_status = request.args.get('filter', 'all')
    sort_by = request.args.get('sort', 'none')
    
    # Load only current user's tasks
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Apply filtering
    if filter_status == 'pending':
        tasks = [task for task in tasks if task.status == 'pending']
    elif filter_status == 'completed':
        tasks = [task for task in tasks if task.status == 'completed']
    
    # Apply sorting
    if sort_by == 'title':
        tasks = sorted(tasks, key=lambda x: x.title.lower())
    elif sort_by == 'status':
        tasks = sorted(tasks, key=lambda x: (x.status, x.title.lower()))
    
    # Calculate task counts for current user only
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    total_count = len(all_tasks)
    completed_count = len([t for t in all_tasks if t.status == 'completed'])
    pending_count = len([t for t in all_tasks if t.status == 'pending'])
    
    return render_template('index.html', tasks=tasks, current_filter=filter_status, current_sort=sort_by,
                         total_count=total_count, completed_count=completed_count, pending_count=pending_count)

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    """Add a new task for current user"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    # Validate title is not empty
    if not title:
        filter_status = request.args.get('filter', 'all')
        sort_by = request.args.get('sort', 'none')
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        error = "Task title cannot be empty!"
        
        # Calculate task counts for error page
        total_count = len(tasks)
        completed_count = len([t for t in tasks if t.status == 'completed'])
        pending_count = len([t for t in tasks if t.status == 'pending'])
        
        return render_template('index.html', tasks=tasks, current_filter=filter_status, current_sort=sort_by, 
                             error=error, total_count=total_count, completed_count=completed_count, pending_count=pending_count)
    
    # Create task with current user's ID
    new_task = Task(title=title, description=description, user_id=current_user.id)
    save_task(new_task)
    
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    """Toggle task completion status"""
    # Verify task belongs to current user
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    if task.status == 'pending':
        task.mark_completed()
    else:
        task.mark_pending()
    
    update_task()
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task_route(task_id):
    """Delete a task"""
    # Verify task belongs to current user
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    delete_task(task)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/clear-completed', methods=['POST'])
@login_required
def clear_completed():
    """Delete all completed tasks for current user"""
    completed_tasks = Task.query.filter_by(user_id=current_user.id, status='completed').all()
    for task in completed_tasks:
        delete_task(task)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit a task"""
    # Verify task belongs to current user
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()
        
        # Validate title is not empty
        if not new_title:
            error = "Task title cannot be empty!"
            return render_template('edit_task.html', task=task, error=error)
        
        task.title = new_title
        task.description = request.form.get('description', '').strip()
        update_task()
        return redirect(url_for('tasks.index'))
    
    return render_template('edit_task.html', task=task)