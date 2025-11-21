Historical_Usage_Graph

Visual Depiction of Historical Document Usage
Historical Usage Graph Library

This library builds exploratory visualizations of SharePoint activity to help identify high-value documents and folders for follow-on cataloging, LLM ingestion, and knowledge-graph construction. It pulls usage data from a SharePoint Web Query (.iqy) or a saved CSV, cleans and aggregates the data, and then generates:

A time-series plot of document activity

A hierarchical folder tree colored by document “age” (days since last modification)

Repository Contents

africom_hist_usage_graph.py – Main script loading SharePoint data, processing it, and generating the visualizations.

utils.py – Helper functions for plotting and color mapping:

hierarchy_pos – Computes node positions for a NetworkX tree layout

plot_time – Builds an interactive time-series of activity

get_color / get_color_from_df – Maps document “age” into colors for the folder tree

africom_library_requirements_histusage.txt – List of Python libraries required to run the script

1. Installation & Environment Setup
Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

Install required packages
pip install pandas numpy matplotlib networkx requests plotly


(Modules like os and datetime are part of the Python standard library.)

Ensure africom_hist_usage_graph.py, utils.py, and your data files are stored in the same directory, so the utils import resolves correctly.

2. Preparing the SharePoint Data

The script expects SharePoint document-usage data in one of two forms:

Option A — .iqy Web Query file (preferred)

Export usage or document library data from SharePoint as an Excel Web Query (query.iqy)

Save query.iqy into the project folder

When the script runs, it will attempt to:

Read the URL stored in query.iqy

Download a fresh CSV named africom_sharepoint_query.csv

If a 401 Unauthorized occurs:

Open query.iqy in Excel

Refresh the data using your credentials

Save the output as africom_sharepoint_query.csv

Re-run the script

Option B — Pre-saved CSV

If you already have the export, save it as:

africom_sharepoint_query.csv


Place it in the project folder and the script will load it automatically.

Required Columns

Your CSV must include:

Path – The full folder/file path in SharePoint

Modified – Last modified timestamp for that item

3. Running the Script

Once the environment and dataset are ready:

python africom_hist_usage_graph.py

What the script does:

Validates that the utils module is imported correctly

Loads data from africom_sharepoint_query.csv

Processes the data:

Converts Modified → date

Aggregates by Path

Computes age (days since last modification)

Assigns colors based on age (green → recent, red → stale)

Generates visualizations:

Time-series chart of document activity using plot_time

Hierarchical folder tree built from the Path structure

Node colors correspond to document age

Plots open interactively in your notebook or browser depending on your configuration.

4. Interpreting the Outputs
Time-Series Plot (Activity Over Time)

X-axis: calendar date

Y-axis: number of document events

Helps identify periods of high or low document activity

Hierarchical Folder Tree

Each node corresponds to a folder or file

Node color indicates recency:

Green: recently modified

Yellow/Orange: moderate age

Red: stale content

Useful for:

Finding heavily used areas of the repository

Identifying content candidates for archiving

Prioritizing documents for tagging, knowledge-graph creation, or LLM ingestion

5. Customization

You can adjust behavior by editing utils.py or africom_hist_usage_graph.py:

Modify color thresholds in get_color

Change time-resampling (breaks in plot_time)

Adjust figure size or node size in the tree graph

Update CSV paths or column names if your exports differ

6. Troubleshooting
KeyError: 'Path' or 'Modified' not found

Ensure your CSV contains these exact column names, or update the script.

401 Unauthorized for .iqy downloads

Open the .iqy in Excel, refresh with your credentials, save a local CSV, and rerun the script.

Missing Python library

Reinstall via:

pip install <library-name>


Verify your virtual environment is active.

Plots not appearing

Some IDEs require configuring the Plotly renderer or running inside a Jupyter environment.

Purpose of This Library

This tool provides a quick, low-overhead method to understand usage patterns in large collections of SharePoint documents. While it does not interpret content, it highlights where the most activity occurs and which documents are most likely to be relevant—helping focus deeper analytic, cataloging, or AI/ML work.
