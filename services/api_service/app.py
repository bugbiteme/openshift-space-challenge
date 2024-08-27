from flask import Flask, send_file
from flask import request
from flask import jsonify
import json
import os

#global variables oxygen level
oxygen_level = 19.5

#global variables spaceship speed
spaceship_speed = 52

app = Flask(__name__)

@app.route('/api/v1/oxygen', methods=['GET'])
def get_oxygen():
	return jsonify({"oxygen_level": oxygen_level})

@app.route('/api/v1/temperature', methods=['GET'])
def get_temperature():
	# load temperatures from json file (temperatures.json) and return json response

	# Define the absolute path to the file
	file_path = os.path.join(os.path.dirname(__file__), 'temperatures.json')

	# read file
	with open(file_path, 'r') as file:
		data = file.read()
	
	# parse file
	temperatures = json.loads(data)
	return jsonify(temperatures)

@app.route('/api/v1/camera1', methods=['GET'])
def get_camera1():
    # Define the absolute path to the file
    file_path = os.path.join(os.path.dirname(__file__), 'cam1.png')

    # Return the image file
    return send_file(file_path, mimetype='image/png')

@app.route('/api/v1/speed', methods=['GET'])
def get_speed():
	return jsonify({"spaceship_speed": spaceship_speed})

@app.route('/api/v1/speed', methods=['POST'])
def set_speed():
	global spaceship_speed
	data = request.get_json()
	spaceship_speed = data['spaceship_speed']
	# round speed to 0 decimal
	if round(spaceship_speed, 0) == 148:
		ack_token = "ack100"
	else:
		ack_number = round(spaceship_speed / 1.5)
		ack_token = "ACK" + f"{ack_number:03d}"

	return jsonify({"spaceship_speed": spaceship_speed, "ack_flag": ack_token})


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)