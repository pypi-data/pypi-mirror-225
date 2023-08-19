from __future__ import annotations
from enum import Enum, IntEnum
from typing import Sequence


class KeyDirection(IntEnum):
    NONE = 0
    UP = 1
    DOWN = 2


class KeyCodes(str, Enum):
    """Key Codes Constants"""

    # https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html
    BACK = "BACK"
    BACKSPACE = "BACKSPACE"
    BKSP = "BKSP"
    BREAK = "BREAK"
    BS = "BS"
    CAP = "CAP"
    CAPSLOCK = "CAPSLOCK"
    DEL = "DEL"
    DELETE = "DELETE"
    DOWN = "DOWN"
    END = "END"
    ENTER = "ENTER"
    ESC = "ESC"
    F1 = "F1"
    F10 = "F10"
    F11 = "F11"
    F12 = "F12"
    F13 = "F13"
    F14 = "F14"
    F15 = "F15"
    F16 = "F16"
    F17 = "F17"
    F18 = "F18"
    F19 = "F19"
    F2 = "F2"
    F20 = "F20"
    F21 = "F21"
    F22 = "F22"
    F23 = "F23"
    F24 = "F24"
    F3 = "F3"
    F4 = "F4"
    F5 = "F5"
    F6 = "F6"
    F7 = "F7"
    F8 = "F8"
    F9 = "F9"
    HELP = "HELP"
    HOME = "HOME"
    INS = "INS"
    INSERT = "INSERT"
    LEFT = "LEFT"
    LWIN = "LWIN"
    NUMLOCK = "NUMLOCK"
    PGDN = "PGDN"
    PGUP = "PGUP"
    PRTSC = "PRTSC"
    RIGHT = "RIGHT"
    RMENU = "RMENU"
    RWIN = "RWIN"
    SCROLLLOCK = "SCROLLLOCK"
    SPACE = "SPACE"
    TAB = "TAB"
    UP = "UP"
    VK_ACCEPT = "VK_ACCEPT"
    VK_ADD = "VK_ADD"
    VK_APPS = "VK_APPS"
    VK_ATTN = "VK_ATTN"
    VK_BACK = "VK_BACK"
    VK_CANCEL = "VK_CANCEL"
    VK_CAPITAL = "VK_CAPITAL"
    VK_CLEAR = "VK_CLEAR"
    VK_CONTROL = "VK_CONTROL"
    VK_CONVERT = "VK_CONVERT"
    VK_CRSEL = "VK_CRSEL"
    VK_DECIMAL = "VK_DECIMAL"
    VK_DELETE = "VK_DELETE"
    VK_DIVIDE = "VK_DIVIDE"
    VK_DOWN = "VK_DOWN"
    VK_END = "VK_END"
    VK_EREOF = "VK_EREOF"
    VK_ESCAPE = "VK_ESCAPE"
    VK_EXECUTE = "VK_EXECUTE"
    VK_EXSEL = "VK_EXSEL"
    VK_F1 = "VK_F1"
    VK_F10 = "VK_F10"
    VK_F11 = "VK_F11"
    VK_F12 = "VK_F12"
    VK_F13 = "VK_F13"
    VK_F14 = "VK_F14"
    VK_F15 = "VK_F15"
    VK_F16 = "VK_F16"
    VK_F17 = "VK_F17"
    VK_F18 = "VK_F18"
    VK_F19 = "VK_F19"
    VK_F2 = "VK_F2"
    VK_F20 = "VK_F20"
    VK_F21 = "VK_F21"
    VK_F22 = "VK_F22"
    VK_F23 = "VK_F23"
    VK_F24 = "VK_F24"
    VK_F3 = "VK_F3"
    VK_F4 = "VK_F4"
    VK_F5 = "VK_F5"
    VK_F6 = "VK_F6"
    VK_F7 = "VK_F7"
    VK_F8 = "VK_F8"
    VK_F9 = "VK_F9"
    VK_FINAL = "VK_FINAL"
    VK_HANGEUL = "VK_HANGEUL"
    VK_HANGUL = "VK_HANGUL"
    VK_HANJA = "VK_HANJA"
    VK_HELP = "VK_HELP"
    VK_HOME = "VK_HOME"
    VK_INSERT = "VK_INSERT"
    VK_JUNJA = "VK_JUNJA"
    VK_KANA = "VK_KANA"
    VK_KANJI = "VK_KANJI"
    VK_LBUTTON = "VK_LBUTTON"
    VK_LCONTROL = "VK_LCONTROL"
    VK_LEFT = "VK_LEFT"
    VK_LMENU = "VK_LMENU"
    VK_LSHIFT = "VK_LSHIFT"
    VK_LWIN = "VK_LWIN"
    VK_MBUTTON = "VK_MBUTTON"
    VK_MENU = "VK_MENU"
    VK_MODECHANGE = "VK_MODECHANGE"
    VK_MULTIPLY = "VK_MULTIPLY"
    VK_NEXT = "VK_NEXT"
    VK_NONAME = "VK_NONAME"
    VK_NONCONVERT = "VK_NONCONVERT"
    VK_NUMLOCK = "VK_NUMLOCK"
    VK_NUMPAD0 = "VK_NUMPAD0"
    VK_NUMPAD1 = "VK_NUMPAD1"
    VK_NUMPAD2 = "VK_NUMPAD2"
    VK_NUMPAD3 = "VK_NUMPAD3"
    VK_NUMPAD4 = "VK_NUMPAD4"
    VK_NUMPAD5 = "VK_NUMPAD5"
    VK_NUMPAD6 = "VK_NUMPAD6"
    VK_NUMPAD7 = "VK_NUMPAD7"
    VK_NUMPAD8 = "VK_NUMPAD8"
    VK_NUMPAD9 = "VK_NUMPAD9"
    VK_OEM_CLEAR = "VK_OEM_CLEAR"
    VK_PA1 = "VK_PA1"
    VK_PAUSE = "VK_PAUSE"
    VK_PLAY = "VK_PLAY"
    VK_PRINT = "VK_PRINT"
    VK_PRIOR = "VK_PRIOR"
    VK_PROCESSKEY = "VK_PROCESSKEY"
    VK_RBUTTON = "VK_RBUTTON"
    VK_RCONTROL = "VK_RCONTROL"
    VK_RETURN = "VK_RETURN"
    VK_RIGHT = "VK_RIGHT"
    VK_RMENU = "VK_RMENU"
    VK_RSHIFT = "VK_RSHIFT"
    VK_RWIN = "VK_RWIN"
    VK_SCROLL = "VK_SCROLL"
    VK_SELECT = "VK_SELECT"
    VK_SEPARATOR = "VK_SEPARATOR"
    VK_SHIFT = "VK_SHIFT"
    VK_SNAPSHOT = "VK_SNAPSHOT"
    VK_SPACE = "VK_SPACE"
    VK_SUBTRACT = "VK_SUBTRACT"
    VK_TAB = "VK_TAB"
    VK_UP = "VK_UP"
    ZOOM = "ZOOM"
    ALT = VK_MENU
    CTL = VK_CONTROL
    SHIFT = VK_SHIFT

    def __str__(self) -> str:
        return f"{{{self.value}}}"

    # @staticmethod
    # def get_key(code: KeyCodes, direction: KeyDirection = KeyDirection.NONE) -> str:
    #     if direction == KeyDirection.NONE:
    #         return str(code)
    #     d = "up" if direction == KeyDirection.UP else "down"
    #     return f"{{{code.value} {d}}}"

    @staticmethod
    def get_key(codes: KeyCodes | str | Sequence[KeyCodes], direction: KeyDirection = KeyDirection.NONE) -> str:
        """
        Gets a keyboard sequence from arguments.

        Args:
            codes (KeyCodes | str | Sequence[KeyCodes]): Key code such as ``KeyCodes.F5`` or ``r`` or ``KeyCodes.ALT``
            direction (KeyDirection, optional): Key Direction. Defaults to ``KeyDirection.NONE``.

        Returns:
            str: Representing Keyboard enulation such as ``{F5}`` or ``{r}`` or ``{VK_MENU down}``
        """
        # get multiple code such as Ctl+Alt+Shift

        def get_a_key(code: KeyCodes | str, direction: KeyDirection = KeyDirection.NONE) -> str:
            if direction == KeyDirection.NONE:
                return str(code)
            d = "up" if direction == KeyDirection.UP else "down"
            return f"{{{code.value} {d}}}"

        if isinstance(codes, (str, KeyCodes)):
            return get_a_key(code=codes, direction=direction)
        lst = []
        for code in codes:
            lst.append(get_a_key(code=code, direction=direction))
        return "".join(lst)

    @staticmethod
    def get_up_down(codes: KeyCodes | str | Sequence[KeyCodes], key: str | KeyCodes, repeat: int = 1) -> str:
        """
        Gets a keyboard sequence from arguments that containd press (donw) and release (up) commands.

        Args:
            codes (KeyCodes | str | Sequence[KeyCodes]): Press and release command(s)
            key (str | KeyCodes): Key to wrap in press and release command
            repeat (int, optional): Number of times to repead commands. Useful when repeated command is needed such as ``ALT+v, ALT+v``. Defaults to 1.

        Returns:
            str: ``key`` wraped in updown commands.

        Example:

            .. code-block:: python

                >>> str_cmd = KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "j")
                >>> print(str_cmd)
                 '{VK_CONTROL down}{VK_SHIFT down}j{VK_CONTROL up}{VK_SHIFT up}'
        """
        result = f"{KeyCodes.get_key(codes, KeyDirection.DOWN)}{key}{KeyCodes.get_key(codes, KeyDirection.UP)}"
        if repeat <= 1:
            return result
        return result * repeat

    @staticmethod
    def get_many_keys(codes: KeyCodes | Sequence[KeyCodes], *keys: str | KeyCodes) -> str:
        """
        Gets keyboard sequence for mulitple keys at onece.

        Args:
            codes (KeyCodes | Sequence[KeyCodes]): Press and release commands
            *keys: Optional Expanded list of keys to wrape in Press and Release commands

        Returns:
            str: Sequenece of keyboard commands

        Example:

            .. code-block:: python

                >>> str_cmd = KeyCodes.get_many_keys(KeyCodes.ALT, "v", "c", "r")
                >>> print(str_cmd)
                 '{VK_MENU down}v{VK_MENU up}{VK_MENU down}c{VK_MENU up}{VK_MENU down}r{VK_MENU up}'
        """
        lst = []
        for key in keys:
            lst.append(f"{KeyCodes.get_key(codes, KeyDirection.DOWN)}{key}{KeyCodes.get_key(codes, KeyDirection.UP)}")
        return "".join(lst)
