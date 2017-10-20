# -*- coding:utf-8 -*-
from celery import Task
from celery import Celery

import celeryconfig

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')
app.config_from_object(celeryconfig)
app.conf.CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'

class DebugTask(Task):
    """基类task方法，可以重写部分东西"""
    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)

@app .task(base=DebugTask)
def add(x, y):
    return x + y

#运行方式　 celery -A server worker --loglevel=info
# if __name__ == '__main__':
#     app.worker_main()