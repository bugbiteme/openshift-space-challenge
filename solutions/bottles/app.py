from flask import Flask

app = Flask(__name__)

from flask import Flask, request, jsonify

grid = { }
min_x, min_y = float('inf'), float('inf')
max_x, max_y = float('-inf'), float('-inf')

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

    # Print the grid based on min and max coordinates
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print(grid.get((x, y), ' '), end="")
        print()
    # Print the received data
    print(data)

    # Return a simple acknowledgment
    return jsonify({"message": "Data received!"})

@app.route('/')
def hello():
    return 'Hello, World!'

app.run(host="0.0.0.0", port=8080)
