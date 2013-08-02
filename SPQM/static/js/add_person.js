var $ = jQuery.noConflict();
$(document).ready(function () {
    $('.btn.icon-plus').click( function () {
        addField($(this).parents('.control-group').find('label').attr('for'));
    });

    function addField (field_type) {
        // TODO:
        if (field_type == 'id_video') {
        } else {}
    }

    // Remove field
    $('.controls').on('click', '.btn.icon-remove', function () {
        $(this).parent('li').remove();
    });

    // Form submit
    $('#add-person').submit( function () {
        // TODO:
        // Loop though all quotes
        $('.field-section .controls').each( function () {
        });
    });
});