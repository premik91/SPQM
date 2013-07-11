var $ = jQuery.noConflict();
$(document).ready(function () {
    function loadPersons() {
        $.ajax({
            type: 'POST',
            url: '/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                number_of_persons: $('.person').length
            },
            success: function (data) {
                // Where to add new persons
                $('.row-fluid:last-of-type').after($('<div>', {'class': 'row-fluid'}));

                // Go through all new persons and add them to the list.
                data = jQuery.parseJSON(data);
                $(data).each(function (index, person) {
                    $('.row-fluid:last-of-type').append(
                        $('<div>', {'class': 'span3'}).append(
                            $('<div>', {'class': 'person'}).append(
                                $('<div>', {'class': 'person-image'}).append(
                                    $('<a>', {'href': '#', 'class': 'btn btn-large btn-danger'}),
                                    $('<img>', {'alt': 'person', 'src': '/static/img/anonymous.png'})
                                ),
                                $('<div>', {'class': 'well widget'}).append(
                                    $('<div>', {'class': 'widget-header'}).append(
                                        $('<h3>', {'class': 'title'}).append(
                                            person.fields.information.fields.first_name + ' ' + person.fields.information.fields.last_name
                                        )
                                    ),
                                    $('<p>').append('Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.')
                                )
                            )
                        )
                    );
                    if (index + 1 % 4 == 0) {
                        // Four persons per row
                        $('.row-fluid:last-of-type').after($('<div>', {'class': 'row-fluid'}));
                    }
                });
                return false
            },
            error: function (xhr, textStatus, errorThrown) {
                alert(errorThrown + xhr.status + xhr.responseText);
            }
        });
    }

    $('#load-more').click(function () {
        loadPersons();
    });
});