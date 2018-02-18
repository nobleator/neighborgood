// server.js

const express = require('express')
const path = require('path')
const app = express()
const port = 7777

app.use(express.static( path.join(__dirname, '/public')))

app.get('/', (req, res) => {
    res.sendFile('index.html')
})

// AJAX endpoint
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
    /*
    Example option:
    'climate': {
        'selected': false,
        'parent': null,
        'children': ['temperature', 'precipitation']
    }
    */
    res.json(options)
    console.log('options sent')
})

// Results (POST) endpoint
app.get('/submit', (req, res) => {
    // Save preference selections
    // Check database for selected criteria values
    // Calculate utility
    var results = {}
    /*
    'new_york': {
        'utility': 83,
        'cost': $301,000
    }
    */
    res.sendFile(results)
})

app.listen(port, (err) => {
    if (err) {
        return console.log('uh oh, something went wrong', err)
    }
    console.log('listening on port %s', port)
})