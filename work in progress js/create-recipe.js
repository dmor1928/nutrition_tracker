//Defining a listener for add_ingredient button (specifically, an onclick handler)
document.getElementById("add_ingredient").onclick  = function() {

    // Get the value of element selected by ingredient dropdown
    var ingredient = document.getElementById("ingredient").value; 

    // Create a text node of the value of element selected in dropdown
    var ingredient_textnode=document.createTextNode(ingredient);

    // Append text node to the list element
    ingredient.appendChild(ingredient_textnode);

    /*
    Recreating the delete button from home.html example
    each thing in the unordererd list ul:
    
    <li class="list-group-item">
        <div class="input-group mb-3">
            <input type="text" class="form-control" aria-label="Amount (to the nearest dollar)">
            <span class="input-group-text"> grams of </span>
            <input class="form-control" value="Crushed tomatoes" readonly>
            <button type="button" class="btn close"">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>       
    </li>
  */

    // Create list element
    var li_element = document.createElement("li")
    li_element.classList.add("list-group-item");

    var div_element = document.createElement("div");
    div_element.classList.add("input-group");
    div_element.classList.add("mb-3");

    var grams_input = document.createElement("input");
    grams_input.type = "text";
    grams_input.classList.add("form-control");
    grams_input.ariaLabel = "Amount (to the nearest gram)";
    
    var grams_of_span = document.createElement("span");
    grams_of_span.classList.add("input-group-text");
    grams_of_span.textContent = " grams of ";

    var ingredient_input = document.createElement("input");
    ingredient_input.classList.add("form-control");
    ingredient_input.readOnly = true; 
    ingredient_input.value = ingredient_textnode;
    
    var deleteButtonText = document.createTextNode("\u00D7");
    var deleteButtonSpanElement = document.createElement("span");
    deleteButtonSpanElement.ariaHidden = "true";
    deleteButtonSpanElement.appendChild(deleteButtonText);
    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.classList.add("btn"); 
    deleteButton.classList.add("close");
    //deleteButton.onClick("deleteIngredient({{ note.id }})");
    deleteButton.appendChild(deleteButtonSpanElement);
    
    div_element.appendChild(grams_input);
    div_element.appendChild(grams_of_span);
    div_element.appendChild(ingredient_input);
    div_element.appendChild(deleteButton);
    
    // Append the button element inside the list element li_element
    li_element.appendChild(div_element);

    // Append li_element to the ul element ingredients_list
    document.getElementById("ingredients_list").appendChild(li_element);
}
