# Sample Data Files

This directory contains test files for various graph types and functionality in the Graph Generator application.

## CSV Files

### `sample_data.csv`
- **Purpose**: General testing for all graph types
- **Columns**: Date, Temperature, Humidity, Pressure, Wind_Speed
- **Use Cases**: Line charts, scatter plots, dual axis charts
- **Data**: Weather data with 15 data points

### `map_scatter_test.csv`
- **Purpose**: Testing scatter plots on maps
- **Columns**: latitude, longitude, value, size, category
- **Use Cases**: Scatter on map functionality
- **Data**: US cities with coordinates and metadata
- **Configuration Options**:
  - Title: Custom map title
  - Map Type: satellite (default), basic, carto-darkmatter, carto-positron, etc.
  - Latitude Column: latitude
  - Longitude Column: longitude
  - Hover Values: value, size, category (multiple selection)
  - Color Column: value (optional)
  - Size Column: size (optional)

## JSON Files
### `sample_data.json`
- **Purpose**: Testing JSON upload
- **Use Cases**: General JSON testing
