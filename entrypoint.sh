#!/usr/bin/env bash

dagster job execute -m data_prep -j all_assets_job && streamlit run visualization.py
