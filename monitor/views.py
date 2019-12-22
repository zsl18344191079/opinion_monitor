from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.db.models import Q
import datetime
import re
from collections import Counter

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
                   Q(time__gt="{}".format(time_point)))
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

        con_rank = []
        data_rank = []
        con_data = {"name": [], "personal_head": [], "con": {}}
        for user in result_data:
            con_rank.append(user.name)
            con_data["name"].append(user.name)
            con_data["personal_head"].append(user.personal_head)
            if screen == "influence":
                data_rank.append(user.fans_num)
            elif screen == "activity":
                data_rank.append(user.attention_num)
            con_data["con"][user.name] = MicroBlogSerializer(MicroBlog.objects.filter(name_id=user.id), many=True).data

        return Response({"con_rank": con_rank, "data_rank": data_rank, "con_data": con_data})


class ConRankView(APIView):

    def get(self, request, format=None):
        screen = request.GET["screen"]
        screen_dic = {
            "point": "like_num",  # 点赞数
            "comment": "comment_num",  # 评论数
            "forward": "forward_num"  # 转发量
        }
        screen_r = "-" + screen_dic[screen]
        result_data = con_list.order_by(screen_r)[:10]

        con_rank = []
        data_rank = []
        con_data = {"name": [], "personal_head": [], "con": {}}

        for con in result_data:
            if con.name.name not in con_data["name"]:
                con_data["name"].append(con.name.name)
                con_data["personal_head"].append(con.name.personal_head)
                con_data["con"][con.name.name] = \
                    MicroBlogSerializer(MicroBlog.objects.filter(name=con.name.id),many=True).data

            con_rank.append(con.content)
            if screen == "point":
                data_rank.append(con.like_num)
            elif screen == "comment":
                data_rank.append(con.comment_num)
            elif screen == "forward":
                data_rank.append(con.forward_num)

        return Response({"con_rank": con_rank, "data_rank": data_rank, "con_data": con_data})


class WordCloudTrendView(APIView):
    def get(self, request, format=None):
        global user_list
        data_dic = {}
        for user in user_list:
            data_dic[user.address[0:2]] = data_dic.get(user.address[0:2], 0) + 1

        data_li = []
        for (key, val) in data_dic.items():
            data_li.append({"name": key, "value": val})

        # 排序
        data_li = sorted(data_li, key=lambda x: x["value"], reverse=True)
        return Response({"data": data_li})


class WordCloudView(APIView):
    def get(self, request, format=None):
        micro_blog_con = MicroBlog.objects.all().select_related("name"). \
                                                filter(Q(name__label="标签：影视明星") &
                                                       Q(name__fans_num__gt=10000) &
                                                       Q(name__fans_num__lt=50000) &
                                                       Q(content__contains="#"))
        print(micro_blog_con.query)
        data_li = []
        for con in micro_blog_con:
            result = re.findall(r"#.*?#", con.content)
            if result:
                for i in result:
                    data_li.append(i)
        data = Counter(data_li)
        return Response({"data": data})
