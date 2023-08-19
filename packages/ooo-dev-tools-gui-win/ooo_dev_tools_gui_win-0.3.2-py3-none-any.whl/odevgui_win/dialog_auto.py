from __future__ import annotations
import threading
import time
from typing import overload
import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from ooodev.utils.data_type.dialog_title import DialogTitle as DialogTitle
from .kind.keys_kind import KeyCodes
from .class_args.send_key_info import SendKeyInfo as SendKeyInfo

# Confirmation
# ahk_class SALSUBFRAME
# ahk_exe soffice.bin


class DialogAuto:
    """Dialog Automation"""

    @overload
    @staticmethod
    def monitor_dialog(send_key: str) -> None:
        ...

    @overload
    @staticmethod
    def monitor_dialog(send_key: str, title_info: DialogTitle) -> None:
        ...

    @overload
    @staticmethod
    def monitor_dialog(send_key: SendKeyInfo) -> None:
        ...

    @overload
    @staticmethod
    def monitor_dialog(send_key: SendKeyInfo, title_info: DialogTitle) -> None:
        ...

    @staticmethod
    def monitor_dialog(send_key: str | SendKeyInfo, title_info: DialogTitle | None = None) -> None:
        """
        Monitors for a dialog and press the button via its short cut keys such as ``alt+y``.

        Args:
            send_key (str | SendKeyInfo): The key for the alt shortcut such as ``y`` or ``n`` or ``c``
            title_info (DialogTitle, Optional): Dialog Title info

        Returns:
            None:

        Note:
            If ``send_key`` is a string then it is sent as with ``ALT``
            ``send_key=c`` results on ``ALT+c`` being sent to dialog.

            If ``send_key`` is :py:class:`~.class_args.send_key_info.SendKeyInfo` then its values is sent to dialog verbatim.
        """
        if title_info is None:
            title_info = DialogTitle("Confirmation")
        if isinstance(send_key, str):
            key_code = f"{KeyCodes.get_up_down(KeyCodes.ALT, send_key)}"
        else:
            key_code = send_key.keys
        # start thread
        x = threading.Thread(target=DialogAuto._confirmation, args=(key_code, title_info), daemon=True)
        x.start()

    @staticmethod
    def _confirmation(key: str, title_info: DialogTitle) -> None:
        # connects to a LibreOffice Dialog such as a Confirmaton dialog.
        d_args = {"class_name": title_info.class_name}
        if title_info.is_regex:
            d_args["title_re"] = title_info.title
        else:
            d_args["title"] = title_info.title
        while 1:
            try:
                _ = Application().connect(**d_args)
            except pywinauto.ElementNotFoundError:
                pass
            else:
                send_keys(key)
            time.sleep(0.7)
