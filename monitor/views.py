from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from MBlog.models import *
from .serializer import *
from django.db.models import Q
import datetime

# 定义全局变量
user_list = None
con_list = None


# 使用APIView
class UserView(APIView):

    def get(self, request, format=None):
        # 获取筛选的粉丝数量
        num = request.GET['num']
        # 定义粉丝数量条件字典，便于查询
        num_dic = {
            "0": (0, 100000),
            "1": (100000, 500000),
            "2": (500000, 1000000),
            "3": (1000000, 100000000)
        }

        # 获取筛选的分类
        category = request.GET['category']
        # 获取筛选的时间
        time = int(request.GET['time'])
        time_point = datetime.datetime.now() - datetime.timedelta(days=+time)

        # 获取满足筛选条件的微博用户
        micro_blog_user = MicroBlogUser.objects.filter(Q(label="标签：影视明星") &
                                                       Q(fans_num__gt=num_dic[num][0]) &
                                                       Q(fans_num__lt=num_dic[num][1]))
        user = MicroBlogUserSerializer(micro_blog_user, many=True)
        # 获取满足筛选条件的相互用户的微博内容
        micro_blog_con = MicroBlog.objects.all().select_related("name"). \
            filter(Q(name__label="标签：影视明星") &
                   Q(name__fans_num__gt=num_dic[num][0]) &
                   Q(name__fans_num__lt=num_dic[num][1]) &
                   Q(time__gt=time_point))
        con = MicroBlogSerializer(micro_blog_con, many=True)

        # 修改全局变量
        global user_list, con_list
        user_list = micro_blog_user
        con_list = micro_blog_con
        return Response({"user": user.data, "con": con.data})


class UserRankView(APIView):

    def get(self, request, format=None):
        screen = request.GET["screen"]
        screen_dic = {
            "influence": "fans_num",  # 影响力
            "activity": "micro_blog_num",  # 活跃度
        }
        screen_r = "-" + screen_dic[screen]
        result_data = user_list.order_by(screen_r)[:10]

        user_li = {"name": [], "personal_head": []}
        data_li = []
        con = {}
        for user in result_data:
            user_li["name"].append(user.name)
            user_li["personal_head"].append(user.personal_head)
            if screen == "influence":
                data_li.append(user.fans_num)
            elif screen == "activity":
                data_li.append(user.attention_num)
            con[user.name] = MicroBlogSerializer(MicroBlog.objects.filter(name_id=user.id), many=True).data

        return Response({"user_li": user_li, "data_li": data_li, "con": con})


class ConRankView(APIView):

    def get(self, request, format=None):
        screen = request.GET["screen"]
        screen_dic = {
            "point": "like_num",  # 点赞数
            "comment": "comment_num",  # 评论数
            "forward": "forward_num"  # 转发量
        }
        screen_r = "-" + screen_dic[screen]
        # result_data = con_list.order_by(screen_r)[:10]
        result_data = MicroBlog.objects.all().select_related("name"). \
                          filter(Q(name__label="标签：影视明星") &
                                 Q(name__fans_num__gt=100000) &
                                 Q(name__fans_num__lt=500000)).order_by(screen_r)[:10]
        # print(result_data.query)
        user_li = {"name": [], "personal_head": []}
        con_li = []
        data_li = []
        con = {}
        for con in result_data:
            user_li["name"].append(con.name.name)
            user_li["personal_head"].append(con.name.personal_head)
            con_li.append(con.content)
            if screen == "point":
                data_li.append(con.like_num)
            elif screen == "comment":
                data_li.append(con.comment_num)
            elif screen == "forward":
                data_li.append(con.forward_num)
            if con.name.name not in user_li["name"]:
                con[con.name] = MicroBlogSerializer(MicroBlog.objects.filter(name_id=con.name), many=True).data

        return Response({"user_li": user_li, "data_li": data_li, "con_li": con_li, "con": con})
