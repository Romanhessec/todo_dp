from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.storage import DataManager

# Singleton DataManager orchestrates Factory + Command + Observer patterns
data_manager = DataManager()

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
@login_required
def index():
    """Display all tasks for current user with multi-dimensional filtering"""
    filter_status = request.args.get('filter', 'all')
    filter_type = request.args.get('type', 'all')
    sort_by = request.args.get('sort', 'none')

    tasks = data_manager.get_tasks(current_user.id, filter_status, filter_type, sort_by)
    stats = data_manager.get_stats(current_user.id)
    history_state = data_manager.history_state(current_user.id)

    return render_template(
        'index.html',
        tasks=tasks,
        current_filter=filter_status,
        current_type=filter_type,
        current_sort=sort_by,
        total_count=stats['total'],
        completed_count=stats['completed'],
        pending_count=stats['pending'],
        history_state=history_state,
    )

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    """Add a new task for current user"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    task_type = request.form.get('task_type', 'simple')
    
    # Validate title is not empty
    if not title:
        filter_status = request.args.get('filter', 'all')
        sort_by = request.args.get('sort', 'none')
        tasks = data_manager.get_tasks(current_user.id, filter_status, sort_by)
        error = "Task title cannot be empty!"
        
        # Calculate task counts for error page
        stats = data_manager.get_stats(current_user.id)
        
        return render_template(
            'index.html',
            tasks=tasks,
            current_filter=filter_status,
            current_sort=sort_by,
            error=error,
            total_count=stats['total'],
            completed_count=stats['completed'],
            pending_count=stats['pending'],
            history_state=data_manager.history_state(current_user.id),
        )
    
    # Factory Method creates the right Task flavor
    data_manager.add_task(current_user.id, title, description, task_type)
    
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    """Toggle task completion status"""
    data_manager.toggle_task(current_user.id, task_id)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task_route(task_id):
    """Delete a task"""
    data_manager.delete_task(current_user.id, task_id)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/clear-completed', methods=['POST'])
@login_required
def clear_completed():
    """Delete all completed tasks for current user"""
    data_manager.clear_completed(current_user.id)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit a task"""
    task = data_manager.get_task_for_user(task_id, current_user.id)
    
    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()
        
        # Validate title is not empty
        if not new_title:
            error = "Task title cannot be empty!"
            return render_template('edit_task.html', task=task, error=error)
        
        new_description = request.form.get('description', '').strip()
        data_manager.edit_task(current_user.id, task_id, new_title, new_description)
        return redirect(url_for('tasks.index'))
    
    return render_template('edit_task.html', task=task)


@tasks_bp.route('/tasks/undo', methods=['POST'])
@login_required
def undo_last():
    """Undo last command (Command pattern history)."""
    if not data_manager.undo(current_user.id):
        flash('Nothing to undo.', 'info')
    return redirect(url_for('tasks.index'))


@tasks_bp.route('/tasks/redo', methods=['POST'])
@login_required
def redo_last():
    """Redo last undone command."""
    if not data_manager.redo(current_user.id):
        flash('Nothing to redo.', 'info')
    return redirect(url_for('tasks.index'))