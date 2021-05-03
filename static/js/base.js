$(function () {
    username = $.cookie('username');
    is_Login = $.cookie('is_Login');
    social_name = $.cookie('name');
    if (is_Login && username) {
        $('#user_center_logout').show();
        $('#user_Login_register').hide();
        document.getElementById('u_name').innerHTML = username;
    } else {
        $('#user_center_logout').hide();
        $('#user_Login_register').show();
    }
    if (social_name) {
        document.getElementById('u_name').innerHTML = social_name;
        $.cookie('is_Login', true, {expires: 14});
        $('#user_center_logout').show();
        $('#user_Login_register').hide();
    }

    // 导航条active状态切换
    $('.navbar-nav li a').each(function () {
        if (this.href == document.location.href) {
            $(this).parent().addClass('active');
        }
    });
    // top
    $(window).scroll(function () {
        var $totop = $('.totop');
        var iNum = $(document).scrollTop();
        if (iNum > 80) {
            $totop.fadeIn();
        } else {
            $totop.fadeOut();
        }
        $totop.click(function () {
            $("html,body").stop().animate({
                "scrollTop": 0
            })
        })
    })
});