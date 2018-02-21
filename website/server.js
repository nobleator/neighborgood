// server.js

const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const app = express()
const port = 7777

app.use(express.static( path.join(__dirname, '/public')))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

app.get('/', (req, res) => {
    res.sendFile('index.html')
})

app.get('/query', (req, res) => {
    // Check database for criteria options (including geneology)
    var options = {
                    'climate': {
                        'selected': false,
                        'parent': null,
                        'children': ['temperature', 'precipitation']
                    },
                    'temperature': {
                        'selected': false,
                        'parent': 'climate',
                        'children': ['hot', 'cold']
                    },
                    'hot': {
                        'selected': false,
                        'parent': 'temperature',
                        'children': []
                    },
                    'cold': {
                        'selected': false,
                        'parent': 'temperature',
                        'children': []
                    },
                    'precipitation': {
                        'selected': false,
                        'parent': 'climate',
                        'children': []
                    },
                    'culture': {
                        'selected': false,
                        'parent': null,
                        'children': ['outdoorsiness', 'arts']
                    },
                    'outdoorsiness': {
                        'selected': false,
                        'parent': 'culture',
                        'children': []
                    },
                    'arts': {
                        'selected': false,
                        'parent': 'culture',
                        'children': []
                    },
                    'jobs': {
                        'selected': false,
                        'parent': null,
                        'children': []
                    }
                }
    res.json(options)
    console.log('options sent')
})

app.post('/submit', (req, res) => {
    // Save preference selections
    // Check database for selected criteria values
    // Calculate utility
    var weights = JSON.parse(Object.keys(req.body)[0])
    console.log(weights)
    var results = {'seattle': {'utility': 7,
                            'cost': 200000},
                'portland': {'utility': 6.6,
                            'cost': 415000},
                'denver': {'utility': 8.5,
                            'cost': 400000},
                'phoenix': {'utility': 5,
                            'cost': 350000}};
    res.json(results)
})

app.listen(port, (err) => {
    if (err) {
        return console.log('uh oh, something went wrong', err)
    }
    console.log('listening on port %s', port)
})