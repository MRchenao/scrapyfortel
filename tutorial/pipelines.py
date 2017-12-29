# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
# 导入:
from sqlalchemy import create_engine
from Model.Article import Article
from Model.ArticleContent import ArticleContent
from sqlalchemy.orm import sessionmaker


class TutorialPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        # 读取settings中配置的数据库参数
        HOSTNAME = settings['MYSQL_HOST']
        DATABASE = settings['MYSQL_DBNAME']
        USERNAME = settings['MYSQL_USER']
        PASSWORD = settings['MYSQL_PASSWD']
        PORT = settings['MYSQL_PORT']
        DB_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
        return cls(DB_URI)  # 相当于connectionstr付给了这个类，self中可以得到

    def __init__(self, DB_URI):
        # 初始化数据库连接:
        self.engine = create_engine(DB_URI)
        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)
        self.DBhandler = self.DBSession()

    def process_item(self, item, spider):
        res = self.query_data(item)
        if res:
            new_article = Article(title=item['title'], link=item['link'], desc=item['desc'],
                                  article_id=item['article_id'])
            new_article_content = ArticleContent(article_content=item['content'], article_id=item['article_id'])
            # 添加到DBhandler:
            self.DBhandler.add(new_article)
            self.DBhandler.add(new_article_content)
        else:
            raise DropItem("Duplicate item found: %s" % item)
        return item

    def query_data(self, item):
        result = self.DBhandler.query(Article.id).filter(Article.link == item['link']).one_or_none()
        if result is None:
            return True
        else:
            return False

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def close_spider(self, spider):
        # 提交即保存到数据库:
        self.DBhandler.commit()
        self.DBhandler.close()
