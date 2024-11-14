// $('#ingredients-table').on('click', 'tbody tr', function(event) {

//     document.getElementById("MyElement").classList.add('MyClass');

//     $(this).addClass('highlight').siblings().removeClass('highlight');
//     console.log("clicked");
//   });

var selected_food_ids = [];
var index = 0;
var selected_appended_class = 'table-primary';
var selected_ingredients_nutrition = {};
var selected_ingredients_rda_percent = total_recipe_user_rda_percent;

for (let key in total_recipe_nutrition) {  // Initialise empty selected_ingredients_nutrition
    if (key != "fdc_id") {
        selected_ingredients_nutrition[key] = total_recipe_nutrition[key];
    }
}

console.log("recipe_ingredients_data TYPE: ");
console.log(typeof recipe_ingredients_data);
console.log(recipe_ingredients_data);

function clickRow(clicked_id){  // Highlights the row

    selected_ingredients_rda_percent = {};

    var new_food_id = clicked_id.split("-")[0];

    for (let key in total_recipe_nutrition) {  // Initialise selected_ingredients_nutrition and selected_ingredients_rda_percent
        if (key != "fdc_id") {
            selected_ingredients_nutrition[key] = 0.0;
            selected_ingredients_rda_percent[key] = 0.0;
        }
    }
    
    var selected_elements = document.getElementsByClassName('selected_appended_class');
    for (var i=0; i< selected_elements.length; i++ ) {
        selected_food_ids.push(selected_elements[i].id);
    }

    if (document.getElementById(clicked_id).classList.contains(selected_appended_class) ) {  // If already contains clicked id, toggle off
        document.getElementById(clicked_id).classList.remove(selected_appended_class);
        selected_food_ids = selected_food_ids.filter(e => e !== new_food_id);

        if (selected_food_ids.length == 0) {  // Show total recipe nutrition
            for (let key in selected_ingredients_nutrition) {
                selected_ingredients_nutrition[key] = total_recipe_nutrition[key];
            }
        }
    } else { 
        document.getElementById(clicked_id).classList.add(selected_appended_class);
        selected_food_ids.push(new_food_id);  // Add to selected_food_ids and update selected_ingredients_nutrition
    }


    var ingredient_amounts = {}
    for (let i = 0; i < selected_food_ids.length; i++) {
        var id = selected_food_ids[i];
        ingredient_amounts[id] = parseFloat(document.getElementById(id + '-ingredientAmount').innerHTML);
    }

    for (let i = 0; i < selected_food_ids.length; i++) {
        var food_id = selected_food_ids[i];
        var ingredient_index = recipe_ingredients_data.findIndex(obj => (obj.food_id).toString() === food_id.toString());
        var ingredient = recipe_ingredients_data[ingredient_index];
        var ingredient_nutrition = getIngredientPortionNutrition(ingredient.nutrition_per_100g, ingredient.amount);

        for (let key in ingredient_nutrition) {
            selected_ingredients_nutrition[key] += parseFloat(ingredient_nutrition[key]);            
        }
    }

    for (let key in selected_ingredients_nutrition) {
        selected_ingredients_nutrition[key] = Math.round(parseFloat(selected_ingredients_nutrition[key]) * 100) / 100;
        // console.log("key: " + key.toString() + ", amount: " + selected_ingredients_nutrition[key].toString());
    }


    for (let key in selected_ingredients_nutrition) {
        var nutrient_rda = parseFloat(user_rda[key]);
        // console.log("Nutrient rda: ");
        // console.log(nutrient_rda);
        
        selected_ingredients_rda_percent[key] = parseFloat(selected_ingredients_nutrition[key]) / nutrient_rda * 100;
        selected_ingredients_rda_percent[key] = Math.round(parseFloat(selected_ingredients_rda_percent[key]) * 10) / 10;

        var limited_selected_ingredients_rda_percent = selected_ingredients_rda_percent[key]
        if (selected_ingredients_rda_percent[key] > 100) {
            limited_selected_ingredients_rda_percent = 100;
        }

        try {
            document.getElementById(key.concat("-", "progressbar")).style.width = limited_selected_ingredients_rda_percent.toString() + "%";
            document.getElementById(key.concat("-", "progressbar")).ariaValueNow = selected_ingredients_rda_percent[key].toString();
            document.getElementById(key.concat("-", "percentage")).innerHTML = selected_ingredients_rda_percent[key].toString() + "%";
            // console.log("key: " + key.toString());
            // console.log("selected_ingredients_rda_percent[" + key + "].toString() + '%': ");
            // console.log(selected_ingredients_rda_percent[key].toString() + "%");
        }
        catch(err) {
            // console.log("key-progressbar doesn't exist, which is fine: " + key);
            // console.log("Error code: " + err);
            // console.log("selected_ingredients_nutrition[key]: ");
            // console.log(selected_ingredients_nutrition[key]);
        }
        finally {
            // console.log("key: " + key.toString());
            document.getElementById(key.concat("-", "nutrientAmount")).innerHTML = selected_ingredients_nutrition[key];
        }
            
    }
}

function getIngredientPortionNutrition(ingredient_nutrition_per_100g, amount) {
    var ingredient_nutrition = {};
    for (let key in ingredient_nutrition_per_100g) {
        ingredient_nutrition[key] = parseFloat(ingredient_nutrition_per_100g[key]) * amount / 100;
    }
    return ingredient_nutrition;
}

function showRDA(el) {
    var percent, nutrient_key;
    percent = el.getElementsByTagName("small")[0];
    nutrient_key = percent.id.replace('-percentage', '');
    percent.style.opacity = 0;
    setTimeout(function(){ 
        percent.innerHTML = "RDA: " + (Math.round(user_rda[nutrient_key] * 10) / 10).toString() + " " + nutrient_units[nutrient_key];
        percent.style.opacity = 1;
    },100);
}

function showPercentage(el) {
    var percent, nutrient_key;
    percent = el.getElementsByTagName("small")[0];
    nutrient_key = percent.id.replace('-percentage', '');
    percent.style.opacity = 0;
    setTimeout(function(){ 
        percent.innerHTML = selected_ingredients_rda_percent[nutrient_key].toString() + "%";
        percent.style.opacity = 1;
    },100);
}

const showRDACheckbox = document.getElementById("flexSwitchCheckShowRDA");

function toggleRDA(checkboxElem) {
    var progress_bar_labels
    if (checkboxElem.checked) {
        console.log("Checkbox is checked..");
        progress_bar_labels = document.getElementsByClassName("progress position-relative");
        console.log(progress_bar_labels);
        for (let i = 0; i < progress_bar_labels.length; i++) {
            var el = progress_bar_labels[i]
            showRDA(el);
        }
    } else {
        console.log("Checkbox is not checked..");
        progress_bar_labels = document.getElementsByClassName("progress position-relative");
        console.log(progress_bar_labels);
        for (let i = 0; i < progress_bar_labels.length; i++) {
            var el = progress_bar_labels[i]
            showPercentage(el);
        }
    }
};