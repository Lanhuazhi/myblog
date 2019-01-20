"""myblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from blog import search_views


handler404 = "blog.views.page_not_found"
handler500 = "blog.views.page_error"

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^', include(('blog.urls', "myblog"), namespace='myblog')),
    url(r'accounts/', include('allauth.urls')),
    url(r'mdeditor/', include('mdeditor.urls')),
    # url(r'^search/', include('haystack.urls')),
    url(r'^search/', search_views.MySeachView(), name='haystack_search'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
