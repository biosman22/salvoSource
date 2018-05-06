
from django.contrib import sitemaps
from django.urls import reverse
from .models import video_info

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1
    changefreq = 'daily'

    def items(self):
        return ['index',]

    def location(self, item):
        return reverse(item)

