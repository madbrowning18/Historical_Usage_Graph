# =============================================================================
# AFRICOM HISTORICAL USAGE GRAPH
# =============================================================================
# This script:
#   1. Pulls AFRICOM SharePoint usage data from a .iqy (web query) file OR a
#      previously-saved CSV.
#   2. Cleans the data and computes document "age" (days since last modified).
#   3. Plots a time-series of activity using utils.plot_time.
#   4. Plots a hierarchical folder tree using paths in the "Path" column,
#      colored by age:
#            # Adjust this function according to your gradient requirements
    # if value <= 25:
    #     return 'green'
    # elif value <= 50:
    #     return 'yellow'
    # elif value <= 75:
    #     return 'orange'
    # else:
    #     return 'red'
#
# Inputs expected in this folder:
#   - query.iqy                     (optional, Excel Web Query)
#   - africom_sharepoint_query.csv  (created automatically or saved from Excel)
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
#   - Fall back to an existing africom_sharepoint_query.csv in this folder.
# =============================================================================

IQY_PATH = "query.iqy"
CSV_PATH = "africom_sharepoint_query.csv"

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
                # Not authorized via raw HTTP; Excel usually can handle this.
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
            print("  2. Refresh & save as africom_sharepoint_query.csv here.")
            print("  3. Rerun this script.")
    else:
        print("No valid URL found in query.iqy.")
        print("Open it in a text editor to check the contents if needed.")
else:
    print(f"No {IQY_PATH} file found. Skipping direct download step.")

# --- Step 2: Load CSV into a DataFrame ---------------------------------------

if os.path.exists(CSV_PATH):
    africom_sharepoint_query = pd.read_csv(CSV_PATH)
    print(f"\nLoaded CSV: {CSV_PATH}")
    print("First few rows:")
    print(africom_sharepoint_query.head())
else:
    print(f"\nNo {CSV_PATH} file found.")
    print("You must either:")
    print("  - Successfully download via query.iqy, OR")
    print("  - Manually save the SharePoint export as africom_sharepoint_query.csv")
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

africom_df = africom_sharepoint_query.copy()

# Ensure the expected columns exist
required_cols = ["Path", "Modified"]
for col in required_cols:
    if col not in africom_df.columns:
        raise KeyError(
            f"Expected column '{col}' not found in the data. "
            f"Available columns are: {list(africom_df.columns)}"
        )

# Convert Modified -> datetime 'date'
africom_df["date"] = pd.to_datetime(africom_df["Modified"], errors="coerce")

# Drop rows where date conversion failed
africom_df = africom_df.dropna(subset=["date"])

# Group: one row per Path with the most recent date
africom_df2 = (
    africom_df.groupby("Path", as_index=False)["date"]
    .max()
    .rename(columns={"date": "last_date"})
)

# Compute age in days
today = pd.to_datetime(datetime.today().date())
africom_df2["age"] = (today - africom_df2["last_date"]).dt.days.astype(int)

# Add color column (green / yellow / red)
africom_df2 = get_color_from_df(africom_df2, age_col="age")

print("\nProcessed per-path DataFrame (africom_df2):")
print(africom_df2.head())


# =============================================================================
# VISUALIZATION 1: TIME-SERIES OF MODIFICATIONS
# =============================================================================
# Use utils.plot_time on the full event-level data.
# =============================================================================

print("\nPlotting time-series of document activity...")
plot_time(africom_df, date_col="date", title="AFRICOM Document Activity Over Time")


# =============================================================================
# VISUALIZATION 2: HIERARCHICAL FOLDER TREE
# =============================================================================
# Use the 'Path' column to build a tree and color leaves by age.
# =============================================================================

print("\nPlotting hierarchical folder tree (may take a moment)...")

# We'll pass only the columns we need to the tree plotter
tree_df = africom_df2[["Path", "age"]].copy()

plot_path_tree(
    tree_df,
    path_col="Path",
    age_col="age",
    figsize=(6, 40),  # tall & skinny like your example
    node_size=10,
)

print("\nDone.")
