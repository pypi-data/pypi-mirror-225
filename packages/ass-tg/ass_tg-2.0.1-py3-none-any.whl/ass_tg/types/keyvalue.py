from typing import Optional, Tuple, Dict

from babel.support import LazyProxy
from stfu_tg import Italic

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgCustomError, ArgError, ArgInListItemError, TypeCheckCustomError
from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.base_abc import ArgFabric, ParsedArg
from ass_tg.types.wrapped import WrappedArgFabricABC


class KeyValueArg(WrappedArgFabricABC):
    startswith: str = '^'
    equal_symbol: str = '='

    know_the_end = True

    key: str

    def __init__(self, key: str, child_fabric, *args):
        super().__init__(child_fabric, *args)

        self.key = key

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (
            LazyProxy(lambda: _("Key-value of {}").format(self.child_fabric.needed_type[0])),
            LazyProxy(lambda: _("Key-values of {}").format(self.child_fabric.needed_type[1]))
        )

    def check(self, text: str, entities: ArgEntities) -> bool:
        return text.startswith(self.startswith)

    def parse(
            self,
            raw_text: str,
            offset: int,
            entities: ArgEntities
    ) -> Tuple[int, ParsedArg]:

        length = 0

        # Deal with prefix
        text = raw_text.removeprefix(self.startswith).lstrip()
        length += len(raw_text) - len(text)

        # Check for the key
        if not text.startswith(self.key):
            # Wrong argument name
            raise ValueError

        # Delete key
        length += len(text) - len(text := text.removeprefix(self.key).lstrip())

        # Deal with =
        if text.startswith(self.equal_symbol):
            length += len(text) - len(text := text.removeprefix(self.equal_symbol).lstrip().rstrip())
        elif not self.child_fabric.default_no_value_value:
            # Contains no value
            raise ArgCustomError(LazyProxy(lambda: _(
                "The optional argument {name} must contain a value!"
            ).format(name=Italic(self.key))))
        else:
            return length, self.child_fabric.default_no_value_value

        try:
            arg_offset = offset + length
            arg = self.child_fabric(text, arg_offset, entities.cut_before(arg_offset))
        except ArgError as e:
            # TODO: better error message
            raise ArgInListItemError(e) from e

        return length + arg.length, arg.value


class KeyValuesArg(ArgFabric):
    key_values: Tuple[KeyValueArg]

    def __init__(self, *key_values: KeyValueArg):
        super().__init__()

        self.key_values = key_values

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (
            l_("Key-values"),
            l_("Key-values"),
        )

    @staticmethod
    def check(
            raw_text: str,
            entities: ArgEntities
    ) -> bool:
        return True

    def parse(self, raw_text: str, offset: int, entities: ArgEntities) -> Tuple[int, Dict[str, Optional[ParsedArg]]]:

        length = 0
        text = raw_text

        data: Dict[str, Optional[ParsedArg]] = {x.key: None for x in self.key_values}

        while text.startswith('^'):
            for key_value in self.key_values:
                arg_offset = offset + length
                arg_entities = entities.cut_before(arg_offset)

                try:
                    if not key_value.check(text, arg_entities):
                        continue
                except TypeCheckCustomError:
                    continue

                try:
                    arg = key_value(text, arg_offset, arg_entities)
                except ValueError:
                    continue
                except ArgError as e:
                    # TODO: better error message
                    raise ArgInListItemError(e) from e

                data[key_value.key] = arg
                length += len(text) + len(text := text[arg.length:].lstrip())

                break

        return length, data
