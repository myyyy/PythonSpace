import sys
from tornado import template

reload(sys)
sys.setdefaultencoding('utf-8')

path = 'template'
loader = template.Loader(path)