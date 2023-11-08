from flask import Flask, render_template
import database_constituents
import database_objects
import database_locations
app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/constituents")
def constituents_page():
    return render_template("constituents.html")

@app.route("/objects")
def objects_page():
    return render_template("objects.html")

@app.route("/locations")
def locations_page():
    return render_template("locations.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
