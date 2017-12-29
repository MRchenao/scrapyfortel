# -*- coding: utf-8 -*-
# 导入:
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Article(Base):
    # 表的名字:
    __tablename__ = 'article'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    link = Column(String(100))
    desc = Column(String(255))
    article_id = Column(String(25))
