const express = require('express');
app = express();

app.use(express.json());

const CSV_TO_MORSE = process.env.MORSE_CSV;
const morseDict = {};

// Parse CSV from environment variable into morseDict
if (CSV_TO_MORSE) {
    const lines = CSV_TO_MORSE.split('\n');
    lines.forEach(line => {
        const [char, morse] = line.split(',');
        morseDict[morse] = char;
    });
    console.log(morseDict['...']);
}

app.post('/decode-morse', (req, res) => {
    const { message } = req.body;
    message.split(' ').map(morseChar => console.log(morseChar))
    const decodedMessage = message.split(' ').map(morseChar => morseDict[morseChar] || '').join('');
    return res.send({ decodedMessage });
});

app.listen(8080, '0.0.0.0', () => {
    console.log('Server started on http://0.0.0.0:8080');
});
