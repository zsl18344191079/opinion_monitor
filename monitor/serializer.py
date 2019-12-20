from rest_framework import serializers
from MBlog.models import *


class MicroBlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroBlogUser
        fields = ("name", "personal_head", "attention_num", "fans_num", "micro_blog_num", "profile", "address", "label")


class MicroBlogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='name.name')
    # wb_id = serializers.IntegerField()

    class Meta:
        model = MicroBlog
        fields = ("user_name", "name", "time", "content", "forward_num", "comment_num", "like_num")
