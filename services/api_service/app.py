from flask import Flask
from flask import request
from flask import jsonify

#global variables oxygen level
oxygen_level = 19.5

app = Flask(__name__)

@app.route('/api/v1/oxygen', methods=['GET'])
def get_oxygen():
	return jsonify({"oxygen_level": oxygen_level})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)