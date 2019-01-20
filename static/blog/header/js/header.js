/* 侧滑菜单*/
$(document).ready(function(){
    var message = document.getElementById("message");
    var winclose = document.getElementById("winclose");
    var header = document.getElementsByClassName("right-mobile-header")
	$("#message").click(function(){
        $(header).animate({right:"+=65%"})
        message.style.display = "none";
	    winclose.style.display= "inline-block";
	});
	$("#winclose").click(function(){
		$(header).animate({right:"-=65%"});
		message.style.display = "inline-block";
	    winclose.style.display= "none";
	});
});
