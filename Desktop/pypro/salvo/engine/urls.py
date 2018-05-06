from django.urls import re_path, path

from . import views
from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticViewSitemap


sitemaps = {'static':StaticViewSitemap,}


urlpatterns = [
    re_path(r'^$', views.index.as_view(), name='index'),
    #re_path(r'^test/', views.test, name='test'),
    re_path(r'^about/', views.about, name='about'),
    re_path(r'^f', views.frame, name='video_info_ajax'),
    re_path(r'^l', views.play_list, name='playlist'),
    re_path(r'^just_titles', views.just_all_titles, name='titles'),
    re_path(r'^more', views.more, name='ajax_more'),
    re_path(r'^top5/', views.top5, name='top5'),
    re_path(r'^t/(?P<stub>.+)$', views.top, name='top'),
    re_path(r'^sitemap\.xml/$', views.AwesomeSitemap ,name ="sitemap"),
    re_path(r'^test$', views.progress_view ,name ="test"),
    path("ds_file" , views.download_and_return),
    path("dc_file" , views.get_the_file),

]
