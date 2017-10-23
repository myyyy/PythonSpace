# -*- coding:utf-8 -*-

from code_doc2doc import get_members
def oauth2restful(**kwargs):
    """装饰器"""
    def wrapper(handler):
        handler.__oauth2restful__ = kwargs
        return handler

    return wrapper

def get_handlers():
    """放到一个文件下用来获取带装饰器的类：输出文档url ...等"""
    member_filter = lambda m: isinstance(m, type) and hasattr(m, '__oauth2restful__')
    print member_filter
    return get_members('py-tip', member_filter)

@oauth2restful()
class ReportmakerGetProjectHandler(object):
    """
    doc
    """
    pass

if __name__ == '__main__':
    print get_handlers()