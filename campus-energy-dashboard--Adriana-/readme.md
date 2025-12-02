# 📘 Energy Consumption Analytics – Capstone Project
## Objective
Build an end-to-end data pipeline that automatically ingests, cleans, analyzes, visualizes, and summarizes campus energy-usage data across multiple buildings.
## Dataset Source
CSV files stored in the /data/ folder
Filenames represent buildings and months (e.g., BuildingA_2024-01.csv)
Each file includes hourly readings:-
timestamp,kwh
2024-01-01 00:00,50
2024-01-01 01:00,42
Metadata (building, month) is extracted from filenames.
## Methodology
### Data Ingestion
Auto-detect CSV files
Clean column names, fix BOM issues
Convert timestamps to datetime
Merge all building files into one DataFrame
### Aggregation
Daily totals via resample("D")
Weekly totals via resample("W")
Building-level summary (mean, min, max, total kWh)
### OOP Modeling
Building, MeterReading, and BuildingManager classes
Supports scalable building-level reporting
### Visualization
Dashboard with daily trends, weekly comparisons, and peak-hour scatter
Saved as output/dashboard.png
### Reporting
Export cleaned data (cleaned_energy_data.csv)
Export building summary (building_summary.csv)
Generate executive summary (summary.txt)
## Insights
Identifies highest-consuming buildings
Highlights peak load hours
Shows daily and weekly usage patterns
Enables comparison of energy efficiency across buildings
# 📁 Output Structure
### project-folder/
│
### data/
#### BuildingA_2024-01.csv
#### BuildingB_2024-01.csv
#### ... (add more CSV files here)
│
### output/
#### cleaned_energy_data.csv      → Cleaned + merged full dataset
#### building_summary.csv         → Stats per building (mean, min, max, total)
#### dashboard.png                → Combined matplotlib dashboard (3 plots)
#### summary.txt                  → Executive summary report
#### ingestion.log                → Log of read files + errors
│
#### ingest.py
#### aggregations.py
#### visualize.py
#### summary.py
#### run_all.py                       → Main script you run

