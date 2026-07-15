from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import RecipeForm
from recipe_logic.main import RecipeComparator


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/comparison", methods=['GET', 'POST'])
def comparison():
    form = RecipeForm()
    if form.validate_on_submit():
        flash("Recipe Comparison requested for recipe {}".format(form.firstRecipe.data))
        flash("and for recipe {}".format(form.secondRecipe.data))
        comparison = RecipeComparator(form.firstRecipe.data,form.secondRecipe.data )
        flash("Compared:".format(print(comparison.get_comparison()))) # this will display it all. I think need to think more about what should be returned then let website decide how it is displayed.
        # TODO return ingredient objects instead of the str, diff should maybe be some object that can be different amount, inherit properties from ingredient?
        return redirect(url_for("index"))
    return render_template("comparison.html", title="Compare Recipes", form=form)
