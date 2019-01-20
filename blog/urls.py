
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from blog import views



urlpatterns = [
    # 博客首页
    url(r"^$", views.home, name="home"),

    # 博客个人中心
    url(r'^mine/$', views.Mine, name="mine"),

    # 文章详情页面展示
    url(r"^detail/(?P<id>\d+)/$", views.Detail, name="detail"),

    # 登陆页面
    url(r'^sign_in/$', views.Sign_in, name="sign_in"),

    # 注册页面
    url(r'^sign_up/$', views.Sign_up, name="sign_up"),

    # 退出登录
    url(r"^login_out/$", views.Login_out, name="login_out"),

    #点赞
    url(r"^on_click/$",views.On_click,name="on_click"),

    #子点赞
    url(r"^sub_on_click/$",views.On_click,name="sub_on_click"),

    #根评论
    # url(r"^comment/$",views.Comments,name="comment"),

    #子评论/二级评论
    url(r"^subcomment/$",views.Subcomments,name="subcomment"),

    #子评论/三级评论
    url(r"^subcomment_second/$",views.Subcomments,name="subcomment_second"),

    # 更多文章
    url(r"^article/(?P<tags_id>\d+)/(?P<group_id>\d+)/",views.ArticleMore,name="article"),

    # #404
    # url(r'^404/$',views.page_not_found,name="404"),
    #
    # #500
    # url(r'^500/$',views.page_error,name="500")

    # 获取用户信息
    # url(r'^accounts/baidu/login/callback/',views.Userinfo, name="login")
]
