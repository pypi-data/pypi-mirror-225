from typing import Any, Generic, List, Tuple, TypeVar, Dict, Optional

from babel.support import LazyProxy
from stfu_tg import Italic, Code

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import (ArgCustomError, ArgInListItemError, ArgTypeError, ArgIsRequiredError,
                               TypeCheckCustomError, ArgSyntaxEntityError)
from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.wrapped import WrappedArgFabricABC

ListArgItemType = TypeVar('ListArgItemType')


class ListArg(WrappedArgFabricABC[List[Any]], Generic[ListArgItemType]):
    """
    ListArg represents an argument that takes one child argument and tries to get a list of them from the text.
    The nested lists (lists in lists) are NOT SUPPORTED!
    It's recommended to use ListArg(DividedArg()) or DividedArg(ListArg()) which is less overhead for end-users.
    More complicated setups stays untested ATM!
    """
    separator: str
    prefix: str
    postfix: str

    def __init__(
            self,
            *args,
            separator: str = ',',
            prefix: str = '(',
            postfix: str = ')',
    ):
        super().__init__(*args)

        self.separator = separator
        self.prefix = prefix
        self.postfix = postfix

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        # TODO: Show settings??
        return (
            # Here we use always plural, because lists contains many items
            LazyProxy(lambda: _("List of {}").format(self.child_fabric.needed_type[1])),
            LazyProxy(lambda: _("Lists of {}").format(self.child_fabric.needed_type[1]))
        )

    @property
    def examples(self) -> Optional[Dict[str, LazyProxy]]:
        if not (child_examples := self.child_fabric.examples):
            return None

        examples = f'{self.separator} '.join(str(x) for x in child_examples.keys())

        return {
            f'{self.prefix}{examples}{self.postfix}': LazyProxy(
                lambda: _("List of {}").format(self.child_fabric.needed_type[1])
            )
        }

    def check(self, text: str, entities: ArgEntities) -> bool:
        if not text.startswith(self.prefix):
            raise TypeCheckCustomError(_("The starting charter {} of list wasn't found!").format(Code(self.prefix)))

        elif self.postfix and entities.get_non_overlapping_index(
                text,
                self.postfix,
                start_offset=len(self.prefix or '')
        ) == -1:
            # TODO: Nested lists?
            raise TypeCheckCustomError(_("The ending charter {} of list wasn't found!").format(Code(self.postfix)))

        # Is empty?
        elif text.find(self.prefix) + 1 == text.find(self.postfix):
            raise TypeCheckCustomError(_("The list is empty!"))

        return True

    def _find_next_separator(self, text: str, entities: ArgEntities, start_offset: int = 0) -> int:
        return entities.get_non_overlapping_index(text, self.separator, start_offset)

    def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> Tuple[int, List[ListArgItemType]]:
        items = []

        # Check for the overlapping entities in prefix
        # TODO: Test this
        prefix_len = len(self.postfix)
        if self.prefix and entities.get_overlapping(0, prefix_len):
            raise ArgSyntaxEntityError(
                l_("➡️ The start prefix text of the lists cannot have the overlapping formatting"),
                description=self.description,
                length=prefix_len,
                offset=offset
            )

        # Deal with syntax
        if self.prefix:
            text = text[prefix_len:]
            entities = entities.cut_before(prefix_len)
        if self.postfix:
            postfix_offset = entities.get_non_overlapping_index(text, self.postfix, prefix_len)
            text = text[:postfix_offset]
            entities = entities.cut_after(postfix_offset)

        # The length of the postfix we add later
        length = prefix_len

        while text:
            # Strip text to the left after removing the prefix
            real_arg_len = len(text) - len(text := text.lstrip())
            real_arg_offset = offset + real_arg_len

            separator_index = self._find_next_separator(text, entities)
            has_separator = separator_index != -1

            arg_text = text if self.child_fabric.know_the_end or not has_separator else text[:separator_index]

            if not arg_text.strip():
                raise ArgIsRequiredError(
                    description=self.child_fabric.description,
                    examples=self.child_fabric.examples,
                    needed_type=self.child_fabric.needed_type,
                    offset=length
                )

            try:
                items.append(arg := self.child_fabric(
                    arg_text,
                    real_arg_offset,
                    entities.cut_before(real_arg_len).cut_after(len(arg_text)),
                    known_end_arg_text=text,
                    not_known_end_arg_text=text[:separator_index] if has_separator else text
                ))

            except ArgTypeError as e:
                raise ArgInListItemError(e) from e

            if not self.child_fabric.know_the_end:
                text = text[separator_index + 1:] if has_separator else ''
                # length += len(text) - len(text := text.lstrip())

                # Calculate the number of extra symbols that wasn't occupied by the argument
                if has_separator:
                    if arg_text[arg.length:].rsplit():
                        raise ArgCustomError(
                            LazyProxy(lambda: _(
                                "Argument '{arg_text}' was parsed, but it has unknown text after it!",
                            ).format(
                                arg_text=Italic(arg_text[:arg.length])
                            )),
                            l_("Please ensure you correctly divided all of arguments."),
                            offset=length + arg.length,
                            length=separator_index - arg.length - 1,
                            strikethrough=True
                        )
                    real_arg_len += len(self.separator)

                # Text after parsed arg text (spaces)
                real_arg_len += len(arg_text[arg.length:])
            else:
                text = text[arg.length:]

                next_separator = self._find_next_separator(text, entities)
                if next_separator != -1 and not text.lstrip().startswith(self.separator):
                    length = next_separator - length - 1
                    raise ArgCustomError(
                        LazyProxy(lambda: _(
                            "Argument '{arg_text}' was parsed, but it has unknown text after it!"
                        ).format(
                            arg_text=Italic(arg_text[:arg.length])
                        )),
                        l_("Please ensure you correctly divided all of arguments."),
                        offset=length + arg.length,
                        length=length,
                        strikethrough=True
                    )

            real_arg_len += arg.length
            real_arg_len += (len(text) - len(text := text.lstrip()))

            if self.child_fabric.know_the_end:
                # Because above we already cut the text before the separator
                # Making an if here fixed a small bug when double separators could be ignored
                real_arg_len += (len(text) - len(text := text.removeprefix(self.separator)))

            length += real_arg_len

            entities = entities.cut_before(real_arg_len)

            if not has_separator:
                # No more separators - returning
                break

            if not arg.length and not text:
                # Argument has no length, and no text left - Means this argument consumes all text
                break

        # Add the end
        length += len(self.postfix)

        return length, items


class DividedArg(ListArg):

    def __init__(self, *args, separator='|'):
        super().__init__(*args, separator=separator, prefix='', postfix='')
