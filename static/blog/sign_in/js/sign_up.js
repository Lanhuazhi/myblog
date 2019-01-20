
/* 注册页面*/

$(function () {
    var namenone = document.getElementById("name-none");
    var pswerror = document.getElementById("psw-error");
     var username = document.getElementById("username")
    var password = document.getElementById("password");
    var nameerror = document.getElementById("name-error");
    var pswnone = document.getElementById("psw-none");

      username.addEventListener("focus",function () {
        nameerror.style.display = "none"
    },false);

      password.addEventListener("focus",function () {
        pswnone.style.display = "none"
    },false);

     username.addEventListener("blur",function () {
         namenone.style.display="none";
         pswerror.style.display = "none"
        instr = this.value;
        if (instr.length<3 || instr.length>12){
            nameerror.style.display = "block";
            pswnone.style.display = "none"
            return
                }
        else {
            password.addEventListener("blur",function () {
                namenone.style.display="none";
                pswerror.style.display = "none"
                 var user = $.trim(username.value)
                 if (user=="") {
                     nameerror.style.display = "block"
                 }else {
                     psw = $.trim(this.value)
                     if (psw == ""){
                         pswnone.style.display = "block"
                     }
                     else {
                            $("#submit-signup").click(function () {
                                $.ajax({
                                    cache:false,
                                    type: "POST",
                                    url:"/sign_up/",
                                    data: {
                                        'username':$("#username").val(),
                                        'password':$("#password").val(),
                                        'passwordagain':$("#password-again").val()
                                    },
                                    async: true,
                                     beforeSend:function (xhr,settings) {
                                        xhr.setRequestHeader("X-CSRFtoken",$.cookie("csrftoken"))
                                    },
                                    success:function (data) {
                                        if (data.data == "error"){
                                            namenone.style.display="block";
                                        }
                                          if (data.data == "msg"){
                                              pswerror.style.display = "block"
                                              namenone.style.display="none";
                                          }
                                          if (data.data=="ok"){
                                              location.href="/mine/";
                                          }
                                    }
                                })
                              })
                     }
                 }
             })
        }
     });

})










     //
