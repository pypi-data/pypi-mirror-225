from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, overload
from ..kind.keys_kind import KeyCodes as KeyCodes, KeyDirection as KeyDirection


@dataclass(frozen=True)
class SendKeyInfo:
    """Window Title Info"""

    keys: str
    """Keys to send"""

    def __str__(self) -> str:
        return self.keys

    @staticmethod
    def from_keys(codes: Sequence[KeyCodes], *keys: str | KeyCodes) -> SendKeyInfo:
        """
        Gets a ``SendKeyInfo`` instance

        Args:
            codes (Sequence[KeyCodes]): codes to set

        Returns:
            SendKeyInfo: New Instance

        Example:
            The following example demonstrates thoe to set keys to send ``Alt+o``, ``Alt+x``, ``Alt+c``

            .. code-block:: python

                >>> key_info = SendKeyInfo.from_keys((KeyCodes.SHIFT, KeyCodes.CTL), "o", "x", "c")
                >>> print(key_info.keys)
                {VK_SHIFT down}{VK_CONTROL down}o{VK_SHIFT up}{VK_CONTROL up}{VK_SHIFT down}{VK_CONTROL down}x{VK_SHIFT up}{VK_CONTROL up}{VK_SHIFT down}{VK_CONTROL down}c{VK_SHIFT up}{VK_CONTROL up}
        """
        return SendKeyInfo(KeyCodes.get_many_keys(codes, *keys))

    @staticmethod
    def from_key(codes: KeyCodes, *keys: str | KeyCodes) -> SendKeyInfo:
        """
        Gets a ``SendKeyInfo`` instance

        Args:
            codes (KeyCodes): code or codes to set

        Returns:
            SendKeyInfo: New Instance

        Example:
            The following example demonstrates thoe to set keys to send ``Alt+o``, ``Alt+x``, ``Alt+c``

            .. code-block:: python

                >>> key_info = SendKeyInfo.from_keys(KeyCodes.ALT, "o", "x", "c")
                >>> print(key_info.keys)
                {VK_MENU down}o{VK_MENU up}{VK_MENU down}x{VK_MENU up}{VK_MENU down}c{VK_MENU up}
        """
        return SendKeyInfo(KeyCodes.get_many_keys(codes, *keys))

    @staticmethod
    def from_code(code: KeyCodes) -> SendKeyInfo:
        """
        Gets a ``SendKeyInfo`` instance

        Args:
            code (KeyCodes): code used to create instance

        Returns:
            SendKeyInfo: New Instance

        Example:
            The following example demonstrates toggling Cap Lock

            .. code-block:: python

                >>> key_info = SendKeyInfo.from_code(KeyCodes.CAPSLOCK)
                >>> print(key_info.keys)
                {CAPSLOCK}
        """
        return SendKeyInfo(str(code))

    @overload
    @staticmethod
    def from_code_str(code: KeyCodes, key: str | KeyCodes) -> SendKeyInfo:
        ...

    @overload
    @staticmethod
    def from_code_str(code: KeyCodes, key: str | KeyCodes, repeat: int) -> SendKeyInfo:
        ...

    @staticmethod
    def from_code_str(code: KeyCodes, key: str | KeyCodes, repeat: int = 1) -> SendKeyInfo:
        """
        Gets a ``SendKeyInfo`` instance

        Args:
            code (KeyCodes): code such as ``KeyCodes.ALT``
            key (str | KeyCodes): Key such as ``s``
            repeat (int, optional): Number of times to repeat the sequence. Defaults to 1.

        Returns:
            SendKeyInfo: New Instance

        Example:
            The following example demonstrates setting to ``Alt+s``

            .. code-block:: python

                >>> key_info = SendKeyInfo.from_code_str(KeyCodes.ALT, "s")
                >>> print(key_info.keys)
                {VK_MENU down}s{VK_MENU up}
        """
        result = KeyCodes.get_up_down(codes=code, key=key, repeat=repeat)
        return SendKeyInfo(result)

    @overload
    @staticmethod
    def from_code_sequence_str(codes: Sequence[KeyCodes], key: str | KeyCodes) -> SendKeyInfo:
        ...

    @overload
    @staticmethod
    def from_code_sequence_str(codes: Sequence[KeyCodes], key: str | KeyCodes, repeat: int) -> SendKeyInfo:
        ...

    @staticmethod
    def from_code_sequence_str(codes: Sequence[KeyCodes], key: str | KeyCodes, repeat: int = 1) -> SendKeyInfo:
        """
        Gets a ``SendKeyInfo`` instance

        Args:
            codes (Sequence[KeyCodes]): Sequence of codes
            key (str | KeyCodes): Key such as ``t``
            repeat (int, optional):  Number of times to repeat the sequence. Defaults to 1.

        Returns:
            SendKeyInfo: New Instance

        Example:
            The following example demonstrates setting to ``Alt+s``

            .. code-block:: python

                >>> key_info = SendKeyInfo.from_code_sequence_str((KeyCodes.SHIFT, KeyCodes.ALT), "t")
                >>> print(key_info.keys)
                {VK_SHIFT down}{VK_MENU down}t{VK_SHIFT up}{VK_MENU up}
        """
        result = KeyCodes.get_up_down(codes=codes, key=key, repeat=repeat)
        return SendKeyInfo(result)
