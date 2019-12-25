# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class MicroblogPipeline(object):
#     def process_item(self, item, spider):
#         return item


import json

# class MicroblogPipeline(object):
#     def open_spider(self, spider):
#         self.file = open("test.json", "w", encoding="utf-8")
#
#     def process_item(self, item, spider):
#         content = json.dumps(dict(item), ensure_ascii=False) + "\n"
#         self.file.write(content)
#         return item
#
#     def close_spider(self, spider):
#         self.file.close()
from MBlog.models import MicroBlogUser
from .items import MicroUserItem

from .items import MicroblogItem


class MicroblogPipeline(object):
    def process_item(self, item, spider):
        # 判断item类型
        if isinstance(item, MicroUserItem):
            # 存库
            item.save()
        elif isinstance(item, MicroblogItem):
            item['name'] = MicroBlogUser.objects.get(name=item['name'])
            item.save()
        return item
