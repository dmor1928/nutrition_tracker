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

    // Get the value of element selected by ingredient dropdown
    var text = document.getElementById("ingredient").value; 

    // Create a text node of the value of element selected in dropdown
    var textnode=document.createTextNode(text);

    // Append text node to the list element
    node.appendChild(textnode);

    // Append the list element to thelist element ingredients_list
    document.getElementById("ingredients_list").appendChild(node);
}
