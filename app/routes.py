from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, limiter
from app.forms import RecipeForm
from recipe_logic.main import RecipeComparator, RecipeExtractionError
from recipe_logic.ocr import extract_text


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

@app.route("/ocr", methods=["POST"])
@limiter.limit("5 per minute")
@limiter.limit("30 per hour")
@limiter.limit("100 per hour", key_func=lambda: "ocr-global")
def ocr():
    image = request.files.get("image")

    if image is None or image.filename == "":
        return jsonify({"error": "No image provided"}), 400

    try:
        text = extract_text(image.stream)
    except Exception:
        app.logger.exception("OCR failed")
        return jsonify({"error": "Could not extract text from image"}), 500

    return jsonify({"text": text})

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Image must be 10 MB or smaller"}), 413

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({
        "error": "Too many image requests. Please try again later."
    }), 429
