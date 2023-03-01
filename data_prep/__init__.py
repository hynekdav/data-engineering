from dagster import Definitions, define_asset_job

from data_prep.assets import (
    criminality_assets,
    relevance_assets,
    states_assets,
    types_assets,
)

all_assets = [*criminality_assets, *relevance_assets, *states_assets, *types_assets]
all_assets_job = define_asset_job(name="all_assets_job")

defs = Definitions(assets=all_assets, jobs=[all_assets_job])
