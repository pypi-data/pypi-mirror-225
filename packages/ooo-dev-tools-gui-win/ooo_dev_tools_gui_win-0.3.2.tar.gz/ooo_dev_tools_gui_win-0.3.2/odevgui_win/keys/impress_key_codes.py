from __future__ import annotations
from ..kind.keys_kind import KeyCodes
from .general import GeneralKeyCodes


class ImpressKeyCodes(GeneralKeyCodes):
    """
    Some Impress Key Codes

    These key code only work if Impress main menu is active (visible).

    One way around this issue is to use :external+odev:py:meth:`ooodev.utils.gui.GUI.show_menu_bar`
    to ensure menu bar is visible.

    ::

        from ooodev.utils.gui import GUI
        GUI.show_memu_bar()

    See Also:
        :ref:`class_robot_keys`
    """

    # alt+v, alt=c, esc, alt+c, enter
    START_SLIDE_SHOW = f"{KeyCodes.F5}"
    """Slide Show > Start From First Slide"""
    START_SLIDE_SHOW_FROM_CURRENT = f"{KeyCodes.get_up_down(KeyCodes.SHIFT, KeyCodes.F5)}"
    """Slide Show > Start From Current Slide"""
    TOGGLE_COLOR_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "c")}{KeyCodes.ESC}{KeyCodes.get_up_down(KeyCodes.ALT, "c")}{KeyCodes.ENTER}'
    """View > Color Bar"""
    TOGGLE_STYLES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "y")}'
    """View > Styles"""
    KB_STYLES = f"{KeyCodes.F11}"
    """Toggle Styles via keyboard shortcut"""
    TOGGLE_NAVIGATOR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "v")}'
    """View > Navigator"""
    KB_NAVIGATOR = f"{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), KeyCodes.F5)}"
    """Navigator via keyboard shortcut"""
    TOGGLE_SLIDE_LAYOUT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "L")}{KeyCodes.ENTER}'
    """View > Slide Layout"""
    TOGGLE_STATUS_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "b")}{KeyCodes.ENTER}'
    """View > Status Bar"""
    TOGGLE_RULERS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "r")}'
    """View > Rulers > Rulers"""
    KB_RULERS = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "r")}'
    """Toggle Rulers via keyboard shortcut"""
    KB_SIDE_BAR = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F5)}"
    """Toggle Sidebar via keyboard shortcut"""
    TOGGLE_SLIDE_PANE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "p")}{KeyCodes.ENTER}'
    """View > Slide Pane"""
    TOGGLE_DEVELOPER_TOOLS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "t", "v")}'
    """Tools > Developers Toolbar"""
    TOGGLE_VIEWS_TAB_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "b", "b")}{KeyCodes.ENTER}'
    """View > Views Tab Bar"""
    VIEW_NORMAL = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "N")}'
    """View > Normal"""
    VIEW_OUTLINE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "o")}'
    """View > Outline"""
    VIEW_NOTES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "e")}'
    """View > Notes"""
    VIEW_SLIDE_SORTER = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "d")}'
    """View > Slide Sorter"""
    VIEW_MASTER_SLIDE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "M")}'
    """View > Master Slide"""
    VIEW_MASTER_NOTES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "a")}'
    """View > Master Notes"""
    VIEW_MASTER_HANDOUT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "u")}'
    """View > Master Handout"""

    def __str__(self) -> str:
        return f"{self.value}"
