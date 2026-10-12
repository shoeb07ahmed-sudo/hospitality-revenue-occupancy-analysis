# Hospitality Booking Analysis

A personal Python analytics portfolio project exploring hotel occupancy and realized revenue patterns. The analysis reports data quality checks, occupancy by room class, city and day type, June occupancy by city, and revenue by city, month and booking platform.

## Data access

This repository does not redistribute the course notebook or CSV datasets. Obtain the learning data from the [official Codebasics hospitality resource](https://codebasics.io/resources/end-to-end-data-analyst-project), then place the five required CSV files in a local `datasets/` folder:

- `dim_date.csv`
- `dim_hotels.csv`
- `dim_rooms.csv`
- `fact_aggregated_bookings.csv`
- `fact_bookings.csv`

The August update file is not required by this original analysis script. Codebasics states that unauthorized sharing of its downloaded dataset/material is prohibited; keep those source files local and follow the provider's terms.

## Run

Install Python 3 and pandas, then run from the repository root:

```bash
python -m pip install pandas
python analysis.py
```

The script prints each summary and writes CSV results under `outputs/`. Local datasets and generated results are ignored by Git.

## Skills demonstrated

- Data quality checks and explicit handling of invalid capacity and guest counts
- Joining fact and dimension tables with relationship validation
- Occupancy and revenue aggregation across business dimensions
- Reproducible CSV outputs using pandas

This is a learning project. Add independently validated business conclusions before using it to describe measured business impact on a resume.
