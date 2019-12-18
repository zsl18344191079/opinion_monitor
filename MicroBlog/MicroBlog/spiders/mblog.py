# -*- coding: utf-8 -*-
import json
import re

import scrapy

from ..items import MicroUserItem, MicroblogItem
from ..utility import analyse


class MblogSpider(scrapy.Spider):
    name = 'mblog'
    allowed_domains = ['weibo.com']
    start_urls = ('https://weibo.com/',)

    def parse(self, response):
        html = response.text
        # 微博找人地址
        find_lst = re.findall(
            r'<a class=\\"S_txt1\\" target=\\"_blank\\" suda-uatrack=\\"key=nologin_home&value=nologin.*?\\" '
            r'href=\\"(.*?)\\" >.*?<span .*?>(.*?)<\\/span><\\/a>',
            html)
        # （地址，分类）
        for url, category in find_lst:
            url = url.replace('\\', '')
            yield scrapy.Request(url=url, meta={'category': category}, callback=self.usr_list, dont_filter=True)

    def usr_list(self, response):
        html = response.text
        category = response.meta['category']
        url = 'https://d.weibo.com'
        # 解析，正则匹配：姓名，主页地址，简介，标签
        mod_info_list = re.findall(r'<dd class=\\"mod_info S_line1\\">(.*?)<\\/dd>', html)

        for mod_info in mod_info_list:
            # 姓名
            name = re.findall(r'<strong  usercard=\\".*?\\" >(.*?)<\\/strong>', mod_info)[0]
            # 主页地址
            href = re.findall(r'<a class=\\"S_txt1\\" target=\\"_blank\\".*?href=\\"(.*?)\\" title=\\".*?\\" >',
                              mod_info)[0].replace('\\', '').replace('//', 'https://')
            # 标签
            label = re.findall(r'<div class=\\"info_relation\\">(.*?)<\\/div>', mod_info)
            # 简介
            profile = re.findall(r'<em class=\\"tit S_txt2\\">简介<\\/em><span>(.*?)<\\/span>', mod_info)[0]
            # 错误页
            error = re.findall(r'https://weibo.com/\?refer_flag=.*', href)
            if error:
                continue
            # 地址
            address = re.findall(r'<em class=\\"tit S_txt2\\">地址<\\/em><span>(.*?)<\\/span>', mod_info)[0]

            personal_url = href + '&is_all=1'
            data = {
                'name': name,
                'address': address,
                'profile': profile,
                'category': category,
                'label': label[0] if label else ''
            }
            yield scrapy.Request(url=personal_url,
                                 meta=data,
                                 callback=self.micro, dont_filter=True)
        # 下一页
        next_page = re.findall(r'<a bpfilter=\\"page\\" class=\\"page next S_txt1 S_line1\\" href=\\"\\(.*?)\\">',
                               html)
        if next_page:
            url = url + next_page[0]
            yield scrapy.Request(url=url, meta={'category': category}, callback=self.usr_list, dont_filter=True)

    def micro(self, response):
        home_html = response.text
        name = response.meta['name']
        label = response.meta['label']
        category = response.meta['category']
        profile = response.meta['profile']
        address = response.meta['address']
        time_flag = 0

        # 下次请求所需参数
        domain = re.findall(r"\$CONFIG\['domain'\]='(.*?)';", home_html)[0]
        pg_id = re.findall(r"\$CONFIG\['page_id'\]='(.*?)';", home_html)[0]

        # 关注，粉丝，微博数
        afm = re.findall(r'<strong class=\\".*?\\">(.*?)<\\/strong>', home_html)
        print(afm)

        # 头像图片地址
        personal_head = re.findall(r'<p class=\\"photo_wrap\\">.*?<img src=\\"(.*?)\\".*?>', home_html)[0].replace('\\',
                                                                                                                   '')
        user_item = MicroUserItem()
        user_item['category'] = category
        user_item['label'] = label
        user_item['micro_blog_num'] = afm[2]
        user_item['attention_num'] = afm[0]
        user_item['fans_num'] = afm[1]
        user_item['address'] = address
        user_item['profile'] = profile
        user_item['personal_head'] = personal_head
        user_item['name'] = name
        yield user_item

        micro_blog_list = re.findall(
            r'<div .*? tbinfo=\\".*?\\" .*?>(.*?)<div node-type=\\"feed_list_repeat\\" '
            r'class=\\"WB_feed_repeat S_bg1\\" style=\\"display:none;\\">',
            home_html)
        for i in micro_blog_list:
            data = analyse(i, 1)
            if data['time'] is False:
                time_flag += 1
                continue
            item = MicroblogItem()
            item['time'] = data['time']
            item['content'] = data['micro_blog']
            item['forward_num'] = data['forward_num']
            item['comment_num'] = data['comment_num']
            item['like_num'] = data['like_num']
            item['forward_content'] = data['forward_micro_blog']
            yield item

        if time_flag >= 2:
            return
        anchor_url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?domain={}&is_all=1&id={}'.format(domain, pg_id)
        # 访问第一页中间15条
        mid_url = anchor_url + '&pagebar=0&page=1&pre_page=1'
        yield scrapy.Request(url=mid_url, meta={'flag': 3, 'page': 1, 'anchor_url': anchor_url, 'name': name},
                             callback=self.micro_next,
                             dont_filter=True)

    def micro_next(self, response):
        time_flag = 0
        home_html = response.text
        name = response.meta['name']
        # 这里的数据格式为json{"code":"100000","msg":"","data":"*****需要的******"}
        home_html = json.loads(home_html)
        json_data = re.sub('\\s+', ' ', home_html['data'])

        # 解析个人发的微博
        micro_blog_list = re.findall(
            '<div.*?tbinfo=".*?".*?>(.*?)'
            '<div node-type="feed_list_repeat" class="WB_feed_repeat S_bg1" style="display:none;">',
            json_data)

        for i in micro_blog_list:
            data = analyse(i, 2)
            if data['time'] is False:
                time_flag += 1
                continue
            item = MicroblogItem()
            item['time'] = data['time']
            item['content'] = data['micro_blog']
            item['forward_num'] = data['forward_num']
            item['comment_num'] = data['comment_num']
            item['like_num'] = data['like_num']
            item['forward_content'] = data['forward_micro_blog']
            yield item

        if time_flag != 0:
            return
        else:
            flag = response.meta['flag']
            page = response.meta['page']
            anchor_url = response.meta['anchor_url']
            data = {
                'page': page,
                'name': name,
                'anchor_url': anchor_url,
            }
            if flag == 1:
                # 下一页
                next = re.findall('<a action-type="login" class="page next S_txt1 S_line1".*?>(.*?)</a>', json_data)
                if next:
                    url = anchor_url + '&page={}'.format(page + 1)
                    data['flag'] = 2
                    data['page'] += 1
                    yield scrapy.Request(url=url, meta=data,
                                         callback=self.micro_next,
                                         dont_filter=True)
                else:
                    return
            elif flag == 2:
                url = anchor_url + '&pagebar=0&page={}&pre_page={}'.format(page, page)
                data['flag'] = 3
                yield scrapy.Request(url=url, meta=data,
                                     callback=self.micro_next,
                                     dont_filter=True)
            elif flag == 3:
                url = anchor_url + '&pagebar=1&page={}&pre_page={}'.format(page, page)
                data['flag'] = 1
                yield scrapy.Request(url=url, meta=data,
                                     callback=self.micro_next,
                                     dont_filter=True)
