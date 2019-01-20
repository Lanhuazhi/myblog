
/* 登陆页面*/
$(function () {
    var nameerror = document.getElementById("name-psw-error")

    $("#submit").click(function () {
        // console.log("dddddddddddddddddd");
        $.ajax({
            cache:false,
            type: "POST",
            url:"/sign_in/",
            data: {
                'username':$("#username").val(),
                'password':$("#password").val(),
            },
            async: true,
            beforeSend:function (xhr,settings) {
                xhr.setRequestHeader("X-CSRFtoken",$.cookie("csrftoken"))
            },
            success:function (data) {
                if (data.data == "ok"){
                    location.href="/mine/"
                }
                if (data.data == "error"){
                    nameerror.style.display="block";
                }

            }
        })
    })

})
 //
 // $.ajaxSetup({
 //            beforeSend:function (xhr,settings) {
 //                xhr.setRequestHeader("X-CSRFtoken",$.cookie("csrftoken"))
 //            }
 //        });