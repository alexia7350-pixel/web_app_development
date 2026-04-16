from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 為了讓匯入更方便，在這裡預先暴露出所有的 Model
from .user import User
from .recipe import Recipe, Ingredient, RecipeIngredient
from .interaction import Collection, Comment
