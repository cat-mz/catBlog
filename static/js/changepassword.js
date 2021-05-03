$(function () {
    /***
     * 分隔符号 ： 前后端分离 解决 csrf_token
     */

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /***
     * 分隔符号 ： 前后端分离 解决 csrf_token
     */

    $('.change_password').submit(function (e) {
        e.preventDefault();
        email = $('#email').val();
        data_content = {
            'email': email
        };
        data_JSON = JSON.stringify(data_content);
        $.ajax({
            url: '',
            type: 'post',
            data: data_JSON,
            contentType: 'application/json',
            dataType: 'json',
            success: function (resp) {
                if (resp.errno == 0) {
                    window.location.href = '/'
                } else {
                    alert(resp.errmsg)
                }
            }
        })
    })

});