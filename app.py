from flask import Flask, render_template
import storage

app = Flask(__name__)


@app.route("/")
@app.route("/catalog")
def catalog():
    items = storage.load_inventory()
    return render_template("catalog.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)