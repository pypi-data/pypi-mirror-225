from typing import Tuple, Dict, Optional

from aiogram.types import User
from babel.support import LazyProxy
from stfu_tg import UserLink
from stfu_tg.formatting import StyleFormationCore

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgTypeError, TypeCheckCustomError, ArgCustomError
from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types import WordArg, OrArg
from ass_tg.types.base_abc import ArgFabric


class UserIDArg(WordArg):
    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("User ID (Numeric)"), l_("User IDs (Numeric)")

    def value(self, text: str) -> int:
        return int(text.split()[0])

    def check_type(self, text: str) -> bool:
        return bool(text) and text.split()[0].isdigit()

    @property
    def examples(self) -> Dict[str, None]:
        return {
            '1234567890': None,
            '33334856': None
        }


class UsernameArg(WordArg):
    prefix = '@'

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Username (starts with @)"), l_("Username (starts with @)")

    def value(self, text: str) -> str:
        return text.split()[0].removeprefix(self.prefix)

    def check_type(self, text: str) -> bool:
        if not text:
            return False

        if not text.startswith(self.prefix):
            raise TypeCheckCustomError(_("Should start with a prefix"))
        if len(text) < 2:
            raise TypeCheckCustomError(_("Username is too short"))
        if len(text) > 32:
            raise TypeCheckCustomError(_("Username is too long"))

        return True

    @property
    def examples(self) -> Dict[str, None]:
        return {
            '@username': None,
            '@ofoxr_bot': None
        }


class UserMentionArg(ArgFabric):
    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("User mention (a link to user)"), l_("User mentions (links to users)")

    @property
    def examples(self) -> dict[str | StyleFormationCore, Optional[LazyProxy]]:
        return {
            UserLink(
                user_id=1111224224,
                name="OrangeFox BOT",
                link=''
            ): None
        }

    @staticmethod
    def check(text: str, entities: ArgEntities) -> bool:
        # It would be nice to check an offset here, but we don't pass it in check()
        return any(x.type == 'mention' for x in entities)

    def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> Tuple[int, User]:
        # Check
        mention_entities = [
            x for x in entities if x.type == 'mention' and x.user and x.offset == offset
        ]

        if not mention_entities:
            raise ArgTypeError(
                needed_type=self.needed_type,
                description=self.description,
                length=len(text),
                offset=offset,
                text=_("Should start with mention!"),
                examples=self.examples
            )

        mention = mention_entities[0]

        if not mention.user:
            raise ArgCustomError(
                _("Unexpected error while trying to get a user! Please report this in the support chat!"),
                _("Error ID: 95450")
            )

        return mention.length, mention.user


class UserArg(OrArg):
    def __init__(self, *args):
        super().__init__(UserMentionArg(), UserIDArg(), UsernameArg(), *args)

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_(
            "User: 'User ID (numeric) / Username (starts with @) / Mention (links to users)'"
        ), l_(
            "Users: 'User IDs (numeric) / Usernames (starts with @) / Mentions (links to users)'"
        )

    @property
    def examples(self) -> Dict[str | StyleFormationCore, LazyProxy]:
        return {
            '1111224224': l_("User ID"),
            '@ofoxr_bot': l_("Username"),
            UserLink(
                user_id=1111224224,
                name="OrangeFox BOT",
                link=''
            ): l_(
                "A link to user, usually creates by mentioning a user without username."
            )
        }
