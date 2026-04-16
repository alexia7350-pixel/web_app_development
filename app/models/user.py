from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 與其他表的關聯
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    collections = db.relationship('Collection', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def get_all(cls):
        """取得所有記錄"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error in get_all (User): {e}")
            return []

    @classmethod
    def get_by_id(cls, user_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error in get_by_id (User): {e}")
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
            print(f"Error in create (User): {e}")
            raise e

    @classmethod
    def update(cls, user_id, data):
        """更新記錄"""
        try:
            record = cls.query.get(user_id)
            if record:
                for key, value in data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                db.session.commit()
                return record
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error in update (User): {e}")
            raise e

    @classmethod
    def delete(cls, user_id):
        """刪除記錄"""
        try:
            record = cls.query.get(user_id)
            if record:
                db.session.delete(record)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error in delete (User): {e}")
            raise e
