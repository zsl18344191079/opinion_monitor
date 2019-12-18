import re
from datetime import datetime, timedelta


def select_pattern(flag):
    if flag == 1:
        # 微博
        mb = re.compile(r'<div class=\\"WB_text W_f14\\" node-type=\\"feed_list_content\\".*?>(.*?)<\\/div>')
        # 转发别人的微博
        fmb = re.compile(
            r'<div class=\\"WB_expand S_bg1\\" node-type=\\"feed_list_forwardContent\\">(.*?)'
            r'<div class=\\"WB_expand_media_box\\"')
        # 别人
        fi = re.compile(r'<a suda-uatrack=\\"key=feed_headnick.*?>(.*?)<\\/a>')
        # 转发内容
        fc = re.compile(r'<div class=\\"WB_text\\" node-type=\\"feed_list_reason\\">(.*?)<\\/div>')
        # 微博时间
        tm = re.compile(r'<div class=\\"WB_from S_txt2\\">.*?<a name=.*?>(.*?)<\\/a>')
        # 转发数
        fn = re.compile(r'<em class=\\"W_ficon ficon_forward S_ficon\\">&#xe607;<\\/em><em>(.*?)<\\/em>')
        # 评论数
        cn = re.compile(r'<em class=\\"W_ficon ficon_repeat S_ficon\\">&#xe608;<\\/em><em>(.*?)<\\/em>')
        # 点赞量
        ln = re.compile(r'<em class=\\"W_ficon ficon_praised S_txt2\\">ñ<\\/em><em>(.*?)<\\/em>')

    else:
        # 微博
        mb = re.compile(r'<div class="WB_text W_f14" node-type="feed_list_content".*?>(.*?)</div>')
        # 转发别人的微博
        fmb = re.compile(
            r'<div class="WB_expand S_bg1" node-type="feed_list_forwardContent">(.*?)'
            r'<div class="WB_expand_media_box')
        # 别人
        fi = re.compile(r'<a suda-uatrack="key=feed_headnick.*?>(.*?)</a>')
        # 转发内容
        fc = re.compile(r'<div class="WB_text" node-type="feed_list_reason">(.*?)</div>')
        # 微博时间
        tm = re.compile(r'<div class="WB_from S_txt2">.*?<a name=.*?>(.*?)</a>')
        # 转发数
        fn = re.compile(r'<em class="W_ficon ficon_forward S_ficon">&#xe607;</em><em>(.*?)</em>')
        # 评论数
        cn = re.compile(r'<em class="W_ficon ficon_repeat S_ficon">&#xe608;</em><em>(.*?)</em>')
        # 点赞量
        ln = re.compile(r'<em class="W_ficon ficon_praised S_txt2">ñ</em><em>(.*?)</em>')
    return mb, fmb, fi, fc, tm, fn, cn, ln


def analyse(i, flag):
    mb, fmb, fi, fc, tm, fn, cn, ln = select_pattern(flag)
    # 微博时间
    time = tm.findall(i)
    # 微博
    micro_blog = mb.findall(i)
    micro_blog = re.sub('<.*?>', '', micro_blog[0]).replace(r'\n', '').replace('&nbsp;', '').strip().replace(
        '\u200b', '').replace(r'\\', '')
    # 转发别人的微博
    forward_micro_blog = fmb.findall(i)
    # 转发数
    forward_num = fn.findall(i)
    # 评论数
    comment_num = cn.findall(i)
    # 点赞量
    like_num = ln.findall(i)

    if '转发' in forward_num:
        forward_num[forward_num.index('转发')] = 0
    if '评论' in comment_num:
        comment_num[comment_num.index('评论')] = 0
    if '赞' in like_num:
        like_num[like_num.index('赞')] = 0

    if forward_micro_blog:
        forward_info = fi.findall(forward_micro_blog[0])
        forward_content = fc.findall(forward_micro_blog[0])
        forward_content = re.sub('<.*?>', '', forward_content[0]).replace(r'\n', '').replace(' ', '').replace(
            '\u200b', '').replace('&nbsp;', '').replace('\\t', '')
        # forward_micro_blog = re.sub('&#xe607;976&#xe608;1596ñ2742', forward_micro_blog)
        forward_micro_blog = {'forward_who': forward_info[0],
                              'forward_content': forward_content,
                              'forward_num': forward_num[0],
                              'comment_num': comment_num[0],
                              'like_num': like_num[0]
                              }
        forward_num = forward_num[1]
        comment_num = comment_num[1]
        like_num = like_num[1]
    else:
        like_num = like_num[0]
        comment_num = comment_num[0]
        forward_num = forward_num[0]

    data = {
        'micro_blog': micro_blog,
        'forward_micro_blog': forward_micro_blog,
        'like_num': like_num,
        'comment_num': comment_num,
        'forward_num': forward_num,
        'time': time_format(time),
    }

    return data


def time_format(time):
    '''
    统一时间格式：2020-01-01 00：00
    :param time: 爬取到的时间
    :return: 如2020-01-01 00：00
    '''
    time = time[0].lstrip()
    t = None
    if '今天' in time:
        now = datetime.now()
        t = datetime.strptime(time, '今天 %H:%M').replace(now.year, now.month, now.day)
    elif '分钟前' in time:
        now = datetime.now()
        minutes = int(time.replace('分钟前', ''))
        t = now - timedelta(minutes=minutes)
    elif '月' in time:
        t = datetime.strptime(time, '%m月%d日 %H:%M').replace(datetime.today().year)
    else:
        return False
    if t:
        time = t.strftime('%Y-%m-%d %H:%M')
    return time
