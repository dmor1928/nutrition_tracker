const addBtn = document.querySelector('.add-btn');
const list = document.querySelector('.list');

const listItems = document.querySelectorAll('.list-item');
function calculateHeightOfListContainer(){
    const firstListItem = listItems[0];
    let heightOfListItem = firstListItem.clientHeight;
    const styleTag = document.createElement('style');
    document.body.prepend(styleTag);
    styleTag.innerHTML = `.list-container.show {
        height: ${heightOfListItem}px;
    }`;
    setTimeout(function(){
        styleTag.innerHTML += `.list-container {
            transition: all 0.6s ease-out;
        }`;
    }, 0);
};
calculateHeightOfListContainer();

function removeListItem(e){
    let container = e.target;
    while(!container.classList.contains('list-container')){
        container = container.parentElement;
    }
    container.classList.remove('show');
    const listItem = container.querySelector('.list-item');
    listItem.classList.remove('show');
    setTimeout(function(){
        container.classList.remove('show');
        container.ontransitionend = function(){
          container.remove();
        }
    }, 350);
}

//DOCUMENT LOAD
document.querySelectorAll('.list .list-container').forEach(function(container) {
    container.onclick = removeListItem;
});

addBtn.onclick = function(e){
    const container = document.createElement('li'); container.classList.add('list-container'); container.setAttribute('role', 'listitem');
    const listItem = document.createElement('div'); listItem.classList.add('list-item'); listItem.innerHTML = 'List Item';
    container.append(listItem);
    addBtn.parentNode.insertBefore(container, addBtn);
    container.onclick = removeListItem;
    setTimeout(function(){
        container.classList.add('show');
        setTimeout(function(){
            listItem.classList.add('show');
        }, 350);
    }, 15);
}