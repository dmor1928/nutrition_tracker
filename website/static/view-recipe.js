// $('#ingredients-table').on('click', 'tbody tr', function(event) {

//     document.getElementById("MyElement").classList.add('MyClass');

//     $(this).addClass('highlight').siblings().removeClass('highlight');
//     console.log("clicked");
//   });

var selected_food_ids = [];
var index = 0;
var selected_appended_class = 'table-primary';
var selected_nutrition_information = {};

for (let key in total_recipe_nutrition) {  // Initialise empty selected_nutrition_information
    if (key != "food_id") {
        selected_nutrition_information[key] = 0.0;
    }
}

console.log("recipe_foods_nutrition TYPE: ");
console.log(typeof recipe_foods_nutrition);
console.log(recipe_foods_nutrition);
console.log("total_recipe_nutrition: ");
console.log(total_recipe_nutrition);
console.log(typeof total_recipe_nutrition);


function clickRow(clicked_id){  // Highlights the row

    var new_food_id = clicked_id.split("-")[0];

    for (let key in total_recipe_nutrition) {  // Initialise selected_nutrition_information to zero
        if (key != "food_id") {
            selected_nutrition_information[key] = 0.0;
        }
    }
    
    var selected_elements = document.getElementsByClassName('selected_appended_class');
    for (var i=0; i< selected_elements.length; i++ ) {
        selected_food_ids.push(selected_elements[i].id);
    }

    if (document.getElementById(clicked_id).classList.contains(selected_appended_class) ) {  // If already contains clicked id, toggle off
        document.getElementById(clicked_id).classList.remove(selected_appended_class);

        // var ingredient_to_subtract_in_array = recipe_foods_nutrition.filter( obj => {
        //     return (obj.food_id === parseInt(food_id));
        // })
        // var ingredient_to_subtract = ingredient_to_subtract_in_array[0];

        selected_food_ids = selected_food_ids.filter(e => e !== new_food_id);

        if (selected_food_ids.length == 0) {  // Show total recipe nutrition
            
            // selected_nutrition_information = total_recipe_nutrition;
            for (let key in selected_nutrition_information) {
                selected_nutrition_information[key] = total_recipe_nutrition[key];
            }

        }
        // else {
        //     for (let key in selected_nutrition_information) {
        //         selected_nutrition_information[key] = selected_nutrition_information[key] - parseFloat(ingredient_to_subtract[key]);
        //     }
        // }
    }

    else {  // Toggle on
        document.getElementById(clicked_id).classList.add(selected_appended_class);
    
        selected_food_ids.push(new_food_id);  // Add to selected_food_ids and update selected_nutrition_information
    
    }

    var ingredients_to_add_amount = [];
    for (let i = 0; i < selected_food_ids.length; i++) {
        var id = selected_food_ids[i];
        ingredients_to_add_amount.push(parseFloat(document.getElementById(id + '-amount').innerHTML) / 100);
    }
    
    console.log("ingredients_to_add_amount: ");
    console.log(ingredients_to_add_amount);


    for (let i = 0; i < selected_food_ids.length; i++) {
        var id = selected_food_ids[i];
        console.log("id: ");
        console.log(id);
        
        var ingredient_to_add_in_array = recipe_foods_nutrition.filter( obj => {
            return (obj.food_id === parseInt(id));
        })
        console.log("ingredient_to_add_in_array: ");
        console.log(ingredient_to_add_in_array);
        var ingredient_to_add = ingredient_to_add_in_array[0];

        for (let key in selected_nutrition_information) {
            selected_nutrition_information[key] = Math.round((parseFloat(selected_nutrition_information[key]) + parseFloat(ingredient_to_add[key]) * ingredients_to_add_amount[i]) * 100) / 100;
            console.log("selected_nutrition_information[key]");
            console.log(selected_nutrition_information[key]);
        }
    }

    // console.log("selected_nutrition_information: ");
    // console.log(selected_nutrition_information);

    console.log("selected_food_ids: ");
    console.log(selected_food_ids);

    console.log("selected_nutrition_information: ");
    console.log(selected_nutrition_information);

    console.log("new_food_id: ");
    console.log(new_food_id);

    for (let key in selected_nutrition_information) {
        if (key != "food_id") {
            // console.log("key: " + key);
            // console.log(selected_nutrition_information[key]);
            document.getElementById(key).innerHTML = selected_nutrition_information[key];
        }
    }
}
