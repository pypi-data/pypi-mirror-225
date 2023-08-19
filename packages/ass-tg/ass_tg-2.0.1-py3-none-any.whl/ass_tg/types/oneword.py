from abc import ABC
from typing import Tuple, Dict

from babel.support import LazyProxy

from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.base_abc import OneWordArgFabricABC


class WordArg(OneWordArgFabricABC, ABC):

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Word (string with no spaces)"), l_("Words (strings with no spaces)")

    def value(self, text: str) -> str:
        return text

    def check_type(self, text: str) -> bool:
        return bool(text.strip())  # Is not empty

    @property
    def examples(self) -> Dict[str, None]:
        return {
            'Hello': None,
            'Foo': None,
            'bar': None
        }


class IntArg(WordArg):

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Integer (number)"), l_("Integers (numbers)")

    def value(self, text: str) -> int:
        return int(text)

    def check_type(self, text: str) -> bool:
        return text.removeprefix('-').isdigit()


class BooleanArg(WordArg):
    default_no_value_value = True

    true_words = ("true", "t", "1", "yes", "y", "+", "on", "enable", "enabled", ":)")
    false_words = ("false", "f", "0", "no", "n", "-", "off", "disable", "disabled", ":(")

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Boolean (Yes / No value)"), l_("Booleans (Yes / No values)")

    @property
    def examples(self) -> Dict[str, LazyProxy]:
        return {
            'true': l_("True (can means Enabled or Yes)"),
            'false': l_("False (can means Disabled or No)"),
        }

    def value(self, text: str) -> bool:
        return text.lower() in self.true_words

    def check_type(self, text: str) -> bool:
        return text.lower() in {*self.true_words, *self.false_words}
