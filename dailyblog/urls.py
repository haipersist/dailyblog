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
from apps.blog.views import ArticleDetailView,CategoryArticleListView,TagArticleListView, \
    IndexView,AuthorView
from apps.blog.urls import router as blog_route


from django.conf import settings
from django.conf.urls.static import static



handler404 = 'apps.blog.views.page_not_found'
handler403 = 'apps.blog.views.permission_forbidden'
handler500 = 'apps.blog.views.server_broken'


admin.autodiscover()

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='web-index-view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include(blog_route.urls)),
    url(r'^blog/',include('apps.blog.urls')),
    url(r'^comment/',include('apps.comment.urls')),
    url(r'^dashboard/',include('apps.dashboard.urls')),
    url(r'^account/',include('apps.account.urls')),
    url(r'^trip/',include('apps.trip.urls')),
    url(r'^job/',include('apps.job.urls')),
    url(r'^wechat/',include('apps.wechat.urls')),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),
    url(r'^author/',AuthorView.as_view(),name='author-display'),
    url(r'^advise/','apps.blog.views.mail_to_bloger',name='advise_to_blogger'),
    url(r'^article/(?P<slug>\w+).html$',ArticleDetailView.as_view(),name='article-detail-view'),
    url(r'^category/(?P<alias>\w+)/',CategoryArticleListView.as_view(),name='category-article-list-view'),
    url(r'^tag/(?P<article_tag>\w+)/$',TagArticleListView.as_view(),name='tag-article-list-view'),
   ]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


