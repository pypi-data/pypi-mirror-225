from typing import Any, Tuple, Dict, Optional

from babel.support import LazyProxy
from stfu_tg import Code, Italic

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgSyntaxEntityError, TypeCheckCustomError, ArgCustomError
from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.wrapped import WrappedArgFabricABC


class SurroundedArg(WrappedArgFabricABC):
    prefix: Optional[str]
    postfix: Optional[str]

    def __init__(self, *args, prefix: Optional[str] = '"', postfix: Optional[str] = '"'):
        super().__init__(*args)

        self.prefix = prefix
        self.postfix = postfix
        self.know_the_end = bool(postfix) or self.child_fabric.know_the_end

    def check(self, text: str, entities: ArgEntities) -> bool:
        if self.prefix and not text.startswith(self.prefix):
            raise TypeCheckCustomError(_("➡️ The Argument should start with {}!").format(Code(self.prefix)))

        if self.postfix and entities.get_non_overlapping_index(text, self.postfix, start_offset=len(self.prefix or
                                                                                                    '')) == -1:
            raise TypeCheckCustomError(_("⬅️️ The Argument should end with {}!").format(Code(self.postfix)))

        return True

    def parse(self, text: str, offset: int, entities: ArgEntities) -> Tuple[int, Any]:
        prefix_length = len(self.prefix or '')
        length = prefix_length

        if self.prefix:
            # The first charter is the start charter.
            if entities.get_overlapping(0, prefix_length):
                raise ArgSyntaxEntityError(
                    l_("➡️ The start text cannot have the overlapping formatting"),
                    description=self.description,
                    length=prefix_length,
                    offset=offset
                )

            text = text.removeprefix(self.prefix)
            entities = entities.cut_before(prefix_length)
        if self.postfix:
            postfix_index = entities.get_non_overlapping_index(text, self.postfix, start_offset=prefix_length)
            entities = entities.cut_after(postfix_index)
            text = text[:postfix_index]

        # Strip text on left
        length += len(text) - len(text := text.lstrip())

        arg_length, data = super().parse(text, offset + prefix_length, entities)
        length += arg_length

        text_after_arg = text[arg_length:]

        if self.postfix and (len(text_after_arg.rstrip()) > 0):
            raise ArgCustomError(
                LazyProxy(lambda: _(
                    "➡️ Argument '{arg_text}' was parsed, but it has unknown text after it!",
                ).format(
                    arg_text=Italic(text[:arg_length])
                )),
                offset=length,
                length=len(text) - arg_length,
                strikethrough=True
            )

        length += len(text_after_arg)
        length += len(self.postfix or '')

        return length, data

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (
            LazyProxy(lambda: _("{} surrounded by {} and {}").format(
                self.child_fabric.needed_type[0],
                self.prefix, self.postfix
            )),
            LazyProxy(lambda: _("{} surrounded by {} and {}").format(
                self.child_fabric.needed_type[1],
                self.prefix, self.postfix
            )),
        )

    @property
    def examples(self) -> Optional[Dict[str, str | LazyProxy]]:
        # TODO: Translates?
        return (
            {
                f'{self.prefix}{e}{self.postfix}':
                    f'{d or e}: {_("Surrounded by {} and {}").format(self.prefix, self.postfix)}'
                for e, d in child_examples.items()
            }
            if (child_examples := self.child_fabric.examples)
            else None
        )

    def unparse(
            self,
            data: Any,
            **kwargs
    ) -> str:
        # TODO: Entities?
        return f'{self.prefix}{self.child_fabric.unparse(data, **kwargs)}{self.postfix}'


class StartsWithArg(SurroundedArg):
    starts_with: str

    def __init__(self, starts_with: str, *args):
        super().__init__(*args)

        self.prefix = starts_with
        self.postfix = None


class UntilArg(SurroundedArg):
    know_the_end = True

    def __init__(self, ends_with: str, *args):
        super().__init__(*args)

        self.prefix = None
        self.postfix = ends_with
