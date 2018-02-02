// Read and set options from server/DB (via AJAX?)
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

function writeOptions(elemID) {
    var output = '<ul>';
    for (var option in options) {
        output += '<li><input type="checkbox" id="' + option + '">' + option + '</li>';
    };
    output += '</ul>';
    document.getElementById(elemID).innerHTML = output;
};

function getChecked(elemID) {
    var comparisons = {null: []};
    for (var option in options) {
        if (options[option]['children'].length > 0) {
            comparisons[option] = [];
        };
    };
    for (var option in options) {
        if (document.getElementById(option).checked) {
            comparisons[options[option]['parent']].push(option);
        };
    };
    output = '';
    for (var parent in comparisons) {
        var subList = comparisons[parent];
        for (var i1 = 0; i1 < subList.length - 1; i1++) {
            for (var i2 = i1 + 1; i2 < subList.length; i2++) {
                output += '<span>' + subList[i1] + '</span>';
                output += '<input type="range" min="-3" max="3" step="1" id="'
                output += subList[i1] + '-' + subList[i2] + '">';
                output += '<span>' + subList[i2] + '</span><br>';
            };
        };
    };
    document.getElementById(elemID).innerHTML = output;
};

function getWeights() {
    var inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type.toLowerCase() == 'range') {
            console.log(inputs[i].id, inputs[i].value);
        };
    };
};

// Add step to filter by geographic region?
// Send request to server with criteria selections and weights
// On server side, process weights to determine utility for all options
// Sort by highest utility (or utility/cost?) and return top 10 options
var results = {'seattle': {'utility': 7,
                           'cost': 200000},
               'portland': {'utility': 6.6,
                           'cost': 415000},
               'denver': {'utility': 8.5,
                           'cost': 400000},
               'phoenix': {'utility': 5,
                           'cost': 350000}};

function writeResultsTable(elemID) {
    var output = '';
    for (var city in results) {
        output += '<tr>';
        output += '<td>' + city + '</td>';
        output += '<td>' + results[city]['utility'] + '</td>';
        output += '<td>' + results[city]['cost'] + '</td>';
        output += '</tr>';
    };        
    document.getElementById(elemID).innerHTML = output;
};

// Inspiration:
// https://codereview.stackexchange.com/questions/37632/sorting-an-html-table-with-javascript
// TODO: Sorting is incomplete/not working

var sortOrder = {'city': 1, 'utility': 1, 'cost': 1};
function sortResults(column) {
    console.log('in sortResults');
    // Get ascending/descending value, reset other columns
    var asc = sortOrder[column];
    for (var city in sortOrder) {
        if (column == city) {
            sortOrder[city] *= -1;
        } else {
            sortOrder[city] = 1;
        };
    };
    // Convert HTML to Array
    var table = document.getElementById('resultsTable');
    var rows = table.rows;
    var tableData = new Array();
    for (var r = 0; r < rows.length; r++) {
        var cells = rows[r].cells;
        tableData[r] = Array();
        for (var c = 0; c < cells.length; c++) {
            tableData[r][c] = cells[c].innerHTML;
        };
    };
    console.log('pre sort');
    console.log(tableData);
    // Sort data in place
    tableData.sort();
    /*tableData.sort(function(a, b)  {
        //return (a[column] == b[column]) ? 0 : ((a[column] > b[column]) ? asc : -1 * asc);
        var retVal = 0;
        var _a = parseFloat(a[column]);
        var _b = parseFloat(b[column]);
        if (a[column] != b[column]) {
            if ((_a == a[column]) && (_b == b[column])) {
                // Numerical column
                retVal = (fA > fB) ? asc : -1 * asc;
            } else {
                // Text column
                retVal = (a[column] > b[column]) ? asc : -1 * asc;
            };
        };
        return retVal;
    });*/
    console.log('post sort');
    console.log(tableData);
    // Replace inner HTML of all individual cells (does not overwrite class/ID)
    for (var r = 0; r < rows.length; r++) {
        var cells = rows[r].cells;
        for (var c = 0; c < cells.length; c++) {
            table.rows[r].cells[c].innerHTML = tableData[r][c];
        };
    };
};
