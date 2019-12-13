from django.shortcuts import render
from django.http import JsonResponse


def get_data(request):
    user = [
        {"id": 1, "name": '小红', "sex": '男', "introduction": '美食博主', "fens_num": 123456, "label": '美食', "article": 8},
        {"id": 2, "name": '小明', "sex": '男', "introduction": '美食博主', "fens_num": 123456, "label": '美食', "article": 8},
        {"id": 3, "name": '小明', "sex": '男', "introduction": '美食博主', "fens_num": 123456, "label": '美食', "article": 8},
    ]
    con = [
        {"name": "我是林柏宏", "time": "12月6日 22:27", "content":
            "一不注意，故事就說到2020年了",
         "forward_num": 39, "comment_num": 192, "like_num": 1104, "forward_content": None},
        {"name": "我是林柏宏", "time": "12月6日 22:27", "content":
            "一不注意，故事就說到2020年了",
         "forward_num": 39, "comment_num": 192, "like_num": 1104, "forward_content": None},
        {"name": "我是林柏宏", "time": "12月6日 22:27", "content":
            "一不注意，故事就說到2020年了 ",
         "forward_num": 39, "comment_num": 192, "like_num": 1104, "forward_content": None},
        {"name": "我是林柏宏", "time": "12月6日 22:27", "content":
            "一不注意，故事就說到2020年了 ",
         "forward_num": 39, "comment_num": 192, "like_num": 1104, "forward_content": None},
        {"name": "我是林柏宏", "time": "12月6日 22:27", "content":
            "一不注意，故事就說到2020年了 ",
         "forward_num": 39, "comment_num": 192, "like_num": 1104, "forward_content": None},

    ]

    return JsonResponse({"status": 200, "message": user, "con": con})


def rank_data(request):
    user = ["小明", "小红", "小军", "王丽", "小草", "大树", "小明", "小红", "小军", "王丽"]
    con = [89, 80, 75, 68, 62, 60, 56, 53, 50, 45]
    return JsonResponse({"status": 200, "message": user, "con": con})

