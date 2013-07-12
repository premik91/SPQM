var $ = jQuery.noConflict();
$(document).ready(function () {
    $('.start-tooltip').tooltip();

    // Hide message after 10 seconds
    $('ul.messages').delay(5000).fadeOut('slow');
});