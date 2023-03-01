import time
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

criminality_path = Path("/tmp/criminality.pqt")


@st.cache_data
def read_criminality():
    return pd.read_parquet(criminality_path)


def main():
    st.title("Kriminalita v ČR v lednu 2023")

    with st.spinner("Čekám na vytvoření dat."):
        while not criminality_path.exists():
            time.sleep(3)

        criminality_df = read_criminality()

    date_from, date_to = st.slider(
        "Časový interval:",
        date(2023, 1, 1),
        date(2023, 2, 1),
        (date(2023, 1, 1), date(2023, 2, 1)),
    )
    st.write("Values:", date_from, date_to)

    possible_states = criminality_df["state"].unique()
    possible_types = criminality_df["types"].explode().unique()

    states = set(
        st.multiselect(
            "Stav objasnění:", options=possible_states, default=possible_states
        )
    )
    types = set(
        st.multiselect("Typ deliktu:", options=possible_types, default=possible_types)
    )

    criminality_df = criminality_df[
        criminality_df["timestamp"].dt.date.between(date_from, date_to)
        & criminality_df["state"].isin(states)
        & criminality_df["types"].map(
            lambda tp_lst: any(typ in types for typ in tp_lst)
        )
    ]

    st.subheader("Surová data")
    st.dataframe(criminality_df)
    st.subheader("Mapa")
    st.map(criminality_df, zoom=6)

    st.markdown("--------------")
    st.markdown("Zdroj: [Policie ČR](https://kriminalita.policie.cz/)")


if __name__ == "__main__":
    main()
