"""
personal library of Matplotlib utility programs.
"""
import matplotlib.axes as axes

from bs_python_utils.bsutils import bs_error_abort


def ax_text(ax: axes.Axes, str_txt: str, x: float, y: float) -> axes.Axes:
    """
    annotate an ax with text in Matplotlib

    Args:
        ax: axis we want to annotate
        str_txt: string of text
        x: position in fraction of horizontal axis
        y: position in fraction of vertical axis

    Returns:
        annotated ax
    """
    if not (isinstance(x, float) and 0 <= x <= 1):
        bs_error_abort("x should be a number between 0.0 and 1.0")
    if not (isinstance(y, float) and 0 <= y <= 1):
        bs_error_abort("y should be a number between 0.0 and 1.0")
    ax.text(
        x,
        y,
        str_txt,
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax.transAxes,
    )
    return ax
