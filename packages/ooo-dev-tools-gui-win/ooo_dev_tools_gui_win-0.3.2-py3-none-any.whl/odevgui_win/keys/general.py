from __future__ import annotations
from ..kind.keys_kind import KeyCodes


class GeneralKeyCodes:
    """
    Some Writer Key Codes

    These key code only work if main menu is active (visible).

    One way around this issue is to use :external+odev:py:meth:`ooodev.utils.gui.GUI.show_menu_bar`
    to ensure menu bar is visible.

    ::

        from ooodev.utils.gui import GUI
        GUI.show_memu_bar()
    """

    KB_SELECT_ALL = f'{KeyCodes.get_up_down(KeyCodes.CTL, "A")}'
    """Select All via keyboard shortcut"""
    KB_UNDO = f'{KeyCodes.get_up_down(KeyCodes.CTL, "Z")}'
    """Undo via keyboard shortcut"""
    KB_REDO = f'{KeyCodes.get_up_down(KeyCodes.CTL, "Y")}'
    """Redo via keyboard shortcut"""
    KB_COPY = f'{KeyCodes.get_up_down(KeyCodes.CTL, "C")}'
    """Copy via keyboard shortcut"""
    KB_CUT = f'{KeyCodes.get_up_down(KeyCodes.CTL, "X")}'
    """Cut via keyboard shortcut"""
    KB_PASTE = f'{KeyCodes.get_up_down(KeyCodes.CTL, "V")}'
    """Paste via keyboard shortcut"""
    KB_PASTE_UNFORMATTED_TEXT = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.ALT, KeyCodes.SHIFT), "V")}'
    """Paste Unformatted Text via keyboard shortcut"""
    KB_BOLD = f'{KeyCodes.get_up_down(KeyCodes.CTL, "B")}'
    """Format Bold via keyboard shortcut"""
    KB_ITALIC = f'{KeyCodes.get_up_down(KeyCodes.CTL, "I")}'
    """Format Italic via keyboard shortcut"""
    KB_UNDERLINE = f'{KeyCodes.get_up_down(KeyCodes.CTL, "U")}'
    """Format Underline via keyboard shortcut"""
    KB_CLEAR_DIRECT = f'{KeyCodes.get_up_down(KeyCodes.CTL, "M")}'
    """Format Clear Direct via keyboard shortcut"""
    KB_ALIGN_LEFT = f'{KeyCodes.get_up_down(KeyCodes.CTL, "L")}'
    """Align Text Left via keyboard shortcut"""
    KB_ALIGN_RIGHT = f'{KeyCodes.get_up_down(KeyCodes.CTL, "R")}'
    """Align Text Right via keyboard shortcut"""
    KB_ALIGN_CENTER = f'{KeyCodes.get_up_down(KeyCodes.CTL, "E")}'
    """Align Text Center via keyboard shortcut"""
    KB_ALIGN_JUSTIFIED = f'{KeyCodes.get_up_down(KeyCodes.CTL, "J")}'
    """Align Text Justified via keyboard shortcut"""
    KB_PRINT = f'{KeyCodes.get_up_down(KeyCodes.CTL, "P")}'
    """Print via keyboard shortcut"""
    KB_PRINT_PREVIEW = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "O")}'
    """Print Preview via keyboard shortcut"""
    KB_EXIT = f'{KeyCodes.get_up_down(KeyCodes.CTL, "Q")}'
    """Exit via keyboard shortcut"""
    KB_SAVE = f'{KeyCodes.get_up_down(KeyCodes.CTL, "S")}'
    """Save via keyboard shortcut"""
