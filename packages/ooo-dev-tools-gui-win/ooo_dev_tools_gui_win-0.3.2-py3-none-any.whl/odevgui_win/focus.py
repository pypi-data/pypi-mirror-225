from __future__ import annotations
from pywinauto.application import Application
import pywinauto


from ooodev.utils.data_type.window_title import WindowTitle as WindowTitle
from ooodev.utils.gui import GUI

from .data_type.rectangle import Rectangle


class Focus:
    @classmethod
    def focus(cls, *titles: WindowTitle) -> Rectangle | None:
        """
        Set focus on first window that matches.

        Arguments:
            *titles: Expandable list of :external+odev:py:class:`ooodev.utils.data_type.window_title.WindowTitle`

        Returns:
            Rectangle: Rectangle representing window if found; Otherwise, ``None``

        See Also:
            :py:meth:`~.focus.Focus.focus_current`
        """
        if len(titles) == 0:
            return False
        app = None
        title_arg = None
        for title in titles:
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
            return None
        try:
            if title_arg.is_regex:
                win = app.window(title_re=title_arg.title)
            else:
                win = app.window(title=title_arg.title)
            win.set_focus()
            return cls._win_to_rect(win)
        except Exception:
            pass
        return None

    @classmethod
    def focus_current(cls) -> Rectangle | None:
        """
        Focuses on the current window detected by :external+odev:py:class:`ooodev.utils.lo.Lo`.

        Returns:
            Rectangle: Rectangle representing window if found; Otherwise, ``None``

        See Also:
            :py:meth:`~.focus.Focus.focus`
        """
        win = cls._focus_hwnd()
        if win:
            return cls._win_to_rect(win)
        win = cls._focus_title()
        if win:
            return cls._win_to_rect(win)
        return None

    @staticmethod
    def _focus_hwnd() -> pywinauto.WindowSpecification | None:
        hwnd = GUI.get_window_handle(None)
        if hwnd is None:
            return False
        if hwnd <= 0:
            return False
        try:
            app = Application().connect(handle=hwnd)
            win = app.window(handle=hwnd)
            win.set_focus()
            return win
        except Exception:
            pass
        return None

    @staticmethod
    def _focus_title() -> pywinauto.WindowSpecification | None:
        try:
            title = GUI.get_title_bar()
            if not title:
                return None
            wt = WindowTitle(title=title)
            app = Application().connect(title=wt.title, class_name=wt.class_name)
            win = app.window(title=wt.title)
            win.set_focus()
            return win
        except Exception:
            pass
        return None

    @staticmethod
    def _win_to_rect(win) -> Rectangle:
        rect = win.rectangle()
        return Rectangle(left=rect.left, right=rect.right, top=rect.top, bottom=rect.bottom)
