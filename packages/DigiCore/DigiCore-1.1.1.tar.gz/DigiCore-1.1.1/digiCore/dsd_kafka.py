"""
kafka 生产者 消费者模块

"""
import json
from math import ceil
from typing import Optional
from confluent_kafka import Producer, TopicPartition, Consumer
from loguru import logger
import traceback

from digiCore import format_error_msg


def chunk(lst, size):
    """
    将大的列表切割为指定大小的小列表套列表
    :param lst: 大列表
    :param size: 小列表数据大小
    :return: list
    """

    return list(
        map(lambda x: lst[x * size:x * size + size],
            list(range(0, ceil(len(lst) / size)))))


def publish_delivery_report(err, msg) -> None:
    """
    发布消息记录
    :param err: 消息的错误信息
    :param msg: 消息
    :return:
    """
    try:
        if err is not None:
            logger.error('Message delivery failed: {}'.format(err))
        else:
            return
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())


class KafkaDao:

    def __init__(self,
                 topic: str,
                 partition: int,
                 brokers: list,
                 sub_server: Optional[str] = 'Test',
                 kafka_consumer_batch: Optional[int] = 1,
                 kafka_consumer_timeout: Optional[int] = 2):
        """
        :param topic: kafka 发送数据 topic
        :param partition: 分区
        :param brokers: 连接kafka集群地址列表
        """
        self.kafka_topic = topic
        self.partition = partition
        self.bootstrap_servers = ",".join(brokers)
        self.sub_server = sub_server
        self.kafka_producer = Producer({'bootstrap.servers': self.bootstrap_servers, "compression.type": "lz4"})
        self.subscriber = self.kafka_config()
        self.kafka_consumer_batch = kafka_consumer_batch
        self.kafka_consumer_timeout = kafka_consumer_timeout

    def produce_data_to_kafka(self, sink_data_list, length=200):
        """
        发送数据到kafka
        :param length: 发送数据最大列表数
        :param sub_server: 子服务名称
        :param sink_data_list: 需要发送的数据列表
        :return: None
        """
        kafka_producer_timeout = 2
        group_data_list = chunk(sink_data_list, length)
        for group_data in group_data_list:
            send_data = {
                "data_channel_identifier": self.sub_server,
                "data": group_data
            }
            bson_data = json.dumps(send_data, ensure_ascii=False).encode('utf-8')
            self.kafka_producer.produce(topic=self.kafka_topic,
                                        key=self.sub_server,
                                        value=bson_data,
                                        partition=self.partition,
                                        callback=publish_delivery_report
                                        )
            self.kafka_producer.poll(kafka_producer_timeout)
            self.kafka_producer.flush()

    def kafka_config(self):
        """
        kafka配置信息
        conf 指定 kafka集群连接地址、消费组、提交方式、取数方式
        :return:
        """
        conf = {"bootstrap.servers": self.bootstrap_servers,  # kafka地址
                "group.id": self.sub_server,  # 消费组
                "enable.auto.commit": True,  # 提交方式，True自动提交
                "default.topic.config": {"auto.offset.reset": "latest"}  # 从提交的offset取数据，未有提交的，从最新的offset开始取数
                }

        topic_part = TopicPartition(self.kafka_topic, self.partition)  # 配置主题+分区
        subscriber = Consumer(conf)  # 配置topic——config
        topic_part_out = subscriber.committed([topic_part])  # 提交主题+分区
        init_offset = topic_part_out[0].offset  # 获取当前offest位置
        topic_part_new = TopicPartition(self.kafka_topic, self.partition,
                                        init_offset - 10)  # 将0位置设置为当前的位置，指针回调kafka_consumer_batch
        subscriber.commit(offsets=[topic_part_new])  # 提交最新offset
        subscriber.assign([topic_part])  # 手动分配 主题+分区
        return subscriber

    def consume_data_from_kafka(self):
        """
        消费子服务 指定分区的kafka数据
        :return: list
        """
        consume_data = self.subscriber.consume(self.kafka_consumer_batch, self.kafka_consumer_timeout)
        if not consume_data:
            return []
        try:
            for msg in consume_data:
                massage = msg.value().decode()
                data_list = json.loads(massage)["data"]
                return data_list
        except Exception as e:
            format_error_msg(e)
            return []
