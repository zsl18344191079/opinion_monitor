from django.shortcuts import render


def home(request):
    """首页"""
    return render(request, 'monitor/home.html')


def condition_screen(request):
    """条件筛选"""
    return render(request, 'monitor/screen.html')


def ranking_list(request):
    """排行榜"""
    return render(request, 'monitor/rank.html')
