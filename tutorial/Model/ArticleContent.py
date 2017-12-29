# -*- coding: utf-8 -*-
# 导入:
from sqlalchemy import Column, String, Integer, TEXT
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class ArticleContent(Base):
    # 表的名字:
    __tablename__ = 'article_content'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    article_content = Column(TEXT)
    article_id = Column(String(25))
