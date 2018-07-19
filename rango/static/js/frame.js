$(document).on('submit', '#like', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/like/',
        data:{
            category_id:$('#cat-id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function () {
            $('#like_count').load(' #like_count');
        }

        });
});


$(function () {

    $('#search').keyup(function () {

        $.ajax({
            type: 'POST',
            url: '/search/',
            data: {
                search_text: $('#search').val(),
                category: $('#cat-name').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
               $('#pagesx').html(data);
            }

        });

    });

});


$(function () {

    $('#searchcategory').keyup(function () {

        $.ajax({
            type: 'POST',
            url: '/categorysearch/',
            data: {
                search_text: $('#searchcategory').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                $('#catresult').html(data);
            }
            });
    });

});