/*
TODO: Remove inline onclick events from index.html and convert to event
listeners.
TODO: Clean up variable declarations (move to top of function).
TODO: Change function names for easier minificaiton.
*/
var options;
function getOptions(callback) {
    xhr = new XMLHttpRequest();
    xhr.open('GET', 'query', true);
    xhr.onload = function() {
        if (xhr.status == 200) {
            options = JSON.parse(xhr.responseText);
            callback(options);
        };
    };
    xhr.send();
};

function writeOptions(elemID) {
    getOptions((data) => {
        var output = '<ul>';
        function write(elem) {
            output += '<li><input type="checkbox" onchange="verifySelection(this);" id="' + elem + '">' + elem + '</li>';
            if (data[elem]['children'].length > 0) {
                output += '<ul>';
                for (var child in data[elem]['children']) {
                    write(data[elem]['children'][child]);
                };
                output += '</ul>';
            };
            return output
        };
        
        for (var option in data) {
            if (data[option]['parent'] == null) {
                write(option);
            };
        };
        output += '</ul>';
        document.getElementById(elemID).innerHTML = output;
    });
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
                                
function verifySelection(elem) {
    // If elem is checked, change parent (and grandparents) and all children 
    // to checked.
    // If elem is unchecked, uncheck all children. Also, check for siblings.
    // If all siblings are unchecked, then uncheck the parent.
    if (elem.checked) {
        function setParentChecked(e) {
            if (e != null) {
                document.getElementById(e).checked = true;
                setParentChecked(options[e]['parent']);
            };
        };
        function setChildrenChecked(e) {
            document.getElementById(e).checked = true;
            for (var child in options[e]['children']) {
                setChildrenChecked(options[e]['children'][child]);
            };
        };
        setParentChecked(elem.id);
        setChildrenChecked(elem.id);
    } else {
        function setChildrenUnchecked(e) {
            document.getElementById(e).checked = false;
            for (var child in options[e]['children']) {
                setChildrenUnchecked(options[e]['children'][child]);
            };
        };
        setChildrenUnchecked(elem.id);
        if (options[elem.id]['parent'] != null) {
            var anySibChecked = false;
            var siblings = options[options[elem.id]['parent']]['children'];
            for (var sibling in siblings) {
                if (document.getElementById(siblings[sibling]).checked) {
                    anySibChecked = true;
                };
            };
            if (!anySibChecked) {
                document.getElementById(options[elem.id]['parent']).checked = false;
            };
        };
    };
};

var results;
function getWeights() {
    var weights = {};
    var inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type.toLowerCase() == 'range') {
            weights[inputs[i].id] = inputs[i].value;
        };
    };
    xhr = new XMLHttpRequest();
    xhr.open('POST', 'submit', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status == 200) {
            results = JSON.parse(xhr.responseText);
            writeResultsTable("resultsTableBody");
        };
    };
    xhr.send(JSON.stringify(weights));
};

// Add step to filter by geographic region?
// Send request to server with criteria selections and weights
// On server side, process weights to determine utility for all options
// Sort by highest utility (or utility/cost?) and return top 10 options
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

// Source: https://www.w3schools.com/howto/howto_js_sort_table.asp  
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("resultsTable");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc"; 
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.getElementsByTagName("TR");
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++; 
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

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
    //tableData.sort();
    tableData.sort(function(a, b)  {
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
    });
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
