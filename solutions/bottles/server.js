const express = require('express');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.json());

let min_x = Infinity;
let min_y = Infinity;
let max_x = -Infinity;
let max_y = -Infinity;
const grid = {};

app.get('/show', (req, res) => {
    let grid_str = "<html><body><pre>";

    for (let y = min_y; y <= max_y; y++) {
        for (let x = min_x; x <= max_x; x++) {
            grid_str += grid[`${x},${y}`] || ' ';
        }
        grid_str += "\n";
    }

    res.send(grid_str + "</pre></body></html>");
});

app.post('/collect-bottles', (req, res) => {
    const data = req.body;

    console.log(data);

    for (let item of data) {
        const char = item.character;
        const x = item.coordinates.x;
        const y = item.coordinates.y;

        grid[`${x},${y}`] = char;

        // Update min and max coordinates
        min_x = Math.min(min_x, x);
        min_y = Math.min(min_y, y);
        max_x = Math.max(max_x, x);
        max_y = Math.max(max_y, y);
    }

    // Return a simple acknowledgment
    res.json({ message: "Data received!" });
});

app.listen(8080, () => {
    console.log(`Server running on port 8080`);
});
