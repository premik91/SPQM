var $ = jQuery.noConflict();
$(document).ready(function () {
    $('.slider').slider({
        range: 'max',
        min: 0,
        max: 100,
        value: 60,
        animate: true,
        slide: function (event, ui) {
            console.log(ui.value);
        }
    });
});