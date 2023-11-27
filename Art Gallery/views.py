import sqlite3
from flask import render_template, request


def home_page():
    return render_template("home.html")


def get_constituents():
    conn = sqlite3.connect('./static/database_constituents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CONSTITUENTS")
    results = cursor.fetchall()
    conn.close()
    return results


def update_constituents(display_name, last_name, display_date, begin_year, end_year, nationality, constituenttype, id):
    conn = sqlite3.connect('./static/database_constituents.db')
    cursor = conn.cursor()
    query = "UPDATE CONSTITUENTS SET forwarddisplayname = ?, lastname = ?, displaydate = ?, beginyear = ?, endyear = ?, nationality = ?, constituenttype = ? WHERE (constituentid = ?)"
    cursor.execute(query, (display_name, last_name, display_date,
                   begin_year, end_year, nationality, constituenttype, id))
    conn.commit()
    cursor.execute("SELECT * FROM CONSTITUENTS")
    results = cursor.fetchall()
    conn.close()
    return results


def delete_constituents(id):
    conn = sqlite3.connect('./static/database_constituents.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    query = "DELETE FROM CONSTITUENTS WHERE (constituentid = ?)"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.execute("SELECT * FROM CONSTITUENTS")
    results = cursor.fetchall()
    conn.close()
    return results


def get_objects_constituents():
    conn = sqlite3.connect('./static/database_constituents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OBJECTS_CONSTITUENTS")
    results = cursor.fetchall()
    conn.close()
    return results


def constituents_page():
    if request.method == "GET":
        constituents = get_constituents()
        objects_constituents = get_objects_constituents()
        return render_template("constituents.html", const=constituents, obj_const=objects_constituents)
    else:
        if "save_const" in request.form:
            objects_constituents = get_objects_constituents()
            form_id = request.form["id"]
            form_displayname = request.form["displayname"]
            form_lastname = request.form["lastname"]
            form_displaydate = request.form["displaydate"]
            form_beginyear = request.form["beginyear"]
            form_endyear = request.form["endyear"]
            form_nationality = request.form["nationality"]
            form_type = request.form["type"]
            updated = update_constituents(form_displayname, form_lastname, form_displaydate,
                                          form_beginyear, form_endyear, form_nationality, form_type, form_id)
            return render_template("constituents.html", const=updated, obj_const=objects_constituents)
        if "delete_const" in request.form:
            form_id = request.form["id"]
            deleted = delete_constituents(form_id)
            objects_constituents = get_objects_constituents()
            return render_template("constituents.html", const=deleted, obj_const=objects_constituents)


def get_objects():
    conn = sqlite3.connect('./static/database_objects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OBJECTS")
    results = cursor.fetchall()
    conn.close()
    return results


def update_objects(accessioned, location_id, title, display_date, browser_time, medium, attribution, obj_id):
    conn = sqlite3.connect('./static/database_objects.db')
    cursor = conn.cursor()
    query = "UPDATE OBJECTS SET accessioned = ?, locationid = ?, title = ?, displaydate = ?, visualbrowsertimespan = ?, medium = ?, attribution = ? WHERE (objectid = ?)"
    cursor.execute(query, (accessioned, location_id, title,
                   display_date, browser_time, medium, attribution, obj_id))
    conn.commit()
    cursor.execute("SELECT * FROM OBJECTS")
    results = cursor.fetchall()
    conn.close()
    return results


def get_objects_historical_data():
    conn = sqlite3.connect('./static/database_objects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OBJECTS_HISORICAL_DATA")
    results = cursor.fetchall()
    conn.close()
    return results


def objects_page():
    if request.method == "GET":
        objects = get_objects()
        objects_historical_data = get_objects_historical_data()
        return render_template("objects.html", obj=objects, obj_hist=objects_historical_data)
    else:
        if "save_objects" in request.form:
            objects_historical_data = get_objects_historical_data()
            form_objid = request.form["objid"]
            form_accessid = request.form["accessid"]
            form_locationid = request.form["locationid"]
            form_title = request.form["title"]
            form_displaydate = request.form["displaydate"]
            form_browsertime = request.form["browsertime"]
            form_medium = request.form["medium"]
            form_attribution = request.form["attribution"]
            updated = update_objects(form_accessid, form_locationid, form_title, form_displaydate,
                                     form_browsertime, form_medium, form_attribution, form_objid)
            return render_template("objects.html", obj=updated, obj_hist=objects_historical_data)


def get_preferred_locations():
    conn = sqlite3.connect('./static/database_locations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PREFERRED_LOCATIONS")
    results = cursor.fetchall()
    conn.close()
    return results


def get_locations():
    conn = sqlite3.connect('./static/database_locations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LOCATIONS_NEW")
    results = cursor.fetchall()
    conn.close()
    return results


def locations_page():
    locations = get_locations()
    preferred_locations = get_preferred_locations()
    return render_template("locations.html", pref_locat=preferred_locations, locat=locations)
