/* 悬停弹出图片提示框*/

$(document).ready(function(){
    $('#weixin').popover({
        trigger: 'hover',//鼠标以上时触发弹出提示框
        html:true,//开启html 为true的话，data-content里就能放html代码了
        content:"<img src='/static/blog/base/img/Screenshot_2018-12-22-01-47-23-842_com.tencent.mm.png'>"
        }

    );
});

$(document).ready(function(){
    $('#qq').popover({
        trigger: 'hover',//鼠标以上时触发弹出提示框
        html:true,//开启html 为true的话，data-content里就能放html代码了
        content:"<img src='/static/blog/base/img/Screenshot_2018-12-22-02-22-24-.png'>"
        }

    );
});

/* 隐藏导航条*/
$(window).scroll(function(){
    var top = $(window).scrollTop();
    // var height = $(window).height();
    var width = $(window).width()
    // console.log(height)
    if(top >1000 && width>768) {
        $("#header-height").fadeOut()
    }
    else {
        $("#header-height").fadeIn()
    }
});

// $(function () {
//     var get_article = document.getElementById("get_article").value
//     $("#my_aricle").click(function () {
//         location.href ="/mine/#my-aricle1/"
//     })
//
// })