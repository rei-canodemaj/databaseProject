from flask import Flask, render_template
import views
import database_constituents
import database_objects
import database_locations
app = Flask(__name__)


app.add_url_rule("/", view_func=views.home_page)
app.add_url_rule("/constituents", view_func=views.constituents_page, methods=["GET", "POST"])
app.add_url_rule("/objects", view_func=views.objects_page)
app.add_url_rule("/locations", view_func=views.locations_page)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
