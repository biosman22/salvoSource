
"""salvo re_path Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a re_path to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a re_path to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import re_path, include
    2. Add a re_path to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import  handler400, handler403, handler404, handler500
# Use include() to add URLS from the catalog application 
from django.urls import re_path , include 

#Add re_path maps to redirect the base re_path to our application
from django.views.generic import RedirectView , TemplateView

# Use static() to add re_path mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

handler404 = 'engine.views.err404'
handler500 = 'engine.views.err500'
handler403 = 'engine.views.err403'
handler400 = 'engine.views.err400'
urlpatterns = [
    re_path(r'^admin/', admin.site.urls), 
    re_path(r'^engine/', include('engine.urls')),
    re_path(r'^$', RedirectView.as_view(url='/engine/', permanent=True)),
    re_path(r'^googled011b93a1ccdb824.html/$', TemplateView.as_view(template_name="googled011b93a1ccdb824.html")),
    re_path(r'^yandex_bcad2094554f24de.html/$', TemplateView.as_view(template_name="yandex_bcad2094554f24de.html")),
    #re_path(r'^robots.txt/$', TemplateView.as_view(template_name="robots.txt",content_type='text')),
    re_path(r'^robots.txt/$', lambda r: HttpResponse("User-agent:*\nDisallow:/*?page*", content_type="text/plain")),
    re_path(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable
]
