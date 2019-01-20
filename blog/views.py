from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
import markdown
from django.http import JsonResponse
import time
from django.db.models import Q
from .models import Comment ,Click,SubComment,SecondComment,Articles,SubClick,Group,Tag
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from allauth.socialaccount.models import SocialAccount

# Create your views here.


def home(request):
    article = Articles.objects.all().order_by("-views")[0:5]
    return render(request, "home.html",{"article":article})


def Mine(request):
    userinfo = request.user
    userinfor= getinfo(userinfo)

    group_type = Group.objects.all()
    group_name_article_list = []
    for group_name in group_type:
        group_name_article = Articles.objects.filter(goupname = group_name)[0:5]
        data = {
            "group_name_article":group_name_article,
            "group_name":group_name
        }
        group_name_article_list.append(data)

    article_ranking = Articles.objects.all().order_by("time")[0:6]

    #标签云的展示
    tags_show = Tag_show()

    # 归档
    data_time_list = Date_time()

    # 最新评论
    new_comment = Comment.objects.all().order_by("time")[0:5]

    context ={}
    context["userinfor"] = userinfor
    context["article_types"] = group_name_article_list
    context["group_type"] = group_type
    context["article_ranking"] =article_ranking
    context["tags_show"] =tags_show
    context["data_time_list"] =data_time_list
    context["new_comment"] = new_comment
    return render(request,"mine_content.html",context)


#标签云
def Tag_show():
    tags_show = Tag.objects.all().order_by("name")
    return tags_show

# 归档
def Date_time():
    data_time = Articles.objects.get_data_time()
    data_time_list = []
    for time in data_time:
        time_list = time.split('/')
        data_time = {
            "year": time_list[0],
            "month": time_list[1]
        }
        data_time_count = Articles.objects.filter(time__icontains=data_time["year"] + "-" + data_time["month"]).count()
        data_time["count"] = data_time_count
        data_time_list.append(data_time)
    return data_time_list


def Detail(request,id):
    userinfo = request.user
    userinfor = getinfo(userinfo)
    if request.method == "POST":
        if request.user.is_authenticated:
            username = request.user.username
            comment = request.POST.get("comment")
            if comment:
                times = time.strftime("%Y-%m-%d %H:%M:%S")
                comment = Comment(username=username,userinfo=userinfor,comment=comment,time=times,article_id=id)
                comment.save()
                return JsonResponse({"status":200})
            else:
                return JsonResponse({"status":400})
        else:
            return JsonResponse({"status":"false"})
    showcomment = Comment.objects.filter(article=id).order_by('-time')
    sub_count = 0
    for item in showcomment:
        sub_count += item.subcomment_set.count()
    commentcount = showcomment.count()+sub_count
    article_views = Articles.objects.get(id = id)
    article_views.articlecomments =commentcount
    article_views.save()
    showcommentpage = Paginator(showcomment,5)
    page = request.GET.get('page')
    try:
        showcommentpages = showcommentpage.page(page)
    except PageNotAnInteger:
        showcommentpages = showcommentpage.page(1)

    # pagenum = showcommentpage.num_pages
    # for i in range(1,showcommentpage.num_pages+1):
    #     a = showcommentpage.page(i).object_list
    # print(showcommentpage.count) # 对象总数
    # print(showcommentpage.num_pages) # 总页数
    # print(showcommentpage.page(2).object_list) # 每页的展示数
    # print(showcommentpage.page(2)) # 获取当前页
    comment_list = SubComment.objects.all().order_by("-time")
    # 文章详情的展示
    articles = Articles.objects.get(id=id)
    articles.views += 1
    articles.save()
    # mfile = open('E://git.md', 'r',encoding='UTF-8').read()
    # articles.content = mfile
    articles.content = markdown.markdown(articles.content.replace("\r\n", '  \n'),
                           extensions=[
                               # 包含 缩写、表格等常用扩展
                               'markdown.extensions.extra',
                               # 语法高亮扩展
                               'markdown.extensions.codehilite',
                           ])

    context ={}
    context["userinfor"] = userinfor
    context["showcomentpage"] = showcommentpages
    context["commentcount"] = commentcount
    context["comment_list"] = comment_list
    context["article"] = articles
    return render(request,"detail.html",context)


#登陆页面
def Sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            request.session["username"] = username
            login(request, user)  # 用户登录
            return JsonResponse({"data": "ok"})
        else:
            return JsonResponse({"data":"error"})

    return render(request,"sign_in.html")


#退出登录
def Login_out(request):
    logout(request)
    return redirect("/")


#注册页面
def Sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password=password.replace(' ','')
        passwordagain = request.POST.get("passwordagain")
        passwordagain = passwordagain.replace(" ","")
        print(username)
        try:
            user = User.objects.get(username=username)
            if user:
                return JsonResponse({"data":"error"})

        except User.DoesNotExist:
            if password ==passwordagain:
                user1 = User.objects.create_user(username=username, password=password)
                user1.save()
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                return JsonResponse({"data":"ok"})
            else:
                return JsonResponse({"data":"msg"})
    return render(request,"sign_up.html")


# 获取个人头像
def getinfo(user):
    # User 模型的使用方法
    # user = request.user.username
    #
    # # socicalaccount = user.socialaccount_set.exists()
    # print(user)
    # print(type(user))
    userinfor = "/static/blog/detail/img/_20190103193128.jpg"
    # if user :
    # 判断是否第三方账号登陆
    if user.is_authenticated:
        socicalaccount = user.socialaccount_set.exists()
    # 如果是第三方账号登陆的，则获取第三方账号的头像
        if socicalaccount:
            # 通过外键获取
            userinfor = user.socialaccount_set.first().get_avatar_url()
            # print(userinfor)
        # 通过导入模型直接获取
        # userinfo = SocialAccount.objects.first()..get_avatar_url()
        return userinfor
    return userinfor


