from flask import Flask, request, render_template
from scraper import get_images_from_url

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    images = []
    url = ""
    error = None

    if request.method == "POST":
        url = request.form.get("url")
        result = get_images_from_url(url)

        if isinstance(result, dict) and "error" in result:
            error = result["error"]
        else:
            images = result

    return render_template("index.html", images=images, url=url, error=error)

if __name__ == "__main__":
    app.run(debug=True)
