import os
import json
import logging
import pandas as pd
import numpy as np
from astropy.time import Time
from tqdm import tqdm
from datetime import datetime
import pytz
from timewise.wise_data_base import WISEDataBase
try:
    from fpbot.pipeline import ForcedPhotometryPipeline, FORCEPHOTODATA
except ImportError:
    ForcedPhotometryPipeline = FORCEPHOTODATA = None

from timewise_sup.mongo import DatabaseConnector, Index, Status


logger = logging.getLogger(__name__)

ztf_start = Time(2458194.5, format="jd")  # from https://irsa.ipac.caltech.edu/data/ZTF/docs/ztf_forced_photometry.pdf
now = Time(datetime.now(pytz.timezone("UTC")))


def check_fpbot():
    if ForcedPhotometryPipeline is None:
        raise ImportError(f"'fpbot' is not installed! Make sure to install timewise-sup with the extra 'fpbot'.")


def download_ztffp(
        base_name: str,
        wise_data: WISEDataBase,
        indices: Index,
        time_intervals: pd.DataFrame,
        download: bool = True,
        psf_fit: bool = True
):
    check_fpbot()
    # select the objects and the data needed for FPBot
    _indices = np.atleast_1d(indices)
    logger.info(f"Downloading ZTF forced photometry for {len(_indices)} objects from {base_name}")
    selection = wise_data.parent_sample.df.loc[np.array(_indices).astype(int)]
    cols = [wise_data.parent_sample.default_keymap[k] for k in ["id", "ra", "dec"]]
    columns = {wise_data.parent_sample.default_keymap[k]: k for k in ["id", "ra", "dec"]}
    renamed_selection = selection[cols].rename(columns=columns)

    pipelines = dict()
    skipped = 0
    logger.info("setting up pipelines")
    for index, r in renamed_selection.iterrows():

        time_interval_jd = time_intervals.loc[str(index), ["t_start", "t_end"]]
        logger.debug(f"{index}: time interval: {time_interval_jd.values}")
        if time_interval_jd[1] < ztf_start.jd:
            logger.debug(f"{index}: t_end={time_interval_jd[0]:.0f} which is before ZTF.")
            skipped += 1

        else:
            p = ForcedPhotometryPipeline(
                file_or_name=f'{base_name}_{index}',
                ra=r["ra"],
                dec=r["dec"],
                jdmin=time_interval_jd[0],
                jdmax=time_interval_jd[1]
            )
            pipelines[index] = p

    logger.info(f"skipped {skipped} of {len(renamed_selection)}: before ZTF.")

    if download:
        logger.info("starting download")
        for index, p in tqdm(pipelines.items(), desc="downloading", total=len(pipelines)):
            p.download()

    if psf_fit:
        logger.info("starting psf fits")
        for index, p in tqdm(pipelines.items(), desc="fitting PSFs", total=len(pipelines)):
            try:
                p.psffit()
            except FileNotFoundError:
                logger.debug(f"No observations for {index}")


def download_ztffp_per_status(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        status: str,
        time_interval_relative_to_peak: tuple[float, float] | None = None,
        download: bool = True,
        psf_fit: bool = True
):
    check_fpbot()
    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    ids = database_connector.get_ids(status)
    peak_times = database_connector.get_peak_time_jd(index=ids)
    peak_times["t_ref"] = peak_times.median(axis=1)

    if time_interval_relative_to_peak is None:
        peak_times["t_start"] = ztf_start.jd
        peak_times["t_end"] = now.jd

    else:
        peak_times["t_start"] = peak_times["t_ref"] + time_interval_relative_to_peak[0]
        peak_times["t_end"] = peak_times["t_ref"] + time_interval_relative_to_peak[1]

    download_ztffp(base_name, wise_data, ids, peak_times, download=download, psf_fit=psf_fit)


def get_ztf_lightcurve(
        base_name: str,
        index: str,
        snr_threshold: float = 5,
) -> pd.DataFrame | None:
    check_fpbot()
    fn = os.path.join(FORCEPHOTODATA, f"{base_name}_{index}.csv")

    if not os.path.isfile(fn):
        logger.debug(f"No file for {index} in {base_name}.")
        return None

    data = pd.read_csv(fn, comment="#")

    # calculate the proportionality constant between a.u. and flux density
    c = 10 ** ((8.9 - data["magzp"]) / 2.5)

    # the flux is just the instrument value times the prop. constant
    flux = data["ampl"] * c
    # the error is calculated by gaussian propagation of the instrument value and the
    # error on the magnitude zeropoint (data["magzpunc"])
    flux_error = np.sqrt(
        (data["ampl.err"] * c) ** 2 +
        (data["ampl"] * c * np.log(10) / 2.5 * data["magzpunc"]) ** 2
    )

    data["flux[Jy]"] = flux
    data["flux_err[Jy]"] = flux_error
    data[f"above_snr"] = (flux / flux_error) > snr_threshold

    return data


