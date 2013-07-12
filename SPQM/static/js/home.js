var $ = jQuery.noConflict();
$(document).ready(function () {
    // If register form had errors, show Modal and disable fade animation
    if (showRegisterForm) $('#registerModal').removeClass('fade').modal('show');
    // Enable fade animation on modal close
    $('#registerModal').on('hidden', function () {
        $('#registerModal').addClass('fade');
    });

    // Load more persons
    var button = $('#load-more .btn');
    var loading = false;
    function loadPersons() {
        // If loading is not already in progress
        if (!loading) {
            loading = true;
            button.text(button.attr('data-loading-text'));
            loader.play();
            $.ajax({
                type: 'POST',
                url: '/',
                data: {
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    number_of_persons: $('.person').length
                },
                success: function (data) {
                    data = jQuery.parseJSON(data);
                    // Where to add new persons
                    $('#main_content .row-fluid:last-of-type').after($('<div>', {'class': 'row-fluid'}));
                    // Go through all new persons and add them to the list.
                    $(data).each(function (index, person) {
                        $('#main_content .row-fluid:last-of-type').append(createPersonHtml(person));
                        // Four persons per row
                        if (index + 1 % 4 == 0) {
                            $('#main_content .row-fluid:last-of-type').after($('<div>', {'class': 'row-fluid'}));
                        }
                    });
                    loader.stop();
                    button.text(button.attr('data-text'));
                    loading = false;
                }, error: function (xhr, textStatus, errorThrown) {
                    console.log(errorThrown + xhr.status + xhr.responseText);
                }
            });
        }
    }

    // If scrolled to bottom, load persons
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() > $(document).height()) {
            loadPersons();
        }
    });

    $('#load-more').click(function () {
        loadPersons();
    });
});

function createPersonHtml(person) {
    return $('<div>', {'class': 'span3'}).append(
        $('<div>', {'class': 'person'}).append(
            $('<div>', {'class': 'person-image'}).append(
                $('<a>', {'href': '#', 'class': 'btn btn-large btn-danger'}).append($('.person a.btn:first').text()),
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
}