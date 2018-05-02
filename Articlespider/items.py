# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-jobbole"


def date_convert(value):
    value = value.strip().replace("·", "").strip()
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    value = value
    matcher = re.match(r"\d", value)
    if matcher:
        nums = int(matcher.group(0))
    else:
        nums = 0
    # if value:
    #     nums=int(value)
    # else:
    #     nums=0
    return nums


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(add_jobbole)  # MapCompose()可传入多个函数
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)

    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    image_urls = scrapy.Field(
        output_processor=MapCompose(return_value)  # 把image_urls转成list格式,否则下载图片回抛出异常
    )
    images = scrapy.Field()
    image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        # input_processor=",".join(tag_list),
        output_processor=Join(",")
    )
    content = scrapy.Field()
