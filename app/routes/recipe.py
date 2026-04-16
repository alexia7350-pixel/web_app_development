from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@recipe_bp.route('/<int:id>', methods=['GET'])
def detail(id):
    """
    食譜詳細資料。
    載入食譜、互動評論與食材清單。渲染 `templates/recipe/detail.html`
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    新增自創食譜 (須登入)。
    GET: 渲染表單。
    POST: 處理表單、儲存圖片、分配食材中介表。
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯食譜 (須為原作者)。
    GET: 載入既有表單資料。
    POST: 更新進資料庫。
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除自己食譜。利用 POST 避免 crawler 誤點擊。
    """
    pass

@recipe_bp.route('/<int:id>/collect', methods=['POST'])
def collect(id):
    """
    將食譜從自己的收藏夾加入或移除。
    自動由 DB 原狀態決定是 Insert 還是 Delete。
    """
    pass

@recipe_bp.route('/<int:id>/comment', methods=['POST'])
def comment(id):
    """
    提交留言與評分 (1-5)。存入 Comment model。
    """
    pass
