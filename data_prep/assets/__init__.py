from dagster import load_assets_from_modules

from data_prep.assets import criminality, relevance, states, types

criminality_assets = load_assets_from_modules([criminality])
relevance_assets = load_assets_from_modules([relevance])
states_assets = load_assets_from_modules([states])
types_assets = load_assets_from_modules([types])
