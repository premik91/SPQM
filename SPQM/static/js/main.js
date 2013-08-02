var $ = jQuery.noConflict();
$(document).ready(function () {
    // If register form had errors, show Modal and disable fade animation
    if (showRegisterForm) $('#registerModal').removeClass('fade').modal('show');
    // Display login form if it had errors
    if (showLoginForm) $('#user_forms').trigger('click');

    // Enable fade animation on modal close
    $('#registerModal').on('hidden', function () {
        $(this).addClass('fade');
    });

    $('.start-tooltip').tooltip();

    // Hide message after 5 seconds
    $('ul.messages').delay(5000).fadeOut('slow');
});