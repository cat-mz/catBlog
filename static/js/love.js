 //需要jquery插件
    /* 鼠标特效 */
    var a_idx = 0;
    jQuery(document).ready(function($) {
        $("body").click(function(e) {
            var a = new Array("❤不做咸鱼！❤","❤拒绝懒惰！❤","❤想做吃货❤","❤拒绝单身❤","❤向大佬学习❤","❤扶我起来~❤","❤come on❤","❤一直在路上~❤","❤累了~❤","❤再趴一会❤","❤66666❤","❤高兴的飞起*****❤");
            var $i = $("<span></span>").text(a[a_idx]);
            a_idx = (a_idx + 1) % a.length;
            var x = e.pageX,
            y = e.pageY;
            $i.css({
                "z-index": 999999999999999999999999999999999999999999999999999999999999999999999,
                "top": y - 20,
                "left": x,
                "position": "absolute",
                "font-weight": "bold",
                "color": "rgb("+~~(255*Math.random())+","+~~(255*Math.random())+","+~~(255*Math.random())+")"
            });
            $("body").append($i);
            $i.animate({
                "top": y - 180,
                "opacity": 0
            },
            1500,
            function() {
                $i.remove();
            });
        });
    });


$(function(){
    $('.user-img').mouseover(function(){
        console.log("123");
        $("#user-img").css("transform"," rotate(360deg)");
    })
    $(".user-img").mouseout(function(){
        $("#user-img").css("transform"," rotate(0deg)");
      });
})
