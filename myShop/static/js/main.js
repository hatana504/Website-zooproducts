function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

const favorites_add_url = '/favorites/add/'
const favorites_remove_url = '/favorites/remove/'
const favorites_api_url = '/favorites/api/'
const favorites_add_class = 'added'

function favorites_add() {
    $('.favorites_add').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()

            const id = $(el).data('id')

            if($(e.target).hasClass(favorites_add_class)) {
                $.ajax({
                    url: favorites_remove_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(favorites_add_class)

                        get_session_favorites_statistics()
                    }
                })
                console.log(id)
            } else {
                $.ajax({
                    url: favorites_add_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(favorites_add_class)

                        get_session_favorites_statistics()
                    }
                })
                console.log('remove')
            }
        })
    })
}

function get_session_favorites() {
    get_session_favorites_statistics()

    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            for (let i = 0; i < json.length; i++) {
                $('.favorites_add').each((index, el) => {
                    const id = $(el).data('id')

                    if (json[i].id == id) {
                        $(el).addClass(favorites_add_class)
                    }
                })
            }
        }
    })
}

function get_session_favorites_statistics() {
    $.getJSON(favorites_api_url, (json) => {
        if (json != null) {
            $('#favorites_statistics').empty()
            $('#favorites_statistics').html(json.length)
        }
        if (json == null) {
            $('#favorites_statistics').empty()
            $('#favorites_statistics').html(0)
        }
    })
}

$(document).ready(function() {
    favorites_add()
    get_session_favorites()
})
