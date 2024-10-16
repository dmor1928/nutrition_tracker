//Defining a listener for add_ingredient button (specifically, an onclick handler)
document.getElementById("add_ingredient").onclick  = function() {

    // Create list element
    var li_element = document.createElement("Li")
    li_element.classList.add("list-group-item");

    // Get the value of element selected by ingredient dropdown
    var ingredient_text = document.getElementById("ingredient").value; 

    // Create a text node of the value of element selected in dropdown
    var ingredient_textnode=document.createTextNode(ingredient_text);


    /*
    Recreating the delete button from home.html example
    each thing in the unordererd list ul:
    
    <li id= class="list-group-item">
        <div class="input-group mb-3">
            <input type="text" class="form-control" aria-label="Amount (to the nearest dollar)">
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
    grams_input.type = "text";
    grams_input.classList.add("form-control");
    grams_input.ariaLabel = "Amount (to the nearest gram)";
    
    var grams_of_span = document.createElement("span");
    grams_of_span.classList.add("input-group-text");
    grams_of_span.textContent = " grams of ";

    var ingredient_input = document.createElement("input");
    ingredient_input.classList.add("form-control");
    ingredient_input.readOnly = true; 
    ingredient_input.value = ingredient_text;
    
    var delete_button_text = document.createTextNode("\u00D7");
    var delete_button_span_element = document.createElement("span");
    delete_button_span_element.ariaHidden = "true";
    delete_button_span_element.appendChild(delete_button_text);
    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.classList.add("btn"); 
    deleteButton.classList.add("close");

    var li_element_id = ingredient_text.replace(/\s+/g, '-').toLowerCase();
    li_element_id = li_element_id.replaceAll(",", "");
    li_element_id = li_element_id + "-li";
    li_element.id = li_element_id;
    
    // When clicked, run delete_recipe_ingredient function and input its id
    //deleteButton.addEventListener("click", delete_recipe_ingredient());
    deleteButton.onclick = function(){
        console.log("clicked");
        document.getElementById(li_element_id).parentNode.removeChild(document.getElementById(li_element_id));
    }

    deleteButton.appendChild(delete_button_span_element);
    
    div_element.appendChild(grams_input);
    div_element.appendChild(grams_of_span);
    div_element.appendChild(ingredient_input);
    div_element.appendChild(deleteButton);
    
    // Append the button element inside the list element li_element
    li_element.appendChild(div_element);

    // Append li_element to the ul element ingredients_list
    document.getElementById("ingredients_list").appendChild(li_element);
    console.log(li_element.id); 
}