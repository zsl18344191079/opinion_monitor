from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from MBlog import views

router = DefaultRouter()
router.register(r'micro_blog_users', views.MicroBlogUserViewSet)
router.register(r'micro_blog', views.MicroBlogViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
