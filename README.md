# Drone Proliferation Data Analysis Project

A comprehensive data analysis project that examines global drone proliferation trends using **PySpark** for distributed data processing, **Seaborn** for statistical visualizations, and **Folium** for interactive geographic mapping.

## 🚁 Project Overview

This project analyzes drone sighting data to identify patterns and trends in drone proliferation worldwide. It demonstrates the integration of:

- **PySpark**: Distributed data processing and analysis at scale
- **Seaborn**: Beautiful statistical visualizations and plots
- **Folium**: Interactive geographic maps with clustered markers and heatmaps

## 📊 Features

### Data Processing (PySpark)
- Generates synthetic drone sighting data with realistic attributes
- Processes data using distributed computing with PySpark
- Performs aggregations and statistical analysis:
  - Sightings by drone type
  - Geographic distribution by country
  - Average flight altitudes
  - Time-based proliferation trends

### Statistical Visualizations (Seaborn)
- **Bar Charts**: Drone sightings by type and country
- **Time Series**: Drone proliferation trends over time
- **Histograms**: Distribution of flight altitudes
- **Scatter Plots**: Correlation between duration and altitude
- All visualizations with professional styling and clear labels

### Geographic Visualizations (Folium)
- **Interactive Map**: Clickable markers for each drone sighting
- **Marker Clusters**: Automatic grouping for better visualization
- **Heat Map**: Density visualization of drone activity
- **Color-coded Icons**: Different colors for different drone types
- **Detailed Popups**: Full information for each sighting

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Java 8 or higher (required for PySpark)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/guerr3/drone_datavisz_project.git
cd drone_datavisz_project
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the analysis script:

```bash
python drone_analysis.py
```

The script will:
1. Generate 1,000 synthetic drone sighting records
2. Process the data using PySpark
3. Display analysis results in the console
4. Generate two output files:
   - `drone_analysis_seaborn.png` - Statistical visualizations
   - `drone_proliferation_map.html` - Interactive map

### Viewing Results

**Statistical Visualizations:**
Open `drone_analysis_seaborn.png` with any image viewer to see:
- Drone sightings by type and country
- Time series of proliferation trends
- Altitude distributions
- Duration vs. altitude correlations

**Interactive Map:**
Open `drone_proliferation_map.html` in a web browser to explore:
- Individual drone sightings with detailed information
- Clustered markers that expand on zoom
- Heat map overlay showing concentration areas
- Toggle between different layers

## 📦 Dependencies

- **pyspark** (3.5.0): Distributed data processing engine
- **pandas** (2.1.4): Data manipulation and analysis
- **numpy** (1.26.2): Numerical computing
- **seaborn** (0.13.0): Statistical data visualization
- **matplotlib** (3.8.2): Plotting library
- **folium** (0.15.1): Interactive maps

## 📈 Sample Data

The project generates synthetic data with the following attributes:
- **Drone ID**: Unique identifier
- **Date**: Sighting date (2020-2024)
- **Location**: City, country, and coordinates
- **Drone Type**: Recreational, Commercial, Military, Racing, or Photography
- **Altitude**: Flight altitude in meters
- **Duration**: Flight duration in minutes

Data covers 10 major cities worldwide:
- New York, Los Angeles, Chicago (USA)
- London (UK), Paris (France)
- Tokyo (Japan), Sydney (Australia)
- Dubai (UAE), Singapore, Toronto (Canada)

## 🎯 Analysis Insights

The analysis provides insights into:
1. **Type Distribution**: Which drone types are most common
2. **Geographic Patterns**: Where drones are most frequently sighted
3. **Temporal Trends**: How drone usage has changed over time
4. **Operational Patterns**: Typical flight altitudes and durations
5. **Regional Differences**: Variations in drone usage across countries

## 🔧 Customization

You can customize the analysis by modifying:

- **Data size**: Change `num_records` in `generate_drone_data()`
- **Cities**: Add or modify cities in the `cities` list
- **Drone types**: Adjust the `drone_types` list
- **Visualizations**: Modify plot types and styles in the visualization functions
- **Map appearance**: Change Folium map tiles, zoom levels, and styling

## 📝 License

This project is open source and available for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with PySpark, Seaborn, and Folium** 🚁📊🗺️