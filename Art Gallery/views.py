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
      