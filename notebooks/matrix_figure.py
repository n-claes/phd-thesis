from venv import create
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pylbo
from panel_label import add_panel_label


def draw_spline(ax, combo1, combo2):
    x0 = 0
    x1 = 1
    x = np.linspace(x0, x1, 100)
    q1 = 4 * (x - x0) * (x1 - x) / (x1 - x0) ** 2
    q2 = np.zeros_like(q1)
    q3 = (2 * x - x1 - x0) * (x - x0) / (x1 - x0) ** 2
    q4 = (2 * x - x1 - x0) * (x - x1) / (x1 - x0) ** 2
    c1 = 3 * ((x - x0) / (x1 - x0)) ** 2 - 2 * ((x - x0) / (x1 - x0)) ** 3
    c2 = 3 * ((x1 - x) / (x1 - x0)) ** 2 - 2 * ((x1 - x) / (x1 - x0)) ** 3
    c3 = (x - x1) * ((x - x0) / (x1 - x0)) ** 2
    c4 = (x - x0) * ((x - x1) / (x1 - x0)) ** 2

    quadratic = [(q1, q2), (q3, q4)]
    cubic = [(c1, c2), (c3, c4)]
    # assuming cubic * quadratic
    spline1_maj_idx = int(combo1[0]) - 1
    spline1_min_idx = int(combo1[1]) - 1
    spline2_maj_idx = int(combo2[0]) - 1
    spline2_min_idx = int(combo2[1]) - 1

    spline1 = cubic[spline1_maj_idx][spline1_min_idx]
    spline2 = quadratic[spline2_maj_idx][spline2_min_idx]

    ax.plot(x, spline1, lw=2)
    ax.plot(x, spline2, lw=2)
    ax.set_ylim(-0.3, 1.4)
    ax.set_xlim(-0.2, 1.2)
    ax.axhline(y=0, color="grey", linestyle="dotted", alpha=0.5)


def create_axes_layout():
    fig = plt.figure(figsize=(9, 9))
    # figure edges in fraction of figure (between 0 and 1)
    space = 0.04
    xl1, xr1 = space, 0.5 - space
    xb1, xt1 = 0.5 + space, 1 - space
    xl2, xr2 = 0.5 + space, 1 - space
    xb2, xt2 = 0.5 + space, 1 - space

    gs1 = fig.add_gridspec(nrows=1, ncols=1, left=xl1, right=xr1, bottom=xb1, top=xt1)
    gs2 = fig.add_gridspec(nrows=1, ncols=1, left=xl2, right=xr2, bottom=xb2, top=xt2)
    width = xr1 - xl1
    gs3 = fig.add_gridspec(
        nrows=4,
        ncols=4,
        left=0.5 - 0.75 * width,
        right=0.5 + 0.75 * width,
        top=0.5 - space,
        bottom=space,
        hspace=0,
        wspace=0,
    )
    ax1 = fig.add_subplot(*gs1)
    ax2 = fig.add_subplot(*gs2)
    axes = np.empty(shape=(4, 4), dtype=type(ax1))
    for i in range(4):
        for j in range(4):
            ax = fig.add_subplot(gs3[i, j])
            axes[i, j] = ax
    for ax in (ax1, ax2, *axes.flatten()):
        ax.set_xticks([])
        ax.set_yticks([])
    return fig, (ax1, ax2, axes)


