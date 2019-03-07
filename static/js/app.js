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
            type:"post",
            url: "like",
            data: {
                'client_id': id,
                csrfmiddlewaretoken: csrf_token
            },
            success: function(e)
            {},
            statusCode: {
                200: function(e) {
                    if (e == 'Maximum like counter') {
                        likes_error.show();
                    } else {
                        var value = parseInt(likes_input.val());
                        likes_input.val(value + 1);
                    }
                }
            },
        });
}
