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
        # 展开全文
        ac = re.compile(r'<a target=\\"_blank\\" href=\\"(.*?)\\" class=\\"WB_text_opt\\"')
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
        # 展开全文
        ac = re.compile(r'<a target="_blank" href="(.*?)" class="WB_text_opt"')
    return mb, fmb, fi, fc, tm, fn, cn, ln, ac


def analyse(i, flag, now):
    mb, fmb, fi, fc, tm, fn, cn, ln, ac = select_pattern(flag)
    # 微博时间
    time = tm.findall(i)
    time = time_format(time, now)
    if time is False:
        return time
    # 微博
    micro_blog = mb.findall(i)
    # 展开全文
    all_content = ac.findall(micro_blog[0])
    if all_content:
        return all_content[0].replace('\\', '')

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

    if forward_micro_blog:
        forward_info = fi.findall(forward_micro_blog[0])
        forward_content = fc.findall(forward_micro_blog[0])
        forward_content = re.sub('<.*?>', '', forward_content[0]).replace(r'\n', '').replace(' ', '').replace(
            '\u200b', '').replace('&nbsp;', '').replace('\\t', '')
        # forward_micro_blog = re.sub('&#xe607;976&#xe608;1596ñ2742', forward_micro_blog)
        forward_micro_blog = {'forward_who': forward_info[0],
                              'forward_content': forward_content,
                              'forward_num': data_format('转发', forward_num[0]),
                              'comment_num': data_format('评论', comment_num[0]),
                              'like_num': data_format('赞', like_num[0])
                              }
        forward_num = data_format('转发', forward_num[1])
        comment_num = data_format('评论', comment_num[1])
        like_num = data_format('赞', like_num[1])
    else:
        forward_num = data_format('转发', forward_num[0])
        comment_num = data_format('评论', comment_num[0])
        like_num = data_format('赞', like_num[0])
    data = {
        'micro_blog': micro_blog,
        'forward_micro_blog': forward_micro_blog,
        'like_num': like_num,
        'comment_num': comment_num,
        'forward_num': forward_num,
        'time': time,
    }

    return data


def time_format(time, now):
    '''
    统一时间格式：2020-01-01 00：00
    :param now: 爬虫开始当前的时间
    :param time: 爬取到的时间
    :return: 如2020-01-01 00：00
    '''
    time = time[0].strip()
    if '今天' in time:
        t = datetime.strptime(time, '今天 %H:%M').replace(now.year, now.month, now.day)
    elif '分钟前' in time:
        minutes = int(time.replace('分钟前', ''))
        t = now - timedelta(minutes=minutes)
    elif '月' in time:
        t = datetime.strptime(time, '%m月%d日 %H:%M').replace(datetime.today().year)
        time_d = now - t
        if time_d.days > 31:
            return False
    else:
        return False
    time = t.strftime('%Y-%m-%d %H:%M')
    return time


def data_format(mode, dt):
    if mode in dt:
        dt = 0
    try:
        return int(dt)
    except ValueError:
        return 1000000
