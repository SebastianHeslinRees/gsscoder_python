# gsscoder_python

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()

> *A lightweight Python package for recoding and aggregating UK Local Authority (LA) statistics across different GSS code vintages, supporting splits and merges in administrative boundaries.*

This is a Python rebuild of the original R package that can be found [here](https://github.com/Greater-London-Authority/gsscoder/tree/main).

---

##  Overview

UK administrative geographies boundaries are constantly changing. Local authorities merge, split, rename, and reorganise - making longitudinal analysis of statistical data challenging. **gsscoder_python** attempts to address these issues by providing tool for recoding between different GSS code vintages.

---

##  Features

- 🔀 **Boundary Changes**: Handles complex LA code changes including:
  - **Splits** - When one authority becomes multiple
  - **Mergers** - When multiple authorities combine
  - **Renames** - When codes change but boundaries remain
- 📊 **Flexible Aggregation**: Supports aggregation by `sum` or `mean` for statistical accuracy


---

##  Quick Start

### Installation

Clone the repository and install locally:

```bash
git clone 
cd gsscoder_python
pip install .
```

### Basic Usage

```python
import gsscoder_python as gss

# Recode your data from 2011 to 2021 codes
recoded_data = gss.recode_gss(
    data=your_dataframe,
    from_year=2011,
    to_year=2021,
    method='sum'  # or 'mean'
)
```

---

## 📚 Documentation

For examples use cases, check out the notebooks in `/example_use/`:
- `test_package.ipynb` 

---

## 🔄 Keeping Data Current

### Package Updates

This package contains lookup tables created from the ONS Code History Database. **Internal package data must be updated whenever ONS releases a new database** (typically in **May** and **December**).

>  **Workflow follows best practices** suggested by [jennybc](https://github.com/r-lib/usethis/issues/1091)

### 📋 Update Instructions

When updating to the latest ONS Code History Database:

#### 1. **Download Latest Data**
Update the URL in `/data-raw/1_package_data.py` with the most recent version:

```python
# Current URL (update as needed):
url = "https://www.arcgis.com/sharing/rest/content/items/3acc892515aa49a8885c2deb734ebd3d/data"
```

#### 2. **Process Data Files**

Run the data processing scripts in order:

```bash
cd data-raw/
python 1_package_data.py    # Downloads and processes raw data
python 2_testthat_data.py   # Generates test data
python 3_datasets.py        # Creates final lookup tables
```

#### 3. **Update Core Files**

The following files will be automatically updated:
- `ChangeHistory.csv` - Complete history of all code changes
- `Changes.csv` - Simplified change mappings  
- `database_date.txt` - Timestamp of current database version

#### 4. **Refresh Tests**

Update test cases to validate against the latest code changes:

```bash
# Run existing tests
python -m pytest tests/

# Update test expectations if needed
# Edit test files to include new boundary changes
```

---

## 🤝 Contributing

We welcome contributions! Please feel free to:
- 🐛 Report bugs
- 💡 Suggest features  
- 📝 Improve documentation
- 🔧 Submit pull requests

---


## 📫 Contact

For questions or feedback, please reach out to [sebastian.heslin-rees@london.gov.uk].

---

## 📄 License
Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg

please email [sebastian.heslin-rees@london.gov.uk] for license infomation.

---

## 📄 Acknowledgements

- [GLA Population Projection]([https://www.gla.gov.uk](https://www.london.gov.uk/)) for the dataset.
