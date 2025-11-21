
# Ask Sage Documentation Upload Example 

**Author:** Mark Espinoza - mark.espinoza@asksage.ai

---

## Overview

This repository contains a Jupyter notebook and supporting files for uploading documentation files into a single Ask Sage dataset for one tenant. This is an example workflow and should be adapted for your own use case. 
**Key points:**
- Only one tenant and one dataset are supported per run.
- Only your Ask Sage email and API key are required.
- The notebook scans the `docs/` directory for **Word (.docx, .doc), PowerPoint (.pptx, .ppt), and PDF (.pdf) files only** and uploads them to the configured dataset.
- Other file types are excluded by default and should not be ingested unless you know what you are doing and have updated the code accordingly.
- Upload status and verification are tracked in `ingestion_log.csv`.

---

## Prerequisites

1. **Python 3.8+**
2. **Jupyter Notebook or VS Code**
3. **Ask Sage API Credentials**
   - You need your Ask Sage account email and API key
4. **Network Access**
   - Ensure outbound HTTPS connectivity to the Ask Sage API

---

## Setup Instructions

### 1. Prepare Credentials

Create a `.env` file in this directory with your Ask Sage account email and API key. Example:

```env
EMAIL=your_email@example.com
API_KEY=your_api_key_here
```

**Note:** The `.env` file is required for authentication. Do not commit this file to source control.

### 2. Install Dependencies

Install required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Open the Notebook

Open `docs-uploading-script.ipynb` in Jupyter or VS Code.

### 4. Run the Workflow

Execute all cells in order. The notebook will:

1. Load your email and API key from `.env` and initialize the Ask Sage client.
2. Fetch available datasets and select the target dataset for uploading documentation.
3. Scan the `docs/` directory for supported document files (**Word, PDF, PowerPoint only**).
4. Load or create `ingestion_log.csv` to track file status.
5. Fetch the current list of ingested files from the Ask Sage API.
6. Reconcile local and remote file lists, categorizing files as new, modified, unchanged, or deleted.
7. Delete modified files from the dataset before re-uploading.
8. Upload new and modified files to the dataset (default: 5 files per run for testing; set `UPLOAD_LIMIT = 'ALL'` to upload all files).
9. Verify ingestion status and update the log accordingly.
10. Log all actions, results, and errors for troubleshooting.
11. Clean up temporary files after completion.

---

## File Descriptions

- `docs-uploading-script.ipynb`: Main notebook containing the upload, verification, and logging workflow for a single tenant and dataset.
- `requirements.txt`: Python dependencies for the script.
- `ingestion_log.csv`: Persistent log tracking ingested files, status, and verification.
- Temporary files: `files_to_upload.csv`, `upload_progress.csv`, `files_to_delete.csv` (deleted at the end).

---

## Output

- `ingestion_log.csv`: Tracks all ingested files, their status, ingestion dates, and verification.
- Console and notebook output: Progress, analysis summaries, and error messages are printed during execution.

---

## Customization

- **Upload Limit:** Change the number of files uploaded per run by modifying `UPLOAD_LIMIT` in the notebook (`5` by default, set to `'ALL'` for full upload).
- **Directory Path:** Adjust the source directory for documentation files as needed (default: `docs/`).
- **API Endpoint and Dataset Name:** You may need to update the API base URLs (`USER_BASE_URL`, `SERVER_BASE_URL`) and the specific name of the dataset in the notebook to match your Ask Sage environment and target dataset.

---

## Troubleshooting

- **API Connectivity Errors:** Check your `.env` file, network access, and API endpoint.
- **Missing Dependencies:** Ensure all packages in `requirements.txt` are installed.
- **Authentication Failures:** Verify your email and API key in `.env`.
- **File Not Uploading:** Check notebook output for error messages and review `ingestion_log.csv`.
- **Verification Pending/Failed:** Use the verification workflow in the notebook to re-check and update file statuses.

**Tips:**
- Always run the notebook from the correct directory to ensure relative paths resolve.
- Do not share or commit your `.env` file.
- Do **not** bulk upload all files at once—prefer uploading a small batch of files at a time for reliability and easier troubleshooting.
- Avoid parallel uploading of more than 10 files at a time. If you do parallel uploads, add a time buffer between batches to avoid API rate limits and ingestion errors.
- Do **not** store tabular or structured data (such as CSV, Excel, or database exports) in an Ask Sage dataset. Only unstructured documents (Word, PowerPoint, PDF) are recommended.

---

## Contact & Support

For questions or troubleshooting, contact Mark Espinoza <mark.espinoza@asksage.ai>

---

## Note

This notebook is an example for a single tenant and dataset. For advanced workflows, you must refactor and extend the code.

**Supported file types:** Only Word, PowerPoint, and PDF files are ingested by default. Other types are ignored unless you intentionally modify the code to include them.

**API URLs and Dataset Name:** The notebook uses default API base URLs and a filter string for the dataset name. You may need to update these values to match your environment and the specific dataset you want to use.
