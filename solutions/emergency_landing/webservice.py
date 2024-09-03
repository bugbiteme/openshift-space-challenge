from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def connect_to_database():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='planetdb2',
            database='mydatabase',
            user='myuser',
            password='mypassword'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

@app.route('/planets', methods=['GET'])
def get_planets():
    connection = connect_to_database()
    if connection is None:
        return "Error connecting to the database", 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM planets")
        planets = cursor.fetchall()
        return jsonify(planets)

    except Error as e:
        print("Error reading data from MySQL table", e)
        return "Error reading data from the database", 500

    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)