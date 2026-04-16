from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def require_admin():
    """
    實作這層防護，確保以下所有 route 只有 role == 'admin' 可進。
    """
    pass

@admin_bp.route('/', methods=['GET'])
def index():
    """ 後台 Dashboard，看基礎數據。 """
    pass

@admin_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def force_edit_recipe(id):
    """ 管理員可以不限身分去編輯任何違規的食譜。 """
    pass

@admin_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def force_delete_recipe(id):
    """ 管理員強制下架食譜。 """
    pass

@admin_bp.route('/users', methods=['GET', 'POST'])
def manage_users():
    """ 
    檢視並管理使用者狀態。
    可以更新 user 身分或是進行停權等。 
    """
    pass
