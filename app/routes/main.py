from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁。
    查詢最新上架的數筆食譜並渲染 templates/index.html
    """
    pass

@main_bp.route('/recipes', methods=['GET'])
def list_recipes():
    """
    食譜列表。
    支援分類與純文字搜尋，渲染 templates/recipe/list.html
    """
    pass

@main_bp.route('/collections', methods=['GET'])
def collections():
    """
    個人收藏夾。
    需登入 (`@login_required`)，找出當前登入者所有的 Collection 並渲染 `templates/recipe/collections.html`
    """
    pass
