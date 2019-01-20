
/*鼠标下拉，导航的变化*/
$(window).scroll(function(){
    if($(window).scrollTop()>100){
        $("#header-height").addClass("min-header");
        $("#header-height").removeClass("max-header");
        $("#min-main").addClass("min-main")
    }
    else {
        $("#header-height").removeClass("min-header");
        $("#header-height").addClass("max-header");
        $("#min-main").removeClass("min-main")
    }
});

/*  手机端导航条的显示*/
$(function () {
    var box = document.getElementById("message-box");
    var message = document.getElementById("message");
    var winclose = document.getElementById("winclose");
    $('#message').click(function () {
            $(box).slideDown("slow");
            message.style.display = "none";
            winclose.style.display= "inline-block";
    });
    $("#winclose").click(function () {
        $(box).slideUp("slow");
        message.style.display = "inline-block";
        winclose.style.display= "none"
    })
});

