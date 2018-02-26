// server.js

require('dotenv').load()
const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const url = require('url')
const pg = require('pg')
const math = require('mathjs')
const app = express()
const port = process.env.PORT || 7777
//const env = process.env.NODE_ENV || 'development'

app.use(express.static( path.join(__dirname, '/public')))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

/*var forceSSL = (req, res, next) => {
    console.log('in forceSSL, x-forwarded-proto: ', req.headers['x-forwarded-proto'])
    if (req.headers['x-forwarded-proto'] !== 'https') {
        return res.redirect(['https://', req.get('Host'), req.url].join(''))
    }
    return next();
}
console.log('env: ', env)
if (env === 'production') {
    app.use(forceSSL)
}*/

const params = url.parse(process.env.DATABASE_URL)
const auth = params.auth.split(':')
const config = {
    user: auth[0],
    password: auth[1],
    host: params.hostname,
    port: params.port,
    database: params.pathname.split('/')[1]
}
console.log('Config: ', config)
const pool = new pg.Pool(config)

app.get('/', (req, res) => {
    res.sendFile('index.html')
})

var options = {}
app.get('/query', (req, res) => {
    pool.connect((err, client, done) => {
        if (err) {
            return console.log('unable to connect to pool', err)
        }
        client.query('SELECT * FROM meta;', (err, qRes) => {
            done()
            if (err) {
                console.log('query failed', err)
                res.status(400).send(err)
            }
            var rows = qRes.rows
            for (var i = 0; i < rows.length; i ++) {
                options[rows[i].criteria] = {
                                            'selected': false,
                                            'parent': rows[i].parent,
                                            'children': []
                                            }
            }
            for (var i = 1; i < rows.length; i ++) {
                var parent = options[rows[i].criteria].parent
                if (parent) {
                    options[parent].children.push(rows[i].criteria)
                }
            }
            res.status(200).json(options)
        })
    })
})

/*var A = math.matrix([[1, 3], [5, 1]])
console.log(A._data)
console.log(calculateWeights(A))*/
function normalize(mat) {
    function getColSum(m, cIndx) {
        var col = math.flatten(math.subset(m, math.index(math.range(0, numberOfRows), colIndx))._data)
        return col.reduce((a, b) => a + b, 0)
    }
    var norm = mat.clone()
    var size = norm.size()
    var numberOfRows = size[0]
    var numberOfCols = size[1]
    for (var rowIndx = 0; rowIndx < numberOfRows; rowIndx++) {
        for (var colIndx = 0; colIndx < numberOfCols; colIndx++) {
            var cellVal = norm.get([rowIndx, colIndx])
            // norm is changing, so use original mat for colSum
            var colSum = getColSum(mat, colIndx)
            var newVal = cellVal / colSum
            norm.subset(math.index(rowIndx, colIndx), newVal)
        }
    }
    return norm
}
function calculateWeights(A) {
    var weights = []
    var nA = normalize(A)
    var size = nA.size()
    var numberOfRows = size[0]
    for (var rowIndx = 0; rowIndx < numberOfRows; rowIndx++) {
        var row = nA._data[rowIndx]
        var rowSum = row.reduce((a, b) => a + b)
        var rowWeight = rowSum / numberOfRows
        weights.push(rowWeight)
    }
    return weights
}

var selectedSiblings = {}
app.post('/submit', (req, res) => {
    // TODO: Save preference selections
    // TODO: Condense/clean up this section?
    var selectedCriteria = []
    var userInput = JSON.parse(Object.keys(req.body)[0])
    console.log(userInput)
    for (var comparison in userInput) {
        var temp = comparison.split('-')
        for (var i = 0; i < temp.length; i++) {
            if (!(selectedCriteria.includes(temp[i]))) {
                selectedCriteria.push(temp[i])
            }
        }
    }
    for (var i = 0; i < selectedCriteria.length; i++) {
        if (options[selectedCriteria[i]].parent in selectedSiblings) {
            selectedSiblings[options[selectedCriteria[i]].parent].push(selectedCriteria[i])
        } else {
            selectedSiblings[options[selectedCriteria[i]].parent] = [selectedCriteria[i]]
        }
    }
    console.log(selectedSiblings)
    for (var parent in selectedSiblings) {
        var siblings = selectedSiblings[parent]
        var matrix = math.eye(siblings.length)
        for (var comparison in userInput) {
            var val = parseFloat(userInput[comparison])
            if (val < 0) {
                val = 1 / (-val)
            } else if (val == 0) {
                val = 1
            }
            var rowElem = comparison.split('-')[0]
            var rowIndx = siblings.indexOf(rowElem)
            var colElem = comparison.split('-')[1]
            var colIndx = siblings.indexOf(colElem)
            matrix.subset(math.index(rowIndx, colIndx), val)
            matrix.subset(math.index(colIndx, rowIndx), 1 / val)
            console.log(matrix)
        }
    }
    
    var results = {}
    pool.connect((err, client, done) => {
        if (err) {
            return console.log('unable to connect to pool', err)
        }
        client.query('SELECT * FROM data LIMIT 1;', (err, qRes) => {
            done()
            if (err) {
                console.log('query failed', err)
                res.status(400).send(err)
            }
            var rows = qRes.rows
            //console.log(rows)
            res.status(200).json(results)
        })
    })
    /*var results = {'seattle': {'utility': 7,
                            'cost': 200000},
                'portland': {'utility': 6.6,
                            'cost': 415000},
                'denver': {'utility': 8.5,
                            'cost': 400000},
                'phoenix': {'utility': 5,
                            'cost': 350000}};
    res.json(results)*/
})

app.listen(port, (err) => {
    if (err) {
        return console.log('uh oh, something went wrong', err)
    }
    console.log('listening on port %s', port)
})
