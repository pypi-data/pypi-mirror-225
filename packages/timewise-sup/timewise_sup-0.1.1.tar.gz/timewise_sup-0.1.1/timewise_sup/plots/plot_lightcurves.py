import os.path

import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import numpy as np
import pandas as pd
from timewise.wise_data_base import WISEDataBase

from timewise_sup.meta_analysis.luminosity import nuFnu
from timewise_sup.meta_analysis.ztf import get_ztf_lightcurve, ztf_start
from timewise_sup.meta_analysis.baseline_subtraction import get_single_lightcurve, get_baseline_subtracted_lightcurves
from timewise_sup.plots import plots_dir, bandcolors


logger = logging.getLogger(__name__)


def plot_sample_lightcurves(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: str,
        include_ztffph: bool = False,
        service: str = "tap",
        load_from_bigdata_dir: bool = False
):
    wise_lcs = get_baseline_subtracted_lightcurves(
        base_name=base_name,
        database_name=database_name,
        wise_data=wise_data,
        status=status,
        service=service,
        load_from_bigdata_dir=load_from_bigdata_dir
    )

    for index, lc_dict in wise_lcs.items():
        logger.debug(f"index {index}")
        wise_lc = pd.DataFrame.from_dict(lc_dict)
        ztf_lc = get_ztf_lightcurve(base_name=base_name, index=index) if include_ztffph else None

        fig, ax = make_lightcurve_plot(wise_lc, ztf_lc)

        if include_ztffph and (ztf_lc is None):
            ax.annotate("no ZTF data", (0.5, 1), xycoords="subfigure fraction")

        d = plots_dir("baseline_subtracted_lightcurves", base_name)
        fn = os.path.join(d, status, f"{index}.pdf")

        d = os.path.dirname(fn)
        if not os.path.isdir(d):
            os.makedirs(d)

        logger.debug(f"saving under {fn}")
        fig.savefig(fn)
        plt.close()


def plot_single_lightcurve(
        base_name: str,
        index: str,
        include_ztffph: bool = False,
        ztf_snr_threshold: float = 5
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:

    wise_lc = get_single_lightcurve(base_name=base_name, index=index)
    if include_ztffph:
        ztf_lc = get_ztf_lightcurve(base_name=base_name, index=index, snr_threshold=ztf_snr_threshold)
    else:
        ztf_lc = None

    return make_lightcurve_plot(wise_lc, ztf_lc)


def make_lightcurve_plot(
        wise_lc: pd.DataFrame,
        ztf_lc: pd.DataFrame = None,
        unit: str = "erg s-1 cm-2"
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:

    fig, ax = plt.subplots()

    for b in ["W1", "W2"]:
        ax.errorbar(
            wise_lc.mean_mjd,
            nuFnu(wise_lc[f"{b}_diff_mean_flux_density"], flux_unit="mJy", band=b, out_unit=unit),
            yerr=nuFnu(wise_lc[f"{b}_diff_flux_density_rms"], flux_unit="mJy", band=b, out_unit=unit),
            marker='s',
            ms=3,
            color=bandcolors[b],
            label=f"WISE {b}",
            ls="",
            zorder=5,
            capsize=2
        )

    if ztf_lc is not None:

        if len(ztf_lc) == 0:
            ax.annotate("no data from ZTF observations", (0.5, 1), xycoords="subfigure fraction", color='red')

        else:

            for b in ["g", "r", "i"]:
                band_mask = ztf_lc["filter"] == f"ZTF_{b}"
                snr_mask = ztf_lc["above_snr"][band_mask]

                f = nuFnu(ztf_lc[band_mask]["flux[Jy]"], flux_unit="Jy", band=f"ZTF_{b}", out_unit=unit)
                ferr = nuFnu(ztf_lc[band_mask]["flux_err[Jy]"], flux_unit="Jy", band=f"ZTF_{b}", out_unit=unit)

                if np.any(snr_mask):
                    ax.errorbar(
                        ztf_lc.obsmjd[band_mask][snr_mask],
                        f[snr_mask],
                        yerr=ferr[snr_mask],
                        marker='o',
                        ms=2,
                        color=bandcolors[f"ZTF_{b}"],
                        label="ZTF " + b,
                        ls="",
                        zorder=4,
                        elinewidth=1
                    )

                if np.any(~snr_mask):
                    ylim = ax.get_ylim()  # upper limits should not adjust the axis limits
                    ax.scatter(
                        ztf_lc.obsmjd[band_mask][~snr_mask],
                        f[~snr_mask] + ferr[~snr_mask],
                        marker="v",
                        s=2,
                        alpha=0.2,
                        color=bandcolors[f"ZTF_{b}"],
                        zorder=2,
                        label=f"ZTF {b} upper limits" if np.all(~snr_mask) else ""
                    )
                    ax.set_ylim(ylim)

        xlim = ax.get_xlim()
        if xlim[0] < ztf_start.mjd < xlim[1]:
            ax.axvline(ztf_start.mjd, ls=":", color="grey")
            ax.annotate(
                "ZTF start", (ztf_start.mjd, ax.get_ylim()[1]),
                xytext=(-2, -2), textcoords='offset points',
                rotation=90, va='top', ha='right', color="grey",
                annotation_clip=False
            )

    ax.set_ylabel(r"$\nu$ F$_{\nu}$ [erg s$^{-1}$ cm$^{-2}$]")
    ax.grid()
    ax.legend()

    return fig, ax
