import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pathlib import Path
import pylbo
from panel_label import add_panel_label

plt.style.use("./mpl_style")

datadir = Path("/Volumes/niels_5TB/PhD/papers/paper_legolas/data").resolve()


def quasi_parker_figure():
    filedir = (datadir / "2_quasi_parker/datfiles").resolve()

    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    axes = ax.flatten()
    limits = ([0.3, 0.7, -1, 3], [0.35, 0.75, -1, 3])
    xticks = (np.linspace(0.35, 0.65, 3), np.linspace(0.40, 0.70, 3))
    yticks = (np.linspace(-1, 3, 3), np.linspace(-1, 3, 3))

    for idx, lambdaval in enumerate(["00", "03"]):
        series = pylbo.load_series(sorted(filedir.glob(f"*l{lambdaval}.dat")))

        xdata = np.linspace(0, np.pi, len(series)) / np.pi
        continua = series.continua
        yscale = 1 / series.get_alfven_speed(which_values="average") ** 2

        # spectrum
        p = pylbo.plot_spectrum_multi(
            series,
            xdata=xdata,
            use_squared_omega=True,
            custom_figure=(fig, axes[idx]),
            markersize=3,
            alpha=0.8,
        )
        p.set_y_scaling(yscale)
        # continua
        slowmin = np.min(continua["slow+"] ** 2, axis=1) * yscale
        alfvenmin = np.min(continua["alfven+"] ** 2, axis=1) * yscale
        p.ax.plot(xdata, slowmin, color="red", lw=2)
        p.ax.plot(xdata, alfvenmin, color="cyan", lw=2)
        # inset
        inset = inset_axes(p.ax, width="35%", height="35%", loc="upper center")
        pins = pylbo.plot_spectrum_multi(
            series,
            xdata=xdata,
            use_squared_omega=True,
            custom_figure=(fig, inset),
            markersize=2,
            alpha=0.05,
        )
        pins.set_y_scaling(yscale)
        x1, x2, y1, y2 = limits[idx]
        inset.set_xlim(x1, x2)
        inset.set_ylim(y1, y2)
        inset.set_xticks(xticks[idx])
        inset.set_yticks(yticks[idx])
        inset.yaxis.tick_right()
        inset.tick_params(axis="x", direction="in", pad=-15)
        for side in ["left", "right", "top", "bottom"]:
            inset.spines[side].set_color("grey")
            inset.spines[side].set_alpha(0.4)
        inset.plot(xdata, slowmin, color="red", lw=2)
        inset.plot(xdata, alfvenmin, color="cyan", lw=2)
        if idx == 1:
            slowmax = np.max(continua["slow+"] ** 2, axis=1) * yscale
            alfvenmax = np.max(continua["alfven+"] ** 2, axis=1) * yscale
            axes[1].plot(xdata, slowmax, color="red", lw=2)
            axes[1].plot(xdata, alfvenmax, color="cyan", lw=2)
            inset.plot(xdata, slowmax, color="red", lw=2)
            inset.plot(xdata, alfvenmax, color="cyan", lw=2)
            axes[1].fill_between(
                xdata, slowmin, slowmax, color="red", alpha=0.8, label=r"$\omega_S$"
            )
            inset.fill_between(xdata, slowmin, slowmax, color="red", alpha=0.4)
            axes[1].fill_between(
                xdata,
                alfvenmin,
                alfvenmax,
                color="cyan",
                alpha=0.8,
                label=r"$\omega_A$",
            )
            inset.fill_between(xdata, alfvenmin, alfvenmax, color="cyan", alpha=0.4)
        p.ax.set_xlim(0, 1)
        p.ax.set_ylim(-4, 15)
        p.ax.set_xlabel(r"$\theta / \pi$")
    axes[0].set_ylabel(r"$\dfrac{\omega^2}{c_A^2}$")
    axes[1].legend(
        bbox_to_anchor=(0.0, 1.02, 1, 0.102),
        loc="lower left",
        ncol=2,
        mode="expand",
        borderaxespad=0,
    )
    axes[0].set_yticks(np.arange(-4, 15, 2))
    axes[1].set_yticks([])
    add_panel_label(axes[0], r"$\lambda = 0.0$", loc="top right", color="none")
    add_panel_label(axes[0], "a", loc="top left")
    add_panel_label(axes[1], r"$\lambda = 0.3$", loc="top right", color="none")
    add_panel_label(axes[1], "b", loc="top left")

    # single spectra
    for idx, lambdaval in enumerate(["00", "03"], start=2):
        ds = pylbo.load(*filedir.glob(f"0030*l{lambdaval}.dat"))
        p2 = pylbo.plot_spectrum(ds, custom_figure=(fig, axes[idx]))
        p2.add_continua(interactive=False)
        p2.ax.get_legend().remove()
        p2.ax.set_title("")
        p2.ax.set_xlim(-0.7, 0.7)
        p2.ax.set_ylim(-0.3, 0.3)
        p2.ax.set_xlabel(r"Re$(\omega)$")
    axes[2].set_ylabel(r"Im$(\omega)$")
    axes[3].set_yticks([])
    axes[3].set_ylabel(None)
    add_panel_label(axes[2], r"$\theta = 0.3\pi$", loc="top right", color="none")
    add_panel_label(axes[2], "c", loc="top left")
    add_panel_label(axes[3], r"$\theta = 0.3\pi$", loc="top right", color="none")
    add_panel_label(axes[3], "d", loc="top left")

    fig.subplots_adjust(hspace=0.2, wspace=0.07)
    fig.savefig(
        "../05-applying_legolas/figures/quasi_parker.png",
        bbox_inches="tight",
        dpi=400,
    )

    plt.show()


