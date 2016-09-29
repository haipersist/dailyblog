"""dailyblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.views import ArticleDetailView,CategoryArticleListView,TagArticleListView,TestForm,IndexView,CategoryViewset, AuthorView
from blog.urls import router as blog_route
from utils.permissions import permission_forbidden
import blog



handler404 = 'blog.views.page_not_found'
handler403 = 'blog.views.permission_forbidden'
handler500 = 'blog.views.server_broken'


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include(blog_route.urls)),
    url(r'^dashboard/',include(blog.urls)),
    #url(r'^blacklist/',include(blacklist.urls)),
    url(r'^$',IndexView.as_view(),name='index-view'),
    url(r'^article/(?P<slug>\w+).html$',ArticleDetailView.as_view(),name='article-detail-view'),
    url(r'^category/(?P<alias>\w+)/',CategoryArticleListView.as_view(),name='category-article-list-view'),
    url(r'^tag/(?P<article_tag>\w+)/$',TagArticleListView.as_view(),name='tag-article-list-view'),
    url(r'^cost/$','blog.views.TestForm',name='cost'),
    url(r'^account/login/$','blog.views.Login',name='login'),
    url(r'^logins/$','blog.views.ajax_login',name='ajax_login'),
    url(r'^account/logout/$','blog.views.Logout',name='logout'),
    url(r'^author/$', AuthorView.as_view(),name='blog_author'),
    url(r'^account/changepassword/$','blog.views.Changepassword',name='changepwd-view'),
    url(r'^account/forgetpasswd/$','blog.views.forgetpasswd',name='forgetpasswd'),
    url(r'^account/resetpwd/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','blog.views.ResetPasswd',name='resetpassword'),
    url(r'^account/register/$','blog.views.Register',name='register-view'),
    url(r'^account/activate/(?P<token>\w+.\w+.[-_\w]*\w+)/$','blog.views.active_user',name='active_user'),
]

urlpatterns += staticfiles_urlpatterns()

