
/*向下滑动局部更新*/
var border = document.getElementsByClassName("detail-article")
var i =0
$(window).scroll(function(){
    var top = $(window).scrollTop();
    var height = $(window).height();
    var height1 = $(document).height()
             if(height1-height-top ==0) {
                 $(border[i+1]).fadeIn(3000)
                 i+=1
          }
});

/*搜索框*/
$(function () {
   var barrage = document.getElementById("welcome");
   var search = document.getElementById("find") ;
   $("#leads-1").click(function () {
       barrage.style.display = "none";
       search.style.display ="inline-block"
   })
})


