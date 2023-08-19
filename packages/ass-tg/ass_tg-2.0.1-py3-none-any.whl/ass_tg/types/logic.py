import contextlib
from typing import Any, Optional, Tuple, Dict

from babel.support import LazyProxy

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgTypeError, TypeCheckCustomError, ArgIsRequiredError
from ass_tg.i18n import lazy_gettext as l_, gettext as _
from ass_tg.types.base_abc import ArgFabric, ParsedArgs
from ass_tg.types.wrapped import WrappedArgFabricABC


class OptionalArg(WrappedArgFabricABC):

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (
            l_("Optional {}").format(self.child_fabric.needed_type[0]),
            l_("Optionals {}").format(self.child_fabric.needed_type[0]),
        )

    def check(self, text: str, entities: ArgEntities) -> bool:
        return True

    def parse(self, text: str, offset: int, entities: ArgEntities) -> Tuple[Optional[int], Any]:
        with contextlib.suppress(ArgTypeError, TypeCheckCustomError):
            if self.child_fabric.check(text, entities):
                arg = self.child_fabric(text, offset, entities)
                return arg.length, arg.value
        return 0, None


class OrArg(ArgFabric):
    args_type: Tuple[ArgFabric, ...]

    def __init__(self, *args_type: ArgFabric):
        super().__init__(args_type[0].description)
        self.args_type = args_type

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (l_(" or ").join(f"'{arg.needed_type[0]}'" for arg in self.args_type),
                l_(" or ").join(f"'{arg.needed_type[1]}'" for arg in self.args_type))

    @staticmethod
    def check(text: str, entities: ArgEntities) -> bool:
        return bool(text)

    def pre_parse(
            self,
            raw_text: str,
            offset: int,
            entities: ArgEntities,
            **data
    ) -> Tuple[int, Any]:
        for arg_fabric in self.args_type:
            try:
                if arg_fabric.know_the_end:
                    text = data.get("know_end_arg_text", raw_text)
                else:
                    text = data.get("not_known_end_arg_text", raw_text)

                try:
                    if not arg_fabric.check(text, entities):
                        continue
                except TypeCheckCustomError:
                    continue

                self.know_the_end = arg_fabric.know_the_end
                arg = arg_fabric(text, offset, entities)

                return arg.length, arg.value

            except ArgTypeError:
                continue

        raise ArgTypeError(
            needed_type=self.needed_type,
            description=self.description,
            examples=self.examples,
            length=len(raw_text),
            offset=offset
        )

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {", ".join(str(x) for x in self.args_type)}'


class AndArg(ArgFabric):
    """
    Represents a basic and the first argument, which contains the child ones.
    Each argument contains its name and a fabric.
    Implements arguments validation.
    """

    fabrics: Dict[str, ArgFabric]

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.fabrics = kwargs

    @property
    def needed_type(self):
        return _(", and ").join(str(x.needed_type[0]) for x in self.fabrics.values()), ""

    @property
    def examples(self) -> Optional[Dict[str, LazyProxy | str]]:

        example_str = ''

        for idx, fabric in enumerate(self.fabrics.values()):
            example_str += " " if idx > 0 else ""

            if not fabric.examples:
                return None

            example_str += str(tuple(fabric.examples.keys())[0])

        return {
            example_str: _("Example syntax")
        }

    @staticmethod
    def check(text: str, entities: ArgEntities) -> bool:
        return True

    def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> Tuple[int, ParsedArgs]:

        args_data = ParsedArgs()
        length = 0
        args_length = 0

        for arg_codename, arg_fabric in self.fabrics.items():
            # Strip text and count offset
            stripped_offset = (len(text) - len(text := text.lstrip()))
            offset += stripped_offset

            arg_entities = entities.cut_before(stripped_offset + args_length)

            if not text.strip():
                raise ArgIsRequiredError(
                    description=arg_fabric.description,
                    examples=arg_fabric.examples,
                    needed_type=arg_fabric.needed_type,
                    offset=offset
                )

            arg = arg_fabric(text, offset, arg_entities)
            length += arg.length
            args_data[arg_codename] = arg

            args_length += arg.length
            offset += arg.length
            text = text[arg.length + stripped_offset:]

            if not arg.length and text:
                # Argument has no length, and no text left - Means this argument consumes all text
                break

        return length, args_data
