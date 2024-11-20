var selectedRecipeFoodID = "recipes-and-foods";
function toggleRecipeFoods(new_id) {
    if (new_id == selectedRecipeFoodID) {
        return 0;
    } else {
        document.getElementById(selectedRecipeFoodID + "-content").style.display = "none";
        document.getElementById(new_id + "-content").style.display = "block";
        selectedRecipeFoodID = new_id;
    }
}

function favouriteItem(element) {
    if (element.classList.contains("bi-star-fill")) {
        element.classList.remove("bi-star-fill");
        element.classList.add("bi-star");
    } else {
        element.classList.remove("bi-star");
        element.classList.add("bi-star-fill");
    }
}