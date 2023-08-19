from __future__ import annotations
from ..kind.keys_kind import KeyCodes
from .general import GeneralKeyCodes


class DrawKeyCodes(GeneralKeyCodes):
    """
    Some Draw Key Codes

    These key code only work if Draw main menu is active (visible).

    One way around this issue is to use :external+odev:py:meth:`ooodev.utils.gui.GUI.show_menu_bar`
    to ensure menu bar is visible.

    ::

        from ooodev.utils.gui import GUI
        GUI.show_memu_bar()

    See Also:
        :ref:`class_robot_keys`
    """

    TOGGLE_COLOR_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "c")}{KeyCodes.ESC}{KeyCodes.get_up_down(KeyCodes.ALT, "c")}{KeyCodes.ENTER}'
    """View > Color Bar"""
    TOGGLE_COMMENTS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "o")}'
    """View > Comments"""
    TOGGLE_DEVELOPER_TOOLS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "t", "v")}'
    """Tools > Developers Toolbar"""
    TOGGLE_GALLERY = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "G")}'
    """View > Gallery"""
    TOGGLE_NAVIGATOR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "v")}'
    """View > Navigator"""
    KB_NAVIGATOR = f"{KeyCodes.F5}"
    """Navigator via keyboard shortcut"""
    TOGGLE_PAGE_PANE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "p")}'
    """View > Page Pane"""
    TOGGLE_RULERS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "r")}'
    """View > Rulers > Rulers"""
    KB_RULERS = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "r")}'
    """Toggle Rulers via keyboard shortcut"""
    TOGGLE_SIDE_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "d")}'
    """View > Sidebar"""
    KB_SIDE_BAR = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F5)}"
    """Toggle Sidebar via keyboard shortcut"""
    TOGGLE_STATUS_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "B")}'
    """View > Status Bar"""
    TOGGLE_STYLES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "y")}'
    """View > Styles"""
    KB_STYLES = f"{KeyCodes.F11}"
    """Toggle Styles via keyboard shortcut"""
    VIEW_MASTER = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "M")}'
    """View > Master"""
    VIEW_NORMAL = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "N")}'
    """View Normal"""
