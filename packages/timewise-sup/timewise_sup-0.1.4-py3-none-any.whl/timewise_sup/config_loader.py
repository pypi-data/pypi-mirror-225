import logging
import inspect
from pydantic import validator
from typing import Callable, Any
from timewise.config_loader import TimewiseConfig, TimewiseConfigLoader

from timewise_sup.ampel_conf import create_ampel_config_file
from timewise_sup.analyse_lightcurves.bayesian_blocks import bayesian_blocks
from timewise_sup.meta_analysis.baseline_subtraction import get_baseline_subtracted_lightcurves
from timewise_sup.plots.plot_lightcurves import plot_sample_lightcurves
from timewise_sup.meta_analysis.ztf import download_ztffp_per_status


logger = logging.getLogger(__name__)


functions = {
    "create_ampel_config_file": create_ampel_config_file,
    "bayesian_blocks": bayesian_blocks,
    "baseline_subtraction": get_baseline_subtracted_lightcurves,
    "plot": plot_sample_lightcurves,
    "download_ztffp_per_status": download_ztffp_per_status
}


class TimewiseSUPConfigLoader(TimewiseConfigLoader):

    timewise_sup_instructions: list[dict] = list()
    database_name: str

    def parse_config(self):
        timewise_config = super().parse_config()
        return TimewiseSUPConfig(
            database_name=self.database_name,
            timewise_sup_instructions=self.timewise_sup_instructions,
            **timewise_config.dict()
        )


class TimewiseSUPConfig(TimewiseConfig):

    timewise_sup_instructions: list[dict] = list()
    database_name: str

    @validator("timewise_sup_instructions")
    def validate_timewise_sup_instructions(cls, v: list[dict]):
        for instructions in v:
            for fct_name, arguments in instructions.items():

                if fct_name not in functions:
                    available = ", ".join(list(functions.keys()))
                    raise ValueError(f"timewise-sup has no function {fct_name}! Must be either of {available}")

                fct = functions[fct_name]
                # this is a mypy bug: https://github.com/python/mypy/issues/10740

                signature = inspect.signature(fct)  # type: ignore
                param_list = list(signature.parameters)
                # check if the function needs base_name
                for k in ["base_name", "database_name", "wise_data"]:
                    if k in param_list:
                        # enter dummy string in arguments
                        arguments[k] = ""
                # check validity of arguments
                try:
                    _arguments = arguments or dict()  # supply empty dict if arguments is None
                    signature.bind(**_arguments)
                except TypeError as e:
                    raise ValueError(f"{fct_name}: {e}!")

        return v

    def run_config(self):
        logger.info("running config")
        super().run_config()

        for instructions in self.timewise_sup_instructions:
            for fct_name, arguments in instructions.items():
                _arguments = arguments or dict()
                fct = functions[fct_name]
                params = list(inspect.signature(fct).parameters)

                if "base_name" in params:
                    arguments["base_name"] = self.wise_data.base_name
                if "database_name" in params:
                    arguments["database_name"] = self.database_name
                if "wise_data" in params:
                    arguments["wise_data"] = self.wise_data

                _arguments = arguments or dict()  # supply empty dict if arguments is None
                logger.info(f"running {fct_name} with arguments {_arguments}")
                fct(**_arguments)

        logger.info("successfully ran config")
