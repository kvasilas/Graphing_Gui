# Graphing Tool - Dash Version

A modern, interactive data visualization and analysis tool built with Plotly Dash. This application allows you to upload various data file formats and create beautiful, interactive graphs and perform data processing operations.

## Features

### 📊 Graph Types
- **Scatter Plot**: Compare two variables with customizable markers
- **Single Line Chart**: Time series and continuous data visualization
- **Dual Axis Line Chart**: Compare data with different scales on separate y-axes
- **Scatter on Map**: Geographic data visualization using interactive maps

### 📁 File Support
- **CSV files**: Comma-separated values
- **TXT files**: Text files with various delimiters (tab, comma, space)
- **LOG files**: Log files with space/tab separation
- **JSON files**: JSON data format
- **ZIP files**: Compressed archives containing CSV files

### 🔧 Data Processing
- **Summary Reports**: Basic statistics, data quality reports, column analysis
- **Data Filtering**: Filter rows based on column values
- **Statistical Analysis**: Mean, median, standard deviation, min/max calculations
- **Data Cleaning**: Remove duplicates, empty rows, standardize text, convert data types

### 🎨 User Interface
- **Dark Theme**: Modern dark interface with blue accent colors
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Notifications**: Instant feedback for all operations
- **Automatic Downloads**: Processed files download automatically
- **Interactive Graphs**: Zoom, pan, hover, and export capabilities

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. **Clone or download** this project
2. **Navigate** to the dash directory:
   ```bash
   cd dash
   ```
3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application
```bash
python app.py
```

The application will start on `http://localhost:8050`

### Basic Workflow
1. **Upload Data**: Drag and drop or select a data file
2. **Choose Operation**: Select either graph generation or data processing
3. **Configure**: Set up your visualization or processing options
4. **Execute**: Generate your graph or download processed data

### Graph Generation
1. Select a graph type from the dropdown
2. Choose X-axis and Y-axis columns
3. Optionally customize the title
4. Click "Generate Graph" to create your visualization

### Data Processing
1. Select a processing type (Summary, Filter, Statistics, Clean)
2. Configure the specific options for your chosen type
3. Click "Process File" to generate and download results

## File Size Limits
- Maximum file size: 1 GB
- Supported formats: CSV, TXT, LOG, JSON, ZIP
- Automatic file type detection and parsing

## Graph Customization

### Scatter Plot
- Multiple Y-axis variables supported
- Customizable marker size and opacity
- Hover information for data points

### Line Charts
- Single and dual-axis options
- Multiple line series with different colors
- Customizable line width and marker styles

### Scatter on Map
- Automatic latitude/longitude detection
- Color-coded data points
- Interactive map with zoom and pan
- Opens in new window for better viewing

## Data Processing Options

### Summary Reports
- **Basic Statistics**: Mean, median, std dev, quartiles for numeric columns
- **Data Quality**: Null counts, unique values, data types per column
- **Column Analysis**: Sample values, data types, unique counts

### Data Filtering
- Filter by exact value matches
- Automatic type conversion (numeric/string)
- Shows before/after row counts

### Statistical Analysis
- Calculate mean, median, standard deviation
- Find minimum and maximum values
- Applied to all numeric columns

### Data Cleaning
- Remove duplicate rows
- Remove rows with missing values
- Standardize text (lowercase, trim whitespace)
- Convert data types automatically

## Technical Details

### Architecture
- **Frontend**: Plotly Dash with Bootstrap components
- **Backend**: Python with Pandas for data processing
- **Visualization**: Plotly.js for interactive graphs
- **Theme**: Dark theme with blue accent colors

### Dependencies
- `dash`: Web application framework
- `dash-bootstrap-components`: UI components
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive visualization
- `numpy`: Numerical computing
- `gunicorn`: Production WSGI server

### Performance
- Optimized for large datasets (up to 1GB)
- Efficient memory usage with streaming file processing
- Fast graph rendering with Plotly's WebGL backend

## Deployment

### Development
```bash
python app.py
```

### Production
```bash
gunicorn app:app.server --bind 0.0.0.0:8050
```

## Browser Compatibility
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Troubleshooting

### Common Issues
1. **File upload fails**: Check file size (max 1GB) and format
2. **Graph not displaying**: Ensure data columns are selected
3. **Map not opening**: Check that latitude/longitude columns exist
4. **Download not working**: Check browser download settings

### Error Messages
- All errors are displayed as notifications in the interface
- Check the browser console for detailed error information
- Server logs provide additional debugging information

## Comparison with Flask Version

### Advantages of Dash Version
- **Native Plotly Integration**: Better performance and features
- **Reactive UI**: Real-time updates without page refreshes
- **Built-in Components**: File upload, download, notifications
- **State Management**: Automatic handling of user interactions
- **Responsive Design**: Better mobile and tablet support
- **Error Handling**: More robust error management

### Feature Parity
- All graph types from Flask version supported
- Same file format support
- Identical data processing capabilities
- Enhanced user experience with modern UI

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests, please create an issue in the project repository.
