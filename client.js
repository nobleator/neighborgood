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
    var comparisons = [];
    var subLists = {null: []};
    for (var option in options) {
        if (document.getElementById(option).checked) {
            comparisons.push(option);
            console.log(option);
            if (option['children'].length > 0) {
                subLists[option] = [];
            };
        };
    };
    console.log(comparisons);
    var output = '';
    for (var i = 0; i < comparisons.length; i++) {
        if (comparisons[i]['selected'] && comparisons[i]['parent'] in subLists) {
            subLists['parent'].push(comparisons[i]);
        };
    };
    output += sublists;
    document.getElementById(elemID).innerHTML = output;
};