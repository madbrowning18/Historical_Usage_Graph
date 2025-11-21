# Historical_Usage_Graph
Visual Depiction of Historical Usage of Documents
AFRICOM Historical Usage Graph Library

This small library builds exploratory visualizations of AFRICOM SharePoint activity to help identify high-value documents and folders for follow-on cataloging, LLM ingestion, and knowledge-graph construction. It pulls usage data from a SharePoint Web Query (.iqy) or a saved CSV, cleans and aggregates the data, and then generates:

A time-series plot of document activity. 

africom_hist_usage_graph

A hierarchical folder tree colored by document “age” (days since last modification). 

africom_hist_usage_graph

Repository Contents

africom_hist_usage_graph.py – Main script that loads SharePoint data, processes it, and generates the visualizations. 

africom_hist_usage_graph

utils.py – Helper functions for plotting and color mapping:

hierarchy_pos – Computes node positions for a tree layout using NetworkX.

plot_time – Builds an interactive time-series of activity.

get_color / get_color_from_df – Map document “age” to colors for the folder tree. 

utils

africom_library_requirements_histusage.txt – List of Python libraries required to run the script. 

africom_library_requirements_hi…

1. Installation & Environment Setup

Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows


Install required packages.
From the project folder, run:

pip install pandas numpy matplotlib networkx requests plotly


(Packages like os and datetime are part of the Python standard library and don’t need to be installed separately.) 

africom_library_requirements_hi…

Make sure the three files (africom_hist_usage_graph.py, utils.py, and your data files) are in the same directory so the utils import works correctly.

2. Preparing the SharePoint Data

The script expects AFRICOM SharePoint usage data in one of two forms: 

africom_hist_usage_graph

Preferred – .iqy Web Query file

Export usage or document library data from SharePoint as an Excel Web Query (query.iqy) and save it into this project folder as query.iqy.

When you run the script, it will:

Read the URL from query.iqy.

Attempt to download a fresh CSV (africom_sharepoint_query.csv) via HTTP.

If it receives a 401 Unauthorized, follow the console instructions:

Open query.iqy in Excel.

Refresh the data with your SharePoint credentials.

Save the results as africom_sharepoint_query.csv in this same folder.

Re-run the script.

Alternative – Pre-saved CSV

If you already have a SharePoint export, save it as:

africom_sharepoint_query.csv


Place it in the project folder. The script will detect and load it directly.

The CSV must contain at least the following columns:

Path – Full folder/file path in SharePoint.

Modified – Last modified date/time for the item. 

africom_hist_usage_graph

3. Running the Script

Once your environment and data are ready:

python africom_hist_usage_graph.py


What the script does: 

africom_hist_usage_graph

Confirms the utils import and prints its file location.

Loads data from africom_sharepoint_query.csv, either downloaded from query.iqy or provided manually.

Processes the data:

Converts Modified to a datetime column date.

Groups by Path to compute the most recent modification date per path.

Computes age (days since last modification).

Assigns a color based on age (green → recently modified, red → stale).

Generates visualizations:

A time-series line chart of document activity over time using plot_time from utils.py.

A hierarchical folder tree using the Path values and NetworkX, with node colors driven by age and the color mapping functions in utils.py.

The plots are interactive (using Plotly and Matplotlib) and open in your browser or notebook, depending on your environment.

4. Interpreting the Outputs

Time-Series Plot (Activity Over Time)

X-axis: calendar time.

Y-axis: count of document modifications (or events) in the chosen interval.

Use this view to spot spikes in activity, exercises, or surges tied to specific operations.

Hierarchical Folder Tree

Each node is a folder or file derived from the Path hierarchy.

Node color reflects recency of modification:

Green: recently modified.

Yellow/Orange: moderate age.

Red: older or potentially stale content.

Use this view to identify:

Heavily used areas of the SharePoint structure.

Cold zones that may be candidates for archiving.

Priority candidates for metadata tagging, KG building, or LLM ingestion.

5. Customization

You can customize several aspects by editing utils.py or africom_hist_usage_graph.py:

Color thresholds (in get_color) to reflect your own age bands.

Resampling frequency (breaks argument in plot_time) to switch between daily, weekly, or monthly activity.

Figure size and node size in the folder tree plotting call to match your display or slide needs.

Input CSV path or column names, if your SharePoint export uses different headers.

6. Troubleshooting

KeyError: 'Path' or 'Modified' not found

Confirm your CSV includes both columns with these exact names, or adjust the script to match your actual column headers.

401 / authentication issues when downloading from .iqy

Use Excel with query.iqy to refresh the query and save a local CSV, as described above.

ModuleNotFoundError for a library

Re-run pip install for the missing package, or verify your virtual environment is activated.

Plots not appearing

In some IDEs you may need to configure the Plotly renderer or ensure the script is run in an environment that supports interactive plots (e.g., Jupyter, VS Code with Python extension, or a browser).

This library is intentionally minimal and designed as a first step in AFRICOM’s knowledge-management pipeline: it doesn’t interpret content, but it surfaces where people are working and what is active, providing a prioritized list of documents and paths for deeper AI/ML analysis.
