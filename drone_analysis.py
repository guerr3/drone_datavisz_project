"""
Drone Proliferation Data Analysis with PySpark, Seaborn, and Folium

This script analyzes drone sightings and proliferation trends using:
- PySpark for distributed data processing
- Seaborn for statistical visualizations
- Folium for interactive geographic maps
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Import PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, DateType

# Import visualization libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster, HeatMap


def generate_drone_data(num_records=1000):
    """
    Generate synthetic drone sighting data for analysis.
    
    Returns:
        list: List of tuples containing drone sighting records
    """
    # Drone types
    drone_types = ['Recreational', 'Commercial', 'Military', 'Racing', 'Photography']
    
    # Major cities with coordinates
    cities = [
        ('New York', 40.7128, -74.0060, 'USA'),
        ('Los Angeles', 34.0522, -118.2437, 'USA'),
        ('Chicago', 41.8781, -87.6298, 'USA'),
        ('London', 51.5074, -0.1278, 'UK'),
        ('Paris', 48.8566, 2.3522, 'France'),
        ('Tokyo', 35.6762, 139.6503, 'Japan'),
        ('Sydney', -33.8688, 151.2093, 'Australia'),
        ('Dubai', 25.2048, 55.2708, 'UAE'),
        ('Singapore', 1.3521, 103.8198, 'Singapore'),
        ('Toronto', 43.6532, -79.3832, 'Canada'),
    ]
    
    data = []
    start_date = datetime(2020, 1, 1)
    
    for i in range(num_records):
        # Random date within the last 4 years with increasing trend
        days_offset = random.randint(0, 365 * 4)
        date = start_date + timedelta(days=days_offset)
        
        # Select random city
        city, lat, lon, country = random.choice(cities)
        
        # Add some randomness to coordinates (within ~10km)
        lat_jitter = random.uniform(-0.1, 0.1)
        lon_jitter = random.uniform(-0.1, 0.1)
        
        # Random drone type with weighted distribution
        drone_type = random.choices(
            drone_types,
            weights=[40, 30, 10, 10, 10],
            k=1
        )[0]
        
        # Random altitude (in meters)
        altitude = random.randint(10, 400)
        
        # Random duration (in minutes)
        duration = random.randint(5, 120)
        
        # Generate ID
        drone_id = f"DRONE-{i+1:05d}"
        
        data.append((
            drone_id,
            date.strftime('%Y-%m-%d'),
            city,
            country,
            lat + lat_jitter,
            lon + lon_jitter,
            drone_type,
            altitude,
            duration
        ))
    
    return data


def create_spark_session():
    """
    Create and configure a Spark session.
    
    Returns:
        SparkSession: Configured Spark session
    """
    spark = SparkSession.builder \
        .appName("Drone Proliferation Analysis") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    
    # Set log level to reduce verbosity
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def analyze_with_pyspark(spark, data):
    """
    Analyze drone data using PySpark.
    
    Args:
        spark: SparkSession
        data: List of drone sighting records
        
    Returns:
        dict: Dictionary containing various analysis results as Pandas DataFrames
    """
    # Define schema
    schema = StructType([
        StructField("drone_id", StringType(), False),
        StructField("date", StringType(), False),
        StructField("city", StringType(), False),
        StructField("country", StringType(), False),
        StructField("latitude", DoubleType(), False),
        StructField("longitude", DoubleType(), False),
        StructField("drone_type", StringType(), False),
        StructField("altitude", IntegerType(), False),
        StructField("duration", IntegerType(), False),
    ])
    
    # Create DataFrame
    df = spark.createDataFrame(data, schema)
    
    # Convert date string to date type
    df = df.withColumn("date", col("date").cast(DateType()))
    
    # Cache for better performance
    df.cache()
    
    print("\n" + "="*70)
    print("DRONE PROLIFERATION ANALYSIS - PySpark Processing")
    print("="*70)
    
    # Basic statistics
    total_sightings = df.count()
    print(f"\nTotal Drone Sightings: {total_sightings}")
    
    # Sightings by type
    print("\n--- Sightings by Drone Type ---")
    by_type = df.groupBy("drone_type") \
        .agg(count("*").alias("count")) \
        .orderBy(col("count").desc())
    by_type.show()
    
    # Sightings by country
    print("\n--- Sightings by Country ---")
    by_country = df.groupBy("country") \
        .agg(count("*").alias("count")) \
        .orderBy(col("count").desc())
    by_country.show()
    
    # Average altitude by drone type
    print("\n--- Average Altitude by Drone Type ---")
    avg_altitude = df.groupBy("drone_type") \
        .agg(avg("altitude").alias("avg_altitude")) \
        .orderBy(col("avg_altitude").desc())
    avg_altitude.show()
    
    # Time series data (by month)
    df_with_year_month = df.withColumn("year", year("date")) \
        .withColumn("month", month("date"))
    
    time_series = df_with_year_month.groupBy("year", "month") \
        .agg(count("*").alias("count")) \
        .orderBy("year", "month")
    
    # Convert to Pandas for visualization
    results = {
        'all_data': df.toPandas(),
        'by_type': by_type.toPandas(),
        'by_country': by_country.toPandas(),
        'avg_altitude': avg_altitude.toPandas(),
        'time_series': time_series.toPandas()
    }
    
    return results


def create_seaborn_visualizations(results):
    """
    Create statistical visualizations using Seaborn.
    
    Args:
        results: Dictionary containing analysis results
        
    Returns:
        None. Saves visualizations to 'drone_analysis_seaborn.png'
    """
    print("\n" + "="*70)
    print("GENERATING SEABORN VISUALIZATIONS")
    print("="*70)
    
    # Set style
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Drone Sightings by Type (Bar Chart)
    plt.subplot(2, 3, 1)
    sns.barplot(data=results['by_type'], x='drone_type', y='count')
    plt.title('Drone Sightings by Type', fontsize=12, fontweight='bold')
    plt.xlabel('Drone Type')
    plt.ylabel('Number of Sightings')
    plt.xticks(rotation=45, ha='right')
    
    # 2. Sightings by Country (Bar Chart)
    plt.subplot(2, 3, 2)
    sns.barplot(data=results['by_country'], x='country', y='count')
    plt.title('Drone Sightings by Country', fontsize=12, fontweight='bold')
    plt.xlabel('Country')
    plt.ylabel('Number of Sightings')
    plt.xticks(rotation=45, ha='right')
    
    # 3. Average Altitude by Drone Type (Bar Chart)
    plt.subplot(2, 3, 3)
    sns.barplot(data=results['avg_altitude'], x='drone_type', y='avg_altitude')
    plt.title('Average Flight Altitude by Type', fontsize=12, fontweight='bold')
    plt.xlabel('Drone Type')
    plt.ylabel('Average Altitude (m)')
    plt.xticks(rotation=45, ha='right')
    
    # 4. Time Series - Drone Proliferation Over Time
    plt.subplot(2, 3, 4)
    ts_data = results['time_series'].copy()
    ts_data['date'] = pd.to_datetime(ts_data['year'].astype(str) + '-' + 
                                     ts_data['month'].astype(str) + '-01')
    ts_data = ts_data.sort_values('date')
    plt.plot(ts_data['date'], ts_data['count'], marker='o', linewidth=2, markersize=4)
    plt.title('Drone Proliferation Over Time', fontsize=12, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Number of Sightings')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # 5. Altitude Distribution (Histogram)
    plt.subplot(2, 3, 5)
    sns.histplot(data=results['all_data'], x='altitude', bins=30, kde=True)
    plt.title('Distribution of Flight Altitudes', fontsize=12, fontweight='bold')
    plt.xlabel('Altitude (m)')
    plt.ylabel('Frequency')
    
    # 6. Duration vs Altitude (Scatter Plot)
    plt.subplot(2, 3, 6)
    sns.scatterplot(data=results['all_data'], x='duration', y='altitude', 
                   hue='drone_type', alpha=0.6, s=50)
    plt.title('Flight Duration vs Altitude', fontsize=12, fontweight='bold')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Altitude (m)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    plt.tight_layout()
    
    # Save the figure
    output_file = 'drone_analysis_seaborn.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Seaborn visualizations saved to: {output_file}")
    
    plt.close()


def create_folium_map(results):
    """
    Create interactive geographic visualizations using Folium.
    
    Args:
        results: Dictionary containing analysis results
        
    Returns:
        None. Saves interactive map to 'drone_proliferation_map.html'
    """
    print("\n" + "="*70)
    print("GENERATING FOLIUM MAP VISUALIZATIONS")
    print("="*70)
    
    df = results['all_data']
    
    # Create base map centered on average coordinates
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 60px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; padding: 10px">
    <b>Global Drone Proliferation Map</b><br>
    Interactive visualization of drone sightings worldwide
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Create marker cluster
    marker_cluster = MarkerCluster(name='Drone Sightings').add_to(m)
    
    # Color mapping for drone types
    color_map = {
        'Recreational': 'blue',
        'Commercial': 'green',
        'Military': 'red',
        'Racing': 'orange',
        'Photography': 'purple'
    }
    
    # Add markers for each sighting
    for idx, row in df.iterrows():
        popup_html = f"""
        <div style="width: 200px">
            <h4>{row['drone_id']}</h4>
            <b>Type:</b> {row['drone_type']}<br>
            <b>Date:</b> {row['date']}<br>
            <b>Location:</b> {row['city']}, {row['country']}<br>
            <b>Altitude:</b> {row['altitude']}m<br>
            <b>Duration:</b> {row['duration']} minutes
        </div>
        """
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['drone_type']} - {row['city']}",
            icon=folium.Icon(color=color_map.get(row['drone_type'], 'gray'), 
                           icon='plane', prefix='fa')
        ).add_to(marker_cluster)
    
    # Add heat map layer
    heat_data = [[row['latitude'], row['longitude']] for idx, row in df.iterrows()]
    HeatMap(heat_data, name='Heat Map', radius=15, blur=25).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 200px; height: 180px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:12px; padding: 10px">
    <b>Drone Types:</b><br>
    <i class="fa fa-plane" style="color:blue"></i> Recreational<br>
    <i class="fa fa-plane" style="color:green"></i> Commercial<br>
    <i class="fa fa-plane" style="color:red"></i> Military<br>
    <i class="fa fa-plane" style="color:orange"></i> Racing<br>
    <i class="fa fa-plane" style="color:purple"></i> Photography
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map
    output_file = 'drone_proliferation_map.html'
    m.save(output_file)
    print(f"\n✓ Interactive Folium map saved to: {output_file}")
    print(f"  Open this file in a web browser to explore the interactive map")


def main():
    """
    Main function to run the complete drone proliferation analysis.
    
    This function orchestrates the entire analysis workflow:
    1. Generates synthetic drone sighting data
    2. Processes data using PySpark (aggregations, statistics)
    3. Creates Seaborn visualizations (saved as PNG)
    4. Creates Folium interactive map (saved as HTML)
    
    Returns:
        None. Generates output files: drone_analysis_seaborn.png and drone_proliferation_map.html
    """
    print("\n" + "="*70)
    print("DRONE PROLIFERATION DATA ANALYSIS")
    print("="*70)
    print("Analyzing drone sightings using PySpark, Seaborn, and Folium")
    print("="*70)
    
    # Generate synthetic data
    print("\n[1/4] Generating synthetic drone sighting data...")
    data = generate_drone_data(num_records=1000)
    print(f"✓ Generated {len(data)} drone sighting records")
    
    # Create Spark session
    print("\n[2/4] Initializing PySpark session...")
    spark = create_spark_session()
    print("✓ PySpark session initialized")
    
    # Analyze with PySpark
    print("\n[3/4] Analyzing data with PySpark...")
    results = analyze_with_pyspark(spark, data)
    print("✓ Analysis complete")
    
    # Create visualizations
    print("\n[4/4] Creating visualizations...")
    create_seaborn_visualizations(results)
    create_folium_map(results)
    
    # Stop Spark session
    spark.stop()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\nOutput files generated:")
    print("  - drone_analysis_seaborn.png (Statistical visualizations)")
    print("  - drone_proliferation_map.html (Interactive geographic map)")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
