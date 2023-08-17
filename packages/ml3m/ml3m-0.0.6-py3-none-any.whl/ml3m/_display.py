from __future__ import annotations

import shutil
import sys
import textwrap
from enum import Enum
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from ._typing import DataItemType

#######################################################################################
#                                                                                     #
#                                        COLOR                                        #
#                                                                                     #
#######################################################################################


class COLOR(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT = "\033[39m"


_color_support = True


if sys.platform == "win32":
    try:
        # https://stackoverflow.com/questions/36760127
        from ctypes import windll

        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:  # pragma: no cover
        _color_support = False


def colored(content: Any, color: COLOR | None) -> str:
    """Return the content that will be printed colored.

    Parameters
    ----------
    content : str
        The content to color.
    color : COLOR
        The color type.

    Returns
    -------
    colored_content : str
        The colored content. Default color if coloring is not supported.
    """
    if _color_support and color is not None:
        return f"{color.value}{content}{COLOR.DEFAULT.value}"
    return f"{content}"


#######################################################################################
#                                                                                     #
#                                        EMOJI                                        #
#                                                                                     #
#######################################################################################


class EMOJI:
    STAR = "\U0001F31F"
    DIAMOND = "\U0001F539"


#######################################################################################
#                                                                                     #
#                                    TEXT WRAPPING                                    #
#                                                                                     #
#######################################################################################


def wrap_with_prefix(
    prefix: Any,
    content: Any,
    max_lines: int | None = None,
    prefix_color: COLOR | None = None,
    content_color: COLOR | None = None,
) -> str:
    """Wraps the content with a prefix in the first line.

    Parameters
    ----------
    prefix : Any
        The prefix, taking 1/4 of the terminal width from the left. If the total length
        of the prefix is fewer than that, take only its total length.
    content : Any
        The content, taking 3/4 of the terminal width from the right.
    max_lines : int, optional
        The maximum number of lines to display. If ``None``, there is no limit. The
        prefix and content, if too long to display within ``max_lines``, will be marked
        with a placeholder "[...]".
    prefix_color : COLOR, optional
        The color of the prefix. If ``None``, do not color the prefix.
    content_color : COLOR, optional
        The color of the content. If ``None``, do not color the content.

    Returns
    -------
    wrapped : str
        The wrapped (and colored) prefix and content.
    """
    prefix_width = shutil.get_terminal_size().columns // 4 - 1
    content_width = prefix_width * 3

    # Possibly adjust the proportion
    if len(prefix) < prefix_width:
        difference = prefix_width - len(prefix)
        prefix_width -= difference
        content_width += difference

    # Make sure the maximum widths are enough for the placeholder
    prefix_width = max(5, prefix_width)
    content_width = max(5, content_width)

    # Wrap the prefix and the content respectively
    prefix_lns = textwrap.wrap(f"{prefix}", width=prefix_width, max_lines=max_lines)
    content_lns = textwrap.wrap(f"{content}", width=content_width, max_lines=max_lines)
    prefix_nlns, content_nlns = len(prefix_lns), len(content_lns)

    # Combine the prefix and the content lines
    lns = []
    for i in range(max(prefix_nlns, content_nlns)):
        prefix_ln = (
            " " * prefix_width
            if i >= prefix_nlns
            else colored(f"{prefix_lns[i]:<{prefix_width}}", prefix_color)
        )
        content_ln = "" if i >= content_nlns else colored(content_lns[i], content_color)
        lns.append(f"{prefix_ln}   {content_ln}")
    return "\n".join(lns)


#######################################################################################
#                                                                                     #
#                                  OTHER FORMATTING                                   #
#                                                                                     #
#######################################################################################


def format_data_item(data_item: DataItemType) -> str:
    """Format a data item into a nice printout.

    Parameters
    ----------
    data_item : DataItemType
        The data item to format.

    Returns
    -------
    formatted_data_item : str
        The formatted data item.
    """
    concatenator = " " + EMOJI.DIAMOND * 3 + " "
    if isinstance(data_item, list):
        return concatenator.join(data_item)
    elif isinstance(data_item, (dict, pd.Series)):
        return concatenator.join(
            [f"{colored(k, COLOR.CYAN)}: {v}" for k, v in data_item.items()]
        )
    else:
        raise TypeError(f"Invalid data item of type {type(data_item)}.")
