from contextvars import ContextVar

from aiogram.utils.i18n import I18n
from babel.support import LazyProxy

gettext_ctx: ContextVar[I18n] = ContextVar('gettext_ass_ctx')


def get_i18n() -> I18n:
    i18n = gettext_ctx.get().get_current(no_error=True)

    if i18n is None:
        raise LookupError("I18n context is not set (ASS)")
    return i18n


def gettext(*args, **kwargs) -> str:
    return get_i18n().gettext(*args, **kwargs)


def lazy_gettext(*args, **kwargs) -> LazyProxy:
    return LazyPluralProxy(gettext, *args, **kwargs)


class LazyPluralProxy(LazyProxy):

    def plural(self, n: int):
        try:
            return self._func(*self._args, n=n, **self._kwargs)
        except AttributeError as error:
            object.__setattr__(self, '_attribute_error', error)
            raise
