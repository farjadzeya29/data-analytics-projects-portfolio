#!/usr/bin/env python3
"""
Adds valid Jupyter Notebooks to all 4 projects and exports data to React applet
"""

import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")

def create_notebook(proj_dir, title, desc, code_cells):
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n",
                    f"**Author:** Farjad Zeya (Data Analyst)  \n",
                    f"**Description:** {desc}\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    for c in code_cells:
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in c.split("\n")]
        })
        
    nb_path = os.path.join(proj_dir, "notebooks/exploratory_analysis.ipynb")
    os.makedirs(os.path.dirname(nb_path), exist_ok=True)
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebook: {nb_path}")

# P1 Notebook
create_notebook(
    os.path.join(PROJECTS_DIR, "01-ecommerce-customer-sales-analytics"),
    "E-Commerce Customer & Sales Analytics — Exploratory Data Analysis",
    "Comprehensive EDA examining sales distributions, product profitability, and customer RFM quantiles.",
    [
        "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n# Load cleaned dataset\ndf = pd.read_csv('../data/processed/ecommerce_transactions_cleaned.csv')\ndf['order_date'] = pd.to_datetime(df['order_date'])\nprint(f'Loaded {len(df)} transactions.')\ndf.head()",
        "# Overall Executive KPIs\ntotal_sales = df['sales'].sum()\ntotal_profit = df['profit'].sum()\nmargin = (total_profit / total_sales) * 100\nprint(f'Total Sales: ${total_sales:,.2f}')\nprint(f'Total Profit: ${total_profit:,.2f}')\nprint(f'Profit Margin: {margin:.2f}%')",
        "# Category Performance Breakdown\ncat_perf = df.groupby('category').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'count'})\ncat_perf['margin_pct'] = (cat_perf['profit'] / cat_perf['sales']) * 100\ncat_perf.round(2)",
        "# RFM Segmentation\nrfm = pd.read_csv('../data/processed/ecommerce_customers_rfm.csv')\nrfm['rfm_segment'].value_counts()"
    ]
)

# P2 Notebook
create_notebook(
    os.path.join(PROJECTS_DIR, "02-banking-customer-churn-retention"),
    "Banking Customer Churn & Retention — Exploratory Data Analysis",
    "Statistical evaluation of account attrition patterns across product count, geography, and activity.",
    [
        "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('../data/processed/banking_churn_cleaned.csv')\nprint(f'Loaded {len(df)} customer records.')\ndf.head()",
        "# Overall Churn Rate\nchurn_rate = df['exited'].mean() * 100\nprint(f'Overall Customer Attrition: {churn_rate:.2f}%')",
        "# Multi-Product Paradox\nprod_churn = df.groupby('num_of_products').agg(total=('customer_id', 'count'), churned=('exited', 'sum'))\nprod_churn['rate'] = (prod_churn['churned'] / prod_churn['total']) * 100\nprod_churn.round(2)",
        "# Active vs Inactive Member Attrition\ndf.groupby('is_active_member')['exited'].mean() * 100"
    ]
)

# P3 Notebook
create_notebook(
    os.path.join(PROJECTS_DIR, "03-supply-chain-delivery-analytics"),
    "Supply Chain & Delivery Performance — Logistics EDA",
    "Detailed evaluation of On-Time Delivery (OTD %), delay distributions, and warehouse dispatch latency.",
    [
        "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('../data/processed/supply_chain_shipments_cleaned.csv')\nprint(f'Loaded {len(df)} commercial shipments.')\ndf.head()",
        "# Network OTD Benchmark\notd = df['on_time_flag'].mean() * 100\navg_delay = df[df['delivery_status'] == 'Delayed']['delivery_delay_days'].mean()\nprint(f'Network OTD: {otd:.2f}%')\nprint(f'Average Delay Duration: {avg_delay:.2f} days')",
        "# Warehouse Hub Fulfillment\nwh_summary = df.groupby('origin_warehouse').agg(shipments=('shipment_id', 'count'), ontime=('on_time_flag', 'sum'))\nwh_summary['otd_pct'] = (wh_summary['ontime'] / wh_summary['shipments']) * 100\nwh_summary.round(2)"
    ]
)

# P4 Notebook
create_notebook(
    os.path.join(PROJECTS_DIR, "04-marketing-campaign-conversion-analytics"),
    "Marketing Campaign & Customer Conversion — Funnel EDA",
    "Lead-to-customer conversion funnel progression, unit CAC, and ROAS channel attribution.",
    [
        "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('../data/processed/marketing_leads_cleaned.csv')\nprint(f'Loaded {len(df)} leads.')\ndf.head()",
        "# Conversion Funnel Volume\nprint('Leads:', len(df))\nprint('MQL:', df['is_mql'].sum())\nprint('SQL:', df['is_sql'].sum())\nprint('Opp:', df['is_opportunity'].sum())\nprint('Won:', df['is_customer'].sum())",
        "# Channel Performance\nch_summary = df.groupby('marketing_channel').agg(leads=('lead_id', 'count'), won=('is_customer', 'sum'), revenue=('deal_value_usd', 'sum'))\nch_summary.round(2)"
    ]
)

# Run export_to_react.py to refresh portfolioData.ts
os.system("python3 ./scripts/export_to_react.py")
print("Notebooks created and portfolioData.ts refreshed!")
