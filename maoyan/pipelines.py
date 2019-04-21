# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import os.path
import urllib3
import maoyan.spiders.DB as db
class MaoyanPipeline(object):
    def process_item(self, item, spider):
        # today = time.strftime('%Y%m%d', time.localtime())
        #
        # base_dir = os.getcwd()
        # fiename = base_dir + '/a.txt'
        # with open(fiename, 'a', encoding='utf-8') as f:
        #     f.write(item['b_movieName'] + '\n')
        #     f.write(item['b_boxInfo'] + '\n')
        db.insertBox(item)
        return item


