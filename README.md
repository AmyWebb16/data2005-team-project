# [IoT Sensor ] - DATA 2005 Team Project

**TU850-2:** DATA 2005 - Data-Centric Programming  
**Assessment:** Team Data Processing Project (20%)

## Team Members

| Name | Role | GitHub |
|------|------|--------|
| Lok Ching Tam | Data Engineer | lokChingt |
| Karla Satrapova | Data Analyst | ksatrapova |
| Amy Webb | Visualization Lead | AmyWebb16 |
| Everyone| Documentation Lead | AmyWebb16, lokChingt, ksatrapova|

## Project Description
The goal of our project is to go through the data pipeline of data processing, analysis, and visualization to see if there are any meaningful patterns and show them through
visualizations. The dataset we have chosen is and IoT sensor dataset of three distinct sensors in diverse environments with spanning over a seven days period. It has variables of  timestamp,
device name, carbon monoxide, humidity, light detected?, liquid petroleum gas, motion detected?, smoke and temperature. We focused on a subset of those variables for our
assignment.​

## Dataset

- **Name:** Environmental Sensor Telemetry Data
- **Source:** (https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k/data )
- **Size:** 405k
- **Format:** CSV

## Project Structure
```
data2005-team-project/
├── data/
│   ├── raw/              # Original dataset files
│   │   └── .gitkeep
│   └── processed/        # Cleaned data
│       └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data_loading.py   # Data Engineer
│   ├── preprocessing.py  # Data Engineer
│   ├── analysis.py       # Data Analyst
│   └── visualization.py  # Visualization Lead
├── notebooks/
│   └── exploration.ipynb # Exploratory analysis
├── outputs/
│   ├── figures/          # Generated plots
│   │   └── .gitkeep
│   └── reports/          # Exported results
│       └── .gitkeep
├── tests/                # Unit tests (optional)
├── requirements.txt      # Dependencies
├── README.md             # Documentation
└── .gitignore            # Git ignore rules
```