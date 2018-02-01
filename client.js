// Read options from DB (via AJAX?)
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
