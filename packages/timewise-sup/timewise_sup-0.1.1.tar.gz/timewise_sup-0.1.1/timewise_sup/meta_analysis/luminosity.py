import logging
import os
import json
import numpy as np
from numpy import typing as npt
import pandas as pd
from astropy import units as u
from astropy.cosmology import Planck18
from astropy import constants
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index, Status
from timewise_sup.meta_analysis.baseline_subtraction import get_lightcurves


logger = logging.getLogger(__name__)


band_wavelengths = {
    "W1": 3.4 * 1e-6 * u.m,   # from Wright et al. (2010) ( 10.1088/0004-6256/140/6/1868 )
    "W2": 4.6 * 1e-6 * u.m,
    "ZTF_g": 4804.79 * u.AA,  # from http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?id=Palomar/ZTF.g&&mode=browse&gname=Palomar&gname2=ZTF
    "ZTF_r": 6436.92 * u.AA,
    "ZTF_i": 7968.22 * u.AA
}


def get_band_nu(band: str) -> float:
    wl = band_wavelengths[band]
    return constants.c / wl


def nuFnu(
        flux: list[float],
        flux_unit: str,
        band: str,
        out_unit: str = "erg s-1 cm-2"
) -> npt.NDArray:
    _flux = np.array(flux) * u.Unit(flux_unit)
    nu = get_band_nu(band)
    return np.array(u.Quantity(_flux * nu).to(out_unit).value)


def calculate_ir_luminosities(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        redshift: dict[str, float] | pd.Series,
        redshift_err: dict[str, float] | pd.Series,
) -> dict:
    indices = tuple(np.atleast_1d(index).astype(int))
    logger.info(f"calculating luminosities for {len(indices)} objects")

    if len(indices) != len(redshift):
        raise ValueError("redshift and index must have the same length!")

    lcs = get_lightcurves(base_name, database_name, wise_data, indices)
    logger.debug(f"got {len(lcs)} lightcurves")
    lcs_with_luminosities = dict()
    for i, lc_dict in lcs.items():
        lc = pd.DataFrame.from_dict(lc_dict, orient="columns")
        iredshift = redshift[i]
        iredshift_err = redshift_err[i]

        lum_dist = Planck18.luminosity_distance(iredshift)
        area = 4 * np.pi * lum_dist ** 2

        lum_dist_ic = Planck18.luminosity_distance(iredshift + iredshift_err * np.array([-1, 1]))
        area_ic = 4 * np.pi * lum_dist_ic ** 2

        for b in ["W1", "W2"]:
            lc[f"{b}_nuFnu_erg_per_s_per_sqcm"] = nuFnu(
                lc[f"{b}_diff_mean_flux_density"],
                flux_unit="mJy",
                band=b,
                out_unit="erg s-1 cm-2"
            )

            lc[f"{b}_nuFnu_err_erg_per_s_per_sqcm"] = nuFnu(
                lc[f"{b}_diff_flux_density_rms"],
                flux_unit="mJy",
                band=b,
                out_unit="erg s-1 cm-2"
            )

            nuFnu_val = u.Quantity(lc[f"{b}_nuFnu_erg_per_s_per_sqcm"] * u.Unit("erg s-1 cm-2"))
            nuFnu_valerr = u.Quantity(lc[f"{b}_nuFnu_err_erg_per_s_per_sqcm"] * u.Unit("erg s-1 cm-2"))

            lum = u.Quantity(nuFnu_val * area).to("erg s-1").value
            lum_err = u.Quantity(
                np.sqrt(
                    (nuFnu_valerr * area) ** 2 + (nuFnu_val * max(abs(area-area_ic))) ** 2
                )
            ).to("erg s-1").value

            lc[f"{b}_ir_luminosity_erg_per_s"] = lum
            lc[f"{b}_ir_luminosity_err_erg_per_s"] = lum_err

        lcs_with_luminosities[i] = lc.to_dict()

    return lcs_with_luminosities


def get_ir_luminosities(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: Status,
        force_new: bool = False
) -> dict:

    logger.info(f"getting luminosities for status {status}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, f"lum_ir_lcs_status{status}.json")

    if (not os.path.isfile(fn)) or force_new:
        logger.debug(f"No file {fn}")
        logger.info("calculating luminosities")

        database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
        indices = database_connector.get_ids(tuple(status))
        redshifts = database_connector.get_redshift(indices)
        lcs = calculate_ir_luminosities(
            base_name,
            database_name,
            wise_data,
            redshifts.index,
            redshifts.ampel_z,
            redshifts.group_z_precision
        )

        logger.debug(f"writing to {fn}")
        with open(fn, "w") as f:
            json.dump(lcs, f)

    else:
        logger.debug(f"reading from {fn}")
        with open(fn, "r") as f:
            lcs = json.load(f)

    return lcs


# def get_peak_ir_luminosity_status(
#         base_name: str,
#         database_name: str,
#         status: (list[str], str),
# ) -> dict:
#     logger.info(f"getting peak IR luminosities for status {status} ({base_name})")
#     lcs = get_ir_luminosities(base_name, database_name, status)
#     logger.debug(f"got {len(lcs)} lightcurves")
#
#     peak_lum = dict()
#     for i, lc_dict in lcs.items():
#         lc = pd.DataFrame.from_dict(lc_dict, orient="columns")
#         peak_lum[i] = dict()
#         for b in ["W1", "W2"]:
#             arg = np.argmax(lc[f"{b}_luminosity_erg_per_s"])
#             peak_lum[i][f"{b}_peak_luminosity_erg_per_s"] = lc[f"{b}_luminosity_erg_per_s"][arg]
#             peak_lum[i][f"{b}_peak_luminosity_err_erg_per_s"] = lc[f"{b}_luminosity_err_erg_per_s"][arg]
#             peak_lum[i][f"{b}_peak_luminosity_mjd"] = lc["mean_mjd"][arg]

