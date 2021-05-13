import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# 字段和字段属性
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index

# 制造一个类，作为所有模型类的基类
Base = declarative_base()


# 创建一个users表
class User(Base):
    # 数据库表名如果不写，默认是类名小写。
    __tablename__ = 'login_users' # 数据库表的名称
    id = Column(Integer, primary_key=True) # id主键
    name = Column(String(32), index=True, nullable=False) # name列，索引，不可为空
    pwd = Column(String(32), index=True, nullable=False)  # name列，索引，不可为空
    # email = Column(String(32), unique=True)
    # # datetime.datetime.now不能加括号，加了括号，永远就是当前时间了
    # ctime = Column(DateTime, default=datetime.datetime.now)
    # extra = Column(Text, nullable=True)

    __table_args = (
        # UniqueConstraint('id', 'name', name='uix_id_name'), # 联合唯一
        # Index('ix_id_name', 'name', 'email'), # 索引
    )


# 建立一对多的关系(一个人只有一个Hobby，一个Hobby可以有很多人喜欢)
class Hobby (Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True)
    caption = Column(String(50), default='篮球')


class Person(Base):
    __tablename__ = 'person'
    nid = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    # hobby值得是tablename而不是类名
    # 一对多的关系，关联字段写在多的一方
    hobby_id = Column(Integer, ForeignKey('hobby.id'))


# 建立多对多的关系
class Girl(Base):
    __tablename__ = 'girl'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Boy(Base):
    __tablename__='boy'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(64), unique=True, nullable=False)


class Boy2Girl(Base):
    __tablename__ = 'boy2girl'
    id = Column(Integer, primary_key=True, autoincrement=True) # 自增默认就是true
    girl_id = Column(Integer, ForeignKey('girl.id'))
    boy_id = Column(Integer, ForeignKey('boy.id'))


# 创建表（库是不能够创建的，需要手动创建）
def create_table():
    # 创建engine对象
    engine = create_engine(
        "mysql+pymysql://root:beauty@127.0.0.1:3306/myflask?charset=utf8",
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=1
    )
    # 通过engine对象创建表
    Base.metadata.create_all(engine)


# 删除表
def drop_table():
    # 创建engine对象
    engine = create_engine(
        "mysql+pymysql://root:beauty@127.0.0.1:3306/myflask?charset=utf8",
        max_overflow=0,
        pool_size=5,
        pool_timeout=30,
        pool_recycle=1
    )
    # 通过engine对象删除所有表（这个所有表是指，被Base管理的表）
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_table() # 如果这个表已经存在了，就不创建了
    print("创建表成功")
    # drop_table()
    # print("删除表成功")

    '''
    sqlalchemy不支持修改字段。
    '''

