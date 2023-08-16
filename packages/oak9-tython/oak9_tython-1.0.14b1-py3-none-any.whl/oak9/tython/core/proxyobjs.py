from typing import TypeVar

_T = TypeVar("_T")


class AbstractProxy(object):
    """
    Delegates all operations (except ``.__subject__``) to another object

    Note: Adapted from https://github.com/neg3ntropy/objproxies
    """
    __slots__ = "__subject__"

    def __init__(self, subject):
        self.__subject__ = subject

    def __call__(self, *args, **kw):
        return self.__subject__(*args, **kw)

    def __getattribute__(self, attr, oga=object.__getattribute__):
        subject = oga(self, '__subject__')
        if attr == '__subject__':
            return subject
        return getattr(subject, attr)

    def __setattr__(self, attr, val, osa=object.__setattr__):
        if attr == '__subject__':
            osa(self, attr, val)
        else:
            setattr(self.__subject__, attr, val)

    def __delattr__(self, attr, oda=object.__delattr__):
        if attr == '__subject__':
            oda(self, attr)
        else:
            delattr(self.__subject__, attr)

    def __bool__(self):
        return bool(self.__subject__)

    def __getitem__(self, arg):
        return self.__subject__[arg]

    def __setitem__(self, arg, val):
        self.__subject__[arg] = val

    def __delitem__(self, arg):
        del self.__subject__[arg]

    def __getslice__(self, i, j):
        return self.__subject__[i:j]

    def __setslice__(self, i, j, val):
        self.__subject__[i:j] = val

    def __delslice__(self, i, j):
        del self.__subject__[i:j]

    def __contains__(self, ob):
        return ob in self.__subject__

    for name in 'repr str hash len abs complex int long float'.split():
        exec("def __%s__(self): return %s(self.__subject__)" % (name, name))

    for name in 'cmp', 'coerce', 'divmod':
        exec("def __%s__(self, ob): return %s(self.__subject__, ob)" % (name, name))

    for name, op in [
        ('lt', '<'), ('gt', '>'), ('le', '<='), ('ge', '>='),
        ('eq', ' == '), ('ne', '!=')
    ]:
        exec("def __%s__(self, ob): return self.__subject__ %s ob" % (name, op))

    for name, op in [('neg', '-'), ('pos', '+'), ('invert', '~')]:
        exec("def __%s__(self): return %s self.__subject__" % (name, op))

    for name, op in [
        ('or', '|'),  ('and', '&'), ('xor', '^'), ('lshift', '<<'), ('rshift', '>>'),
        ('add', '+'), ('sub', '-'), ('mul', '*'), ('div', '/'), ('mod', '%'),
        ('truediv', '/'), ('floordiv', '//')
    ]:
        exec((
            "def __%(name)s__(self, ob):\n"
            "    return self.__subject__ %(op)s ob\n"
            "\n"
            "def __r%(name)s__(self, ob):\n"
            "    return ob %(op)s self.__subject__\n"
            "\n"
            "def __i%(name)s__(self, ob):\n"
            "    self.__subject__ %(op)s=ob\n"
            "    return self\n"
        ) % locals())

    del name, op

    # Oddball signatures
    def __index__(self):
        return self.__subject__.__index__()

    def __rdivmod__(self, ob):
        return divmod(ob, self.__subject__)

    def __pow__(self, *args):
        return pow(self.__subject__, *args)

    def __ipow__(self, ob):
        self.__subject__ **= ob
        return self

    def __rpow__(self, ob):
        return pow(ob, self.__subject__)


class AbstractWrapper(AbstractProxy):
    """Mixin to allow extra behaviors and attributes on proxy instance"""
    __slots__ = ()

    def __getattribute__(self, attr, oga=object.__getattribute__):
        if attr.startswith('__'):
            subject = oga(self, '__subject__')
            if attr == '__subject__':
                return subject
            return getattr(subject, attr)
        return oga(self, attr)

    def __getattr__(self, attr, oga=object.__getattribute__):
        return getattr(oga(self, '__subject__'), attr)

    def __setattr__(self, attr, val, osa=object.__setattr__):
        if (
            attr == '__subject__' or
            hasattr(type(self), attr) and not attr.startswith('__')
        ):
            osa(self, attr, val)
        else:
            setattr(self.__subject__, attr, val)

    def __delattr__(self, attr, oda=object.__delattr__):
        if (
            attr == '__subject__' or
            hasattr(type(self), attr) and not attr.startswith('__')
        ):
            oda(self, attr)
        else:
            delattr(self.__subject__, attr)


class PathTrackerWrapper(AbstractWrapper):
    _id = ''

    def __init__(self, subject, cur_path=None):
        super().__init__(subject)

        # Properties must be defined on the class
        self._id = cur_path or ''

    def __getattr__(self, attr_name, **kwargs):
        val = super().__getattr__(attr_name, **kwargs)

        if attr_name == '_cur_path':
            return val
        else:
            path = self._id + '.' + attr_name if self._id else attr_name
            return PathTrackerProxy.create(val, path)

    def __getitem__(self, key):
        val = super().__getitem__(key)
        path = self._id + f'[{key}]' if self._id else key
        return PathTrackerProxy.create(val, path)


class DictWrapper(PathTrackerWrapper):
    """
    Overrides dictionary access methods get(), keys(), values(), and items() to
    return proxied values as well.
    """
    def __init__(self, subject, cur_path=None):
        super().__init__(subject)
        self._id = cur_path

    def get(self, key, default=None):
        try:
            return PathTrackerProxy.create(self.__subject__[key], self._id + f'[{key}]')
        except KeyError:
            return default

    def items(self):
        return [
            (
                PathTrackerProxy.create(k, self._id + f'[{k}]'),
                PathTrackerProxy.create(v, self._id + f'[{k}]')
            )
            for k, v in self.__subject__.items()
        ]

    def keys(self):
        return [PathTrackerProxy.create(k, self._id + f'[{k}]') for k in self.__subject__.keys()]

    def values(self):
        return [PathTrackerProxy.create(v, self._id + f'[{k}]') for k, v in self.__subject__.items()]

def normalize_name_format(resource) -> str:
    """
    normalize_name_format returns a snake case version of the objects name
    Args:
        resource:  DESCRIPTOR Property from resource that contains the resource name.
    Returns:
        name: returns name of object in snake case
    """
    resource_name: str = resource.name[0]
    for counter, character in enumerate(resource.name):
        if character == "_" or counter == 0:
            continue
        elif character.isupper() and (resource_name[-1].islower() or resource_name[-1].isdigit()):
            resource_name += '_' + character
        else:
            resource_name += character

    return resource_name.lower()

class PathTrackerProxy:
    @staticmethod
    def create(subject: _T, cur_path=None) -> _T:
        if cur_path is None and 'DESCRIPTOR' in subject.__dir__():
            cur_path = normalize_name_format(subject.DESCRIPTOR)
        if type(subject) == dict:
            return DictWrapper(subject, cur_path)

        return PathTrackerWrapper(subject, cur_path)
