from __future__ import annotations
from ..kind.keys_kind import KeyCodes
from .general import GeneralKeyCodes


class CalcKeyCodes(GeneralKeyCodes):
    """
    Some Calc Key Codes

    These key code only work if Calc main menu is active (visible).

    One way around this issue is to use :external+odev:py:meth:`ooodev.utils.gui.GUI.show_menu_bar`
    to ensure menu bar is visible.

    ::

        from ooodev.utils.gui import GUI
        GUI.show_memu_bar()

    See Also:
        :ref:`class_robot_keys`
    """

    EDIT_CELL_EDIT_MODE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "e", "m")}'
    """Edit > Cell Edit Mode"""
    KB_CELL_EDIT_MODE = f"{KeyCodes.F2}"
    """Edit > Cell Edit Mode"""
    EDIT_CELL_PROTECTION = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "e", "n")}'
    """Edit > Cell Protection"""
    FILE_PREVIEW_BROWSER = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "f", "b")}'
    """File > Preview in web broswer"""
    FORMAT_SINGLE_UNDERLINE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "g")}'
    """Format > Text > Single Underline"""
    FORMAT_DOUBLE_UNDERLINE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "d")}'
    """Format > Text > Double Underline"""
    FORMAT_STRIKE_THROUGH = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "o")}'
    """Format > Text >Strickthrough"""
    FORMAT_OVERLINE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "v")}'
    """Format > Text > Overline"""
    FORMAT_SHADOW = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "w")}'
    """Format > Text > Shadow"""
    FORMAT_OUTLINE_FONT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "f")}'
    """Format > Text > Outline Font Effect"""
    FORMAT_WRAP_TEXT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "x")}'
    """Format > Text > Wrap Text"""
    FORMAT_UPPERCASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "u")}'
    """format > Text > UPPERCASE"""
    FORMAT_LOWERCASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "l")}'
    """Format > Text > lowercase"""
    FORMAT_CYCLE_CASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "y")}'
    """Format > Text Cycle Case"""
    KB_CYCLE_CASE = f"{KeyCodes.get_up_down(KeyCodes.SHIFT, KeyCodes.F3)}"
    """Text Cycle Case via keyboard shortcut"""
    FORMAT_SENTENCE_CASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "s")}'
    """Format > Text > Sentence Case"""
    FORMAT_CAP_EVERY_WORD = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "c")}'
    """Format > Text > Captalizie every word"""
    FORMAT_TOGGLE_CASE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "o", "x", "t")}'
    """Format > Text > tOGGLE cASE"""
    STYLES_DEFAULT = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "d")}'
    """Styles > Defalut"""
    STYLES_ACCENT1 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "a")}'
    """Sytyes > Accent 1"""
    STYLES_ACCENT2 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "2")}'
    """Sytyes > Accent 2"""
    STYLES_ACCENT3 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "3")}'
    """Sytyes > Accent 3"""
    STYLES_HEADING1 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "h")}'
    """Sytyes > Headding 1"""
    STYLES_HEADING2 = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "i")}'
    """Sytyes > Headding 2"""
    STYLES_GOOD = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "g")}'
    """Syles > Good"""
    STYLES_BAD = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "b")}'
    """Syles > Bad"""
    STYLES_NEUTRAL = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "l")}'
    """Syles > Neutral"""
    STYLES_ERROR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "e")}'
    """Syles > Error"""
    STYLES_WARNING = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "w")}'
    """Syles > Warning"""
    STYLES_FOOTNOTE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "f")}'
    """Syles > Footnote"""
    STYLES_NOTE = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "o")}'
    """Syles > Note"""
    STYLES_MANAGE_STYLES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "y", "y")}'
    """Styles > Manage Styles"""
    KB_MANAGE_STYLES = f"{KeyCodes.F11}"
    """Manage Styles via keyboard shortcut"""
    TOGGLE_DEVELOPER_TOOLS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "t", "p")}'
    """Tools > Developers Toolbar"""
    VIEW_NORMAL = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "n")}'
    """View > Normal"""
    VIEW_PAGE_BREAK = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "p")}'
    """View > Page Break"""
    TOGGLE_FORMULA_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "f")}'
    """View > Formula Bar"""
    TOGGLE_STATUS_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "b")}'
    """View > Status Bar"""
    TOGGLE_GRID_LINES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "l")}'
    """View > View Grid Lines"""
    TOGGLE_VALUE_HIGH_LIGHTING = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "h")}'
    """View > Value Hightlighting"""
    KB_VALUE_HIGH_LIGHTING = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F8)}"
    """Value Hightlighting via keyboard shortcut"""
    TOGGLE_FORMULA = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "o")}'
    """View > Show Formula"""
    KB_FORMULA = f'{KeyCodes.get_up_down(KeyCodes.CTL, "`")}'
    """Show Formula via keyboard shortcut"""
    TOGGLE_SPLIT_WINDOW = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "s")}'
    """View > Split Window"""
    TOGGLE_FREEZE_ROWS_COLS = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "r")}'
    """View > Freeze Rows and Columns"""
    VIEW_FREEZE_FIRST_COL = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "c", "f")}'
    """View > Freeze Cells > Freeze First Column"""
    VIEW_FREEZE_FIRST_ROW = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "c", "r")}'
    """View > Freeze Cells > Freeze First Row"""
    TOGGLE_SIDE_BAR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "a")}'
    """View > Sidebar"""
    KB_SIDE_BAR = f"{KeyCodes.get_up_down(KeyCodes.CTL, KeyCodes.F5)}"
    """Toggle Sidebar via keyboard shortcut"""
    TOGGLE_STYLES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "y")}'
    """View > Styles"""
    KB_STYLES = f"{KeyCodes.F11}"
    """Toggle Styles via keyboard shortcut"""
    TOGGLE_GALLERY = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "g")}'
    """View > Gallery"""
    TOGGLE_NAVIGATOR = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "v")}'
    """View > Navigator"""
    KB_NAVIGATOR = f"{KeyCodes.F5}"
    """Navigator via keyboard shortcut"""
    VIEW_FUNCTION_LIST = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "u")}{KeyCodes.ENTER}'
    """View > Function List"""
    TOGGLE_DATA_SOURCES = f'{KeyCodes.get_many_keys(KeyCodes.ALT, "v", "d")}'
    """View > Data Sources"""
    KB_DATA_SOURCES = f"{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), KeyCodes.F4)}"
    """Data Sources via keyboard shortcut"""
    TOGGLE_FULL_SCREEN = f'{KeyCodes.get_up_down((KeyCodes.CTL, KeyCodes.SHIFT), "j")}'
    """View > Full Screen"""
