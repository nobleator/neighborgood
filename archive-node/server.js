// server.js
//==============================================================================
//

var express = require('express');
var app = express();
var path = require('path');
var http = require('http').Server(app);
var bodyParser = require('body-parser');

app.use(express.static(path.join(__dirname + '/')));
app.use(bodyParser.urlencoded({ extended: true }));

app.set('port', (process.env.PORT || 7777));
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.get('/intro', function(req, res) {
    res.render(__dirname + '/views/intro');
});
var criteria = ['Economic', 'Climate', 'Social']
app.get('/criteria', function(req, res) {
    res.render(__dirname + '/views/criteria', {criteria: criteria});
});
function getPermutations(arr) {
    // Get permutations (non-ordered, so 'a,b' === 'b,a')
    var result = []
    for (var i = 0; i < arr.length; i++) {
        for (var j = i + 1; j < arr.length; j++) {
            result.push([arr[i], arr[j]])
        }
    }
    return result
}
app.get('/weights', function(req, res) {
    res.render(__dirname + '/views/weights', {comparisons: getPermutations(criteria)});
});
/*app.get('/results', function(req, res) {
    res.render(__dirname + '/views/results', {data: 'TESTING PLZ WORK'});
});*/
function getWeights(criteria, comparisons) {
    var matrix = []
    var L = criteria.length
    // Create empty matrix
    for (var i = 0; i < L; i++) {
        matrix.push(new Array(L).fill(0));
        matrix[i][i] = 1;
    }
    // Convert comparisons to matrix
    for (var key in comparisons) {
        var val = Number(comparisons[key]);
        var temp = key.split(',');
        var row = criteria.indexOf(temp[0]);
        var col = criteria.indexOf(temp[1]);
        matrix[row][col] = val;
        matrix[col][row] = 1 / val;
    }
    // Find column sums
    var colSum = new Array(L).fill(0);
    for (var rowIndx = 0; rowIndx < L; rowIndx++) {
        for (var colIndx = 0; colIndx < L; colIndx++) {
            colSum[colIndx] += matrix[rowIndx][colIndx];
        }   
    }
    // Normalize matrix by column sums
    for (var rowIndx = 0; rowIndx < L; rowIndx++) {
        for (var colIndx = 0; colIndx < L; colIndx++) {
            matrix[rowIndx][colIndx] = matrix[rowIndx][colIndx] / colSum[colIndx];
        }   
    }
    // Find row averages (i.e., final weights)
    var rowAvg = new Array(L).fill(0);
    for (var rowIndx = 0; rowIndx < L; rowIndx++) {
        var rowSum = 0;
        for (var colIndx = 0; colIndx < L; colIndx++) {
            rowSum += matrix[rowIndx][colIndx];
        }
        rowAvg[rowIndx] = rowSum / L;
        rowSum = 0;
    }
    // Zip criteria and weights together
    var result = criteria.map(function(e, i) {
        return [e, rowAvg[i]];
    });
    return result
}
// Data for criteria values -> Replace with real data at some point
var valueData = {
                    'Washington DC': {
                        'Economic': 9,
                        'Climate': 4,
                        'Social': 8
                    },
                    'San Francisco': {
                        'Economic': 8,
                        'Climate': 10,
                        'Social': 5
                    }
                }

function getUtility(weights, values) {
    var result = 0
    for (var pair in weights) {
        // criteria = pair[0];
        // weight = pair[1];
        result += pair[1]*values[pair[0]];
    }
    return result
}

app.post('/results', function(req, res) {
    var weights = getWeights(criteria, req.body);
    var utility = {}
    for (var location in valueData) {
        var values = valueData[location];
        utility[location] = getUtility(weights, values);
    }
    res.render(__dirname + '/views/results', {data: utility});
});


http.listen(app.get('port'), function() {
    console.log('listening on port ' + app.get('port'));
});
