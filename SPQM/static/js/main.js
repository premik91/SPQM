var $ = jQuery.noConflict();
$(document).ready(function () {
    $('.start-tooltip').tooltip();
    $('.slider').slider({
        range: 'max',
        min: 0,
        max: 100,
        value: 60,
        animate: true
    });
});