//Defining a listener for add_ingredient button (specifically, an onclick handler)
// document.getElementById("add_ingredient").onclick
function addToIngredientList(elt) {

    // Create list element
    var li_element = document.createElement("Li")
    li_element.classList.add("list-group-item"); //bootstrap

    // Get the value of element selected by ingredient dropdown

    // var selected_ingredient = document.getElementById("ingredient");
    var selected_ingredient_value = elt.value;
    // var food_id = selected_ingredient.options[selected_ingredient.selectedIndex].id;
    var food_id = elt.id;

    // Check if ingredient already in list by checking if "-li" element already exists
    if (!(Object.is(document.getElementById(food_id + "-li"), null))) {
        console.log("food_id " + food_id + " already in list");
        return;
    } 

    // Create a text node of the value of element selected in dropdown
    var ingredient_textnode=document.createTextNode(selected_ingredient_value);

    if (selected_ingredient_value == "Choose...")  // Makes 'choose...' unable to be added
        return;

    //Removing punctuation and spaces so naming id's etc is easier
    var formatted_ingredient_text = selected_ingredient_value.replace(/\s+/g, '-').toLowerCase();
    formatted_ingredient_text = formatted_ingredient_text.replaceAll(",", "");

    /*
    Recreating the delete button from home.html example
    each thing in the unordererd list ul:
    
    <li id="[food_id]-li" class="list-group-item">
        <div class="input-group mb-3">
            <input name="[food_id]-grams" type="number" class="form-control" aria-label="Amount (to the nearest dollar)">
            <span class="input-group-text"> grams of </span>
            <input class="form-control" value="Crushed tomatoes" readonly>
            <button type="button" id="Crushed tomatoes" class="btn close"">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>       
    </li>
  */

    var div_element = document.createElement("div");
    div_element.classList.add("input-group");
    div_element.classList.add("mb-3");

    var grams_input = document.createElement("input");
    grams_input.type = "number";
    grams_input.classList.add("form-control");
    grams_input.ariaLabel = "Amount (to the nearest gram)";
    grams_input.min = "1";
    grams_input.name = food_id
    
    var grams_of_span = document.createElement("span");
    grams_of_span.classList.add("input-group-text");
    grams_of_span.textContent = " grams of ";

    var ingredient_input = document.createElement("input");
    ingredient_input.classList.add("form-control");
    ingredient_input.readOnly = true; 
    ingredient_input.value = selected_ingredient_value;
    
    var delete_button_text = document.createTextNode("\u00D7");
    var delete_button_span_element = document.createElement("span");
    delete_button_span_element.ariaHidden = "true";
    delete_button_span_element.appendChild(delete_button_text);
    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.classList.add("btn"); 
    deleteButton.classList.add("close");

    // For checking if li_element already exists in list to prevent duplicates
    li_element.id = food_id + "-li";
    
    // When clicked, run delete_recipe_ingredient function and input its id
    //deleteButton.addEventListener("click", delete_recipe_ingredient());
    deleteButton.onclick = function(){
        console.log("Deleted food_id " + food_id);
        document.getElementById(li_element.id).parentNode.removeChild(document.getElementById(li_element.id));
        
        if (isEmpty('recipe-ingredients')) {
            console.log("it's empty!");
            document.getElementById('emptyListMessage').style.display = '';
        } else {
            document.getElementById('emptyListMessage').style.display = 'none';
        }
    }

    deleteButton.appendChild(delete_button_span_element);
    
    div_element.appendChild(grams_input);
    div_element.appendChild(grams_of_span);
    div_element.appendChild(ingredient_input);
    div_element.appendChild(deleteButton);
    
    // Append the button element inside the list element li_element
    li_element.appendChild(div_element);

    // Append li_element to the ul element ingredients_list
    document.getElementById("recipe-ingredients").appendChild(li_element);

    if (!(isEmpty('recipe-ingredients'))) {
        document.getElementById('emptyListMessage').style.display = 'none';
        console.log("It's not empty!")
    }
}

function filterFunction() {
    var input, input_value, filters, ul, button, li, i;
    input = document.getElementById("searchInput");
    ul = document.getElementById("foodsList");
    li = ul.getElementsByTagName("li");

    // For each word in input, run a filter
    input_value = input.value.replaceAll(',', '');
    input_value = input_value.replaceAll('-', ' ');
    input_value = input_value.toUpperCase().trim();
    filters = input_value.split(' ');
    //filter = input.value.toUpperCase();

    console.log(filters);

    if (filters[0] == '') {
        for (i = 0; i < li.length; i++) {
            li[i].style.display = "none";
        }
    }

    for (i = 0; i < li.length; i++) {
        txtValue = li[i].getElementsByTagName("button")[0].textContent || li[i].getElementsByTagName("button")[0].value;
        txtValue = txtValue.replace('-', '');
        if (allFilters(filters, txtValue)) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function allFilters(filters, txtValue) {
    var j, filter;
    for (j = 0; j < filters.length; j++) {
        filter = filters[j];
        if (!(txtValue.toUpperCase().indexOf(filter) > -1)) {
            return false;
        }
    }
    return true;
};

var typingTimer;
var doneTypingInterval = 100;
var input = document.getElementById('searchInput');

input.onkeyup = function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
};

input.onkeydown = function () {
    clearTimeout(typingTimer);
};

function doneTyping () {
    filterFunction();
};


var searchInputArea = document.getElementById('searchInput');
var foodsListWindow = document.getElementById('foodsList');
var searchListWrapper = document.getElementById('searchListWrapper');

function clickOptionTest(elt) {
    console.log("Option clicked!");
    addToIngredientList(elt);
    searchInputArea.value = elt.value;
    foodsListWindow.style.display = 'none';
};

searchInputArea.onclick = function() {
    foodsListWindow.style.display = '';
};

// searchListWrapper.onblur = function() {
//     foodsListWindow.style.display = 'none';
// };

document.addEventListener("click", (evt) => {
    const flyoutEl = document.getElementById("searchListWrapper");
    const flyoutEl2 = document.getElementById("recipe-ingredients");
    let targetEl = evt.target; // clicked element      
    do {
      if(targetEl == flyoutEl || targetEl == flyoutEl2) {
        // This is a click inside, does nothing, just return.
        // console.log("Clicked inside!");
        return;
      }
      // Go up the DOM
      targetEl = targetEl.parentNode;
    } while (targetEl);
    // This is a click outside.      
    // console.log("Clicked outside!");
    foodsListWindow.style.display = 'none';
});


var recipeIngredientsList = document.getElementById('recipe-ingredients');

function isEmpty(id) {
    console.log(document.getElementById(id).innerHTML.trim());
    return document.getElementById(id).innerHTML.trim() == "";
};