# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem
import re
import requests
from fontTools.ttLib import TTFont
import os
import json
from lxml import etree
import datetime
NUM_ATTR = {
        '8': {'x': '177', 'y': '388', 'on': '1'},
        '7': {'x': '47', 'y': '622', 'on': '1'},
        '6': {'x': '410', 'y': '534', 'on': '1'},
        '5': {'x': '134', 'y': '195', 'on': '1'},
        '1': {'x': '373', 'y': '0', 'on': '1'},
        '3': {'x': '130', 'y': '201', 'on': '1'},
        '4': {'x': '323', 'y': '0', 'on': '1'},
        '9': {'x': '139', 'y': '173', 'on': '1'},
        '2': {'x': '503', 'y': '84', 'on': '1'},
        '0': {'x': '42', 'y': '353', 'on': '1'},
        '.': {'x': '20', 'y': '20', 'on': '1'},
    }
class MaoyanspiderSpider(scrapy.Spider):
    name = 'maoyanSpider'
    allowed_domains = ['maoyan.com']

    # start_urls = ['http://www.maoyan.com/board/4?offset=%s'%i for i in range(0,100,10)]
    # https://maoyan.com/films?showType=3
    # start_urls = ['http://maoyan.com/films?showType=3&offset=%s' % i for i in range(0, 1800, 30)]
    # start_urls = ['https://maoyan.com/films?showType=3']
    # start_urls = ['http://maoyan.com/films/%s' % i for i in range(100000, 1000000, 1)]
    base_url = 'http://maoyan.com'
    # start_urls = ['http://maoyan.com/films?showType=3&yearId=1&offset=%s' % i for i in range(0, 1890, 30)]
    start_urls = ['http://box.maoyan.com/promovie/api/box/second.json']
    def parse(self, response):  # 解析函数，用来解析返回的结果，提取数据
        # response对象里面scrapy已经封装好了xpath、css方法，可以直接用
        # xpath就是写xpath，css就是写css选择器，返回的都是一个list
        # 这个是用xpath获取页面上所有的电影

        # 下面是css选择器
        # all_movie = response.css('dl.board-wrapper dd')
        item = MaoyanItem()  # 实例化item
        sites = json.loads(response.body_as_unicode())
        list = sites['data']['list']
        for l in list:
            item['b_movieName'] = l['movieName']
            item['b_avgSeatView'] = l['avgSeatView']
            item['b_avgShowView'] = l['avgShowView']
            item['b_avgViewBox'] = l['avgViewBox']
            item['b_boxInfo'] = l['boxInfo']
            item['b_movieId'] = l['movieId']
            item['b_releaseInfo'] = l['releaseInfo']
            item['b_seatRate'] = l['seatRate']
            item['b_showInfo'] = l['showInfo']
            item['b_showRate'] = l['showRate']
            item['b_splitAvgViewBox'] = l['splitAvgViewBox']
            item['b_splitBoxInfo'] = l['splitBoxInfo']
            item['b_splitBoxRate'] = l['splitBoxRate']
            item['b_splitSumBoxInfo'] = l['splitSumBoxInfo']
            item['b_sumBoxInfo'] = l['sumBoxInfo']
            item['b_viewInfo'] = l['viewInfo']
            item['b_viewInfoV2'] = l['viewInfoV2']
            item['b_currentTime'] = datetime.datetime.now()
            yield item

        # all_movie = response.css('ul[class="row"]')
        # # all_movie = response.xpath('//dl=[@class="movie-list"]')
        # # 这个是用css选择器获取到，效果和xpath是一样的
        # for movie in all_movie:
        #     item = MaoyanItem()  # 实例化item
        #     item['b_ranking'] = response.css('li[class="col0"]::text').extract()[0]
        #     item['b_movie'] = response.css('li[class="col1"] p[class="first-line"]::text').extract()[0]
        #     item['b_time'] = response.css('li[class="col1"] p[class="second-line"]::text').extract()[0]
        #     item['b_time'] = response.css('li[class="col2 tr"]::text').extract()[0] + '万'
        #     item['b_average_price'] = response.css('li[class="col3 tr"]::text').extract()[0]
        #     item['b_average_people'] = response.css('li[class="col4 tr"]::text').extract()[0]
        #     item['b_deadline'] = datetime.datetime.now().strftime('%Y-%m-%d')


    def download_font(self, link):
        download_link = 'http://vfile.meituan.net/colorstone/' + link
        woff = requests.get(download_link)
        with open(r'./fonts/' + link, 'wb') as f:
            f.write(woff.content)

    def get_font(self, link):
        file_list = os.listdir(r'.\fonts')
        if link not in file_list:
            self.download_font(link)
            print("字体不在库中:", link)
        else:
            print("字体在库中:", link)
        self.font = TTFont('./fonts/' + link)
        self.transform = './transform/' + link.replace('.woff', '.json')

    def modify_data(self, data):
        print(data)
        trans_form = self.get_transform()
        for name, num in trans_form.items():
            if name in data:
                data = data.replace(name, num)
        return data

    def get_transform(self):
        file_list = os.listdir(r'.\transform')
        if self.transform in file_list:
            with open(self.transform, 'r') as f:
                file = f.read()
            return json.loads(file)
        else:
            translate_form = self.parse_transform()
            with open(self.transform, 'w') as f:
                f.write(json.dumps(translate_form))
            return translate_form

    def parse_transform(self):
        self.font.saveXML('trans.xml')
        tree = etree.parse("trans.xml")
        TTGlyph = tree.xpath(".//TTGlyph")
        translate_form = {}
        for ttg in TTGlyph[1:11]:
            ttg_dic = dict(ttg.attrib)
            attr_dic = dict(ttg.xpath('./contour/pt')[0].attrib)
            hexstr = ttg_dic['name'][3:7]
            name = chr(int(hexstr, 16))  # 字符串转 16进制数字 再转unicode
            ttg_dic.pop('name')
            for num, dic in NUM_ATTR.items():
                if dic == attr_dic:
                    translate_form[name] = num
        return translate_form

    # def parse(self, response):  # 解析函数，用来解析返回的结果，提取数据
    #     # response对象里面scrapy已经封装好了xpath、css方法，可以直接用
    #     # xpath就是写xpath，css就是写css选择器，返回的都是一个list
    #     # 这个是用xpath获取页面上所有的电影
    #
    #     # 下面是css选择器
    #     # all_movie = response.css('dl.board-wrapper dd')
    #     all_movie = response.css('dd')
    #     # all_movie = response.xpath('//dl=[@class="movie-list"]')
    #     # 这个是用css选择器获取到，效果和xpath是一样的
    #     for movie in all_movie:
    #         item = MaoyanItem()  # 实例化item
    #         item['movie_name'] = movie.css('div[class="channel-detail movie-item-title"] a::text').extract()[0]
    #         #item['posters'] = movie.css('img[class="board-img"]::attr(data-src)').extract_first()  # 电影海报url
    #         #item['star'] = movie.css('p[class="star"]::text').extract_first().strip()  # 主演
    #         #item['release_time'] = movie.css('p[class="releasetime"]::text').extract_first().strip()  # 发布时间
    #         # 获取评分信息
    #         score_integer = movie.css('div[class="channel-detail channel-detail-orange"] i[class="integer"]::text').extract()[0]
    #         score_fraction = movie.css('div[class="channel-detail channel-detail-orange"] i[class="fraction"]::text').extract()[0]
    #         # score0 = movie.css('div[class="channel-detail channel-detail-orange"]::text').extract()[0]
    #         score = score_integer + score_fraction
    #         item['score'] = "".join(score)
    #         # # 处理存在评分和暂无评分的两种情况
    #         # if score0 != "":
    #         #     item['score'] = score0
    #         #     print(11)
    #         #     # print(score[0])
    #         # else:
    #         #     score = score_integer + score_fraction
    #         #     item['score'] = "".join(score)
    #         #     # ("score=" + score)
    #
    #         item['url'] = self.base_url + movie.css('div[class="channel-detail movie-item-title"] a::attr(href)').extract()[0]
    #         item['movie_id'] = movie.css('div[class="channel-detail movie-item-title"] a::attr(href)').extract()[0].split('/')[-1]
    #         print(dict(item))
    #         yield scrapy.Request(item['url'], meta={'item': item}, callback=self.detail_parse)
    #         # yield item
    def detail_parse(self,response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        # 一级内页数据提取
        # 电影介绍
        font_link = re.findall(r'vfile.meituan.net/colorstone/(\w+\.woff)',
                              response.text)[0]
        self.get_font(font_link)
        bo = response.css('div[class="movie-index-content box"] span[class="no-info"]::text').extract()
        if bo:
            item['c_box'] = '暂无'
        else:
            box = response.css('div[class="movie-index-content box"] span[class="stonefont"]::text').extract()[0]
            box_unit = response.css('div[class="movie-index-content box"] span[class="unit"]::text').extract()[0]
            box = self.modify_data(box)
            item['c_box'] = box + box_unit
        item['director'] = response.css('li[class="celebrity "] div[class="info"] a::text').extract()[0].split()[0]
        all_actor = response.css('li[class="celebrity actor"]')[:3]
        actor0 = ''
        for actor in all_actor:
            actor1 = actor.css('div[class="info"] a::text').extract()[0].split()[0]
            # role1 = actor.css('div[class="info"] span[class="role"]::text').extract()[0].split()[0]
            actor0 = actor0 + actor1 + ' '
        item['actor'] = actor0
        item['intro'] = response.css('div[class="mod-content"] span[class="dra"]::text').extract()[0]
        item['time'] = response.css('div[class="movie-brief-container"] ul li[class="ellipsis"]::text').extract()[-1]
        item['country'] = response.css('div[class="movie-brief-container"] ul li[class="ellipsis"]::text').extract()[1].split('\n')[1].strip()
        item['duration'] = response.css('div[class="movie-brief-container"] ul li[class="ellipsis"]::text').extract()[1].split('\n')[2].split('/')[1].strip()
        item['type'] = response.css('div[class="movie-brief-container"] ul li[class="ellipsis"]::text').extract()[0]
        return item
        # item['yaoqiu'] = response.xpath("//*[@id='position_detail']/div/table/tr[4]/td/ul[1]").xpath('string(.)').extract()[0]
        # 二级内页地址爬取
        # yield scrapy.Request(item['url'] + "&123", meta={'item': item}, callback=self.detail_parse2)
        # 有下级页面爬取 注释掉数据返回
        # return item
    # def detail_parse(self, response):
    #     # 接收上级已爬取的数据
    #     # item = response.meta['item']
    #     all_comment = response.css('div[class="comment-list-container"] ul li[class="comment-container "]')
    #     c_movie = response.css('div[class="movie-brief-container"] h3[class="name"]::text').extract()[0]
    #     # all_movie = response.xpath('//dl=[@class="movie-list"]')
    #     # 这个是用css选择器获取到，效果和xpath是一样的
    #     for comment in all_comment:
    #         item = MaoyanItem()  # 实例化item
    #         item['c_user'] = comment.css('div[class="user"] span[class="name"]::text').extract()[0]
    #         item['c_movie'] = c_movie
    #
    #         item['c_comment'] = comment.css('div[class="comment-content"]::text').extract()[0]
    #         item['c_good'] = comment.css('div[class="approve "] span[class="num"]::text').extract()[0]
    #         item['c_time'] = comment.css('div[class="time"]::attr(title)').extract()[0]
    #         font_link = re.findall(r'vfile.meituan.net/colorstone/(\w+\.woff)',
    #                                response.text)[0]
    #         self.get_font(font_link)
    #         box = response.css('div[class="movie-index-content box"] span[class="stonefont"]::text').extract()[0]
    #         box_unit = response.css('div[class="movie-index-content box"] span[class="unit"]::text').extract()[0]
    #         box = self.modify_data(box)
    #         item['c_box'] = box + box_unit
    #         yield item
