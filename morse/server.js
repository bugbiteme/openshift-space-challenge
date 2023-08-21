// Middleware to parse JSON
app.use(express.json());

const CSV_TO_MORSE = process.env.MORSE_CSV;
const morseDict = {};

// Parse CSV from environment variable into morseDict
if (CSV_TO_MORSE) {
    const lines = CSV_TO_MORSE.split('\n');
    console,
    lines.forEach(line => {
        const [char, morse] = line.split(',');
        morseDict[morse] = char;
    });
}

app.post('/decode', (req, res) => {
    const { morseMessage } = req.body;

    if (!morseMessage) {
        return res.status(400).send({ error: 'morseMessage is required' });
    }

    const decodedMessage = morseMessage.split(' ').map(morseChar => morseDict[morseChar] || '').join('');

    return res.send({ decodedMessage });
});
