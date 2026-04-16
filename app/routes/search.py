from flask import Blueprint

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/ingredients', methods=['GET', 'POST'])
def by_ingredients():
    """
    從冰箱現有食材反查食譜。
    GET: 渲染 UI。
    POST: 接受 JSON/Form 內含的食材陣列，查出配備這些食材的推薦食譜，最後在相同頁面下方渲染結果列表。
    渲染 `templates/search/ingredients.html`
    """
    pass
