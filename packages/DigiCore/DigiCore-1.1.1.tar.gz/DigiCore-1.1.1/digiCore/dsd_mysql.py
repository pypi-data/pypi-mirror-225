"""
Mysql

TiDB连接池的使用

实现增删改查功能

"""
import json

import pymysql as pymysql
from dbutils.pooled_db import PooledDB
from collections import OrderedDict

from digiCore import Decorate

def create_ordered_dict(field_list: list, unordered_dict: dict):
    """
    根据传入的列表字段参数，构建一个有序的字典
    :param unordered_dict: 需要插入到数据库的字典数据
    :param field_list: 数据库字段
    :return: dict
    """
    # 原始数据中没有的字段则赋值为 None
    diff_keys = set(field_list) - set(unordered_dict.keys())
    for key in diff_keys:
        unordered_dict[key] = 'None'

    # 原始数据中多的字段，则删除
    diff_keys = set(unordered_dict.keys()) - set(field_list)
    for key in diff_keys:
        unordered_dict.pop(key)

    ordered_dict = OrderedDict([(field, unordered_dict[field]) for field in field_list])
    return ordered_dict


def get_dict_value(json_data: dict):
    """
    获取字典的values，转化为字符转类型
    :param json_data: 插入数据库的数据
    :return: 返回 元组类型 的 字符串
    """
    value_list = []
    # 如果是字符串类型的value，则直接不做处理，
    # 如果是非字符串类型的value，则进行解码
    for value in json_data.values():
        if isinstance(value, str):
            str_value = value
        else:
            str_value = json.dumps(value)
        value_list.append(str_value)
    tup_data = tuple(value_list)
    sql_data = str(tup_data)
    return sql_data


def list_to_sql_values(field_list: list, data_list: [dict]):
    """
    将列表套字典格式的数据，转化为字符串类型的元组：(...),(...),(...)
    :param field_list: 字段列表
    :param data_list: 插入数据库的数据列表
    :return: 字符串类型的元组
    """
    value_list = []
    for json_data in data_list:
        # 对字典数据根据列表顺序进行排序
        ordered_dict = create_ordered_dict(field_list, json_data)
        # 将字典转化为 元组格式的 字符串
        sql_data = get_dict_value(ordered_dict)
        value_list.append(sql_data)
    sql_values = ",".join(value_list)
    return sql_values


def create_insert_sql(db_table: str, field_list: list, sql_values: str):
    """
    根据字段列表 和 字段对应需要插入的数据，构建出insert的sql语句
    :param db_table: 数据库表名称
    :param field_list: 字段列表
    :param sql_values: 字段对应需要插入的values
    :return: str
    """

    # 使用 ', '.join() 将列表组合成完整的结果字符串
    result_str = ', '.join(field_list)

    # 生成字符串的生成器表达式
    value_strs = [f"{field}=values({field})" for field in field_list]

    # 在 SQL 语句中使用该字符串
    insert_sql = f"INSERT INTO {db_table}({result_str}) VALUES {sql_values} ON DUPLICATE KEY UPDATE {', '.join(value_strs)}"
    return insert_sql


class TiDBConnectionPool(object):
    """
    Tidb\Mysql的连接池，根据提供的账号密码产生一个连接

    未指定连接的数据库，如需要使用原生sql进行数据库操作，
    务必在表名称之前添加对应的数据库名称：如：dwd.dwd_crawler_amazon_on_hand_i_h

    :param host : 数据库或集群连接地址
    :param port ：数据库或集群端口号
    :param user : 用户名
    :param passwd ：密码

    """

    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 passwd: str
                 ):

        self.host = host
        self.port: int = port
        self.user = user
        self.passwd = passwd

        # mysql 连接池
        self.db_pool = PooledDB(
            creator=pymysql,
            maxcached=1000,
            maxconnections=100,
            blocking=True,
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __enter__(self):
        # 获取一个数据库连接
        self.conn = self.db_pool.connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交事务并关闭数据库连接
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


class TiDBDao():

    def __init__(self, host: str, port: int, user: str, passwd: str):
        self.conn_pool = TiDBConnectionPool(host, port, user, passwd)

    @Decorate.def_retry(msg="Mysql: 查询单条数据失败！")
    def query_one(self, sql: str):
        """
        查询并返回数据库中的一条数据
        :param sql: 查询sql语句
        :return: dict
        """
        with self.conn_pool as conn:
            mysql_cursor = conn.cursor()
            mysql_cursor.execute(sql)
            data = mysql_cursor.fetchone()
            return data

    @Decorate.def_retry(msg="Mysql: 查询批量数据失败！")
    def query_list(self, sql: str):
        """
        查询并返回数据库中的全部数据
        :param sql: 查询sql语句
        :return: list
        """
        with self.conn_pool as conn:
            mysql_cursor = conn.cursor()
            mysql_cursor.execute(sql)
            data = mysql_cursor.fetchall()
            return data

    @Decorate.def_retry(msg="Mysql: 批量插入失败！")
    def insert_data(self, db_table: str, field_list: list, data_list: [dict]):
        """
        查询并返回数据库中的一条数据
        :param db_table: 数据库及表名称
        :param data_list: 字段对应的列表套字典数据
        :param field_list: 字段列表
        :param sql: 查询sql语句
        :return:
        """
        if not data_list:
            return
        sql_values = list_to_sql_values(field_list, data_list)
        insert_sql = create_insert_sql(db_table, field_list, sql_values)
        with self.conn_pool as conn:
            mysql_cursor = conn.cursor()
            mysql_cursor.execute(insert_sql)

    @Decorate.def_retry(msg="Mysql: sql语句commit提交失败,检查sql语句！")
    def commit_sql(self, sql: str):
        """
        提交sql语句
        用于 建表 、删除表使用
        :param sql: sql语句
        :return:
        """
        with self.conn_pool as conn:
            mysql_cursor = conn.cursor()
            mysql_cursor.execute(sql)

    @Decorate.def_retry(msg="表删除失败！")
    def delete_table(self, table_name: str):
        """
        删除表
        :param table_name: dim.dim_gsm_lx_ad_shop_list_i_d
        :return:
        """
        sql = f"drop table if exists {table_name}"
        self.commit_sql(sql)

    @Decorate.def_retry(msg="建表失败！")
    def create_table(self, create_sql: str):
        """
        创建表
        :param create_sql: crate table if not exists ...
        :return:
        """
        sql = create_sql.replace('\n', ' ')
        self.commit_sql(sql)