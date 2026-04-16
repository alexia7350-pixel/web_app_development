from datetime import datetime
from . import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade='all, delete-orphan')
    collections = db.relationship('Collection', backref='recipe', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error in get_all (Recipe): {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            print(f"Error in get_by_id (Recipe): {e}")
            return None

    @classmethod
    def create(cls, data):
        """新增一筆記錄"""
        try:
            new_record = cls(**data)
            db.session.add(new_record)
            db.session.commit()
            return new_record
        except Exception as e:
            db.session.rollback()
            print(f"Error in create (Recipe): {e}")
            raise e

    @classmethod
    def update(cls, recipe_id, data):
        """更新記錄"""
        try:
            record = cls.query.get(recipe_id)
            if record:
                for key, value in data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                db.session.commit()
                return record
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error in update (Recipe): {e}")
            raise e

    @classmethod
    def delete(cls, recipe_id):
        """刪除記錄"""
        try:
            record = cls.query.get(recipe_id)
            if record:
                db.session.delete(record)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error in delete (Recipe): {e}")
            raise e

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    recipe_ingredients = db.relationship('RecipeIngredient', backref='ingredient', lazy=True)

    @classmethod
    def get_all(cls):
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error in get_all (Ingredient): {e}")
            return []

    @classmethod
    def get_by_name(cls, name):
        try:
            return cls.query.filter_by(name=name).first()
        except Exception as e:
            return None

    @classmethod
    def create(cls, data):
        try:
            new_record = cls(**data)
            db.session.add(new_record)
            db.session.commit()
            return new_record
        except Exception as e:
            db.session.rollback()
            print(f"Error in create (Ingredient): {e}")
            raise e

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    amount = db.Column(db.String(100))

    @classmethod
    def create(cls, data):
        try:
            new_record = cls(**data)
            db.session.add(new_record)
            db.session.commit()
            return new_record
        except Exception as e:
            db.session.rollback()
            print(f"Error in create (RecipeIngredient): {e}")
            raise e
