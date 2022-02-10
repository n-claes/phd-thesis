import numpy as np
import matplotlib.pyplot as plt
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
        inset.tick_params(axis="both", labelsize=12)
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


def main():
    quasi_parker_figure()


if __name__ == "__main__":
    main()
