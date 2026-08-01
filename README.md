# RecipeTools

Compare recipes side-by-side to identify differences in ingredients, quantities, and measurements. 

Live at **[recipetools.app](https://recipetools.app)**.

---

## Overview

RecipeTools parses two recipe inputs—either via URL or raw text—and outputs a comparative breakdown of their ingredients. 

Features include:
*   **Ingredient Parsing:** Handles fractions, decimals, standard volumes, masses, and outlier units.
*   **Density-Aware Conversion:** Embedded lookup table converts solid ingredients to grams and liquid ingredients to milliliters.
*   **Smart Matching:** Filters adjectives and scores keywords to pair equivalent ingredients.
*   **Unit Toggling:** Switch individual items or the global view between metric and kitchen units.
*   **Privacy:** All processing occurs without accounts, tracking, or persistent data storage.

---

## Demo

Visit **[recipetools.app](https://recipetools.app)** and try:
*   [[Link to Brownie Recipe 1](https://www.loveandlemons.com/brownies-recipe/)]
*   [[Link to Brownie Recipe 2](https://sallysbakingaddiction.com/seriously-fudgy-homemade-brownies/)]

---

## Screenshots

<p><strong>Input View</strong></p>
<div><kbd><img src="screenshots/input-view.png" alt="Input View" height="400px" /></kbd></div>

<p><strong>Input View Dark Mode</strong></p>
<div><kbd><img src="screenshots/input-view-dark.png" alt="Input View Dark Mode" height="400px" /></kbd></div>

<p><strong>Comparison Table Showing Matching Ingredients</strong></p>
<div><kbd><img src="screenshots/comparison-view.png" alt="Comparison Table" height="400px" /></kbd></div>

<p><strong>Comparison View - Click Switch Units to change all units from Metric to Kitchen or Vice Versa</strong></p>
<div><kbd><img src="screenshots/comparison-view-switch-units.png" alt="Switch Units" height="400px" /></kbd></div>

<p><strong>Input View - If a website can't be scraped an error appears</strong></p>
<div><kbd><img src="screenshots/error-url.png" alt="URL Error" height="400px" /></kbd></div>

<p><strong>Text Input - Text button allows ingredients to be copy and pasted</strong></p>
<div><kbd><img src="screenshots/input-text.png" alt="Text Input" height="400px" /></kbd></div>

<p><strong>Comparison with Text - Comparison Table Display same information without recipe title</strong></p>
<div><kbd><img src="screenshots/comparison-text.png" alt="Comparison with Text" height="400px" /></kbd></div>

<p><strong>Individual Ingredients can also switch units by clicking on the ingredient in the difference column - Before Switch</strong></p>
<div><kbd><img src="screenshots/teaspoon-to-gram-tp.png" alt="Before Switch" height="400px" /></kbd></div>

<p><strong>After Switch</strong></p>
<div><kbd><img src="screenshots/teaspoon-to-gram-g.png" alt="After Switch" height="400px" /></kbd></div>

---

## How It Works

1.  **Input:** Two recipe sources are provided via URL or text.
2.  **Scraping:** URLs are processed using a lightweight scraper to extract the ingredient lists.
3.  **Parsing:** `ingredient-parser` processes each line and instantiates an `Ingredient` object.
4.  **Enrichment:** Density and state (solid/liquid) are assigned, and baseline conversions are executed.
5.  **Matching:** Each ingredient string is lowercased, stripped of punctuation, and split. Adjectives are removed and plural forms are singularized.
6.  **Comparison:** Pairs are matched greedily by calculating the Jaccard similarity score. 
7.  **Rendering:** Absolute differences are calculated and pushed to a Jinja2 template.

### Similarity Calculation

Unmatched ingredients reflect a total difference against an empty clone object. Matched pairs are scored using the following formula:

$$score = \frac{|keywords_A \cap keywords_B|}{|keywords_A \cup keywords_B|}$$

---

## Tech Stack

*   **Backend:** Python 3, Flask, Jinja2
*   **Parsing:** ingredient-parser, NLTK
*   **Math:** fractions, inflect
*   **Frontend:** Vanilla JavaScript, CSS
*   **Deployment:** Docker Compose

---

## Project Structure

| Class | Purpose |
| :--- | :--- |
| `Ingredient` | Stores name, amount, and measure. Executes unit conversions and difference calculations. |
| `Recipe` | Wraps a list of `Ingredient` objects. Calls `compare_recipe()` to handle matching logic. |
| `RecipeComparator` | Validates input, builds `Recipe` instances, and stores the final comparison output. |

---

## Running Locally

1. Clone the repository and navigate to the directory.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Run the Flask server:

```bash
flask run
```

*Note: The NLTK data is included in the `nltk_data/` folder. If data is missing, download it manually using `python -m nltk.downloader punkt averaged_perceptron_tagger`.*

---

## Limitations

*   **Scraper Reliability:** URL extraction relies on standard HTML structures and will fail on non-standard recipe blogs.
*   **Density Table:** Unknown ingredients default to 240 g/cup (water density).
*   **Parser Accuracy:** `ingredient-parser` can misinterpret unusual formatting.
*   **Fractions:** Unit conversion rounds to a denominator of 48 for kitchen measures. Extremely small values may be lost in rounding.

---

## Contributing

Open a pull request or issue on GitHub for:
*   Bug reports and edge-case ingredient strings.
*   Density JSON additions.
*   Keyword filtering and algorithm improvements.

## License

Open source under the MIT License.
