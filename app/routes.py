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
    comparisonData = None
    recipe1 = None
    recipe2 = None
    if form.validate_on_submit():
        try:
            comparator = RecipeComparator(form.firstRecipe.data,
                                          form.secondRecipe.data)
            comparisonData = comparator.get_comparison()
            recipe1 = comparator.get_first_recipe()
            recipe2 = comparator.get_second_recipe()
        except ValueError as e:
            # Extract the URL from the error message
            msg = str(e)
            match = re.search(r'url:\s*(.+)', msg)
            failed_url = match.group(1).strip() if match else "unknown URL"
            flash(
                f"Could not process recipe from {failed_url}. The "
                f"site may be blocking requests or the URL is invalid.",
                "error")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}",
                  "error")


    return render_template("comparison.html",
                           title="Compare Recipes", form=form,
                           results = comparisonData,
                           recipe1=recipe1, recipe2=recipe2)
