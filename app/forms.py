from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import URL, Optional

class RecipeForm(FlaskForm):
    firstRecipe = URLField("Recipe 1 URL", validators=[Optional(),URL()])
    firstRecipeText = TextAreaField("Recipe 1 Text")
    type_a = HiddenField("Type A", default="url")

    secondRecipe = URLField("Recipe 2 URL", validators=[Optional(), URL()])
    secondRecipeText = TextAreaField("Recipe 2 Text")
    type_b = HiddenField("Type B", default="url")
    submit = SubmitField("Compare Recipes")
