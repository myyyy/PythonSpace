
import os
import sys
import tornado.web

def route(pattern=None, order=0):
    """
    set router for RequestHandler 
    @url('/blog/info/(.*)')
    """
    def actual(handler):
        ''' set attr for handler'''
        assert(issubclass(handler, tornado.web.RequestHandler))
        if not hasattr(handler, "__urls__") or not handler.__urls__:
            handler.__urls__ = []
        
        if not pattern:
            p = '/{0}/{1}'.format(handler.__module__,handler.__name__).lower()
            p = p.replace('.','/')
            handler.__urls__.append((p, 0))
        else:
            handler.__urls__.append((pattern,order))
        
        return handler

    return actual