var $ = jQuery.noConflict();
$(document).ready(function () {
    $('.start-tooltip').tooltip();

    // Hide message after 5 seconds
    $('ul.messages').delay(5000).fadeOut('slow');
});