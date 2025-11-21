# =============================================================================
# HISTORICAL USAGE GRAPH
# =============================================================================
# This script:
#   1. Pulls SharePoint usage data from a .iqy (web query) file OR a
#      previously-saved CSV.
#   2. Cleans the data and computes document "age" (days since last modified).
#   3. Plots a time-series of activity using utils.plot_time.
#   4. Plots a hierarchical folder tree using paths in the "Path" column,
#      colored by age:
#            # Example gradient function (edit to your preference)
#            # if value <= 25: return 'green'
#            # elif value <= 50: return 'yellow'
#            # elif value <= 75: return 'orange'
#            # else: return 'red'
#
# Inputs expected in this folder:
#   - query.iqy                      (optional, Excel Web Query)
#   - sharepoint_usage_query.csv     (created automatically or saved manually)
#
# Outputs: interactive matplotlib plots (timeline + folder tree).
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================

import os
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib
import networkx as nx
import requests

import utils
from utils import (
    hierarchy_pos,
    plot_time,
    get_color,
    get_color_from_df    
)


# =============================================================================
# BASIC SANITY CHECK (where are we importing utils from?)
# =============================================================================

print("Using utils from:", utils.__file__)
print("Current working directory:", os.getcwd())


# =============================================================================
# SHAREPOINT LOAD: IQY -> CSV
# =============================================================================
# We either:
#   - Read the URL from query.iqy and download a fresh CSV, OR
#   - Fall back to an existing sharepoint_usage_query.csv in this folder.
# =============================================================================

IQY_PATH = "query.iqy"
CSV_PATH = "sharepoint_usage_query.csv"

data_url = None

# --- Step 1: Try to read URL from .iqy and download to CSV -------------------
if os.path.exists(IQY_PATH):
    print(f"Found SharePoint Web Query file: {IQY_PATH}")

    with open(IQY_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("http"):
            data_url = line.strip()
            break

    if data_url:
        print(f"Attempting to download data from:\n  {data_url}")

        try:
            response = requests.get(data_url)

            if response.status_code == 401:
                print("\nReceived 401 Unauthorized from SharePoint.")
                print("Workaround:")
                print("  1. Open query.iqy in Excel.")
                print("  2. Refresh the data (Excel uses your logged-in account).")
                print(f"  3. Save as '{CSV_PATH}' in this folder.")
                print("  4. Rerun this script.")
            else:
                response.raise_for_status()
                with open(CSV_PATH, "wb") as f:
                    f.write(response.content)
                print(f"Data successfully downloaded to {CSV_PATH}")
        except requests.exceptions.RequestException as e:
            print("\nError downloading data from SharePoint:")
            print(" ", e)
            print("\nIf this persists:")
            print("  1. Open query.iqy in Excel.")
            print("  2. Refresh & save as sharepoint_usage_query.csv here.")
            print("  3. Rerun this script.")
    else:
        print("No valid URL found in query.iqy.")
        print("Open it in a text editor to check the contents if needed.")
else:
    print(f"No {IQY_PATH} file found. Skipping direct download step.")

# --- Step 2: Load CSV into a DataFrame ---------------------------------------

if os.path.exists(CSV_PATH):
    usage_df_raw = pd.read_csv(CSV_PATH)
    print(f"\nLoaded CSV: {CSV_PATH}")
    print("First few rows:")
    print(usage_df_raw.head())
else:
    print(f"\nNo {CSV_PATH} file found.")
    print("You must either:")
    print("  - Successfully download via query.iqy, OR")
    print("  - Manually save the SharePoint export as sharepoint_usage_query.csv")
    raise SystemExit("Stopping: no data available.")


# =============================================================================
# DATA PROCESSING
# =============================================================================
# We:
#   1. Convert 'Modified' to a datetime column 'date'.
#   2. Group by 'Path' to find the most recent modification per path.
#   3. Compute 'age' (days since last modified).
#   4. Add a 'color' column based on get_color (green / yellow / red).
# =============================================================================

usage_df = usage_df_raw.copy()

# Ensure expected columns exist
required_cols = ["Path", "Modified"]
for col in required_cols:
    if col not in usage_df.columns:
        raise KeyError(
            f"Expected column '{col}' not found in the data. "
            f"Available columns are: {list(usage_df.columns)}"
        )

# Convert Modified -> datetime 'date'
usage_df["date"] = pd.to_datetime(usage_df["Modified"], errors="coerce")

# Drop rows where date conversion failed
usage_df = usage_df.dropna(subset=["date"])

# Group: one row per Path with most recent date
usage_df2 = (
    usage_df.groupby("Path", as_index=False)["date"]
    .max()
    .rename(columns={"date": "last_date"})
)

# Compute age in days
today = pd.to_datetime(datetime.today().date())
usage_df2["age"] = (today - usage_df2["last_date"]).dt.days.astype(int)

# Add color column
usage_df2["color"] = usage_df2["age"].apply(get_color)


print("\nProcessed per-path DataFrame (usage_df2):")
print(usage_df2.head())


# =============================================================================
# VISUALIZATION 1: TIME-SERIES OF DOCUMENT ACTIVITY
# =============================================================================

print("\nPlotting time-series of document activity...")
plot_time(
    usage_df,
    date_col="date",
    title="Document Activity Over Time"
)


# =============================================================================
# VISUALIZATION 2: HIERARCHICAL FOLDER TREE
# =============================================================================

print("\nPlotting hierarchical folder tree (may take a moment)...")

tree_df = usage_df2[["Path", "age"]].copy()

# Ensure plot_path_tree is imported or defined
from utils import plot_path_tree

plot_path_tree(
    tree_df,
    path_col="Path",
    age_col="age",
    figsize=(6, 40),
    node_size=10,
)

print("\nDone.")
