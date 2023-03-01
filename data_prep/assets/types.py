from dagster import asset

from data_prep.utils.download_lookup_table import download_table


@asset
def types():
    return download_table("https://kriminalita.policie.cz/api/v2/downloads/types.json")
