# -*- coding:utf-8 -*-

from celery import Celery
from server import add
import time
result = add.delay(4,4)

print "Waiting result..." 
while not result.ready():
  time.sleep(2)
  
print "Result:",result.get()