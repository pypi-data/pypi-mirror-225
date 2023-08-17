import argparse
import json
import logging
import subprocess
from timewise.wise_data_base import WISEDataBase

from timewise_sup.ampel_conf import ampel_conf_filename
from timewise_sup.analyse_lightcurves.create_job_file_yaml import make_ampel_job_file

logger = logging.getLogger("timewise_sup.analyze_lightcurves.bayesian_blocks")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_name", type=str)
    parser.add_argument("chunk", type=int)
    parser.add_argument("--t2units", type=str, nargs="+")
    parser.add_argument("--precut_filter", type=bool, default=False, const=True, nargs="?")
    parser.add_argument("--logging-level", "-l", type=str, default="WARNING")
    return parser


def run_bayesian_blocks():
    cfg = vars(get_parser().parse_args())

    logging_level = cfg.pop("logging_level")

    # logging level might be something like `10` in which case we have to transform to an integer
    try:
        logging_level = int(logging_level)
    except ValueError:
        pass

    logging.getLogger("timewise_sup").setLevel(logging_level)
    logger.setLevel(logging_level)
    logger.debug(json.dumps(cfg, indent=4))
    bayesian_blocks(**cfg)


def keys_in_list(keys, arr):
    return any([any([k in element for element in arr]) for k in keys])


def bayesian_blocks(
    base_name: str,
    database_name: str,
    wise_data: WISEDataBase,
    chunk: int | None,
    t2units: list[str],
    load_from_bigdata_dir: bool = True,
    service: str = "tap",
    precut_filter: bool | None = False,
):

    fn = make_ampel_job_file(
        base_name=base_name,
        wise_data=wise_data,
        database_name=database_name,
        chunk=chunk,
        t2units=t2units,
        precut_filter=precut_filter,
        concurrent=False,
        split_units=False,
        load_from_bigdata_dir=load_from_bigdata_dir,
        service=service
    )

    logger.info("running ampel")
    with subprocess.Popen(["ampel", "job", "-config", ampel_conf_filename(), "-schema", fn]) as p:
        out, err = p.communicate()
        if out is not None:
            logger.info(out.decode())
        if err is not None:
            logger.error(err.decode())


if __name__ == "__main__":
    run_bayesian_blocks()
