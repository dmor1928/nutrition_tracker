var selectedRecipeFoodID = document.getElementById("my-recipes").id;
function toggleRecipeFoods(id) {
    if (id == selectedRecipeFoodID) {
        return 0;
    } else {
        document.getElementById(selectedRecipeFoodID + "-content").style.display = "none";
        document.getElementById(id + "-content").style.display = "block";
        selectedRecipeFoodID = id;
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