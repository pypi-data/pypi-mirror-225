from __future__ import annotations
from ..kind.keys_kind import KeyCodes
from .general import GeneralKeyCodes


class WriterKeyCodes(GeneralKeyCodes):
    """
    Some Writer Key Codes

    These key code only work if Writer main menu is active (visible).

    One way around this issue is to use :external+odev:py:meth:`ooodev.utils.gui.GUI.show_menu_bar`
    to ensure menu bar is visible.

    ::

        from ooodev.utils.gui import GUI
        GUI.show_memu_bar()

    See Also:
        :ref:`class_robot_keys`
    """

    FILE_PREVIEW_BROWSER = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "f", "b")}'
    """File > Preview in web broswer"""
    FORMAT_CAP_EVERY_WORD = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "c")}'
    """Format > Text > Captalizie every word"""
    FORMAT_CYCLE_CASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "y")}'
    """Format > Text Cycle Case"""
    KB_CYCLE_CASE = f"{KeyCodes.get_many_keys(KeyCodes.SHIFT, KeyCodes.F3)}"
    """Text Cycle Case via keyboard shortcut"""
    FORMAT_DECREASE_SIZE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "e")}'
    """Format > Text > Decrease Size"""
    KB_DECREASE_SIZE = f'{KeyCodes.get_up_down(KeyCodes.CTL, "[")}'
    """Decrease Size via keyboard shortcut"""
    FORMAT_DOUBLE_UNDERLINE = f'{KeyCodes.get_up_down(KeyCodes.CTL, "D")}'
    """Format > Text > Double Underline"""
    FORMAT_INCREASE_SIZE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "z")}'
    """Format > Text > Increase Size"""
    KB_INCREASE_SIZE = f'{KeyCodes.get_up_down(KeyCodes.CTL, "]")}'
    """Increase Size via keyboard shortcut"""
    FORMAT_LOWERCASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "l")}'
    """Format > Text > lowercase"""
    FORMAT_OUTLINE_FONT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "f")}'
    """Format > Text > Outline Font Effect"""
    FORMAT_OVERLINE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "v")}'
    """Format > Text > Overline"""
    FORMAT_STRIKE_THROUGH = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "o")}'
    """Format > Text >Strickthrough"""
    FORMAT_SENTENCE_CASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "s")}'
    """Format > Text > Sentence Case"""
    FORMAT_SHADOW = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "w")}'
    """Format > Text > Shadow"""
    FORMAT_SINGLE_UNDERLINE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "g")}'
    """Format > Text > Single Underline"""
    FORMAT_SMALL_CAPS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "m")}'
    """Format > Text Small Caps"""
    KB_SMALL_CAPS = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "K")}'
    """Text Small Caps via keyboard shortcut"""
    FORMAT_SUBSCRIPT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "r")}'
    """Format > Text > Subscript"""
    KB_SUBSCRIPT = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "b")}'
    """Subscript via keyboard shortcut"""
    FORMAT_SUPERSCRIPT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "p")}'
    """Format > Text > Superscript"""
    KB_SUPERSCRIPT = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "p")}'
    """Superscript via keyboard shortcut"""
    FORMAT_TOGGLE_CASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "t")}'
    """Format > Text > tOGGLE cASE"""
    FORMAT_UPPERCASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "u")}'
    """format > Text > UPPERCASE"""
    STYLE_DEFAULT_CHAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "c")}'
    """Style > Default Character"""
    STYLES_EMPHASIS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "m")}'
    """Style > Emphasis"""
    STYLES_EMPHASIS_STRONG = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "s")}'
    """Style > Strong Enphasis"""
    STYLES_HEADING1 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "1")}'
    """Sytye > Headding 1"""
    KB_HEADING1 = f'{KeyCodes.get_up_down(KeyCodes.CTL, "1")}'
    """Headding 1 via keyboard shortcut"""
    STYLES_HEADING2 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "2")}'
    """Sytye > Headding 2"""
    KB_HEADING2 = f'{KeyCodes.get_up_down(KeyCodes.CTL, "2")}'
    """Headding 2 via keyboard shortcut"""
    STYLES_HEADING3 = f'{KeyCodes.get_up_down(KeyCodes.CTL, "3")}'
    """Sytye > Headding 3"""
    KB_HEADING3 = f'{KeyCodes.get_up_down(KeyCodes.CTL, "3")}'
    """Headding 3 via keyoard shortcut"""
    STYLES_NO_LIST = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "i")}'
    """Style > No List"""
    KB_NO_LIST = f"{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT),KeyCodes.F12)}"
    """No List via keyboard shortcut"""
    STYLES_PRE_FORMATTED = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "f")}'
    """Style > Preformatted Text"""
    STYLES_QUOTATION = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "o")}'
    """Style > Quotation"""
    STYLES_QUOTATIONS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "q")}'
    """Style > Quotations"""
    STYLES_SOURCE_TEXT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "r")}'
    """Style > Source Text"""
    STYLES_SUBTITLE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "b")}'
    """Style > Subtitle"""
    STYLES_TEXT_BODY = f'{KeyCodes.get_up_down(KeyCodes.CTL, "0")}'
    """Style > Text Body"""
    STYLES_TITLE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "t")}'
    """Style > Title"""
    TOGGLE_DEVELOPER_TOOLS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "t", "v")}'
    """Tools > Developers Toolbar"""
    TOGGLE_DATA_SOURCES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "d")}'
    """View > Data Sources"""
    KB_DATA_SOURCES = f"{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), KeyCodes.F4)}"
    """Data Sources via keyboard shortcut"""
    TOGGLE_FIELD_HIDDEN_PARA = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "h")}'
    """View > Field Hiddend Paragraphs"""
    TOGGLE_FIELD_NAMES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "f")}'
    """View > Field Names"""
    KB_FIELD_NAMES = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F8)}"
    """Field Names via keyboard shortcut"""
    TOGGLE_FIELD_SHADINGS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "l")}'
    """View > Field Shadings"""
    KB_FIELD_SHADINGS = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F8)}"
    """Field Shadings via keyboard shortcut"""
    TOGGLE_FORMATTING_MARKS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "m")}'
    """View > Formatting Marks"""
    KB_FORMATTING_MARKS = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F10)}"
    """Formatting Marks via keyboard shortcut"""
    TOGGLE_FULL_SCREEN = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "u")}'
    """View > Full Screen"""
    KB_FULL_SCREEN = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "j")}'
    """Full Screen via keyboard shortcut"""
    TOGGLE_GALLERY = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "G")}'
    """View > Gallery"""
    TOGGLE_HORIZONTIAL_SCROLLBAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "s", "h")}'
    """View > Scrollbars > Horizontal Scroll bar"""
    TOGGLE_IMAGES_CHARTS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "i", "i")}{KeyCodes.ESC}{KeyCodes.get_up_down(KeyCodes.ALT, "i")}{KeyCodes.ENTER}'
    """View > Images and Charts"""
    TOGGLE_NAVIGATOR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "v")}'
    """View > Navigator"""
    KB_NAVIGATOR = f"{KeyCodes.F5}"
    """Navigator via keyboard shortcut"""
    TOGGLE_RULERS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "r", "r")}'
    """View > Rulers > Rulers"""
    KB_RULERS = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "r")}'
    """Toggle Rulers via keyboard shortcut"""
    TOGGLE_SHOW_WHITESPACE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "e")}'
    """View > Show Whitespace"""
    KB_SIDE_BAR = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F5)}"
    """Toggle Sidebar via keyboard shortcut"""
    TOGGLE_STATUS_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "b")}'
    """View > Status Bar"""
    TOGGLE_STYLES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "y")}'
    """View > Styles"""
    KB_STYLES = f"{KeyCodes.F11}"
    """Toggle Styles via keyboard shortcut"""
    TOGGLE_TABLE_BOUNDRIES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "a")}'
    """View > Table Boundries"""
    TOGGLE_TEXT_BOUNDRIES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "x")}'
    """View > Text Boundries"""
    TOGGLE_TRACKED_CHANGES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "t")}{KeyCodes.ESC}{KeyCodes.get_up_down(KeyCodes.ALT, "t")}{KeyCodes.ENTER}'
    """View > Show Track Changes"""
    TOGGLE_VERTICAL_RULER = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "r", "v")}'
    """View > Ruler > Vertical Ruler"""
    TOGGLE_VERTICAL_SCROLLBAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "s", "v")}'
    """View > Scrollbars > Vertical Scroll bar"""
    VIEW_NORMAL = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "n")}'
    """View > Normal"""
    VIEW_WEB = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "w")}'
    """View > Web"""
