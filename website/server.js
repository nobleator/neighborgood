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
// var asc_preferred = {}
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
            for (var i = 1; i < rows.length; i ++) {
                options[rows[i].criteria] = {
                                            "selected": false,
                                            "parent": rows[i].parent,
                                            "children": []
                                            }
                // asc_preferred[rows[i].criteria] = rows[i].asc_preferred
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
/*
function linearize(x, maxX, minX, asc) {
    // Transforms number x in the range [a, b] to the number y in the range [c, d]
    // y = (x - a)((d - c)/(b - a)) + c
    var c = 0
    var d = 10
    if (asc) {
        var a = minX
        var b = maxX
    } else {
        var a = maxX
        var b = minX
    }
    return (x - a) * ((d - c) / (b - a)) + c
}
*/
app.post('/submit', (req, res) => {
    // TODO: Save preference selections
    // TODO: Condense/clean up this section
    var selectedCriteria = []
    var userInput = req.body
    
    var selectedSiblings = {}
    var options = userInput['options']
    for (var criteria in options) {
        if (options[criteria]['selected']) {
            var parent = options[criteria]['parent']
            if (parent in selectedSiblings) {
                selectedSiblings[parent].push(criteria)
            } else {
                selectedSiblings[parent] = [criteria]
            }
        }
    }

    function getWeights(elemArr) {
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
        var matrix = math.eye(elemArr.length)
        for (var comparison in userInput['weights']) {
            var val = parseFloat(userInput['weights'][comparison])
            if (val < 0) {
                val = 1 / (-val)
            } else if (val == 0) {
                val = 1
            }
            var rowElem = comparison.split('-')[0]
            var rowIndx = elemArr.indexOf(rowElem)
            var colElem = comparison.split('-')[1]
            var colIndx = elemArr.indexOf(colElem)
            if (rowIndx < 0 || colIndx < 0) {
                continue
            }
            matrix.subset(math.index(rowIndx, colIndx), val)
            matrix.subset(math.index(colIndx, rowIndx), 1 / val)
        }
        return calculateWeights(matrix)
    }

    weights = {};
    for (var criteria in options) {
        siblings = selectedSiblings[userInput['options'][criteria]['parent']]
        if (criteria in weights) {
            continue
        }
        if (!options[criteria]['selected']) {
            weights[criteria] = 0
        } else if (siblings.length < 2) {
            weights[criteria] = 1
        } else {
            sibWeights = getWeights(siblings);
            for (var i = 0; i < siblings.length; i++) {
                weights[siblings[i]] = sibWeights[i]
            } 
        } 
    }
    pool.connect((err, client, done) => {
        if (err) {
            return console.log('unable to connect to pool', err)
        }
        client.query('SELECT * FROM data;', (err, qRes) => {
            done()
            if (err) {
                console.log('query failed', err)
                res.status(400).send(err)
            }
            var rows = qRes.rows
            cities = {}
            for (var i = 1; i < rows.length; i++) {
                cities[rows[i]['city']] = {}
                for (var criteria in rows[i]) {
                    cities[rows[i]['city']][criteria] = parseFloat(rows[i][criteria])
                }
            }
            /*
            maximums = {}
            minimums = {}
            for (var city in cities) {
                for (var criteria in cities[city]) {
                    if (!(criteria in maximums) || cities[city][criteria] > maximums[criteria]) {
                        maximums[criteria] = cities[city][criteria]
                    }
                    if (!(criteria in minimums) || cities[city][criteria] < minimums[criteria]) {
                        minimums[criteria] = cities[city][criteria]
                    }
                }
            }
            // asc_preferred = {criteria: true if ascending, false otherwise}
            for (var city in cities) {
                results[city] = {'utility': 0, 'cost': cities[city]['housing_cost']}
                for (var criteria in cities[city]) {
                    var score = linearize(cities[city][criteria], maximums[criteria], minimums[criteria], asc_preferred[criteria])
                    results[city]['utility'] += score * weights[criteria]
                }
                // Edit output formatting
                results[city]['utility'] = Math.round(results[city]['utility'] * 100) / 100
                //results[city]['cost'] = results[city]['cost'].toLocaleString('en-US', {style: 'currency', currency: 'USD'})
            }
            */
            results = {}
            for (var city in cities) {
                results[city] = {'utility': 0, 'cost': cities[city]['housing_cost']}
                for (var criteria in cities[city]) {
                    if (criteria in userInput['options'] && userInput['options'][criteria]['selected']) {
                        results[city]['utility'] += (cities[city][criteria] * weights[criteria])
                    }
                }
                // Edit output formatting
                results[city]['utility'] = Math.round(results[city]['utility'] * 100) / 100
                //results[city]['cost'] = results[city]['cost'].toLocaleString('en-US', {style: 'currency', currency: 'USD'})
            }
            function getTopTen() {
                function findMin(arr) {
                    var minUtility = 1000000
                    for (var i = 0; i < arr.length; i++) {
                        var elem = arr[i]
                        if (results[elem]['utility'] < minUtility) {
                            minCity = elem
                            minUtility = results[elem]['utility']
                        }
                    }
                    return minCity
                }
                var topTen = []
                for (var city in results) {
                    if (topTen.length < 10) {
                        topTen.push(city)
                    } else if (results[city]['utility'] > results[minCity]['utility']) {
                        var index = topTen.indexOf(minCity)
                        if (index > -1) {
                            topTen.splice(index, 1)
                        }
                        topTen.push(city)
                    }
                    var minCity = findMin(topTen)
                }
                return topTen
            }
            topTenResults = {}
            topTen = getTopTen()
            for (var i = 0; i < topTen.length; i++) {
                topTenResults[topTen[i]] = results[topTen[i]]
            }
            res.status(200).json(topTenResults)
        })
    })
})

app.listen(port, (err) => {
    if (err) {
        return console.log('uh oh, something went wrong', err)
    }
    console.log('listening on port %s', port)
})
