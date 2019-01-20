//文章评论
//  $.ajaxSetup({
//             beforeSend:function (xhr,settings) {
//                 xhr.setRequestHeader("X-CSRFtoken",$.cookie("csrftoken"))
//             },
//         });

$(function () {
    $("#btn-submit").click(function () {
        var article_id = this.value
        var csrfToken = $("[name='csrfmiddlewaretoken']").val();
        var comment = document.getElementById("comment").value;
        $.post("/detail/"+article_id+"/", {"comment":comment,"csrfmiddlewaretoken": csrfToken}, function (data) {
            if (data.status == "200"){
                alert("提交成功");
                // window.open("#artice-coment") /*刷新页面回到id 的文职*/
                location.href="#artice-coment"
            }
            if (data.status == "400"){
                alert("评论内容不能为空")
            }
            if (data.status == "false"){
                location.href="/accounts/login/"
            }
        })
    })
});

//点击查看回复
$(function () {
    var comment_replay = document.getElementsByClassName("comment-replay");
    var comment_replay_cancel = document.getElementsByClassName("comment-replay-cancel");
    for (var i=0;i<comment_replay.length;i++) {
        $(comment_replay[i]).click(function () {
            var fatherid = this.value
            document.getElementById("replay"+fatherid).style.display = "none";
            document.getElementById("replay-cancel"+fatherid).style.display = "block";
            $(document.getElementById("fathercomment"+fatherid)).slideDown("slow")

            // document.getElementById(fatherid).style.display ="block"
        })
    }

    for (var i=0;i<comment_replay_cancel.length;i++) {
        $(comment_replay_cancel[i]).click(function () {
            var fatherid = this.value
            document.getElementById("replay"+fatherid).style.display = "block";
            document.getElementById("replay-cancel"+fatherid).style.display = "none";
            $(document.getElementById("fathercomment"+fatherid)).slideUp("slow")
        })
    }

});

//点赞功能
$(function () {
    var click = document.getElementsByClassName("click");
    var subclick = document.getElementsByClassName("subclick");
    for (var i=0;i<click.length;i++) {
        $(click[i]) .click(function () {
            var clickid = this.value
            $.get("/on_click/",{"clickid":clickid},function (data) {
                if (data.status == "200"){
                    document.getElementById("onclick"+clickid).innerHTML =data.data
                }
                if (data.status =="400") {
                    location.href="/accounts/login/"
                }
            })
        })
    }
     for (var i=0;i<subclick.length;i++){
        $(subclick[i]).click(function () {
            var subclick_id = this.value
            $.get("/sub_on_click/",{"subclick_id":subclick_id},function (data) {
                if (data.status == "200"){
                    document.getElementById("onclick"+subclick_id).innerHTML =data.data
                }
                if (data.status =="400") {
                    location.href="/accounts/login/"
                }
            })
        })
    }
});

$(function () {
    var comment_replay = document.getElementsByClassName("comment-replay");
    var comment_replay_cancel = document.getElementsByClassName("comment-replay-cancel");
    for (var i=0;i<comment_replay.length;i++) {
        $(comment_replay[i]).click(function () {
            var fatherid = this.value
            document.getElementById("replay"+fatherid).style.display = "none";
            document.getElementById("replay-cancel"+fatherid).style.display = "block";
            $(document.getElementById("fathercomment"+fatherid)).slideDown("slow")

            // document.getElementById(fatherid).style.display ="block"
        })
    }

    for (var i=0;i<comment_replay_cancel.length;i++) {
    $(comment_replay_cancel[i]).click(function () {
        var fatherid = this.value
        document.getElementById("replay"+fatherid).style.display = "block";
        document.getElementById("replay-cancel"+fatherid).style.display = "none";
        $(document.getElementById("fathercomment"+fatherid)).slideUp("slow")
    })
    }

});

//子评论 （二级评论）
$(function () {
    var subcomment_btn = document.getElementsByClassName("subcomment-btn")
    for (var i =0 ;i<subcomment_btn.length;i++){
    $(subcomment_btn[i]).click(function () {
        var csrfToken = $("[name='csrfmiddlewaretoken']").val();
        var fatherid = this.value
        var subcomment = document.getElementById("subcomment"+fatherid).value;

        $.ajax({
            cache:false,
            type:"POST",
            url:"/subcomment/",
            data: {
                "csrfmiddlewaretoken": csrfToken,
                "fatherid": fatherid,
                "subcomment": subcomment,
            },
            async: true,
            success:function (data) {
            if (data["status"] == "200") {
                var commnent_html = "<div class=\"each-comment\">\n" +
                    "<div class=\"user\" style=\"background-image:url(" + data["subuserinfo"] + ")\"></div>\n" +
                    "<div class=\"user-comment subcomment\">\n" +
                    "<ul>\n" +
                    "<li>\n" +
                    "<div class=\"user-click\">\n" +
                    " <div class=\"username\" >\n" +
                    "<a  href=\"javascript:window.stop()\"><h5>" + data["subusername"] + "</h5></a>\n" +
                    "</div>\n" +
                    "<div class=\"group-click\">\n" +
                    "<section >\n" +
                    "<button href=\"javascript:window.stop()\" class=\"subclick \" value=\"{{ comment.id }}\"><i class=\"fa fa-thumbs-o-up\"></i></button>\n" +
                    "<span  id=\"onclick{{ comment.id }}\">" + data["on_click"] + "</span>\n" +
                    "</section>\n" +
                    "</div>\n" +
                    "</div>\n" +
                    "</li>\n" +
                    "<li class=\"comment-content\">\n" +
                    "<div style=\"font-size: 12px\"><span style=\"color: lightskyblue\">@" + data["returneduser"] + ":</span>&nbsp&nbsp" + data["subcomment"] + "</div>\n" +
                    "</li>\n" +
                    "<li class=\"comment-footer\">\n" +
                    "<span class=\"comment-time\" style=\"color: gray\">" + data["time"] + "&nbsp· &nbsp</span>\n" +
                    "</li>\n" +
                    " </ul>\n" +
                    "</div>\n" +
                    "</div>"
                $(document.getElementById("comment-show" + fatherid)).prepend(commnent_html)
                $(document.getElementById("subcomment" + fatherid)).val("")
            }
            if (data.status == "400") {
                window.open("http://lruqiao.top:8000/accounts/login/")
            }
            if (data.data == "failse") {
                alert("评论内容不能为空")
            }
            }
        })
    })

  }
})

