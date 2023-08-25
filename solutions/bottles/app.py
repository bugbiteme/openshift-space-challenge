from flask import Flask, request, jsonify

app = Flask(__name__)

grid = { }
min_x, min_y = float('inf'), float('inf')
max_x, max_y = float('-inf'), float('-inf')

@app.route('/show')
def show():
    global min_x, min_y, max_x, max_y

    # Build the grid string based on min and max coordinates
    grid_str = "<html><body><pre>"
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            grid_str += grid.get((x, y), ' ')
        grid_str += "\n"

    return grid_str + "</pre></body></html>"

@app.route('/collect-bottles', methods=['POST'])
def collect_bottles():

    global min_x , min_y, max_x, max_y

    # Get the JSON data from the request
    data = request.json

    for item in data:
        char = item['character']
        x = item['coordinates']['x']
        y = item['coordinates']['y']

        grid[(x, y)] = char

        # Update min and max coordinates
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    # Return a simple acknowledgment
    return jsonify({"message": "Data received!"})

@app.route('/')
def hello():
    return 'Hello, World!'

app.run(host="0.0.0.0", port=8080)
