from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, URL

class RecipeForm(FlaskForm):
    firstRecipe = URLField("Recipe", validators=[DataRequired(), URL()])
    secondRecipe = URLField("Recipe", validators=[DataRequired(), URL()])
    submit = SubmitField("Compare Recipes")
