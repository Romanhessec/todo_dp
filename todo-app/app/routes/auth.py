from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user - simple function, no patterns"""
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Simple validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user - simple instantiation, no Factory pattern
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Save user
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user - simple function, no patterns"""
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # Simple validation
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return redirect(url_for('auth.login'))
        
        # Find user - simple query
        user = User.query.filter_by(username=username).first()
        
        # Check password - simple if statement
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('tasks.index'))
        
        flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout user - simple function"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