def get_ztf_id_from_nuclear_sample(
        base_name: str,
        wise_data: WISEDataBase,
        index: str
) -> dict | None:
    # TODO: add upper limits!
    logger.info(f"Getting crossmatch to {index} of {base_name} from ZTF nuclear")

    crossmatch_data_dir = os.path.join(os.path.dirname(__file__), "data")
    crossmatch_files = {
        "news_sample": os.path.join(crossmatch_data_dir, "crossmatch_news_to_ztfnuc.json")
    }

    if base_name not in crossmatch_files:
        raise KeyError(f"No crossmatch file given for {base_name}")

    logger.debug(f"loading {crossmatch_files[base_name]}")
    with open(crossmatch_files[base_name], "r") as f:
        crossmatch = json.load(f)

    allwise_id = wise_data.parent_sample.df.iloc["Allwise_id", index]
    logger.debug(f"AllWISE ID: {allwise_id}")

    if allwise_id not in crossmatch:
        logger.debug("No match")
        return None

    return crossmatch[allwise_id]


def get_ztf_observability(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index | None = None,
        status: Status | None = None
) -> pd.DataFrame:

    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)

    if index is None:
        if status is None:
            raise ValueError("Either of index or status must be given!")
        else:
            indices = database_connector.get_ids(status)
    else:
        indices = list(np.atleast_1d(index))

    # -------------     spacial observability: Dec above -30 degrees      -------------- #
    #              as motivated by https://www.ipac.caltech.edu/news/dr12
    dec = wise_data.parent_sample.df.loc[np.array(indices).astype(int)][wise_data.parent_sample.default_keymap["dec"]]
    sky_vis = dec >= -29
    sky_vis.index = sky_vis.index.astype(str)
    logger.info(f"{sum(sky_vis)} in ZTF FoV")

    # ------------- temporal observability: peak date after 17 March 2018 -------------- #
    #            as also motivated by https://www.ipac.caltech.edu/news/dr12
    peak_times = database_connector.get_peak_time_jd(index=indices)
    ztf_start_jd = ztf_start.jd
    temporal_vis_per_band = peak_times >= ztf_start_jd
    temporal_vis = temporal_vis_per_band.any(axis=1)
    logger.info(f"{sum(temporal_vis)} in ZTF era")

    # -------------      observability: in ZTF sky during ZTF period      -------------- #
    vis = sky_vis & temporal_vis
    logger.info(f"{sum(vis)} in ZTF FoV and era")

    return vis


def ztf_detected(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        snr_threshold: float = 5,
        n_detections: int = 1,
        time_interval_relative_to_peak: tuple[float, float] = (-365, 2*365),
) -> pd.DataFrame:

    vis = get_ztf_observability(base_name, database_name, wise_data, index)
    vis_indices = vis.index[vis]

    database_connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    peak_times = database_connector.get_peak_time_jd(index=vis_indices).median(axis=1)

    detected = dict()

    for i in tqdm(vis_indices, desc="going through forced photometry"):

        i_peak_time = Time(peak_times.loc[i], format="jd")

        lc = get_ztf_lightcurve(
            base_name=base_name,
            index=i,
            snr_threshold=snr_threshold,
        )

        if lc is None:
            continue

        lc_times = lc["obsmjd"]
        time_mask = (
                (lc_times >= i_peak_time.mjd + time_interval_relative_to_peak[0]) &
                (lc_times <= i_peak_time.mjd + time_interval_relative_to_peak[1])
        )

        idetected = dict()
        for f in ["g", "r", "i"]:
            if lc is not None:
                bandmask = lc["filter"] == f"ZTF_{f}"

                idetected[f] = np.sum(lc["above_snr"][bandmask] & time_mask) >= n_detections
            else:
                pass
                # idetected[f] = False

        detected[i] = idetected

    return pd.DataFrame.from_dict(detected, orient="index")
