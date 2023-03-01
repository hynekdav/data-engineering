from pathlib import Path

import httpx
import pandas as pd
from dagster import AssetIn, asset


@asset
def criminality() -> pd.DataFrame:
    url = "https://kriminalita.policie.cz/api/v2/downloads/202301.geojson"

    resp = httpx.get(url)
    resp.raise_for_status()
    data = resp.json()

    df = pd.json_normalize(data["features"])
    df["lon"], df["lat"] = df["geometry.coordinates"].str
    df["timestamp"] = pd.to_datetime(df["properties.date"])
    df["state"] = df["properties.state"]
    df["relevance"] = df["properties.relevance"]
    df["types"] = df["properties.types"]
    df["id"] = df["properties.id"]

    return df[["id", "timestamp", "lon", "lat", "state", "relevance", "types"]]


@asset(
    ins={
        "criminality_df": AssetIn("criminality"),
        "relevance_df": AssetIn("relevance"),
        "states_df": AssetIn("states"),
        "types_df": AssetIn("types"),
    }
)
def join_criminality(
    criminality_df: pd.DataFrame,
    relevance_df: pd.DataFrame,
    states_df: pd.DataFrame,
    types_df: pd.DataFrame,
) -> pd.DataFrame:
    criminality_df["relevance"] = criminality_df["relevance"].map(relevance_df["name"])
    criminality_df["state"] = criminality_df["state"].map(states_df["name"])
    criminality_df["types"] = criminality_df["types"].map(
        lambda tp: set(filter(None, map(types_df["name"].get, tp)))
    )

    return criminality_df


@asset(ins={"criminality_df": AssetIn("join_criminality")})
def filter_criminality(criminality_df: pd.DataFrame) -> pd.DataFrame:
    criminality_df = criminality_df[criminality_df["relevance"] == "Místo spáchání"]
    criminality_df.drop("relevance", axis="columns", inplace=True)

    criminality_df = criminality_df[
        ~criminality_df["state"].isin(
            {
                "skutek není trestným činem",
                "skutek se nestal",
                "fingovaná trestná činnost",
            }
        )
    ]
    criminality_df.reset_index(drop=True, inplace=True)

    return criminality_df


@asset(ins={"criminality_df": AssetIn("filter_criminality")})
def save_criminality(criminality_df: pd.DataFrame) -> None:
    criminality_path = Path("/tmp/criminality.pqt")
    criminality_df.to_parquet(criminality_path)
