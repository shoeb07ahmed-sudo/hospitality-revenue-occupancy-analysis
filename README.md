# Hospitality Revenue and Occupancy Analysis

An exploratory data analysis project using AtliQ Hotels booking data. The Jupyter notebook cleans and combines booking, hotel, room, and date tables to examine occupancy and revenue patterns across cities, room categories, hotel types, months, and booking platforms.

> Educational project based on the Codebasics hospitality analysis course project. Dataset and tutorial credit belongs to the original course/project authors. This repository is a personal learning portfolio; review the source terms before redistributing the data.

## Questions explored

- What is the average occupancy rate by room category and city?
- How does occupancy differ between weekdays and weekends?
- What does June occupancy look like across cities?
- How does revenue vary by city, month, hotel type, and booking platform?
- How do ratings and booking capacity relate to the analysis?

The notebook also demonstrates data exploration, handling invalid guest counts, outlier checks, occupancy percentage calculations, merging tables, appending August data, and visualizing results.

## Project structure

```text
.
├── datasets/                 # CSV input tables used by the notebook
└── hotels_analysis.ipynb     # Exploratory analysis and charts
```

## Run the notebook

Use Python 3 with Jupyter Notebook or JupyterLab. Install the libraries used by the notebook:

```bash
python -m pip install pandas numpy matplotlib jupyter
```

Then start Jupyter from the repository root and open `hotels_analysis.ipynb`. The notebook reads its CSV files from the relative `datasets/` directory.

## Data

The `datasets/` folder contains the date, hotel, and room dimensions; booking and aggregated booking facts; and the August data file used in the notebook. These files are included so the analysis can be reproduced. Please retain the attribution above if you reuse this educational project.

## Portfolio note

This repository preserves the course notebook and its exercises. Before presenting it as a finished resume project, add a short section with your own conclusions and explain what decisions the results could inform. Avoid claiming business impact unless you have independently validated it.
