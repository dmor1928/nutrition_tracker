//Defining a listener for add_ingredient button (specifically, an onclick handler)
document.getElementById("add_ingredient").onclick  = function() {

    // Create list element
    var li_element = document.createElement("Li")
    li_element.classList.add("list-group-item"); //bootstrap

    // Get the value of element selected by ingredient dropdown

    var selected_ingredient = document.getElementById("ingredient");
    var selected_ingredient_value = selected_ingredient.value;
    var food_id = selected_ingredient.options[selected_ingredient.selectedIndex].id;

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

    PrintElem("recipe-ingredients")
}

function deleteIngredient(food_id) {
    console.log("Deleted food_id " + food_id);
    document.getElementById(food_id + "-li").parentNode.removeChild(document.getElementById(food_id + "-li"));
}

// form.addEventListener('submit', function(event) {
//     event.preventDefault();    // prevent page from refreshing
//     const formData = new FormData(form);  // grab the data inside the form fields
//     fetch('/create-recipe', {   // assuming the backend is hosted on the same server
//         method: 'POST',
//         body: formData,
//     })
// });