//三级回复
$(function () {
    var subcomment_replay = document.getElementsByClassName("subcomment-replay");
    var subcomment_replay_cancel = document.getElementsByClassName("subcomment-replay-cancel");
    for (var i=0;i<subcomment_replay.length;i++) {
        $(subcomment_replay[i]).click(function () {
            var comment_father_id = this.value
            document.getElementById("replay"+comment_father_id).style.display = "none";
            document.getElementById("replay-cancel"+comment_father_id).style.display = "block";
            $(document.getElementById("subcommentwrap"+comment_father_id)).slideDown("slow")

            // document.getElementById(fatherid).style.display ="block"
        })
    }

    for (var i=0;i<subcomment_replay_cancel.length;i++) {
    $(subcomment_replay_cancel[i]).click(function () {
            var comment_father_id = this.value
            document.getElementById("replay"+comment_father_id).style.display = "block";
            document.getElementById("replay-cancel"+comment_father_id).style.display = "none";
            $(document.getElementById("subcommentwrap"+comment_father_id)).slideUp("slow")
    })
    }

});

//子评论（三级评论）
$(function () {
    var subcomment_btn_2 = document.getElementsByClassName("subcomment-btn-2");
    for (var i=0;i<subcomment_btn_2.length;i++) {
        $(subcomment_btn_2[i]).click(function () {
            var csrfToken = $("[name='csrfmiddlewaretoken']").val();
            var comment_father_id = this.value
            var subcomment_second = document.getElementById("subcomment"+comment_father_id).value;
            $.ajax({
                cache:false,
                type:"POST",
                url: "/subcomment_second/",
                data: {
                    "csrfmiddlewaretoken": csrfToken,
                    "comment_father_id": comment_father_id,
                    "subcomment_second": subcomment_second
                },
                async: true,
                success:function (data) {
                if (data["status"] == "200") {
                    var commnent_html = "<div class=\"each-comment\">\n" +
                        "<div class=\"user\" style=\"background-image:url(" + data["subuserinfo"] + ")\"></div>\n" +
                        "<div class=\"user-comment subcomment\">\n" +
                        "<ul>\n" +
                        "<li>\n" +
                        "<div class=\"user-click\">\n" +
                        " <div class=\"username\" >\n" +
                        "<a  href=\"javascript:window.stop()\"><h5>" + data["subusername"] + "</h5></a>\n" +
                        "</div>\n" +
                        "<div class=\"group-click\">\n" +
                        "<section >\n" +
                        "<button href=\"javascript:window.stop()\" class=\"subclick \" value=\"{{ comment.id }}\"><i class=\"fa fa-thumbs-o-up\"></i></button>\n" +
                        "<span  id=\"onclick{{ comment.id }}\">" + data["on_click"] + "</span>\n" +
                        "</section>\n" +
                        "</div>\n" +
                        "</div>\n" +
                        "</li>\n" +
                        "<li class=\"comment-content\">\n" +
                        "<div style=\"font-size: 12px\"><span style=\"color: lightskyblue\">@" + data["returneduser"] + ":</span>&nbsp&nbsp" + data["subcomment"] + "</div>\n" +
                        "</li>\n" +
                        "<li class=\"comment-footer\">\n" +
                        "<span class=\"comment-time\" style=\"color: gray\">" + data["time"] + "&nbsp· &nbsp</span>\n" +
                        "</li>\n" +
                        " </ul>\n" +
                        "</div>\n" +
                        "</div>"
                    $(document.getElementById("comment-show" + data["fatherid"])).prepend(commnent_html)
                    $(document.getElementById("subcomment" + comment_father_id)).val("")
                }
                if (data.status == "400") {
                    window.open("http://lruqiao.top:8000/accounts/login/")
                }
                if (data.data == "failse") {
                    alert("评论内容不能为空")
                }
            }
            })

        })

    }
});
