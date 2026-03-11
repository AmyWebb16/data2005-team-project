# [IoT Sensor ] - DATA 2005 Team Project

**TU850-2:** DATA 2005 - Data-Centric Programming  
**Assessment:** Team Data Processing Project (20%)

## Team Members

| Name | Role | GitHub |
|------|------|--------|
| Lok Ching Tam | Data Engineer | lokChingt |
| Karla Satrapova | Data Analyst | ksatrapova |
| Amy Webb | Visualization Lead | AmyWebb16 |
| Amy Webb | Documentation Lead | AmyWebb16|

## Project Description

[Brief description of your project and chosen domain]

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