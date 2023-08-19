from typing import Iterable, Optional, Tuple, Dict

from babel.support import LazyProxy
from stfu_tg import Italic, Section, KeyValue, Code, Doc, Bold
from stfu_tg.formatting import StyleFormationCore

from ass_tg.i18n import gettext as _


class ArgError(Exception):
    length: Optional[int] = None
    offset: int
    strikethrough: bool = False
    add_after: str = ''

    examples: Optional[Dict[str | StyleFormationCore, Optional[LazyProxy]]]

    # Instead of highlighting the error from the message text we highlight this one (means we also add the text)
    error_placeholder: Optional[str] = None

    # Some additional data after the error for the error highlighting text
    error_postfix: Optional[str] = None

    @property
    def doc(self) -> Tuple[str]:
        raise NotImplementedError

    def get_examples(self) -> Optional[Section]:
        return Section(*(KeyValue(
            Code(k) if not isinstance(k, StyleFormationCore) else k,
            v,
            title_bold=False
        ) if v else Code(k) for k, v in self.examples.items()),
                       title=_("Examples"), title_bold=False) if self.examples else None


class ArgTypeError(ArgError):
    needed_type: Tuple[str | LazyProxy, str | LazyProxy]
    description: Optional[str | LazyProxy]

    def __init__(
            self,
            needed_type: Tuple[str | LazyProxy, str | LazyProxy],
            description: Optional[str | LazyProxy],
            length: Optional[int],
            offset: int,
            text: Optional[str | LazyProxy] = None,
            examples: Optional[Dict[str | StyleFormationCore, Optional[LazyProxy]]] = None
    ):
        self.needed_type = needed_type
        self.description = description

        self.length = length
        self.offset = offset

        self.text = text

        self.examples = examples

    @property
    def doc(self):
        title = _("The argument {description} has an invalid type").format(
            description=f'({self.description})' if self.description else ''
        )
        doc = Doc(Section(self.text, title=title)) if self.text else Doc(Bold(title))
        doc += Section(Italic(self.needed_type[0]), title=_("Needed type"), title_bold=False)
        doc += self.get_examples()

        return doc


class ArgInListItemError(ArgError):
    def __init__(
            self,
            child_error: ArgError,
            length: Optional[int] = None,
            offset: Optional[int] = None,
    ):
        self.child_error = child_error
        self.this_arg_length = length
        self.this_arg_offset = offset

    @property
    def doc(self):
        return self.child_error.doc

    @property
    def length(self):
        return self.this_arg_length or self.child_error.length

    @property
    def offset(self):
        return self.this_arg_offset or self.child_error.offset


class ArgIsRequiredError(ArgError):
    error_placeholder = ' ____'
    error_postfix = ' '

    def __init__(
            self,
            description: Optional[str | LazyProxy],
            examples: Optional[Dict[str | StyleFormationCore, Optional[LazyProxy]]],
            needed_type: Tuple[str | LazyProxy, str | LazyProxy],
            offset: Optional[int] = None,
    ):
        self.description = description
        self.examples = examples
        self.needed_type = needed_type

        self.offset = offset or -1
        self.length = len(self.error_placeholder or '')

    @property
    def doc(self):
        return (
            Bold(_("❌ The required argument {description} wasn't provided!").format(
                description=f'({self.description})' if self.description else ''
            )),
            Section(Italic(self.needed_type[0]), title=_("Needed type"), title_bold=False),

            self.get_examples()
        )


class ArgCustomError(ArgError):

    def __init__(
            self,
            *texts: Iterable[str | LazyProxy],
            length: Optional[int] = None,
            offset: int = 0,  # TODO: Deal with 0
            strikethrough: bool = False
    ):
        self.texts = texts

        self.length = length
        self.offset = offset
        self.strikethrough = strikethrough

    @property
    def doc(self) -> Tuple[str]:
        return *(str(x) for x in self.texts),


class ArgSyntaxEntityError(ArgError):
    def __init__(
            self,
            text: LazyProxy,
            description: Optional[str | LazyProxy],
            length: Optional[int] = None,
            offset: int = 0
    ):
        self.description = description

        self.text = text

        self.length = length
        self.offset = offset

    @property
    def doc(self):
        return (
            _("The argument {description} has an invalid formatting!").format(
                description=f'({self.description})' if self.description else ''
            ),
            self.text,
        )


ARGS_EXCEPTIONS = (ArgTypeError, ArgIsRequiredError, ArgInListItemError, ArgCustomError, ArgSyntaxEntityError)


class TypeCheckCustomError(Exception):
    def __init__(self, text: str | LazyProxy):
        self.text = text
