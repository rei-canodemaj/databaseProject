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
        cursor.execute(query, (display_name, last_name, display_date, begin_year, end_year, nationality, constituenttype, id))
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
        constituents = get_constituents()
        objects_constituents = get_objects_constituents()
        return render_template("constituents.html", const=constituents, obj_const=objects_constituents)
      
def get_objects():
    conn = sqlite3.connect('./static/database_objects.db')
    cursor = conn.cursor()
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
        objects = get_objects()
        objects_historical_data = get_objects_historical_data()
        return render_template("objects.html", obj=objects, obj_hist=objects_historical_data)
   