def discrete_alfven_figure():
    filedir = (datadir / "11_discrete_alfven_efs/datfiles").resolve()
    ds = pylbo.load(*sorted(filedir.glob("*.dat")))

    fig, axes = plt.subplots(3, 6, figsize=(16, 7))
    grid = axes[0, 1].get_gridspec()
    [ax.remove() for ax in axes[:, 0:3].flatten()]
    axl = fig.add_subplot(grid[:, 0:3])
    [ax.remove() for ax in axes[0, 3::]]
    axt = fig.add_subplot(grid[0, 3::])
    mini_axes = axes[1::, 3::]

    insetl = inset_axes(axl, width="45%", height="30%", loc="lower left")
    insetr = inset_axes(axl, width="45%", height="30%", loc="lower right")

    axl.plot(ds.eigenvalues.real, ds.eigenvalues.imag, ".b", alpha=1)
    axl.axhline(y=0, linestyle="dotted", color="grey", alpha=0.3)
    axl.axvline(x=0, linestyle="dotted", color="grey", alpha=0.3)
    wa = ds.continua["alfven-"]
    axl.plot(
        np.real(wa), np.imag(wa), color="cyan", lw=7, alpha=0.5, label=r"$\omega_A$"
    )
    y1, y2 = -0.03, 0.03
    insetr.set_xlim(-0.10972, -0.10959)
    insetl.set_xlim(-0.109693, -0.109677)
    for inset in (insetr, insetl):
        inset.set_ylim(y1, y2)
        inset.axhline(y=0, color="grey", linestyle="dotted", lw=1, alpha=0.8)
        inset.plot(ds.eigenvalues.real, ds.eigenvalues.imag, ".b", alpha=1)
        inset.set_xticks([])
        inset.set_yticks([])
        for side in ["left", "right", "top", "bottom"]:
            inset.spines[side].set_color("grey")
            inset.spines[side].set_alpha(0.4)
        inset.plot(
            np.real(wa),
            np.imag(wa),
            color="cyan",
            lw=7,
            alpha=0.5,
            label=r"$\omega_A$",
        )
    insetr_bounds = patches.Rectangle(
        (-0.11, -0.001),
        width=5e-4,
        height=0.002,
        facecolor="none",
        edgecolor="grey",
        linestyle="solid",
        alpha=0.3,
        lw=1,
    )
    insetl_bounds = patches.Rectangle(
        (-0.109697, -0.003),
        width=2e-5,
        height=0.006,
        facecolor="none",
        edgecolor="grey",
        linestyle="solid",
        alpha=0.3,
        lw=1,
    )
    axl.add_patch(insetr_bounds)
    insetr.add_patch(insetl_bounds)
    axl.legend(loc="upper left")
    cp1 = patches.ConnectionPatch(
        (-0.11, -0.001),
        (0, 1),
        coordsA="data",
        coordsB="axes fraction",
        axesA=axl,
        axesB=insetr,
        linestyle="dotted",
        color="grey",
        alpha=0.5,
    )
    cp2 = patches.ConnectionPatch(
        (-0.11 + 5e-4, -0.001),
        (1, 1),
        coordsA="data",
        coordsB="axes fraction",
        axesA=axl,
        axesB=insetr,
        linestyle="dotted",
        color="grey",
        alpha=0.5,
    )
    cp3 = patches.ConnectionPatch(
        (1, 1),
        (-0.109697, 0.003),
        coordsA="axes fraction",
        coordsB="data",
        axesA=insetl,
        axesB=insetr,
        linestyle="dotted",
        color="grey",
        alpha=0.5,
    )
    cp4 = patches.ConnectionPatch(
        (1, 0),
        (-0.109697, -0.003),
        coordsA="axes fraction",
        coordsB="data",
        axesA=insetl,
        axesB=insetr,
        linestyle="dotted",
        color="grey",
        alpha=0.5,
    )
    axl.add_artist(cp1)
    axl.add_artist(cp2)
    insetr.add_artist(cp3)
    insetr.add_artist(cp4)

    wa_min_idx = ds.continua["alfven+"].argmin()
    axt.plot(ds.grid_gauss, -wa, color="cyan", lw=3, label=r"$\omega_A$")
    axt.plot(
        ds.grid_gauss[wa_min_idx],
        -wa[wa_min_idx],
        color="red",
        marker="X",
        markersize=7,
        alpha=0.8,
    )
    axt.set_ylim(0.10, 0.16)
    axt.yaxis.tick_right()
    axt.xaxis.tick_top()
    axt.xaxis.set_label_position("top")
    axt.set_xlabel("r", labelpad=-35)
    axt.legend(loc="upper left")

    axl.set_xlabel(r"Re($\omega$)")
    axl.set_ylabel(r"Im($\omega$)")
    axl.set_xlim([-0.13, -0.1])
    axl.set_xticks(np.arange(-0.125, -0.104, 0.005))
    axl.set_ylim([-0.03, 0.03])

    ev_guesses = [
        -0.1044 + 1.7261e-7j,
        -0.1091 + 6.6883e-8j,
        -0.1096 + 8.3800e-9j,
        -0.109678 + 2.53365e-9j,
        -0.109687 + 3.77786e-10j,
        -0.109688 + 7.44559e-11j,
    ]
    _, evs = ds.get_nearest_eigenvalues(ev_guesses)
    for i, ev in enumerate(evs, start=1):
        print("Eigenvalue found: {}".format(ev))
        ax = axl
        margin = 1.8e-3
        text = r"$\omega_{}$".format(i)
        if i > 2:
            ax = insetr
            margin = 5.5e-3
        if i > 4:
            ax = insetl
            margin = 5.5e-3
        ax.scatter(ev.real, ev.imag, s=100, edgecolor="red", facecolor="none")
        ax.text(
            ev.real,
            ev.imag + margin,
            text,
            verticalalignment="center",
            horizontalalignment="center",
        )
    eigfuncs = ds.get_eigenfunctions(ev_guesses=ev_guesses)
    for i, ax in enumerate(mini_axes.flatten()):
        ax.axvline(
            x=ds.grid_gauss[wa_min_idx],
            color="red",
            linestyle="dashed",
            lw=1,
            alpha=0.8,
        )
        ax.axhline(y=0, color="grey", linestyle="dotted", lw=1, alpha=0.8)
        rvr = eigfuncs[i].get("v1").imag * ds.ef_grid
        ax.plot(ds.ef_grid, rvr, alpha=0.7)
        ax.set_xticks([])
        ax.set_yticks([])
        text = r"$\omega_{}$".format(i + 1)
        add_panel_label(ax, text, loc="bottom left")
    for ax in mini_axes[-1, :]:
        ax.set_xticks([0.1, 0.5, 0.9])
        ax.set_xlabel("r")
    fig.text(0.915, 1 / 3, r"Im$(rv_r)$", ha="center", rotation="vertical")

    add_panel_label(axl, "a", loc="top right")
    add_panel_label(axt, "b", loc="top right")

    fig.subplots_adjust(hspace=0.04, wspace=0.02)
    fig.savefig(
        "../05-applying_legolas/figures/discrete_alfven.png",
        bbox_inches="tight",
        dpi=400,
    )


def main():
    # quasi_parker_figure()
    discrete_alfven_figure()


if __name__ == "__main__":
    main()
    plt.show()
