// server.js

const express = require('express')
const app = express()
const port = 7777

app.get('/', (req, res) => {
    res.send('Hello server')
})

app.listen(port, (err) => {
    if (err) {
        return console.log('uh oh, something went wrong', err)
    }
    console.log('listening on port %s', port)
})