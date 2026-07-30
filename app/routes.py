from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import RecipeForm
from recipe_logic.main import RecipeComparator, RecipeExtractionError


@app.route("/")
@app.route("/index")
def index():
    # return render_template("index.html", title="Home")
    return redirect(url_for("comparison"))

@app.route("/comparison", methods=['GET', 'POST'])
def comparison():
    if request.method == "POST":
        # make copy of form
        form_data = request.form.copy()

        # strip inactive input fields
        if form_data.get('type_a') != 'url':
            form_data['firstRecipe'] = ''
        else:
            form_data['firstRecipeText'] = ''

        if form_data.get('type_b') != 'url':
            form_data['secondRecipe'] = ''
        else:
            form_data['secondRecipeText'] = ''

        form = RecipeForm(formdata=form_data)
    else:
        form = RecipeForm()

    comparisonData = None
    recipe1 = None
    recipe2 = None


    if form.validate_on_submit():
        try:
            inputA = form.firstRecipe.data if form.type_a.data == 'url' \
                else form.firstRecipeText.data
            inputB = form.secondRecipe.data if form.type_b.data == 'url' \
                else form.secondRecipeText.data
            if not inputA or not inputB:
                flash("Please provide input for both recipes.", "error")
            else:
                comparator = RecipeComparator(inputA,
                                              form.type_a.data,
                                              inputB,
                                              form.type_b.data
                                              )
                comparisonData = comparator.get_comparison()
                recipe1 = comparator.get_first_recipe()
                recipe2 = comparator.get_second_recipe()
        except RecipeExtractionError as e:
            app.logger.error(f"Scraping failed for URL: {e.url}")
            flash(str(e), "error")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}",
                  "error")


    return render_template("comparison.html",
                           title="Compare Recipes", form=form,
                           results = comparisonData,
                           recipe1=recipe1, recipe2=recipe2)