def make_plot():
    fig, (ax1, ax2, axes) = create_axes_layout()

    # obtain dataset
    ds = pylbo.load("files/matrix.dat")

    # top-left figure
    rows, cols, vals = ds.get_matrix_A()
    ax1.scatter(rows, cols, s=6, edgecolor="navy", lw=0.5)
    visualticks = np.arange(0, ds.matrix_gridpoints + 0.1, 32)
    ax1.set_xticks(visualticks)
    ax1.set_yticks(visualticks)
    ax1.tick_params(which="both", labelsize=13)
    gridticks = visualticks + 0.5
    for i in gridticks:
        ax1.axvline(x=i, linestyle="dashed", color="grey", alpha=0.5)
        ax1.axhline(y=i, linestyle="dashed", color="grey", alpha=0.5)
    ax1.set_aspect("equal")
    ax1.invert_yaxis()
    x1, y1 = 16.5, 16.5
    zoompatch = patches.Rectangle(
        xy=(x1, y1),
        width=32,
        height=32,
        linestyle="solid",
        edgecolor="black",
        facecolor="none",
        alpha=0.5,
    )
    # zoomed patch and connected lines
    ax1.add_patch(zoompatch)
    cp1 = patches.ConnectionPatch(
        (x1 + 32, y1),
        (0, 1),
        coordsA="data",
        coordsB="axes fraction",
        axesA=ax1,
        axesB=ax2,
        linestyle="solid",
        edgecolor="black",
        alpha=0.5,
    )
    cp2 = patches.ConnectionPatch(
        (x1 + 32, y1 + 32),
        (0, 0),
        coordsA="data",
        coordsB="axes fraction",
        axesA=ax1,
        axesB=ax2,
        linestyle="solid",
        edgecolor="black",
        alpha=0.5,
    )
    ax1.add_artist(cp1)
    ax1.add_artist(cp2)

    # top-right figure
    ax2.scatter(rows, cols, s=10, edgecolor="navy", lw=1)
    maingrid_ticks = np.arange(x1, x1 + 32.1, 16)
    for i in maingrid_ticks:
        ax2.axvline(x=i, linestyle="dashed", color="grey", alpha=0.5)
        ax2.axhline(y=i, linestyle="dashed", color="grey", alpha=0.5)
    minorgrid_ticks = np.arange(x1 - 0.5, x1 + 32 - 0.5, 2) + 0.5
    for i in minorgrid_ticks:
        ax2.axvline(x=i, linestyle="dotted", color="grey", alpha=0.3)
        ax2.axhline(y=i, linestyle="dotted", color="grey", alpha=0.3)
    minigrid_tics = np.arange(x1 - 0.5, x1 + 32 - 0.5, 1) + 0.5
    for i in minigrid_tics:
        ax2.axvline(x=i, linestyle="solid", color="grey", alpha=0.1)
        ax2.axhline(y=i, linestyle="solid", color="grey", alpha=0.1)
    ax2.set_aspect("equal")
    ax2.set_xlim(x1 - 0.3, x1 + 32.3)
    ax2.set_ylim(x1 - 0.3, x1 + 32.3)
    ax2.invert_yaxis()
    # variable labels
    unknowns = [
        r"$\rho_1$",
        r"$v_1$",
        r"$v_2$",
        r"$v_3$",
        r"$T_1$",
        r"$a_1$",
        r"$a_2$",
        r"$a_3$",
    ]
    for i, var in enumerate(unknowns):
        # top row
        loc = x1 + 1 + i * 2
        ax2.text(
            x=loc,
            y=y1 - 2,
            s=var,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=12,
        )
        ax2.text(
            x=x1 - 2,
            y=loc,
            s=var,
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=12,
        )
    # boxes around (v1, T1)
    c1, c2 = 8, 2
    facecolors = [(0, 1, 1), (0, 1, 0), (1, 0, 0), (1, 1, 0)]  # RGB value
    for i, (x, y) in enumerate(
        [
            (x1 + c1, y1 + c2),
            (x1 + c1 + 16, y1 + c2),
            (x1 + c1, y1 + c2 + 16),
            (x1 + c1 + 16, y1 + c2 + 16),
        ]
    ):
        patch = patches.Rectangle(
            xy=(x, y),
            width=2,
            height=2,
            linestyle="solid",
            edgecolor="black",
            facecolor=(*facecolors[i], 0.1),
        )
        ax2.add_patch(patch)
    # annotated box
    boxprops = dict(boxstyle="round", color="grey", alpha=0.05)
    arrowprops = dict(arrowstyle="->", connectionstyle="arc3, rad=0.25")
    ax2.annotate(
        "A(2, 5)",
        xy=(x1 + 25, y1 + 2),
        xytext=(x1 + 27, y1 - 2),
        bbox=boxprops,
        arrowprops=arrowprops,
    )

    # bottom figures
    for i in range(4):
        axes[1, i].spines["bottom"].set_linewidth(2)
        axes[i, 1].spines["right"].set_linewidth(2)
    combos = ["12", "22", "11", "21"]
    for row, combo in enumerate(combos):
        for col in range(len(combos)):
            text = "$pH_j^{{{}}}H_j^{{{}}}$".format(combo, combos[col])
            axes[row, col].text(
                0.5,
                0.82,
                s=text,
                transform=axes[row, col].transAxes,
                horizontalalignment="center",
            )
            draw_spline(axes[row, col], combo1=combo, combo2=combos[col])
    for ax in axes[-1, :]:
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["$x_{j-1}$", "$x_j$"])
    for i, axx in enumerate(
        [axes[0:2, 0:2], axes[0:2, 2:4], axes[2:4, 0:2], axes[2:4, 2:4]]
    ):
        for ax in axx.flatten():
            ax.set_facecolor((*facecolors[i], 0.05))

    add_panel_label(ax1, "a", loc="top left", outside=True, color="none", bold=True)
    add_panel_label(ax2, "b", loc="top left", outside=True, color="none", bold=True)
    add_panel_label(
        axes[0, 0], "c", loc="top left", outside=True, color="none", bold=True
    )

    fig.savefig(
        "../04-legolas/figures/matrix_assembly.png",
        bbox_inches="tight",
        dpi=400,
    )


if __name__ == "__main__":
    make_plot()
    plt.show()
