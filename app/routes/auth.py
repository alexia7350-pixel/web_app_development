from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    使用者註冊。
    GET: 渲染 templates/auth/register.html
    POST: 接收表單並將密碼雜湊後存入 DB，註冊完導向登入。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入處理。
    GET: 渲染 templates/auth/login.html
    POST: 驗證帳密並建立 session。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    登出處理，清除 session 並回到首頁。
    """
    pass
