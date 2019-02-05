function deleteClient(id) {
    if (confirm('Are you sure?')) {
        form = document.getElementById("deleteClientForm_" + id);
        form.submit();
    } else {
        return false;
    }
}

function likePhoto(id) {
    csrf_token = $(".like-form").find('input[name=csrfmiddlewaretoken]').val();
    likes_input = $("#like-counter_" + id);
    likes_error = $("#likes_error_" + id);
    $.ajax(
        {
            type:"patch",
            url: "api/like",
            data: {
                'client_id': id,
                csrfmiddlewaretoken: csrf_token
            },
            success: function(e)
            {},
            statusCode: {
                200: function() { 
                    var value = parseInt(likes_input.val());
                    likes_input.val(value + 1);
                },
                304: function() { 
                    likes_error.show();
                }
            },
        });
}
