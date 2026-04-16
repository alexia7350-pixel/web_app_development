from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    使用者註冊。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('所有欄位皆為必填', 'danger')
            return redirect(url_for('auth.register'))
            
        # Check if user exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('此帳號或 Email 已經被註冊過！', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        try:
            User.create({'username': username, 'email': email, 'password_hash': hashed_password})
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('註冊失敗，系統發生錯誤。', 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入處理。
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # 建立 session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'登入成功！歡迎回來，{user.username}。', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email 或密碼錯誤，請重新輸入。', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    登出處理，清除 session 並回到首頁。
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))
