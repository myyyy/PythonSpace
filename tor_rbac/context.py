# coding:utf-8
from __future__ import absolute_import

import functools

__all__ = ["Identity", "PermissionException"]

class Permission(object):
    """To check Permission"""
    def __init__(self, checker,exception=None,**exception_kwargs):
        self._check = checker
        self.exception = exception or PermissionDenied
        self.exception_kwargs = exception_kwargs

    def __call__(self, wrapped):
        def wrapper(*args, **kwargs):
            with self:
                return wrapped(*args, **kwargs)
        return functools.update_wrapper(wrapper, wrapped)

    def __enter__(self):
        self.in_context = True
        self.check()
        return self

    def __exit__(self, exception_type, exception, traceback):
        self.in_context = False

    def __bool__(self):
        return bool(self._check())

    def __nonzero__(self):
        return self.__bool__()

    def check(self):
        if not self._check():
            raise self.exception(**self.exception_kwargs)
        return True

class Identity(object):
    """A context of identity, providing the enviroment to control access."""
    def __init__(self, arg):
        self.acl = acl
        self.roles = []
    def set_roles_loader(self,role)
        self.roles.append(role)

    def check_permission(self, operation, resource,
                         assertion=None, **exception_kwargs)
        exception = exception_kwargs.pop("exception", PermissionException)
        checker = functools.partial(self._check,
                                    operation=operation, resource=resource,
                                    **assertion or {})
        return PermissionContext(checker, exception, **exception_kwargs)

    def _check(self,operation,resource,**assertion):
        """
            To check permission 
            return True or False
        """
        role_list = list(self.roles)
        assert role_list, "permission error"
        return self.acl.is_any_allowed(role_list, operation, resource,
                                       **assertion)

    def has_roles(self, role_groups):
        had_roles = self.roles
        return any(all(role in had_roles for role in role_group)
                   for role_group in role_groups)

class PermissionException(Exception):
    """The exception for denied access request."""

    def __init__(self, message="", **kwargs):
        super(PermissionException, self).__init__(message)
        self.kwargs = kwargs
        self.kwargs['message'] = message