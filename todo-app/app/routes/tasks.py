from flask import Blueprint, render_template, request, redirect, url_for
from app.models.task import Task
from app.utils.storage import load_tasks, save_tasks

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """Display all tasks"""
    filter_status = request.args.get('filter', 'all')
    sort_by = request.args.get('sort', 'none')
    
    tasks = load_tasks()
    
    # Apply filtering
    if filter_status == 'pending':
        tasks = [task for task in tasks if task.status == 'pending']
    elif filter_status == 'completed':
        tasks = [task for task in tasks if task.status == 'completed']
    
    # Apply sorting
    if sort_by == 'title':
        tasks = sorted(tasks, key=lambda x: x.title.lower())
    elif sort_by == 'status':
        # Sort by status (pending first), then by title within each status
        tasks = sorted(tasks, key=lambda x: (x.status, x.title.lower()))
    
    # Calculate task counts
    all_tasks = load_tasks()
    total_count = len(all_tasks)
    completed_count = len([t for t in all_tasks if t.status == 'completed'])
    pending_count = len([t for t in all_tasks if t.status == 'pending'])
    
    return render_template('index.html', tasks=tasks, current_filter=filter_status, current_sort=sort_by,
                         total_count=total_count, completed_count=completed_count, pending_count=pending_count)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """Add a new task"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    # Validate title is not empty
    if not title:
        filter_status = request.args.get('filter', 'all')
        sort_by = request.args.get('sort', 'none')
        tasks = load_tasks()
        error = "Task title cannot be empty!"
        return render_template('index.html', tasks=tasks, current_filter=filter_status, current_sort=sort_by, error=error)
    
    tasks = load_tasks()
    new_task = Task(title=title, description=description)
    tasks.append(new_task)
    save_tasks(tasks)
    
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """Toggle task completion status"""
    tasks = load_tasks()
    
    for task in tasks:
        if task.task_id == task_id:
            if task.status == 'pending':
                task.mark_completed()
            else:
                task.mark_pending()
            break
    
    save_tasks(tasks)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    tasks = [task for task in tasks if task.task_id != task_id]
    save_tasks(tasks)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit a task"""
    tasks = load_tasks()
    task = None
    
    for t in tasks:
        if t.task_id == task_id:
            task = t
            break
    
    if not task:
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()
        
        # Validate title is not empty
        if not new_title:
            error = "Task title cannot be empty!"
            return render_template('edit_task.html', task=task, error=error)
        
        task.title = new_title
        task.description = request.form.get('description', '').strip()
        save_tasks(tasks)
        return redirect(url_for('tasks.index'))
    
    return render_template('edit_task.html', task=task)