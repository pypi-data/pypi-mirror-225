"""
Decorate 中间件

"""
import time
from loguru import logger
from functools import wraps


def format_error_msg(e):
    """
    格式化错误信息
    :param e:
    :return:
    """
    logger.error(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
    logger.error(f'error line:{e.__traceback__.tb_lineno}')
    logger.error(f'error message:{e.args}')


class Decorate():
    @classmethod
    def def_retry(cls, msg=None, error_type=None, max_retry_count: int = 5, time_interval: int = 2):
        """
        任务重试装饰器
        Args:
        max_retry_count: 最大重试次数 默认5次
        time_interval: 每次重试间隔 默认2s
        """

        def _retry(task_func):
            @wraps(task_func)
            def wrapper(*args, **kwargs):
                for retry_count in range(max_retry_count):
                    try:
                        task_result = task_func(*args, **kwargs)
                        return task_result
                    except Exception as e:
                        logger.error(msg if msg else f"{max_retry_count}： 函数报错，正在重试！")
                        format_error_msg(e)
                        time.sleep(time_interval)
                return error_type if error_type else 4001

            return wrapper

        return _retry