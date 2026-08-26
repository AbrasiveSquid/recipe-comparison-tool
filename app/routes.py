from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, limiter
from app.forms import RecipeForm
from recipe_logic.main import RecipeComparator, RecipeExtractionError
from recipe_logic.ocr import extract_text
from recipe_logic.tracking import track_event
from app.feedback import send_feedback
from urllib.parse import urlparse

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
        track_event("page_view", get_traffic_source())

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
                track_event("comparison")
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
        track_event("ocr_success")
    except Exception:
        track_event("ocr_failure")
        app.logger.exception("OCR failed")
        return jsonify({"error": "Could not extract text from image"}), 500

    return jsonify({"text": text})

def get_traffic_source():
    utm_source = request.args.get("utm_source", "").lower()

    known_sources = {
        "reddit",
        "linkedin",
        "hackernews",
    }

    if utm_source in known_sources:
        return utm_source

    if request.referrer:
        hostname = urlparse(request.referrer).hostname or ""

        if "google." in hostname:
            return "google"
        if "reddit.com" in hostname:
            return "reddit"
        if "linkedin.com" in hostname:
            return "linkedin"
        if "ycombinator.com" in hostname:
            return "hackernews"

        return "other"

    return "direct"

@app.route("/feedback", methods=["POST"])
@limiter.limit("3 per hour")
def feedback():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Feedback message is required"}), 400

    if len(message) > 2000:
        return jsonify({"error": "Feedback message is too long"}), 400

    try:
        send_feedback(message)
    except Exception:
        app.logger.exception("Failed to send feedback")
        return jsonify({"error": "Could not send feedback"}), 500

    return jsonify({"message": "Feedback sent"}), 200

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "Image must be 10 MB or smaller"}), 413

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({
        "error": "Too many image requests. Please try again later."
    }), 429
