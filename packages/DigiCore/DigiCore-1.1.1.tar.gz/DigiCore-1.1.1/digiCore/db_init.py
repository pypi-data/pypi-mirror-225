import yaml

from digiCore.dsd_kafka import KafkaDao
from digiCore.dsd_mongodb import MongoDao
from digiCore.dsd_mysql import TiDBDao
from digiCore.dsd_redis import RedisDao


class InstantiationDB:
    """
    实例化数据库对象
    """

    def __init__(self, YAML_PATH='config.yaml'):
        self.YAML_PATH = YAML_PATH
        self.LOAD = self.get_db_info()

    def get_db_info(self):
        """
        读取配置文件中的数据库地址
        :return:
        """
        with open(self.YAML_PATH) as f:
            LOAD = yaml.safe_load(f)
        return LOAD

    def get_tidb_ob(self):
        tidb_ob = TiDBDao(
            host=self.LOAD['DB']['hostname'],
            port=self.LOAD['DB']['port'],
            user=self.LOAD['DB']['username'],
            passwd=self.LOAD['DB']['password'],
        )
        return tidb_ob

    def get_service_info_data(self, db):
        """
        获取数据库信息
        :return:
        """
        env = self.LOAD['env']
        tidb_ob = self.get_tidb_ob()
        sql = f'select hostname,username,port,password,brokers from dim.dim_dsd_service_db_info_i_manual where env="{env}" and db="{db}"'
        service = tidb_ob.query_one(sql)
        return service

    def load_tidb_ob(self):
        """
        实例化tidb数据库对象
        :return:
        """
        service = self.get_service_info_data('TIDB')
        tidb_ob = TiDBDao(
            host=service['hostname'],
            user=service['username'],
            port=service['port'],
            passwd=service['password']
        )
        return tidb_ob

    def load_redis_ob(self):
        """
        实例化redis对象
        :param service:
        :return:
        """
        service = self.get_service_info_data('Redis')
        redis_ob = RedisDao(
            host=service['hostname'],
            port=service['port'],
            password=service['password'],
            db=5
        )
        return redis_ob

    def load_mongodb_ob(self):
        """
        实例化mongodb对象
        :param service:
        :return: mongodb://root:DoocnProMongoDB201.@192.168.0.201:57017/
        """
        service = self.get_service_info_data('MongoDB')
        host = service['hostname']
        user = service['username']
        port = service['port']
        passwd = service['password']
        mongodb_url = f"mongodb://{user}:{passwd}@{host}:{port}/"
        mongo_ob = MongoDao(
            mongodb_url=mongodb_url
        )
        return mongo_ob

    def load_kafka_ob(self, topic: str,
                      partition: int,
                      brokers=None,
                      sub_server='Test'):
        """
        实例化kafka对象
        :return:
        """
        if brokers is None:
            brokers = ['192.168.0.201:9092', '192.168.0.200:9092', '192.168.0.12:9092']

        kafka_ob = KafkaDao(topic,partition,brokers,sub_server)
        return kafka_ob
