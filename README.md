Logistics Operations KPI Dashboard

A Python-based data project that simulates a logistics operations reporting workflow.

The project generates a synthetic shipment dataset, cleans and validates the data, calculates operational KPIs, exports processed CSV files, and produces a final HTML dashboard with charts and business insights.

This project is designed as a portfolio case study for data, operations, logistics, supply chain, KPI reporting, and process improvement roles.

---

Dashboard Preview

"Dashboard preview" (report/screenshots/dashboard_preview.png)

Final dashboard output:

"report/dashboard_logistica.html"

---

Project Workflow

Synthetic data generation
        ↓
Data cleaning and validation
        ↓
KPI calculation
        ↓
CSV export
        ↓
Notebook analysis
        ↓
HTML dashboard generation

---

Main Features

- Synthetic logistics dataset generation
- Data cleaning and validation
- Operational KPI calculation
- Grouped KPI analysis by carrier, station, and exception type
- Reproducible pipeline with fixed random seed
- Final HTML dashboard generated from Python scripts
- Jupyter Notebook analysis
- GitHub-ready project structure

---

KPIs Calculated

The project calculates:

- Total shipments
- Total packages
- Delivered packages
- Failed packages
- Delivery success rate
- Failed delivery rate
- Average delay
- Delayed shipments
- Percentage of delayed shipments
- Top operational exceptions

---

Folder Structure

dashboard_kpi_logistica
│   main.py
│   README.md
│   requirements.txt
│
├── dati
│   ├── grezzi
│   │   └── shipments.csv
│   └── elaborati
│       ├── shipments_clean.csv
│       ├── kpi_generali.csv
│       ├── kpi_carrier.csv
│       ├── kpi_station.csv
│       └── kpi_anomalie.csv
│
├── documenti
│   └── dizionario_dati.md
│
├── notebooks
│   └── logistics_kpi_analysis.ipynb
│
├── report
│   ├── dashboard_logistica.html
│   ├── kpi_report.txt
│   ├── grafici
│   │   ├── anomalie_principali.png
│   │   ├── failed_rate_carrier.png
│   │   └── ritardo_medio_station.png
│   └── screenshots
│       └── dashboard_preview.png
│
└── sorgente
    ├── calcola_kpi.py
    ├── genera_dashboard_html.py
    ├── genera_dati_finti.py
    ├── pulisci_dati.py
    └── utils.py

---

Dataset

The dataset is synthetically generated for portfolio and learning purposes.

Each row represents one logistics shipment or operational route.

Field| Description
"shipment_id"| Unique shipment identifier
"date"| Shipment date
"station"| Logistics station
"carrier"| Delivery carrier
"route_id"| Route identifier
"planned_departure"| Planned departure time
"actual_departure"| Actual departure time
"packages"| Total packages
"delivered_packages"| Successfully delivered packages
"failed_packages"| Failed packages
"late_minutes"| Delay in minutes
"exception_type"| Main operational exception

---

Technologies Used

- Python
- CSV module
- Pathlib
- Matplotlib
- Jupyter Notebook
- HTML/CSS

All data is synthetic and generated for demonstration purposes.

---

How to Run

Install requirements:

pip install -r requirements.txt

Run the full pipeline:

python main.py

This command regenerates the synthetic dataset, cleans the data, calculates KPIs, exports CSV files, and generates the final dashboard.

To regenerate only the dashboard:

python sorgente/genera_dashboard_html.py

---

Reproducibility

The synthetic dataset generation uses a fixed random seed.

This means that running:

python main.py

will regenerate the same dataset, KPIs, charts, and final dashboard output.

---

Portfolio Value

This project demonstrates the ability to:

- Structure a Python data project
- Generate and process operational data
- Validate data quality
- Calculate logistics KPIs
- Export clean datasets for reporting
- Create a reproducible dashboard
- Document a project for GitHub

It is especially relevant for roles related to logistics operations, supply chain, operations analysis, KPI reporting, process improvement, and junior data analysis.

---

Notes

This is a portfolio project based on synthetic data.

The objective is not to replicate a full enterprise BI system, but to show a complete and reproducible data workflow from raw data to final reporting output.
