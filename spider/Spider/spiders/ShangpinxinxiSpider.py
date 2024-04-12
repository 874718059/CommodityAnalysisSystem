# # -*- coding: utf-8 -*-

# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import ShangpinxinxiItem
import time
from datetime import datetime,timedelta
import datetime as formattime
import re
import random
import platform
import json
import os
import urllib
from urllib.parse import urlparse
import requests
import emoji
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from selenium.webdriver import ChromeOptions, ActionChains
from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 商品信息
class ShangpinxinxiSpider(scrapy.Spider):
    name = 'shangpinxinxiSpider'
    spiderUrl = 'https://api.m.jd.com/?appid=search-pc-java&functionId=pc_search_s_new&client=pc&clientVersion=1.0.0&t=1702559089960&body=%7B%22keyword%22%3A%22%E5%AE%B6%E7%94%A8%E7%94%B5%E5%99%A8+%E6%95%B0%E7%A0%81+%E5%AE%B6%E5%B1%85+%E7%BE%8E%E5%A6%86+%E9%A3%9F%E5%93%81%22%2C%22wq%22%3A%22%E5%AE%B6%E7%94%A8%E7%94%B5%E5%99%A8+%E6%95%B0%E7%A0%81+%E5%AE%B6%E5%B1%85+%E7%BE%8E%E5%A6%86+%E9%A3%9F%E5%93%81%22%2C%22pvid%22%3A%22a2a996791aab42e9ad8b68f16f94197b%22%2C%22isList%22%3A0%2C%22page%22%3A%22{}%22%2C%22s%22%3A%221%22%2C%22click%22%3A%220%22%2C%22log_id%22%3A%221702559064094.4675%22%2C%22show_items%22%3A%22%22%7D&loginType=3&uuid=181111935.1408214845.1694007854.1702556902.1702556938.5&area=19_1634_1638_8462&h5st=20231214210449990%3Bggg5i3tnzm9i55t3%3Bf06cc%3Btk03wae611c3618ntD4QCKUwmhd42MmFrZbMyJ8DqRdjV-CAYtwx6cmZkPSVutZrYiT2i77H8IJxDEr2WLUlNOB0pycR%3B447aca034adb11942964605690cef959%3B4.1%3B1702559089990%3Bee3cf7f6b94dc20e9265d83066bb9ceece4bb89e2b7e8bf5afb1bfd928788174bfa06c210ddd4437d8a2e234330c3a3980b96c3953b1ab788029ae792b39e11334a726f4ed230d5e3515dc0a763f838d8f3e2e7f830157d7b3ae2499dfeb9e1e0f639edcd875cf0339fadc1d87dc8a62dff67fb6b49df25a74edd50d35ab35cc9f444bb51188b37a73c72ff793e42d6b044acf689a5c7d6de10afcee1b44ae11035934b4b22a015b3b89a2059f21c425a0cd861ba7d69e00ddac2efad39fa5c480179543ac1f3552043b49ba98930e389c84017c8ae3476437e7376b6b6779dd205749224f57c308dbf76e9f37f3d34353a7246efc08da19cf7803020fe4fe843c70098ba0b74e908e48bb85427ca382a6f0c5add62f5ca7c49083240028bb81&x-api-eid-token=jdd03TLYH3MYYJCLOXSDCOBJTFTYB37CLOWCYVGHFXVWEWNPVYOCSHPZ5CNNUVSMXVX4ZT6FGINGLA3UNYNQ4APJTAA6TXEAAAAMMNBUFKVYAAAAACDHPSJV7ZRGQ4AX'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''
    realtime = False

    headers = {
        'Cookie':'__jdu=1408214845; shshshfpa=20348775-8a30-a2f6-b509-852ca2eeafff-1694007856; shshshfpx=20348775-8a30-a2f6-b509-852ca2eeafff-1694007856; areaId=19; ipLoc-djd=19-1634-1638-8462; unpl=JF8EALBnNSttC0IGUR8GTBZHTA5UWw8JTx4LP28BVgkLQgBRSQceFxl7XlVdXxRLFB9vYhRXXFNIXQ4fBSsSEXteXVdZDEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrAh4TGUhdUVdYDHsWM2hXNWRVXkhUAxsyGiIRex8AAloPSxMEZyoFUVxRSFQAEgcfIhF7Xg; PCSYCityID=CN_440000_441400_0; TARGET_UNIT=bjcenter; jsavif=1; 3AB9D23F7A4B3CSS=jdd03TLYH3MYYJCLOXSDCOBJTFTYB37CLOWCYVGHFXVWEWNPVYOCSHPZ5CNNUVSMXVX4ZT6FGINGLA3UNYNQ4APJTAA6TXEAAAAMMNBIBSIQAAAAAC63LNSFESGNNTMX; TrackID=1ITPuwkiyKLcLHCehRqukiA8Oje82qXZev5oP87n0YjLM3taIpVFGOFmQjEcmkMkT02otPhbRrbU9QEDbSYCDuFfvnd6s7EwhJRMzyo4WzIU; thor=B9F817AEADBFC8B42D5167C559F46FE4BB7DF22880342624D61C33160F58AF28EA9D579372A4098D3E7A3486AC609703A27E490773F2C7A06AE1135A948CA044877A07D9FF538DA4E37AA6F573472742717395D2782EC0DA3B5DCB46C8A0E9586EB3F4D1F3ACB23E7E26B7B0EE98B012FA3B7A6CBED6D2ACC65EEDC2D625420D3576BC0F2CC0423632680E0A8D155D3227EAC2D47D07CB2579288B854E6DA46F; flash=2_dySApIG65izZ7ww_j5iaOPD85Rxs67FWz2p9J8z8UlfQyCo62MpB0R0sEnXwZrirWXkKOIrbzzwUrhQ8KmBENuEPx9LEXjR6HkOrKJx4iSs*; pinId=unO17dTt4ErrQApJpPk_yg; pin=jd_ydXaDhPDdEiA; unick=jd_ydXaDhPDdEiA; ceshi3.com=000; _tp=fQJ2MNKLngyHX5zIm8AqaQ%3D%3D; _pst=jd_ydXaDhPDdEiA; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_b8ce55f5f6b14c0589a953eb8eec4448|1702557161162; joyya=1702557166.1702557180.24.0732uk0; 3AB9D23F7A4B3C9B=TLYH3MYYJCLOXSDCOBJTFTYB37CLOWCYVGHFXVWEWNPVYOCSHPZ5CNNUVSMXVX4ZT6FGINGLA3UNYNQ4APJTAA6TXE; token=e10740559827b23f2ba9d71426cbac28,3,945865; __tk=nDkwVMR0WUb0Vxb0V0ALV0n5iUy5Vli5RZR0VxPyRUyEiUnMVDeJnJ,3,945865; shshshsID=6b9f9b05e2bab33a453d097cf546f7b3_7_1702557188024; __jda=181111935.1408214845.1694007854.1702556902.1702556938.5; __jdb=181111935.20.1408214845|5.1702556938; __jdc=181111935; shshshfpb=AAu_7UGiMEjSHdYowova1CYUsou6v_xaUAHhWTQAAAAA',
'Origin':'https://search.jd.com'
    }

    def __init__(self,realtime=False,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.realtime = realtime=='true'

    def start_requests(self):

        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, 'o2l3x9ar_shangpinxinxi') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        pageNum = 1 + 1
        for url in self.start_urls:
            if '{}' in url:
                for page in range(1, pageNum):
                    next_link = url.format(page)
                    yield scrapy.Request(
                        url=next_link,
                        headers=self.headers,
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                    callback=self.parse
                )

    # 列表解析
    def parse(self, response):
        _url = urlparse(self.spiderUrl)
        self.protocol = _url.scheme
        self.hostname = _url.netloc
        plat = platform.system().lower()
        if not self.realtime and (plat == 'linux' or plat == 'windows'):
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, 'o2l3x9ar_shangpinxinxi') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return
        list = response.css('div#J_goodsList ul[class="gl-warp clearfix"] li')
        for item in list:
            fields = ShangpinxinxiItem()

            if '(.*?)' in '''div.p-img > a::attr(href)''':
                try:
                    fields["laiyuan"] = str( re.findall(r'''div.p-img > a::attr(href)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["laiyuan"] = str( self.remove_html(item.css('div.p-img > a::attr(href)').extract_first()))

                except:
                    pass
            if fields["laiyuan"].startswith('//'):
                fields["laiyuan"] = self.protocol + ':' + fields["laiyuan"]
            elif fields["laiyuan"].startswith('/'):
                fields["laiyuan"] = self.protocol + '://' + self.hostname + fields["laiyuan"]
            elif fields["laiyuan"].startswith('http'):
                pass
            else:
                fields["laiyuan"] = self.protocol + '://' + self.hostname + '/' + fields["laiyuan"]
            if '(.*?)' in '''div[class="p-name p-name-type-2"] > a > em::text''':
                try:
                    fields["biaoti"] = str( re.findall(r'''div[class="p-name p-name-type-2"] > a > em::text''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["biaoti"] = str( self.remove_html(item.css('div[class="p-name p-name-type-2"] > a > em::text').extract_first()))

                except:
                    pass
            if '(.*?)' in '''div.p-img > a >img::attr(data-lazy-img)''':
                try:
                    fields["fengmian"] = str( re.findall(r'''div.p-img > a >img::attr(data-lazy-img)''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["fengmian"] = str( self.remove_html(item.css('div.p-img > a >img::attr(data-lazy-img)').extract_first()))

                except:
                    pass
            if fields["fengmian"].startswith('//'):
                fields["fengmian"] = self.protocol + ':' + fields["fengmian"]
            elif fields["fengmian"].startswith('/'):
                fields["fengmian"] = self.protocol + '://' + self.hostname + fields["fengmian"]
            elif fields["fengmian"].startswith('http'):
                pass
            else:
                fields["fengmian"] = self.protocol + '://' + self.hostname + '/' + fields["fengmian"]
            if '(.*?)' in '''div.p-price > strong > i::text''':
                try:
                    fields["jiage"] = str( re.findall(r'''div.p-price > strong > i::text''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["jiage"] = str( self.remove_html(item.css('div.p-price > strong > i::text').extract_first()))

                except:
                    pass
            if '(.*?)' in '''<i data-price="(.*?)">''':
                try:
                    fields["spid"] = str( re.findall(r'''<i data-price="(.*?)">''', item.extract(), re.DOTALL)[0].strip())

                except:
                    pass
            else:
                try:
                    fields["spid"] = str( self.remove_html(item.css('<i data-price="(.*?)">').extract_first()))

                except:
                    pass
            detailUrlRule =  item.css('').extract_first()
            if self.protocol in detailUrlRule:
                pass
            elif detailUrlRule.startswith('//'):
                detailUrlRule = self.protocol + ':' + detailUrlRule
            elif detailUrlRule.startswith('/'):
                detailUrlRule = self.protocol + '://' + self.hostname + detailUrlRule
                # fields["laiyuan"] = detailUrlRule
            else:
                detailUrlRule = self.protocol + '://' + self.hostname + '/' + detailUrlRule
            yield scrapy.Request(url=detailUrlRule, meta={'fields': fields}, headers=self.headers, callback=self.detail_parse, dont_filter=True)

    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']
        try:
            if '(.*?)' in '''["productCommentSummary"]["averageScore"]''':
                fields["pingjunfen"] = str( re.findall(r'''["productCommentSummary"]["averageScore"]''', response.text, re.S)[0].strip())

            else:
                if 'pingjunfen' != 'xiangqing' and 'pingjunfen' != 'detail' and 'pingjunfen' != 'pinglun' and 'pingjunfen' != 'zuofa':
                    fields["pingjunfen"] = str( self.remove_html(response.css('''["productCommentSummary"]["averageScore"]''').extract_first()))

                else:
                    try:
                        fields["pingjunfen"] = str( emoji.demojize(response.css('''["productCommentSummary"]["averageScore"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["commentCountStr"]''':
                fields["sppj"] = str( re.findall(r'''["productCommentSummary"]["commentCountStr"]''', response.text, re.S)[0].strip())

            else:
                if 'sppj' != 'xiangqing' and 'sppj' != 'detail' and 'sppj' != 'pinglun' and 'sppj' != 'zuofa':
                    fields["sppj"] = str( self.remove_html(response.css('''["productCommentSummary"]["commentCountStr"]''').extract_first()))

                else:
                    try:
                        fields["sppj"] = str( emoji.demojize(response.css('''["productCommentSummary"]["commentCountStr"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["goodCountStr"]''':
                fields["haoping"] = str( re.findall(r'''["productCommentSummary"]["goodCountStr"]''', response.text, re.S)[0].strip())

            else:
                if 'haoping' != 'xiangqing' and 'haoping' != 'detail' and 'haoping' != 'pinglun' and 'haoping' != 'zuofa':
                    fields["haoping"] = str( self.remove_html(response.css('''["productCommentSummary"]["goodCountStr"]''').extract_first()))

                else:
                    try:
                        fields["haoping"] = str( emoji.demojize(response.css('''["productCommentSummary"]["goodCountStr"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["goodRate"]''':
                fields["haopingdu"] = str( re.findall(r'''["productCommentSummary"]["goodRate"]''', response.text, re.S)[0].strip())

            else:
                if 'haopingdu' != 'xiangqing' and 'haopingdu' != 'detail' and 'haopingdu' != 'pinglun' and 'haopingdu' != 'zuofa':
                    fields["haopingdu"] = str( self.remove_html(response.css('''["productCommentSummary"]["goodRate"]''').extract_first()))

                else:
                    try:
                        fields["haopingdu"] = str( emoji.demojize(response.css('''["productCommentSummary"]["goodRate"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["generalCountStr"]''':
                fields["zhongping"] = str( re.findall(r'''["productCommentSummary"]["generalCountStr"]''', response.text, re.S)[0].strip())

            else:
                if 'zhongping' != 'xiangqing' and 'zhongping' != 'detail' and 'zhongping' != 'pinglun' and 'zhongping' != 'zuofa':
                    fields["zhongping"] = str( self.remove_html(response.css('''["productCommentSummary"]["generalCountStr"]''').extract_first()))

                else:
                    try:
                        fields["zhongping"] = str( emoji.demojize(response.css('''["productCommentSummary"]["generalCountStr"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["generalRate"]''':
                fields["zhongpingdu"] = str( re.findall(r'''["productCommentSummary"]["generalRate"]''', response.text, re.S)[0].strip())

            else:
                if 'zhongpingdu' != 'xiangqing' and 'zhongpingdu' != 'detail' and 'zhongpingdu' != 'pinglun' and 'zhongpingdu' != 'zuofa':
                    fields["zhongpingdu"] = str( self.remove_html(response.css('''["productCommentSummary"]["generalRate"]''').extract_first()))

                else:
                    try:
                        fields["zhongpingdu"] = str( emoji.demojize(response.css('''["productCommentSummary"]["generalRate"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["poorCountStr"]''':
                fields["chaping"] = str( re.findall(r'''["productCommentSummary"]["poorCountStr"]''', response.text, re.S)[0].strip())

            else:
                if 'chaping' != 'xiangqing' and 'chaping' != 'detail' and 'chaping' != 'pinglun' and 'chaping' != 'zuofa':
                    fields["chaping"] = str( self.remove_html(response.css('''["productCommentSummary"]["poorCountStr"]''').extract_first()))

                else:
                    try:
                        fields["chaping"] = str( emoji.demojize(response.css('''["productCommentSummary"]["poorCountStr"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        try:
            if '(.*?)' in '''["productCommentSummary"]["poorRate"]''':
                fields["chapingdu"] = str( re.findall(r'''["productCommentSummary"]["poorRate"]''', response.text, re.S)[0].strip())

            else:
                if 'chapingdu' != 'xiangqing' and 'chapingdu' != 'detail' and 'chapingdu' != 'pinglun' and 'chapingdu' != 'zuofa':
                    fields["chapingdu"] = str( self.remove_html(response.css('''["productCommentSummary"]["poorRate"]''').extract_first()))

                else:
                    try:
                        fields["chapingdu"] = str( emoji.demojize(response.css('''["productCommentSummary"]["poorRate"]''').extract_first()))

                    except:
                        pass
        except:
            pass
        return fields

    # 数据清洗
    def pandas_filter(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost/spidero2l3x9ar?charset=UTF8MB4')
        df = pd.read_sql('select * from shangpinxinxi limit 50', con = engine)

        # 重复数据过滤
        df.duplicated()
        df.drop_duplicates()

        #空数据过滤
        df.isnull()
        df.dropna()

        # 填充空数据
        df.fillna(value = '暂无')

        # 异常值过滤

        # 滤出 大于800 和 小于 100 的
        a = np.random.randint(0, 1000, size = 200)
        cond = (a<=800) & (a>=100)
        a[cond]

        # 过滤正态分布的异常值
        b = np.random.randn(100000)
        # 3σ过滤异常值，σ即是标准差
        cond = np.abs(b) > 3 * 1
        b[cond]

        # 正态分布数据
        df2 = pd.DataFrame(data = np.random.randn(10000,3))
        # 3σ过滤异常值，σ即是标准差
        cond = (df2 > 3*df2.std()).any(axis = 1)
        # 不满⾜条件的⾏索引
        index = df2[cond].index
        # 根据⾏索引，进⾏数据删除
        df2.drop(labels=index,axis = 0)

    # 去除多余html标签
    def remove_html(self, html):
        if html == None:
            return ''
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', html).strip()

    # 数据库连接
    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')

        try:
            database = self.databaseName
        except:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)
        return connect

    # 断表是否存在
    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]

        if table_name in table_list:
            return 1
        else:
            return 0

    # 数据缓存源
    def temp_data(self):

        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into `shangpinxinxi`(
                id
                ,laiyuan
                ,biaoti
                ,fengmian
                ,jiage
                ,spid
                ,pingjunfen
                ,sppj
                ,haoping
                ,haopingdu
                ,zhongping
                ,zhongpingdu
                ,chaping
                ,chapingdu
            )
            select
                id
                ,laiyuan
                ,biaoti
                ,fengmian
                ,jiage
                ,spid
                ,pingjunfen
                ,sppj
                ,haoping
                ,haopingdu
                ,zhongping
                ,zhongpingdu
                ,chaping
                ,chapingdu
            from `o2l3x9ar_shangpinxinxi`
            where(not exists (select
                id
                ,laiyuan
                ,biaoti
                ,fengmian
                ,jiage
                ,spid
                ,pingjunfen
                ,sppj
                ,haoping
                ,haopingdu
                ,zhongping
                ,zhongpingdu
                ,chaping
                ,chapingdu
            from `shangpinxinxi` where
                `shangpinxinxi`.id=`o2l3x9ar_shangpinxinxi`.id
            ))
        '''

        cursor.execute(sql)
        connect.commit()
        connect.close()
