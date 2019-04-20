import pymysql
pymysql.install_as_MySQLdb()
import datetime
import os
PATH = os.getcwd()

# 数据库连接conn
conn = pymysql.connect(host='localhost', port=3308, user='root', passwd='mysql',
                       db='spider', charset='utf8')



'''
插入电影数据
'''
def insertMovie(item):
    with conn:
        # 获取连接的cursor
        cur = conn.cursor()
        sql1 = "INSERT INTO `spider`.`movie`(`movie_mid`,`movie_name`,`movie_time`,`movie_type`,`movie_rating`,`movie_intro`,`movie_duration`,`movie_country`,`movie_director`,`movie_actor`,`movie_money`) VALUES ( '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(item['movie_id'], item['movie_name'], item['time'], item['type'], item['score'], item['intro'], item['duration'], item['country'], item['director'], item['actor'], item['c_box'])
        cur.execute(sql1)

def insertComment(item):
    with conn:
        # 获取连接的cursor
        cur = conn.cursor()
        sql1 = "INSERT INTO `spider`.`comment`(`c_movie`,`c_user`,`c_comment`,`c_good`,`c_time`) VALUES ( '%s','%s','%s','%s','%s');"%(item['c_movie'],item['c_user'],item['c_comment'],item['c_good'],item['c_time'])
        cur.execute(sql1)

def insertBox(item):
    with conn:
        # 获取连接的cursor
        cur = conn.cursor()
        sql1 = "INSERT INTO `spider`.`box`(`b_movieName`,`b_movieId`,`b_boxInfo`,`b_avgViewBox`,`b_avgShowView`,`b_avgSeatView`,`b_releaseInfo`,`b_seatRate`,`b_showInfo`,`b_showRate`,`b_splitAvgViewBox`,`b_splitBoxInfo`,`b_splitBoxRate`,`b_splitSumBoxInfo`,`b_sumBoxInfo`,`b_viewInfo`,`b_viewInfoV2`,`b_currentTime`) VALUES ( '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(item['b_movieName'],item['b_movieId'],item['b_boxInfo'],item['b_avgViewBox'],item['b_avgShowView'],item['b_avgSeatView'],item['b_releaseInfo'],item['b_seatRate'],item['b_showInfo'],item['b_showRate'],item['b_splitAvgViewBox'],item['b_splitBoxInfo'],item['b_splitBoxRate'],item['b_splitSumBoxInfo'],item['b_sumBoxInfo'],item['b_viewInfo'],item['b_viewInfoV2'],item['b_currentTime'])
        cur.execute(sql1)