/*
document.getElementById("add_ingredient").onclick = function() {
    //First things first, we need our text:
    var text = document.getElementById("ingredient").value; //.value gets input values

    //Now construct a quick list element
    var li = "<li>" + text + "</li>";

    //Now use appendChild and add it to the list!
    document.getElementById("ingredients_list").appendChild(li);
}
*/

//Defining a listener for add_ingredient button (specifically, an onclick handler)
document.getElementById("add_ingredient").onclick  = function() {

    // Create list element
    var node = document.createElement("Li");
    node.classList.add("list-group-item");

    // Get the value of element selected by ingredient dropdown
    var text = document.getElementById("ingredient").value; 

    // Create a text node of the value of element selected in dropdown
    var textnode=document.createTextNode(text);

    // Append text node to the list element
    node.appendChild(textnode);

    /*
    Recreating the delete button from home.html example
    <button type="button" class="close" onClick="deleteNote({{ note.id }})">
            <span aria-hidden="true">&times;</span>
    </button> */

    
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

    // Append the button element inside the node
    node.appendChild(deleteButton);

    // Append the list element to the list element ingredients_list
    document.getElementById("ingredients_list").appendChild(node);
}
