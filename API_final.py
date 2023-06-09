from flask import Flask, make_response, jsonify, request, Response
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "hundreadrows"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    #converting bytes to strings
    data = [{k: v.decode() if isinstance(v, bytes) else v for k, v in item.items()} for item in data]
    return data

import xml.dom.minidom

def generate_xml_response(data_list, root_element = "root"):
    root = ET.Element(root_element)
    for data in data_list:
        element = ET.SubElement(root, "user_details")
        for key, value in data.items():
            sub_element = ET.SubElement(element, key)
            sub_element.text = str(value)
    
    xml_string = ET.tostring(root, encoding = 'utf-8', method = 'xml')
    readable_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent= "  ")
    
    return readable_xml

#index page
@app.route("/")
def home_page():
    return Response("""
    Hundredrows DATABASE User Details (using CRUD)

    SELECT OPERATION
    [1] Create User Detail/s
    [2] Retrieve User Detail/s
    [3] Update User Detail/s
    [4] Delete User Detail/s
    [E] Exit
    """, mimetype="text/plain")

'''
@app.errorhandler(404)
def not_found_error(error):
    return True
'''

@app.route("/user_details", methods=["GET"])
def get_customers():
    query = """SELECT user_id, username, first_name, last_name, gender, password FROM hundredorws.user_details;"""
    data = data_fetch(query)
    format_param = request.args.get('format')

    if format_param == 'xml':
        response = generate_xml_response(data, root_element="user_details")
        return Response(response, content_type='application/xml')
    else:
        return make_response(jsonify(data), 200)

@app.route("/user_details/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    query = f"""SELECT user_id, username, first_name, last_name, gender, password FROM hundredrows.user_details WHERE id = {id};"""
    data = data_fetch(query)
    if data == []:
        return make_response(jsonify(f"User Details with {id} user id has no record in this table!"), 404)

    format_param = request.args.get('format')
    if format_param == 'xml':
        response = generate_xml_response(data, root_element="user_details")
        return Response(response, content_type='application/xml')
    else:
        return make_response(jsonify(data), 200)

@app.route("/user_details", methods=["POST"])
def add_customer():
    info = request.get_json()
    user_id = info["id"]
    first_name = info["first_name"]
    last_name = info["last_name"]
    gender = info["gender"]
    password = info["password"]

    query = f"""INSERT INTO customers (user_id, first_name, last_name, gender, password)
            VALUES ('{user_id}', '{first_name}', '{last_name}', '{gender}', '{password}')"""

    data = data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify("User Detail/s successfully added!"), 201,)

@app.route("/user_details/<int:id>", methods=["PUT"])
def update_customer(id):
    info = request.get_json()
    user_id = info["id"]
    first_name = info["first_name"]
    last_name = info["last_name"]
    gender = info["gender"]
    password = info["password"]

    check_query = f"SELECT * FROM hundredrows.user_details WHERE user_id = {id}"
    existing_customer = data_fetch(check_query)
    if not existing_customer:
        return make_response(jsonify(f"User details with {id} id does not exist!"), 404)

    query = f"""UPDATE user_details
            SET user_id = '{id}', 
            first_name = '{first_name}', 
            last_name = '{last_name}', 
            gender = '{gender}', 
            password = '{password}'
            WHERE user_id = {id};"""

    data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify(f"User Details/s with {id} id, its record have been successfully updated!"), 201)

@app.route("/user_details/<int:id>", methods=["DELETE"])
def delete_customer(id):
    check_query = f"SELECT * FROM hundredrows.user_details WHERE id = {id}"
    existing_customer = data_fetch(check_query)
    if not existing_customer:
        return make_response(jsonify(f"User Detail/s with {id} id does not exist!"), 404)

    query = f""" DELETE FROM hundredrows.user_details WHERE id = {id}; """
    data_fetch(query)
    mysql.connection.commit()
    return make_response(jsonify(f"User Details with {id} id, its records has been successfully deleted!"), 200)


if __name__ == "__main__""":
    app.run(debug=True)