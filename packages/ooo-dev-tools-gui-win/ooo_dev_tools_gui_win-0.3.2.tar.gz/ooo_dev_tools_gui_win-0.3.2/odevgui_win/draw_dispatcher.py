from __future__ import annotations

import uno
from com.sun.star.drawing import XShape
from com.sun.star.drawing import XDrawPage

from ooodev.utils.data_type.window_title import WindowTitle
from ooodev.utils.lo import Lo
from ooodev.office.draw import Draw

import pywinauto
from pywinauto.keyboard import send_keys

from .focus import Focus
from .exceptions import ElementNotFoundError


class DrawDispatcher:
    """Draw Dispat Automation"""

    @staticmethod
    def create_dispatch_shape(slide: XDrawPage, shape_dispatch: str) -> XShape | None:
        """
        Creates a dispatch shape in two steps.

        1. Select the shape by calling :external+odev:py:meth:`ooodev.utils.lo.Lo.dispatch_cmd`
        2. Creates the shape on screen by imitating a press and drag on the visible page.

        A reference to the created shape is obtained by assuming that it's the new
        top-most element on the page.

        Args:
            slide (XDrawPage): Draw Page
            shape_dispatch (str): Shape Dispatch Command
            *titles: Optional Extended sequence of title information. This is used to match windows title.

        Raises:
            ElementNotFoundError: If unable to find a LibreOffice window to dispatch to.

        Returns:
            XShape | None: Shape on Success; Otherwise, ``None``.

        Notes:
            Assumes that connection to LibreOffice has been made with :external+odev:py:meth:`ooodev.utils.lo.Lo.load_office`.
        """
        num_shapes = slide.getCount()

        # select the shape icon; Office must be visible
        Lo.dispatch_cmd(shape_dispatch)
        # wait just a sec.
        # Lo.delay(1_000)

        # click and drag on the page to create the shape on the page;
        # the current page must be visible

        rect = Focus.focus_current()
        if not rect:
            rect = Focus.focus(WindowTitle(".*LibreOffice Draw", True), WindowTitle(".*LibreOffice Impress", True))

        if not rect:
            raise ElementNotFoundError()

        Lo.delay(500)
        center_x = round((rect.right - rect.left) / 2) + rect.left
        center_y = round((rect.bottom - rect.top) / 2) + rect.top

        pywinauto.mouse.press(button="left", coords=(center_x, center_y))
        pywinauto.mouse.release(button="left", coords=(center_x + 50, center_y + 50))

        # get a reference to the shape by assuming it's the top one on the page
        Lo.delay(300)
        num_shapes2 = slide.getCount()
        shape = None
        if num_shapes2 == num_shapes + 1:
            Lo.print(f'Shape "{shape_dispatch}" created')
            shape = Draw.find_top_shape(slide)
        else:
            Lo.print(f'Shape "{shape_dispatch}" NOT created')

        # escape deselects the shape that was just created.
        # this is critial in cases where one shape is drawn on top of another.
        send_keys("{VK_ESCAPE}")
        return shape
