"""opinion_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls.static import static

# from django.views.generic.base import TemplateView
from opinion_monitor import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('monitor.urls')),
                  url(r'^', include('MBlog.urls')),
                  url(r'^api-auth/', include('rest_framework.urls')),
                  # django-allauth插件
                  re_path(r'^accounts/', include('allauth.urls')),
                  # django-allauth用户信息扩展
                  re_path(r'^accounts/', include('Myaccount.urls', namespace='accounts')),
                  # path('', TemplateView.as_view(template_name="index.html"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件
