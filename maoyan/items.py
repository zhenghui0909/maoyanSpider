# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
	b_avgSeatView = scrapy.Field()
	b_avgShowView = scrapy.Field()
	b_avgViewBox = scrapy.Field()
	b_boxInfo = scrapy.Field()
	b_movieId = scrapy.Field()
	b_movieName = scrapy.Field()
	b_releaseInfo = scrapy.Field()
	b_seatRate = scrapy.Field()
	b_showInfo = scrapy.Field()
	b_showRate = scrapy.Field()
	b_splitAvgViewBox = scrapy.Field()
	b_splitBoxInfo = scrapy.Field()
	b_splitBoxRate = scrapy.Field()
	b_splitSumBoxInfo = scrapy.Field()
	b_sumBoxInfo = scrapy.Field()
	b_viewInfo = scrapy.Field()
	b_viewInfoV2 = scrapy.Field()
	b_currentTime = scrapy.Field()
    # c_user = scrapy.Field()
    # c_movie = scrapy.Field()
    # c_good = scrapy.Field()
    # c_comment = scrapy.Field()
    # c_time = scrapy.Field()
    # c_box = scrapy.Field()
    # # define the fields for your item here like:
    # # name = scrapy.Field()
    # movie_name = scrapy.Field()
    # score = scrapy.Field()
    # url = scrapy.Field()
    # intro = scrapy.Field()
    # time = scrapy.Field()
    # country = scrapy.Field()
    # duration = scrapy.Field()
    # type = scrapy.Field()
    # actor = scrapy.Field()
    # director = scrapy.Field()
    # movie_id = scrapy.Field()
    # rate = scrapy.Field()
