from __future__ import annotations
from typing import List, overload
import time

import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

from ooodev.utils.data_type.window_title import WindowTitle as WindowTitle

from .class_args.send_key_info import SendKeyInfo as SendKeyInfo
from .focus import Focus
from .exceptions import ElementNotFoundError


class RobotKeys:
    """Robot Keys"""

    @staticmethod
    def send_current(key: SendKeyInfo) -> None:
        """
        Sends key to the current LibreOffice window.
        Assumes window was created with :external+odev:py:meth:`ooodev.utils.lo.Lo.load_office`.

        Args:
            key (SendKeyInfo): Keys to emulate

        Raises:
            ElementNotFoundError: If unable to find and focus window.

        Returns:
            None:

        Note:
            There are many include keyboard shortcuts for LibreOffice included in this package.

            .. cssclass:: ul-list

                * :py:class:`~.calc_key_codes.CalcKeyCodes`
                * :py:class:`~.draw_key_codes.DrawKeyCodes`
                * :py:class:`~.impress_key_codes.ImpressKeyCodes`
                * :py:class:`~.writer_key_codes.WriterKeyCodes`
        """
        win = Focus.focus_current()

        if not win:
            raise ElementNotFoundError()

        send_keys(key.keys)

    @overload
    @staticmethod
    def send(key: SendKeyInfo) -> None:
        ...

    @overload
    @staticmethod
    def send(key: SendKeyInfo, *titles: WindowTitle) -> None:
        ...

    @staticmethod
    def send(key: SendKeyInfo, *titles: WindowTitle) -> None:
        """
        Emulates typing keys with keyboard.

        If titles are include then the first matching title will have keys sent to it.

        Args:
            key (SendKeyInfo): Keys to emulate
            *titles: Optonal expandable list of :external+odev:py:class:`ooodev.utils.data_type.window_title.WindowTitle`

        Raises:
            ElementNotFoundError: If titles are include but no title is matched.

        Returns:
            None:

        Note:
            There are many include keyboard shortcuts for LibreOffice included in this package.

            .. cssclass:: ul-list

                * :py:class:`~.calc_key_codes.CalcKeyCodes`
                * :py:class:`~.draw_key_codes.DrawKeyCodes`
                * :py:class:`~.impress_key_codes.ImpressKeyCodes`
                * :py:class:`~.writer_key_codes.WriterKeyCodes`
        """
        lst_titles: List[WindowTitle] = list(titles)
        if len(lst_titles) > 0:
            app = None
            title_arg = None
            for title in lst_titles:
                d_args = {"class_name": title.class_name}
                if title.is_regex:
                    d_args["title_re"] = title.title
                else:
                    d_args["title"] = title.title
                try:
                    app = Application().connect(**d_args)
                    title_arg = title
                    if app:
                        break
                except pywinauto.ElementNotFoundError:
                    app = None
            if app is None:
                raise pywinauto.ElementNotFoundError()
            if title_arg.is_regex:
                win = app.window(title_re=title_arg.title)
            else:
                win = app.window(title=title_arg.title)
            if app is None:
                raise pywinauto.ElementNotFoundError()
            if title_arg.is_regex:
                win = app.window(title_re=title_arg.title)
            else:
                win = app.window(title=title_arg.title)
            win.set_focus()
            time.sleep(0.5)
        send_keys(key.keys)
