from typing import Any, Tuple, Optional
from warnings import warn

from babel.support import LazyProxy

from ass_tg.i18n import gettext as _
from .base_abc import ArgFabric
from .text import TextArg
from .text_rules import SurroundedArg
from ..entities import ArgEntities


class RestTextArg(TextArg):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warn('RestTextArg is deprecated! Use TextArg instead!', DeprecationWarning, stacklevel=2)


class QuotedTextArg(SurroundedArg):
    def __init__(self, *args, **kwargs):
        super().__init__(
            TextArg(),
            *args,
            **kwargs
        )
        warn('QuotedTextArg is deprecated! Use SurroundedArg(TextArg()) instead!', DeprecationWarning, stacklevel=2)
        # Sometimes we can reach WrappedArgFabricABC which can override this
        self.know_the_end = True


DOES_NOT_CONTAIN_DEFAULT_ARGS = "The default implementation of StackedArg should have current_arg and stacked_arg!"


class StackedArg(ArgFabric):
    """
    Used when need to construct a fabric for an argument that contains other argument(s) inside, but it not the same
    syntax as the child argument.

    ⚠ This argument can be used as a parent class (to make own argument based on this) or in its own (as argument).

    Every stacked argument must have a start symbol (default to "(") and end symbol (default is ")")
    For example:
        current_argument_text ( child_argument_text )
    """

    # Code name help:
    # We name current argument as the first part of the argument

    know_the_end = True
    stacked_arg_start: str
    stacked_arg_end: str

    def __init__(
            self, *args,
            current_arg: Optional[ArgFabric] = None,
            stacked_arg: Optional[ArgFabric] = None,
            stacked_arg_start: str = '(',
            stacked_arg_end: str = ')'
    ):
        super().__init__(*args)

        self.current_arg = current_arg
        self.stacked_arg = stacked_arg

        self.stacked_arg_start = stacked_arg_start
        self.stacked_arg_end = stacked_arg_end

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        if not self.current_arg or not self.stacked_arg:
            raise ValueError(DOES_NOT_CONTAIN_DEFAULT_ARGS)

        return (
            LazyProxy(lambda: _("'{current_arg}' followed by parentheses with '{stacked_arg}' inside.").format(
                current_arg=self.current_arg.needed_type[0],  # type: ignore
                stacked_arg=self.stacked_arg.needed_type[0],  # type: ignore
            )),
            LazyProxy(lambda: _("'{current_arg}' followed by parentheses with '{stacked_arg}' inside.").format(
                current_arg=self.current_arg.needed_type[1],  # type: ignore
                stacked_arg=self.stacked_arg.needed_type[1],  # type: ignore
            ))
        )

    def check(self, raw_text: str, entities: ArgEntities) -> bool:
        """Change this method to overwrite the checking of the argument"""
        return self.stacked_arg_start in raw_text and self.stacked_arg_end in raw_text

    def parse(self, text: str, offset: int, entities: ArgEntities):
        if not self.current_arg or not self.stacked_arg:
            raise ValueError(DOES_NOT_CONTAIN_DEFAULT_ARGS)

        # TODO: proper exceptions and parsing entities
        length = len(self.stacked_arg_start)

        text, _rest = text.rsplit(')', 1)

        # Add unused text to length + length of end symbol
        length += len(self.stacked_arg_end) + len(_rest)

        current_text, stacked_text = text.split('(', 1)

        # Let's parse current argument
        entities = entities.cut_before(offset)
        current_arg = self.parse_current(current_text, offset, entities.cut_after(len(current_text)))
        length += current_arg.length
        # Calculate unconsumed length
        length += len(current_text[current_arg.length:])

        # Let's parse stacked argument
        # Remove spaces
        length += len(stacked_text) - len(stacked_text := stacked_text.lstrip())
        stacked_arg = self.parse_stacked(stacked_text, length, entities.cut_before(len(stacked_text)))
        length += stacked_arg.length
        length += len(stacked_text[stacked_arg.length:])

        return length, self.return_value(current_arg.value, stacked_arg.value)

    @staticmethod
    def return_value(current_arg_value: Any, stacked_arg_value: Any) -> Any:
        """Change this method to change the argument's value"""
        return current_arg_value, stacked_arg_value

    def parse_current(self, text: str, offset: int, entities: ArgEntities, **kwargs):
        if not self.current_arg or not self.stacked_arg:
            raise ValueError(DOES_NOT_CONTAIN_DEFAULT_ARGS)

        """Change this method to overwrite the parsing of current argument"""
        return self.current_arg(text, offset, entities, **kwargs)

    def parse_stacked(self, text: str, offset: int, entities: ArgEntities, **kwargs):
        if not self.current_arg or not self.stacked_arg:
            raise ValueError(DOES_NOT_CONTAIN_DEFAULT_ARGS)

        """Change this method to overwrite the parsing of stacked argument"""
        return self.stacked_arg(text, offset, entities, **kwargs)
