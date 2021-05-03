function code(callback) {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    var image_code_url = "/user/imagecode?uuid=" + uuid;
    callback(uuid, image_code_url)
}

function showCode() {
    code(function (uuid, image_code_url) {
        $('#code_img').attr('src', image_code_url)
        $('#uuuid').val(uuid)
    })
}


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
    showCode(); //页面一加载显示 下面点击切换
    $(".code").click(function () {
        showCode();
    });

    //为表单的提交自定义的函数行为    (事件e)
    $(".form-register").submit(function (e) {
        e.preventDefault();
        username = $("#username").val();
        code = $("#code").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        email = $("#email").val();
        uuuid = $('#uuuid').val();
        if (!username || !code || !passwd || !passwd2 || !email) {
            alert("参数不完整，请重新填写！");
            return;
        }
        //调用ajax向后端发送请求,防止重复校验
        var request_data = {
            username: username,
            code: code,
            password: passwd,
            password2: passwd2,
            email: email,
            uuid: uuuid
        };

        var request_json = JSON.stringify(request_data);

        $.ajax({
            url: "",
            type: "post",
            data: request_json,
            contentType: "application/json",
            dataType: "json",
            success: function (resp) {
                if (resp.errno == "0") {
                    alert(resp.errmsg);
                    //注册成功跳转登录页面
                    location.href = "/";
                }
                else {
                    alert(resp.errmsg);
                }
            }
        })
    });
});