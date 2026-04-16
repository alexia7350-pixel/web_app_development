import os
from flask import Flask
from config import Config
from app.models import db

def create_app(config_class=Config):
    # 設定根目錄
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'app', 'templates')
    static_dir = os.path.join(base_dir, 'app', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # 初始化副件
    db.init_app(app)

    # 註冊 Blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.recipe import recipe_bp
    from app.routes.search import search_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(admin_bp)

    # 確認 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database Initialized successfully.")
