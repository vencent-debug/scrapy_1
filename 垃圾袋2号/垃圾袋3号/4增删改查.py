from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, text
from 垃圾袋3号.models import User # 只是pycharm的报错，不会影响我们

engine = create_engine(
    "mysql+pymysql://root:beauty@127.0.0.1:3306/myflask?charset=utf8",
    max_overflow=0,
    pool_size=5
)
Session = sessionmaker(bind=engine) # 得到一个类
# session = Session()
session = scoped_session(Session)


def insert(name, pwd):
    # 1. 批量的加入一些记录
    obj0 = User(name=name, pwd=pwd)
    session.add_all(obj0)
    session.commit()
    # 这里并没有真正的关闭连接，而是将连接放回连接池中
    session.close()


def delete(name):
    # 2. 简单删除
    # res = session.query(User).filter_by(name='admin').first() # 查询
    # 注意通过filter_by()只能允许查到一条信息，这样才可以。否则报错。
    # res = session.query(User).filter_by(name='peace').delete() # 查询

    # 使用filter()表达式匹配来写
    session.query(User).filter(User.name == name).delete()
    session.commit()
    session.close()


def update(id, name, pwd):
    # 3. 简单修改
    session.query(User).filter_by(id=id).update({'name': name})
    session.query(User).filter_by(id=id).update({'pwd': 'pwd'})
    session.commit()
    session.close()


def query(name):
    # 4. 简单查询——查所有
    # return session.query(User).all()
    # return session.query(User).first()
    # return session.query.filter_by(参数)
    # return session.query.filter(表达式)
    # 原生sql直接转对象
    res = session.query(User).from_statement(text('select * from login_users where name=:name')).params(name=name).all()
    return res


if __name__ == '__main__':
    print('---------操作开始----------')
    # insert()
    # print("插入成功...")

    # delete()
    # print("删除成功...")

    # update()
    # print("修改成功...")

    records = query('war')
    print(records)
    print("查询成功...")


