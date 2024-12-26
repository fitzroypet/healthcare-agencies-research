# Healthcare Agencies Research

## Overview

The Healthcare Agencies Research project is designed to analyze and visualize data related to healthcare agencies in various locations. This project provides insights into company formations, types, statuses, and geographic distributions, helping stakeholders understand the healthcare landscape better. Additionally, it integrates with the Companies House API to fetch real-time data about companies based on specific SIC codes and locations.

## Features

- **Data Loading and Cleaning**: Load and preprocess CSV data files containing information about healthcare agencies.
- **Data Visualization**: Generate various visualizations, including:
  - Company formations by year
  - Postal code distribution
  - Company types distribution
  - SIC code analysis
  - Company status over time
  - Healthcare service type distribution
  - Company age distribution
  - Geographic concentration
- **Summary Report Generation**: Create a comprehensive summary report that includes key statistics and insights derived from the data.
- **Companies House API Integration**: Fetch company data from the Companies House API based on specified SIC codes and locations.

## Technologies Used

- Python 3.x
- Pandas
- Matplotlib
- Plotly
- NumPy
- Requests
- Jupyter Notebook (optional for exploratory data analysis)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fitzroypet/healthcare-agencies-research.git
   cd healthcare-agencies-research
   ```

2. Install the required packages:
   ```bash
   pip install pandas matplotlib plotly numpy requests
   ```

3. Set up your environment variable for the Companies House API key:
   ```bash
   export COMPANIES_HOUSE_API_KEY='your_api_key_here'
   ```

## Usage

### Fetching Data from Companies House API

1. Run the API script to fetch company data:
   ```bash
   python companies_search.py
   ```

   This script will:
   - Search for companies based on specified SIC codes and location (change location and SIC codes as preferred).
   - Save the results to a CSV file in the `data` directory.

### Analyzing and Visualizing Data

1. Prepare your CSV data files in the `data` directory. The files should follow the naming convention `healthcare_agencies_<location>_<timestamp>.csv`.

2. Run the main analysis script:
   ```bash
   python visualize_data.py
   ```

   This script will:
   - Load and clean the data.
   - Generate visualizations saved in the `visualizations` directory.
   - Create a summary report saved in the `reports` directory.

## Directory Structure

```
healthcare_analysis/
└── <location>/
    └── <timestamp>/
        ├── data/
        ├── reports/
        └── visualizations/
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors and the open-source community for their support and resources.