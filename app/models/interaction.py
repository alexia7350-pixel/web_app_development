from datetime import datetime
from . import db

class Collection(db.Model):
    __tablename__ = 'collections'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_by_user(cls, user_id):
        try:
            return cls.query.filter_by(user_id=user_id).all()
        except Exception as e:
            return []
            
    @classmethod
    def create(cls, data):
        try:
            # 確保不會重複收藏
            existing = cls.query.filter_by(user_id=data.get('user_id'), recipe_id=data.get('recipe_id')).first()
            if existing:
                return existing
            new_record = cls(**data)
            db.session.add(new_record)
            db.session.commit()
            return new_record
        except Exception as e:
            db.session.rollback()
            print(f"Error in create (Collection): {e}")
            raise e

    @classmethod
    def delete(cls, user_id, recipe_id):
        try:
            record = cls.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
            if record:
                db.session.delete(record)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error in delete (Collection): {e}")
            raise e


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    rating = db.Column(db.Integer)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_by_recipe(cls, recipe_id):
        try:
            return cls.query.filter_by(recipe_id=recipe_id).all()
        except Exception as e:
            return []

    @classmethod
    def create(cls, data):
        try:
            new_record = cls(**data)
            db.session.add(new_record)
            db.session.commit()
            return new_record
        except Exception as e:
            db.session.rollback()
            print(f"Error in create (Comment): {e}")
            raise e

    @classmethod
    def delete(cls, comment_id):
        try:
            record = cls.query.get(comment_id)
            if record:
                db.session.delete(record)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error in delete (Comment): {e}")
            raise e
