import datetime
import re
from typing import Tuple, Dict

from babel.support import LazyProxy

from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.oneword import WordArg

ACTION_TIME_REGEX = re.compile(r"(\d+[ywdhm])")
ACTION_TIME_CHECK_REGEX = re.compile(r"^(\d+[ywdhm])+$")


class ActionTimeArg(WordArg):
    know_the_end = True

    def check_type(self, text: str) -> bool:
        return text != "" and text[0].isdigit() and bool(ACTION_TIME_CHECK_REGEX.match(text))

    @property
    def examples(self) -> Dict[str, LazyProxy]:
        return {
            '2d': l_('2 days'),
            '3w2d': l_('3 weeks and 2 days')
        }

    @staticmethod
    def parse_string(text: str) -> int:

        minutes = 0

        for item in ACTION_TIME_REGEX.findall(text):
            last_charter = item[-1]

            num = item.removesuffix(last_charter).strip()
            if not num.isdigit():
                raise ValueError("Not digit")

            # NOTE: Please use the first letter of the "years" in your language
            if last_charter in {"y", _('y')}:
                minutes += int(item[:-1]) * 60 * 24 * 365
            # NOTE: Please use the first letter of the "weeks" in your language
            elif last_charter in {"w", _('w')}:
                minutes += int(item[:-1]) * 60 * 24 * 7
            # NOTE: Please use the first letter of the "days" in your language
            elif last_charter in {"d", _('d')}:
                minutes += int(item[:-1]) * 60 * 24
            # NOTE: Please use the first letter of the "hours" in your language
            elif last_charter in {"h", _('h')}:
                minutes += int(item[:-1]) * 60
            # NOTE: Please use the first letter of the "minutes" in your language
            elif last_charter in {"m", _('m')}:
                minutes += int(item[:-1])
            else:
                raise ValueError("Unknown time unit")

        return minutes

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Action time"), l_("Action times")

    def value(self, text: str) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.parse_string(text))