#点赞
def On_click(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            username = request.user.username
            print(username)
            if request.path == "/on_click/":
                clickid = request.GET.get("clickid")
                print(clickid)
                clickuser = Comment.objects.get(id=clickid)
                # 选择该条评论的点赞用户，过滤出来是登陆用户的
                userlick = clickuser.click_set.filter(username=username)
                #如果登陆用户还没点赞过这条评论则加1
                if not userlick:
                    print("该用户还没点赞")
                    clickuser.onclick += 1
                    clickuser.save()
                    click = Click(username=username)
                    click.save()
                    click.target.add(clickuser)
                    return JsonResponse({"data": clickuser.onclick, "status": 200})
                else:
                    clickuser.onclick -= 1
                    clickuser.save()
                    # 移除该用户和评论的关系
                    userlick[0].target.remove(clickuser)
                    userlick[0].delete()
                    return JsonResponse({"data": clickuser.onclick, "status": 200})
            elif request.path == "/sub_on_click/":
                print("88888888888888888888")
                clickid = request.GET.get("subclick_id")
                print(clickid)
                clickuser = SubComment.objects.get(id=clickid)
                # 选择该条评论的点赞用户，过滤出来是登陆用户的
                userlick = clickuser.subclick_set.filter(subusername=username)
                print(userlick)
                #如果登陆用户还没点赞过这条评论则加1
                if not userlick:
                    print("该用户还没点赞")
                    clickuser.onclick += 1
                    clickuser.save()
                    click = SubClick(subusername=username)
                    click.save()
                    click.target.add(clickuser)
                    return JsonResponse({"data": clickuser.onclick, "status": 200})
                else:
                    clickuser.onclick -= 1
                    clickuser.save()
                    # 移除该用户和评论的关系
                    userlick[0].target.remove(clickuser)
                    userlick[0].delete()
                    return JsonResponse({"data": clickuser.onclick, "status": 200})

        return JsonResponse({"status":400})


#子评论
def Subcomments(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            userinfo = request.user
            userinfor = getinfo(userinfo)
            data = {}
            username = request.user.username
            print(username)
            if request.path == "/subcomment/":
                subcomment =request.POST.get("subcomment")
                print(subcomment)
                fatherid =request.POST.get("fatherid")
                print(fatherid)
                returned_username = Comment.objects.get(id = fatherid)
                if subcomment:
                    times = time.strftime("%Y-%m-%d %H:%M:%S")
                    subcomments = SubComment()
                    subcomments.subusername = username
                    subcomments.returneduser = returned_username.username
                    subcomments.subuserinfo = userinfor
                    subcomments.subcomment = subcomment
                    subcomments.time = times
                    subcomments.fathercomment_id = fatherid
                    subcomments.save()
                    data["status"] = "200"
                    data["subusername"] = subcomments.subusername
                    data["returneduser"] = subcomments.returneduser
                    data["subuserinfo"] = subcomments.subuserinfo
                    data["subcomment"] = subcomments.subcomment
                    data["on_click"] = subcomments.onclick
                    data["time"] = subcomments.time
                    return JsonResponse(data)
                return JsonResponse({"data":"failse"})
            elif request.path == "/subcomment_second/":
                subcomments_second = request.POST.get("subcomment_second")
                comment_father_id = request.POST.get("comment_father_id")
                returned = SubComment.objects.get(id=comment_father_id)
                if subcomments_second:
                    times = time.strftime("%Y-%m-%d %H:%M:%S")
                    second_comments = SecondComment()
                    second_comments.subusername = username
                    second_comments.returneduser = returned.subusername
                    second_comments.subuserinfo = userinfor
                    second_comments.subcomment = subcomments_second
                    second_comments.time = times
                    second_comments.fathercomment_id = returned.fathercomment_id
                    second_comments.second_father_comments_id = comment_father_id
                    second_comments.save()
                    data["status"] = "200"
                    data["subusername"] = second_comments.subusername
                    data["returneduser"] = second_comments.returneduser
                    data["subuserinfo"] = second_comments.subuserinfo
                    data["subcomment"] = second_comments.subcomment
                    data["time"] = second_comments.time
                    data["on_click"] = second_comments.onclick
                    data["fatherid"] = second_comments.fathercomment_id
                    return JsonResponse(data)
            else:
                return JsonResponse({"data": "failse"})
    return JsonResponse({"status":"400"})


# 或取分类全部的文章
def ArticleMore(request,tags_id,group_id):
    tags_show = Tag_show()
    if tags_id == "0" and group_id =="0":
        year = request.GET.get("year")
        print(year)
        month = request.GET.get("month")
        print(month)
        detail_show = Articles.objects.filter(time__icontains=year + "-" + month)
        name = year + "-"+month
    elif tags_id == "0":
        detail_show = Articles.objects.filter(goupname_id = group_id)
        name = Group.objects.get(id = group_id)
    else:
        detail_show = Articles.objects.filter(tags=tags_id)
        name = Tag.objects.get(id =tags_id)

    # 归档展示
    data_time_list = Date_time()

    new_comment = Comment.objects.all().order_by("time")[0:5]

    context={}
    context["tags_show"] = tags_show
    context["detail_show"] = detail_show
    context["name"] = name
    context["data_time_list"] =data_time_list
    context["new_comment"] = new_comment
    return render(request,"article.html",context)

# 404
def page_not_found(request):
    return render(request,'error/404.html')

#500
def page_error(request):
    return render(request,'error/500.html')
