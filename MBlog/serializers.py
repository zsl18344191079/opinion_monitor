from rest_framework import serializers

from MBlog.models import MicroBlog, MicroBlogUser


class MicroBlogSerializer(serializers.ModelSerializer):
    micro_blog_user_name = serializers.ReadOnlyField(source='name.name')

    class Meta:
        model = MicroBlog
        fields = "__all__"


class MicroBlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroBlogUser
        fields = "__all__"
