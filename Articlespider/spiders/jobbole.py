# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from urllib import parse
from Articlespider.items import JobboleArticleItem, ArticleItemLoader
from Articlespider.utils.comeon import get_md5
from scrapy.loader import ItemLoader
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']  # 开始爬取的url

    def parse(self, response):
        # 解析当前列表页中所有文章的url,并交给scrapy下载后进行解析
        post_nudes = response.css("#archive .floated-thumb.post .post-thumb a")
        for post_nude in post_nudes:
            image_url = post_nude.css("img::attr(src)").extract_first()
            post_url = post_nude.css("::attr(href)").extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
        # 获取下一页列表页
        next_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobboleArticleItem()
        image_urls = response.meta.get("front_image_url", "")  # 文章封面图

        # # title= response.xpath('//*[@id="post-113926"]/div[1]/h1/text()').extract_first()
        # title = response.css("div.entry-header > h1::text").extract_first()
        # # create_date=response.xpath('//*[@id="post-113926"]/div[2]/p/text()[1]').extract_first().strip().replace("·","").strip()
        # create_date = response.css("div.entry-meta > p::text").extract_first().strip().replace("·", "").strip()
        # # praise_nums=int(response.xpath('//*[@id="113926votetotal"]/text()').extract_first())
        # praise_nums = response.css("h10::text").extract_first()
        # matcher = re.findall(r"/d", \
        #                      # response.xpath('//*[@id="post-113926"]/div[3]/div[23]/span[2]/text()').extract_first())
        #                      response.css(".bookmark-btn::text").extract_first())
        # if matcher:
        #     fav_nums = matcher[0]
        # matcher = re.findall(r"/d", \
        #                      # response.xpath('//*[@id="post-113926"]/div[3]/div[23]/a/span/text()').extract_first())
        #                      response.css('a[href="#article-comment"] span::text').extract_first())
        # if matcher:
        #     comment_nums = matcher[0]
        # # content=response.xpath('//div[@class="entry"]').extract_first()
        # content = response.css('div.entry').extract_first()
        # # tag_list=response.xpath('//*[@id="post-113926"]/div[2]/p/a/text()').extract()
        # tag_list = response.css('div.entry-meta p.entry-meta-hide-on-mobile a::text').extract()
        # tags = ",".join(tag_list)
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["tags"] = tags
        # article_item["image_urls"] = [image_urls]
        # article_item["content"] = content

        # 通过Itemloader 加载item
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        # item_loader.add_xpath()   #xpath选择器结果赋值
        item_loader.add_css("title", "div.entry-header > h1::text")  # css选择器结果赋值
        item_loader.add_value("url", response.url)  # 直接赋值
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "div.entry-meta > p::text")
        item_loader.add_css("praise_nums", "h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("comment_nums", 'a[href="#article-comment"] span::text')
        item_loader.add_css("tags", "div.entry-meta p.entry-meta-hide-on-mobile a::text")
        item_loader.add_value("image_urls", [image_urls])
        item_loader.add_css("content", "div.entry")
        article_item = item_loader.load_item()
        yield article_item
        # answer=title+create_date+praise_nums+fav_nums+comment_nums+tags
        # with open("answer1.txt",'a') as f:
        #     f.write(answer)
        #     f.write("\n")
