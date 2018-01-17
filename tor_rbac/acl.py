# coding:utf-8
from __future__ import absolute_import

__all__=['Registry']

class Registry(object):
    """To reg access Handler"""
    def __init__(self, arg):
        self._role = {}
        self._resource = {}
        self._allowed = {}
    def add_role(self,role)
        self._role.setdefault(role, set())

    def add_resource(self,resource):
         self._resources.setdefault(resource, set())

    def add_allow(self,role,operation,resource,assertion=None):
         assert not role or role in self._roles
         assert not resource or resource in self._resources
    def is_allowed(self, role, operation, resource, check_allowed=True, **assertion_kwargs)
        assert not role or role in self._roles
        assert not resource or resource in self._resources