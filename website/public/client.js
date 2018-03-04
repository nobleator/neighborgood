/*
TODO: Clean up variable declarations (move to top of function, use const and let, etc).
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

function makeReadable(word) {
    var translated = '';
    var cap = true;
    for (var cIndx = 0; cIndx < word.length; cIndx++) {
        ch = word.charAt(cIndx);
        if (ch == '_') {
            translated += ' ';
            cap = true;
        } else if (cap) {
            translated += word.charAt(cIndx).toUpperCase();
            cap = false;
        } else {
            translated += word.charAt(cIndx);
        }
    }
    return translated;
};

function writeOptions() {
    var elemID = 'criteria-list';
    getOptions((data) => {
        var output = '<div class="row">';
        function write(elem) {
            output += '<div class="subrow"><input type="checkbox" onchange="verifySelection(this);" id="' + elem + '">';
            output += '<label for="' + elem + '"class="ck-button">' + makeReadable(elem) + '</label></div>'
            if (data[elem]['children'].length > 0) {
                for (var child in data[elem]['children']) {
                    write(data[elem]['children'][child]);
                };
            };
            return output
        };
        
        for (var option in data) {
            if (data[option]['parent'] == null) {
                output += '<div class="cell">';
                write(option);
                output += '</div>';
            };
        };
        output += '</div>';
        document.getElementById(elemID).innerHTML = output;
    });
};

function getChecked() {
    var elemID = 'weights';
    var comparisons = {null: []};
    for (var option in options) {
        if (options[option]['children'].length > 0) {
            comparisons[option] = [];
        };
    };
    for (var option in options) {
        if (document.getElementById(option).checked) {
            comparisons[options[option]['parent']].push(option);
            options[option]['selected'] = true;
        } else {
            options[option]['selected'] = false;
        };
    };
    output = '';
    for (var parent in comparisons) {
        var subList = comparisons[parent];
        for (var i1 = 0; i1 < subList.length - 1; i1++) {
            for (var i2 = i1 + 1; i2 < subList.length; i2++) {
                output += '<div class="range">';
                output += '<span class="left">' + makeReadable(subList[i1]) + '</span>';
                output += '<input type="range" min="-9" max="9" step="1" id="'
                output += subList[i1] + '-' + subList[i2] + '">';
                output += '<span class="right">' + makeReadable(subList[i2]) + '</span>';
                output += '</div>';
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

function progressBar() {
    var elem = document.getElementById("progBarInner"); 
    var width = 1;
    var id = setInterval(frame, 25);
    function frame() {
        if (width >= 100) {
            document.getElementById("resultsTable").style.visibility = "visible";
            clearInterval(id);
        } else {
            width++; 
            elem.style.width = width + '%'; 
        }
    }
};

var results;
function getWeights() {
    progressBar();
    var weights = {};
    var inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type.toLowerCase() == 'range') {
            weights[inputs[i].id] = inputs[i].value;
        };
    };
    xhr = new XMLHttpRequest();
    xhr.open('POST', 'submit', true);
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onload = function() {
        if (xhr.status == 200) {
            results = JSON.parse(xhr.responseText);
            console.log('about to call writeResultsTable...');
            writeResultsTable();
        };
    };
    var respObj = {"options": options, "weights": weights};
    xhr.send(JSON.stringify(respObj));
};

// Add step to filter by geographic region?
function writeResultsTable() {
    console.log('in writeResultsTable...');
    var elemID = "resultsTableBody";
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

// Event listeners and initialization
function init() {
    writeOptions();
    document.getElementById('submitChecked').addEventListener('click', getChecked, false);
    document.getElementById('submitWeights').addEventListener('click', getWeights, false);
    document.getElementById('sort0').addEventListener('click', () => { sortTable(0); }, false);
    document.getElementById('sort1').addEventListener('click', () => { sortTable(1); }, false);
    document.getElementById('sort2').addEventListener('click', () => { sortTable(2); }, false);
}
window.addEventListener('load', init, false);
