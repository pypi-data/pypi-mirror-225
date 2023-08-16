"""
reids连接池

实现增删改查功能

"""
import json

from redis import ConnectionPool,StrictRedis

from digiCore import Decorate


class RedisConnectionPool():

    def __init__(self,
                 host: str,
                 port: int,
                 password: str,
                 db: int):
        self.__pool__ = ConnectionPool(host=host,
                                       port=port,
                                       password=password,
                                       db=db,
                                       max_connections=100)

    def __call__(self):
        return StrictRedis(connection_pool=self.__pool__)

    def __enter__(self):
        self.redis_conn = self()
        return self.redis_conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class RedisDao:

    def __init__(self, host: str, port: int, password: str, db: int):
        self.conn = RedisConnectionPool(host, port, password, db)

    @Decorate.def_retry(msg="redis: 获取任务队列长度失败，正在重试连接！")
    def get_task_list_len(self, task_name: str):
        """
        获取任务列表长度
        :param task_name: 任务队列名称
        :return: int
        """
        with self.conn as redis_conn:
            return redis_conn.llen(task_name)

    @Decorate.def_retry(msg="redis: 添加任务失败，正在重试连接！")
    def push_task(self, queue: str, task_list: list):
        """
        将任务添加到redis进行缓存
        :param queue: 任务队列名称
        :param task_list: 任务实例
        :return: True
        """
        with self.conn as redis_conn:
            for task_json in task_list:
                bson_data = json.dumps(task_json)
                redis_conn.lpush(queue, bson_data)

    @Decorate.def_retry(msg="redis: 弹出任务失败，正在重试连接！")
    def pop_task(self, queue: str):
        """
        从任务队列中弹出一个任务实例

        队列存在数据的时候 返回 json格式数据
        队列不存在数据的时候，返回 None
        :param queue: 任务队列名称
        :return: json/None
        """
        with self.conn as redis_conn:
            bson_data = redis_conn.rpop(queue)
            if not bson_data:
                return None
            data_json = json.loads(bson_data)
            return data_json

    @Decorate.def_retry(msg="redis: access_token获取失败，正在重试连接！")
    def get_lingxing_api_access_token(self):
        """
        获取领星API的token
        """
        AUTH_TOKEN = "common-lingxing-access-token:common:token"
        with self.conn as redis_conn:
            token = json.loads(redis_conn.get(AUTH_TOKEN))
            if token:
                return token.get("access_token")
            else:
                return None

    @Decorate.def_retry(msg="redis: auth_token获取失败，正在重试连接！")
    def get_lingxing_crawler_auth_token(self):
        """
        获取领星爬虫页面的token
        """
        AUTH_TOKEN = "common-lingxing-access-token:common:auth_tokens"
        with self.conn as redis_conn:
            token = redis_conn.srandmember(AUTH_TOKEN).decode()
            if token:
                return token
            else:
                return None

    @Decorate.def_retry(msg="删除队列失败，正在重试连接！")
    def del_task_from_redis(self, queue: str):
        """
        删除任务队列
        :param queue:
        :return:
        """
        with self.conn as redis_conn:
            redis_conn.delete(queue)