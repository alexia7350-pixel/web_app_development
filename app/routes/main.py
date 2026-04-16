from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """ 首頁 """
    return render_template('index.html')

@main_bp.route('/recipes', methods=['GET'])
def list_recipes():
    return "食譜列表頁（尚未實作模板）"

@main_bp.route('/collections', methods=['GET'])
def collections():
    return "我的收藏夾（尚未實作模板）"
