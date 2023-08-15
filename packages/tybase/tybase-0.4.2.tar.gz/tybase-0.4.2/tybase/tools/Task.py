import pickle
from uuid import uuid4
import redis
import requests
from loguru import logger
import time


class TaskRunner:
    """
        from tybase.tools.Task import TaskRunner
        def my_notify_callback(task):
            url = 'YOUR_NOTIFY_URL'
            headers = {"TOKEN": "YOUR_NOTIFY_TOKEN"}
            data = {
                "queue_id": task.id,
                "convert_url": task.result,
                "status": 100 if task.status == "completed" else 250
            }

            try:
                response = requests.post(url, json=data, headers=headers)
                print(response.status_code, "成功")
            except Exception as e:
                print(f'Notify failed due to: {str(e)}')


        def my_work_function(param1, param2):
            # 这里执行你的实际工作
            return "result"

        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=1)


        # 创建后台任务
        task = TaskRunner.Task(my_work_function, {'param1': 'value1', 'param2': 'value2'}, callback=my_notify_callback)

        redis_config = {
            'host': '',
            'port': '',
            'password': '',
            'decode_responses': True  # 或者 False，根据你的需求
        }
        runner = TaskRunner(redis_config, my_notify_callback)

        runner.run_task(task)
        executor.submit(run_task, task)  # 异步执行

    #不返回值,可以通过回调函数来通知
    def my_notify_callback(task):
        print('Task ID:', task.id)
        print('Task status:', task.status)
        print('Task result:', task.result)
        # ...
    """

    def __init__(self, redis_config, notify_callback):
        self.r = redis.Redis(**redis_config)
        self.notify_callback = notify_callback

    def notify(self, task):
        try:
            self.notify_callback(task)
        except Exception as e:
            logger.exception(f'Notify failed due to: {str(e)}')

    class Task:
        def __init__(self, func, params, callback=None):
            self.id = str(uuid4())
            self.start_time = time.time()
            self.status = "pending"
            self.func = func
            self.params = params
            self.result = None
            self.callback = callback
            self.end_time = None
            self.duration = None

        def run(self):
            try:
                self.result = self.func(**self.params)
                self.status = "completed"
            except Exception as e:
                self.status = "failed"
                logger.exception(f'Task {self.id} failed due to: {str(e)}')
            finally:
                self.end_time = time.time()
                self.duration = self.end_time - self.start_time
                if self.callback:
                    self.callback(self)

    def run_task(self, task):
        logger.info(f'Setting task {task.id} to Redis')
        self.r.setex(task.id, 2 * 60 * 60, pickle.dumps(task))
        task.run()
        # 创建并启动线程来运行任务
        self.r.setex(task.id, 2 * 60 * 60, pickle.dumps(task))


if __name__ == '__main__':
    pass
