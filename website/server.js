// server.js

require('dotenv').load()
const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const url = require('url')
const pg = require('pg')
const app = express()
const port = process.env.PORT || 7777
const env = process.env.NODE_ENV || 'development'

app.use(express.static( path.join(__dirname, '/public')))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

var forceSSL = (req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
        return res.redirect(['https://', req.get('Host'), req.url].join(''));
    }
    return next();
}

app.configure( () => {
    if (env === 'production') {
        app.use(forceSSL);
    }
})

const params = url.parse(process.env.DATABASE_URL)
const auth = params.auth.split(':')
const config = {
    user: auth[0],
    password: auth[1],
    host: params.hostname,
    port: params.port,
    database: params.pathname.split('/')[1]
}
console.log(config)
const pool = new pg.Pool(config)

app.get('/', (req, res) => {
    res.sendFile('index.html')
})

app.get('/query', (req, res) => {
    var options = {}
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

app.post('/submit', (req, res) => {
    // TODO: Save preference selections
    // Check database for selected criteria values
    // Calculate utility
    var selectedCriteria = []
    var weights = JSON.parse(Object.keys(req.body)[0])
    console.log(weights)
    for (var comparison in weights) {
        var temp = comparison.split('-');
        for (var i = 0; i < temp.length; i++) {
            if (!(selectedCriteria.includes(temp[i]))) {
                selectedCriteria.push(temp[i])
            }
        }
    }
    console.log(selectedCriteria)
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
            console.log(rows)
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
