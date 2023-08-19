from typing import Tuple, Dict

from aiogram.utils.text_decorations import html_decoration
from babel.support import LazyProxy

from ass_tg.entities import ArgEntities
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.base_abc import ArgFabric


class TextArg(ArgFabric):

    def __init__(self, *args, parse_entities: bool = False):
        super().__init__(*args)
        self.parse_entities = parse_entities

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Text"), l_("Text")

    @staticmethod
    def check(text: str, entities: ArgEntities) -> bool:
        return text != ""

    def parse(self, text: str, offset: int, entities: ArgEntities) -> Tuple[int, str]:
        length = len(text)

        if self.parse_entities:
            text = html_decoration.unparse(text, entities)

        return length, text

    @property
    def examples(self) -> Dict[str, None]:
        return {
            'Foo': None,
            'Foo Bar': None
        }

    def unparse(
            self,
            data: str,
            **kwargs
    ) -> str:
        return data
