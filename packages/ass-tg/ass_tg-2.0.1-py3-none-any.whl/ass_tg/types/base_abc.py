from abc import ABC
from typing import Any, Generic, Optional, Tuple, TypeVar, Dict, List

from babel.support import LazyProxy
from stfu_tg.formatting import StyleFormationCore

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgTypeError, TypeCheckCustomError

ArgValueType = TypeVar('ArgValueType')


class ArgFabric(Generic[ArgValueType]):
    """Provides a way to create an argument fabric."""
    description: Optional[LazyProxy | str] = None

    # Some parameters used by the other arguments
    know_the_end: bool = False
    default_no_value_value: Optional[Any] = None

    def __init__(self, description: Optional[LazyProxy | str] = None):
        self.description = description

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        """
        Returns a needed type text.
        """
        raise NotImplementedError

    @property
    def examples(self) -> Optional[Dict[str | StyleFormationCore, Optional[LazyProxy]]]:
        """
        Returns a dictionary of examples using this argument, and its description.
        description is optional as well as the dictionary itself.
        """
        return None

    @staticmethod
    def check(
            text: str,
            entities: ArgEntities
    ) -> bool:
        """
        Checks if the given text is valid for this type.
        It should check by the start of the text, as it could contain other arguments separated.
        Return boolean or raises TypeCheckCustomError.

        Be aware that text CAN BE longer and more entities CAN BE SUPPLIED than argument should take.
        You CAN NOT check the Argument type by the end of the text!
        """
        return True

    def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> Tuple[int, ArgValueType]:
        """
        Parses the arguments texts and returns the length of argument and value.
        Returns None if there's no more arguments.

        Be aware that text CAN BE longer and more entities CAN BE SUPPLIED than argument should take.
        You should use only what you need and return an occupied amount of symbols.
        """

        raise NotImplementedError

    def pre_parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities,
            **_kwargs
    ) -> Tuple[int, ArgValueType]:
        """
        Very special function, usually you DON'T use it. Unless you need to access _kwargs
        """
        return self.parse(text, offset, entities)

    def unparse(
            self,
            data: ArgValueType,
            **kwargs
    ) -> str:
        """Unparses the argument data back into text"""

        raise NotImplementedError

    @staticmethod
    def get_end(raw_text: str, entities: ArgEntities) -> int:
        return len(raw_text)

    def __call__(
            self,
            text: str,
            offset: int,
            entities: ArgEntities,
            **kwargs) -> "ParsedArg[ArgValueType]":

        arg_type_error_text = None
        try:
            is_ok = self.check(text, entities)
        except TypeCheckCustomError as e:
            is_ok = False
            arg_type_error_text = e.text

        if not is_ok:
            raise ArgTypeError(
                needed_type=self.needed_type,
                description=self.description,
                offset=offset,
                length=self.get_end(text, entities),
                text=arg_type_error_text or None,
                examples=self.examples or {},
            )

        length, value = self.pre_parse(text, offset, entities, **kwargs)
        return ParsedArg(self, value, offset, length)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


ParsedArgType = TypeVar('ParsedArgType')


class ParsedArg(ABC, Generic[ParsedArgType]):
    """Argument object."""

    fabric: ArgFabric
    value: ParsedArgType

    offset: int
    length: int

    def __init__(self, fabric: ArgFabric, value: ParsedArgType, offset: int, length: int):
        self.fabric = fabric
        self.value = value
        self.offset = offset
        self.length = length

    def get_value(self) -> Any:
        if isinstance(self.value, ParsedArg):
            return self.value.get_value()

        elif isinstance(self.value, List):
            return [x.get_value() if isinstance(x, ParsedArg) else x for x in self.value]

        return self.value

    @property
    def values(self) -> Tuple[ParsedArgType]:
        if not isinstance(self.value, list):
            raise TypeError("Value must be a ArgFabric")

        return tuple(x.value for x in self.value)

    def __repr__(self):
        return f"<{self.fabric}: {self.value=} {self.length=}>"


class ParsedArgs(Dict[str, ParsedArg]):
    pass


class OneWordArgFabricABC(ArgFabric, ABC):
    needed_type: Tuple[LazyProxy, LazyProxy]
    args_separator: str = ' '

    def check_type(self, text: str) -> bool:
        raise NotImplementedError

    def simple_check(self, text: str, entities: ArgEntities) -> bool:
        return text.lstrip() != ""

    def value(self, text: str) -> Any:
        raise NotImplementedError

    def parse(self, raw_text: str, offset: int, entities: ArgEntities) -> Tuple[int, Any]:
        first_word, *_rest = raw_text.split(self.args_separator, 1)

        if not self.check_type(first_word):
            raise ArgTypeError(
                # text=first_word,
                needed_type=self.needed_type,
                description=self.description,
                length=len(first_word),
                offset=offset,
                examples=self.examples or {}
            )

        return len(first_word), self.value(first_word)
