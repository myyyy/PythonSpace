# -*- coding:utf-8 -*-

import os
import sys

app_path = lambda f: os.path.join(os.getcwd(), f)

def get_modules(m_path):
    ''' get all py module in m_path '''
    path = app_path(m_path)
    py_filter = lambda f: fnmatch(f, '*.py') and not f.startswith('__')
    names = [os.path.splitext(n)[0] for n in os.listdir(path) if py_filter(n)]
    sys.path.append(os.getcwd())
    return [__import__("{0}.{1}".format(m_path, n)).__dict__[n] for n in names]

def get_modules(m_path):
    ''' get all py module in m_path '''
    path = app_path(m_path)
    py_filter = lambda f: fnmatch(f, '*.py') and not f.startswith('__')
    names = [os.path.splitext(n)[0] for n in os.listdir(path) if py_filter(n)]
    sys.path.append(os.getcwd())
    return [__import__("{0}.{1}".format(m_path, n)).__dict__[n] for n in names]


def _get_members(m_path, member_filter=None, in_module=None):
    ''' get all members in m_path for member_filter'''
    modules = get_modules(m_path)
    if not member_filter:
        member_filter = lambda m: isinstance(m, type)

    if in_module:
        m = __import__("{0}.{1}".format(m_path, in_module)).__dict__[in_module]
        return dict(("{0}.{1}".format(v.__module__, k), v) for k, v in getmembers(m, member_filter))

    ret = {}
    for m in modules:
        members = dict(("{0}.{1}".format(
            v.__module__, k), v) for k, v in getmembers(m, member_filter))
        ret.update(members)
    return ret


def get_members(dirs, member_filter=None):
    if isinstance(dirs, str):
        dirs = (dirs,)

    ms = {}
    for path in dirs:
        try:
            ms.update(_get_members(path,member_filter=member_filter))
        except Exception as e:
            print e

    return ms