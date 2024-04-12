# 数据容器文件

import scrapy

class SpiderItem(scrapy.Item):
    pass

class ShangpinxinxiItem(scrapy.Item):
    # 来源
    laiyuan = scrapy.Field()
    # 标题
    biaoti = scrapy.Field()
    # 封面
    fengmian = scrapy.Field()
    # 价格
    jiage = scrapy.Field()
    # 商品ID
    spid = scrapy.Field()
    # 平均分
    pingjunfen = scrapy.Field()
    # 商品评价
    sppj = scrapy.Field()
    # 好评
    haoping = scrapy.Field()
    # 好评度
    haopingdu = scrapy.Field()
    # 中评
    zhongping = scrapy.Field()
    # 中评度
    zhongpingdu = scrapy.Field()
    # 差评
    chaping = scrapy.Field()
    # 差评度
    chapingdu = scrapy.Field()

