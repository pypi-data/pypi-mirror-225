from typing import Any, Awaitable, Callable, Dict, Optional, List

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.filters import CommandObject
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import I18n
from stfu_tg import Section, Underline, Strikethrough

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ARGS_EXCEPTIONS, ArgError
from ass_tg.i18n import gettext as _
from ass_tg.i18n import gettext_ctx
from ass_tg.types import CutCommandEntitiesArg, AndArg
from ass_tg.types.base_abc import ArgFabric


class ArgsMiddleware(BaseMiddleware):
    i18n: I18n

    def __init__(
            self,
            error_additional_items=(),
            error_markup_buttons: Optional[List[List[InlineKeyboardButton]]] = None,
            i18n: Optional[I18n] = None
    ):
        super().__init__()
        self.i18n = i18n or I18n(path='/')
        self.error_additional_items = error_additional_items
        self.error_markup_buttons = error_markup_buttons

    @staticmethod
    def _extract_command_prefix(command: Optional[CommandObject]) -> str:
        if not command:
            return ''
        command_prefix = '!' if command.prefix == '/' else command.prefix
        return f'{command_prefix}{command.command} '

    @staticmethod
    def _extract_prefix(raw_text: str, error: ArgError) -> str:
        prefix = raw_text[:error.offset] if error.offset else raw_text
        if len(prefix) > 15:
            prefix = f'... {prefix[-15:]}'
        return prefix

    @staticmethod
    def _extract_error(raw_text: str, error: ArgError) -> str:
        if error.error_placeholder:
            # Here we want to use a placeholder instead of the error.
            error_text = error.error_placeholder[:error.length or 0]
        else:
            cut_from = error.offset
            cut_to = error.offset + (error.length or 0)

            error_text = raw_text[cut_from:cut_to]
        if len(error_text) > 25:
            error_text = f'.. {error_text[25:]} ..'

        return str(Strikethrough(error_text) if error.strikethrough else Underline(error_text))

    @staticmethod
    def _extract_postfix(raw_text: str, error: ArgError):
        error_length = 0 if error.error_placeholder else error.length

        postfix = ''

        if error.error_postfix:
            postfix += error.error_postfix

        postfix += raw_text[error.offset + (error_length or 0):]

        if len(postfix) > 15:
            postfix = f'{postfix[:15]} ...'
        return postfix

    def highlight_failed_argument(
            self,
            error: ArgError,
            command: Optional[CommandObject],
            raw_text: str
    ) -> str:
        text = self._extract_command_prefix(command)

        if error.offset > 0:
            text += self._extract_prefix(raw_text, error)

        if error.length:
            text += self._extract_error(raw_text, error)
            text += self._extract_postfix(raw_text, error)

        text += str(Underline(error.add_after))

        # Here we use HTML as STFU will try to escape its own formatting in further steps
        return f'<i>{text}</i>'

    async def send_error(self, message: Message, error: ArgError, command: Optional[CommandObject]) -> None:
        raw_text = (command.args if command else message.text) or ''

        doc = Section(
            self.highlight_failed_argument(error, command, raw_text),
            ' ',
            *error.doc,
            *self.error_additional_items,
            title=_('⚠️ Argument validation error'),
            title_underline=False,
        )

        await message.reply(
            str(doc),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=self.error_markup_buttons)
            if self.error_markup_buttons else None,
            disable_web_page_preview=True
        )

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:

        if base_arg := get_flag(data, "args"):
            if isinstance(base_arg, dict):
                base_arg = CutCommandEntitiesArg(AndArg(**base_arg))
            elif not isinstance(base_arg, ArgFabric):
                raise ValueError

            command: Optional[CommandObject] = data.get('command')

            text = (command.args or '') if command else ''
            with self.i18n.context():
                gettext_ctx.set(self.i18n)
                try:
                    arg = base_arg(text, 0, ArgEntities(message.entities or []), command=command)
                    data['arg'] = arg

                    # Expose argument values as our new simplified way
                    for arg_name, arg_data in arg.value.items():
                        data[arg_name] = arg_data.get_value()
                except ARGS_EXCEPTIONS as e:
                    await self.send_error(message, e, command)
                    return

        return await handler(message, data)
