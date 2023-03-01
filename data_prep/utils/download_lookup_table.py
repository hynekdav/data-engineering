import httpx
import pandas as pd


def download_table(url: str):
    resp = httpx.get(url)
    resp.raise_for_status()

    data = resp.json()
    lookup_table = pd.json_normalize(data.get("polozky"))
    lookup_table = lookup_table[["nazev.cs"]]
    lookup_table.rename({"nazev.cs": "name"}, axis="columns", inplace=True)
    return lookup_table
