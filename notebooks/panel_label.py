def add_panel_label(
    ax,
    text,
    loc="top left",
    fs=15,
    alpha=0.2,
    color="grey",
    boxstyle="round",
    bold=False,
    outside=False,
):
    """
    Annotates given text in one of the corners of the specified axis.
    Optional bounding boxes can be supplied and will be aligned properly.
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The matplotlib axes.
    text : str
        The text to annotate.
    loc : str, optional
        Where to place the annotation, options are "top left" (default), "top right",
        "bottom left" or "bottom right".
    fs : int, optional
        fontsize, by default 15
    alpha : float, optional
        Alpha-value of the bounding box, by default 0.2
    color : str, optional
        Facecolor of the bounding box, by default "grey"
    boxstyle : str, optional
        Style of the bounding box, by default "round" which makes rounded edges,
        `boxstyle="circle"` encircles the text. Supply `None` for no bounding box.
    bold : bool, optional
        If `True`, annotates the text in boldface.
    Raises
    ------
    ValueError
        If `loc` is invalid.
    """
    allowed_locs = ["top left", "top right", "bottom left", "bottom right"]
    if loc not in allowed_locs:
        raise ValueError(
            f"Invalid 'loc' argument, got '{loc}' but expected one of {allowed_locs}"
        )
    if boxstyle is None:
        bbox = dict(facecolor="none", alpha=0)
    else:
        bbox = dict(facecolor=color, alpha=alpha, boxstyle=boxstyle, pad=0.2)
    va = "center"
    ha = "center"

    # add optional kwargs
    kwargs = {}
    if bold:
        kwargs["weight"] = "bold"

    # draw sample to know limits of bounding box
    text_sample = ax.text(
        0.5,
        0.5,
        text,
        transform=ax.transAxes,
        fontsize=fs,
        bbox=bbox,
        ha=ha,
        va=va,
        **kwargs,
    )
    ax.figure.canvas.draw()
    # retrieve bounding box, make it slightly (2%) larger to prevent hugging the axes
    bb = text_sample.get_bbox_patch().get_extents().transformed(ax.transAxes.inverted())
    bb_width = 1.02 * (bb.x1 - bb.x0)
    bb_height = 1.02 * (bb.y1 - bb.y0)
    text_sample.remove()

    # draw "actual" label:
    if loc == "top left":
        x = 0.5 * bb_width
        y = 1 - 0.5 * bb_height
        if outside:
            x = x - bb_width
            y = y + bb_height
    elif loc == "top right":
        x = 1 - 0.5 * bb_width
        y = 1 - 0.5 * bb_height
        if outside:
            x, y = x + bb_width, y + bb_height
    elif loc == "bottom left":
        x = 0.5 * bb_width
        y = 0.5 * bb_height
        if outside:
            x, y = x - bb_width, y - bb_height
    elif loc == "bottom right":
        x = 1 - 0.5 * bb_width
        y = 0.5 * bb_height
        if outside:
            x, y = x + bb_width, y - bb_height
    else:
        raise ValueError
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        fontsize=fs,
        bbox=bbox,
        ha=ha,
        va=va,
        **kwargs,
    )
