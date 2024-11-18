/* global bootstrap: false */
(function () {
  'use strict'
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()

function toggleSidebar() {
  document.querySelector('.side-bar')
    .classList.toggle('collapse');

  var collapsableFeaturesItems = document.querySelectorAll('.features-item-dropdown');
  var collapsableFeaturesItemsArray = [...collapsableFeaturesItems];
  collapsableFeaturesItemsArray.forEach(element => {
    var myCollapse = new bootstrap.Collapse(element, {
      toggle: false
    });
    myCollapse.hide();
  }) 

  document.querySelector('main')
    .classList.toggle('main-side-bar-closed');
}