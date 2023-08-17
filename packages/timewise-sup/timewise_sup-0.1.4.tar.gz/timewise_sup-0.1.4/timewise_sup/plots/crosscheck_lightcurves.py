import logging
import os
import pandas as pd
import matplotlib.pyplot as plt

from timewise_sup.samples.sjoerts_flares import get_test_flares_config
from timewise_sup.plots.plot_lightcurves import bandcolors
from timewise_sup.environment import load_environment
from timewise_sup.meta_analysis.luminosity import get_ir_luminosities
from timewise_sup.plots import plots_dir


logger = logging.getLogger(__name__)
tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")


def make_crosscheck_lightcurves_plots(
        show: bool = False
):
    logger.info("making crosscheck lightcurve plots")
    sjoerts_colors = {"W1": "darkred", "W2": "indianred"}

    # load data for flares from https://arxiv.org/abs/2111.09391
    test_config = get_test_flares_config()
    z = test_config.wise_data.parent_sample.df["z"]

    # get redshift and ids for flares where available
    zdict = dict()
    tpeak_dict = dict()
    for i, iz in z.items():
        try:
            zdict[i] = float(iz)
            tpeak_dict[i] = float(test_config.wise_data.parent_sample.df.loc[i, "tpeak"])
        except ValueError:
            pass

    ids = tuple(zdict.keys())

    # calculate luminosities
    lums = get_ir_luminosities(
        test_config.wise_data.base_name,
        test_config.database_name,
        test_config.wise_data,
        ids,
    )

    # plot the lightcurves for the three flares with lightcurve data in https://arxiv.org/abs/2111.09391
    for name in ["AT2019dsg", "AT2019fdr", "AT2019aalc"]:
        logger.info(f"making plot for {name}")

        id = test_config.wise_data.parent_sample.df.index[test_config.wise_data.parent_sample.df.name == name][0]
        wise_lc = pd.DataFrame.from_dict(
            lums[id], orient="columns"
        )
        tpeak = tpeak_dict[id]

        fig, ax = plt.subplots()

        for b in ["W1", "W2"]:
            ax.errorbar(
                wise_lc.mean_mjd - tpeak,
                wise_lc[f"{b}_luminosity_erg_per_s"],
                yerr=wise_lc[f"{b}_luminosity_err_erg_per_s"],
                marker='s',
                ecolor="k",
                capsize=2,
                ls="",
                color=bandcolors[b],
                label=f"WISE {b} (AIR-FLARES)",
                zorder=5,
                barsabove=True
            )

            # load the reference data
            without_at = name.replace("AT", "")
            ref_fn = os.path.join(tsup_data_dir, f"neutrino_flares/{without_at}_{b}.csv")
            logger.debug(f"loading {ref_fn}")
            ref = pd.read_csv(
                ref_fn,
                sep=";",
                decimal=",",
                names=["time_from_peak", "luminosity"]
            )

            ax.scatter(
                ref.time_from_peak,
                ref.luminosity * 1e43,
                marker='x',
                s=30,
                color=sjoerts_colors[b],
                label=f"WISE {b} (Sjoert)",
                zorder=5
            )

        ax.set_xlabel(f"t - {tpeak} [d]")
        ax.set_ylabel(r"Luminosity [erg s$^{-1}$]")
        ax.set_title(name)
        ax.legend()
        ax.grid()

        fn = os.path.join(plots_dir("crosscheck_lightcurves", "crosscheck"), f"{name}_crosscheck.pdf")
        logger.info(f"saving under {fn}")
        fig.savefig(fn)

        if show:
            plt.show()

        plt.close()
