from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from MBlog.models import MicroBlogUser, MicroBlog
from MBlog.serializers import MicroBlogUserSerializer, MicroBlogSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'micro_blog_users': reverse('micro-blog-user-list', request=request, format=format),
        'micro_blog': reverse('micro-blog-list', request=request, format=format)
    })


class MicroBlogUserViewSet(viewsets.ModelViewSet):
    queryset = MicroBlogUser.objects.all()
    serializer_class = MicroBlogUserSerializer


class MicroBlogViewSet(viewsets.ModelViewSet):
    queryset = MicroBlog.objects.filter(name_id__lt=10)
    serializer_class = MicroBlogSerializer
