# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        # 此处item已经获取到数据，可以将其保存到数据库
        return item


class JsonWithEncodingPipeline(object):
    # 自定义导出jaon文件
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spoder_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter导出jaon文件
    def __init__(self):
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '', 'article_spider', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = 'insert into jobbole_article(title,url,create_date,image_path,fav_nums,praise_nums,url_object_id,image_urls,tags,content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

        self.cursor.execute(insert_sql, (
            item["title"], item["url"], item["create_date"], item["image_path"], item["fav_nums"], item["praise_nums"],
            item["url_object_id"], item['image_urls'], item["tags"], item["content"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体插入
        insert_sql = 'insert into jobbole_article(title,url,create_date,image_path,fav_nums,praise_nums,url_object_id,image_urls,tags,content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

        cursor.execute(insert_sql, (
        item["title"], item["url"], item["create_date"], item["image_path"], item["fav_nums"], item["praise_nums"],
        item["url_object_id"], item['image_urls'], item["tags"], item["content"]))


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["image_path"] = image_file_path
        return item
