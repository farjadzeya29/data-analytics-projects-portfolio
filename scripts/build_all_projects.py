#!/usr/bin/env python3
"""
Master Builder for Farjad Zeya's 4 Data Analytics Portfolio Projects:
1. E-Commerce Customer & Sales Analytics (SQL, Python, Power BI)
2. Banking Customer Churn & Retention Analysis (SQL, Python, Power BI)
3. Supply Chain & Delivery Performance Analytics (SQL, Excel, Power BI)
4. Marketing Campaign & Customer Conversion Analytics (SQL, Python, Power BI)

Generates:
- Complete file structures
- Synthetic datasets (raw with realistic quirks + processed cleaned)
- MySQL SQL scripts (schema, data analysis, advanced queries)
- Python pipelines (cleaning, analysis, visualization, data generation)
- Jupyter Notebooks (.ipynb JSON)
- Power BI Specifications & DAX measures
- Business Insights Reports
- Streamlit interactive apps
- Requirements.txt, .gitignore, LICENSE
- Comprehensive 18-section README.md for each project
- Root PORTFOLIO_README.md
- React JSON data bundles for the interactive web showcase
"""

import os
import csv
import json
import random
import math
from datetime import datetime, timedelta

random.seed(42)

BASE_DIR = "/projects"
REACT_DATA_DIR = "/src/data"

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(REACT_DATA_DIR, exist_ok=True)

print("Starting generation of all 4 Data Analytics projects...")
