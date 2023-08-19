import logging
import os
from time import time

import numpy as np
import pandas as pd

from cpilib.cpi.base_classes import CPICountries
from cpilib.utils import get_eurostat_dataset

logger = logging.getLogger(__name__)


class HICP(CPICountries):
    """CPI class for the Harmonized Index of Consumer Prices (HICP)."""

    def __init__(self, prices=None, item_weights=None, country_weights=None):
        if prices is None and item_weights is None and country_weights is None:
            prices, item_weights, country_weights = self._load_data()  # Use a separate method to load the data

        super().__init__(prices, item_weights, country_weights, 2015)
        logger.info("Done.")

    @staticmethod
    def clean_dataframe(data: pd.DataFrame, date_format: str = None) -> pd.DataFrame:
        """Helper function to clean up dataframe."""
        if date_format is not None:
            data.index = pd.to_datetime(data.index, format=date_format)
        else:
            data.index = pd.to_datetime(data.index)
        return (
            data.replace(pd.NA, np.nan)
            .replace(": c", np.nan)
            .applymap(lambda x: x.rstrip(" d") if isinstance(x, str) else x)
            .applymap(lambda x: x.rstrip(" du") if isinstance(x, str) else x)
            .applymap(lambda x: x.rstrip(" er") if isinstance(x, str) else x)
            .astype(float)
            .sort_index(axis=0)
        )

    def _load_data(self):
        logger.info("Loading HICP object from Eurostat...")
        prices = get_eurostat_dataset("prc_hicp_midx")
        prices = self.clean_dataframe(prices["I15"], date_format="%YM%m").swaplevel(0, 1, axis=1).sort_index(axis=1)

        item_weights = get_eurostat_dataset("prc_hicp_inw")
        item_weights = self.clean_dataframe(item_weights).swaplevel(0, 1, axis=1).sort_index(axis=1)

        country_weights = get_eurostat_dataset("prc_hicp_cow")
        country_weights = self.clean_dataframe(country_weights["COWEA19"])

        prices.to_parquet("cache/prices.parquet")
        item_weights.to_parquet("cache/item_weights.parquet")
        country_weights.to_parquet("cache/country_weights.parquet")

        return prices, item_weights, country_weights

    @classmethod
    def from_cache(cls, time_limit: float = None):
        """
        Create a HICP object from cached data, if it exists and is not too old.
        If no cached data is found or the cache is too old, creates a new object from the `__init__` method.
        `time_limit` is the maximum age of the cache in days.
        """
        cache_files = ["cache/prices.parquet", "cache/item_weights.parquet", "cache/country_weights.parquet"]
        if all(os.path.exists(path) for path in cache_files):
            if time_limit is not None:
                # Get the last modified times of the cache files
                last_modified_times = [os.path.getmtime(path) for path in cache_files]
                # If any of the cache files is older than the time limit, re-create the object
                if max(last_modified_times) < time() - time_limit * 86400:  # Convert days to seconds
                    logger.info("Cache is older than the time limit. Re-creating HICP object...")
                    return cls()

            logger.info("Loading HICP object from cache...")
            prices = pd.read_parquet(cache_files[0])
            item_weights = pd.read_parquet(cache_files[1])
            country_weights = pd.read_parquet(cache_files[2])
            return cls(prices, item_weights, country_weights)

        logger.info("Initializing HICP object...")
        return cls()
