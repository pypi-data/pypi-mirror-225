import logging
import pandas as pd

from timewise_sup.mongo import DatabaseConnector


logger = logging.getLogger(__name__)


def get_catalog_match_mask(
        base_name: str,
        database_name: str,
        index: list[str | int] | str | int
) -> pd.DataFrame:
    logger.info("getting catalog match mask")
    matches = DatabaseConnector(base_name=base_name, database_name=database_name).get_catalog_matches(index)
    has_match_dict = {i: {c: match is not None for c, match in imatches.items()} for i, imatches in matches.items()}
    has_match_masks = pd.DataFrame.from_dict(has_match_dict, orient="index").fillna(False)
    return has_match_masks
