from flask import Flask, render_template
import views

import database_constituents
import database_objects
import database_locations
app = Flask(__name__)


app.add_url_rule("/", view_func=views.home_page)
app.add_url_rule("/constituents", view_func=views.constituents_page)
    

@app.route("/objects")
def objects_page():
    return render_template("objects.html")

@app.route("/locations")
def locations_page():
    return render_template("locations.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
