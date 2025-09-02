# Graph Generator

Interactive Flask web application for generating beautiful graphs from CSV data with drag-and-drop functionality and configurable styling options.

## Features

- **Drag & Drop Interface**: Simply drag and drop your CSV file to get started
- **Multiple Graph Types**: 
  - Scatter Plot
  - Single Axis Line Chart
  - Dual Axis Line Chart
  - Scatter on Map
- **Interactive Graphs**: Powered by Plotly for zoom, pan, and hover interactions.  See https://plotly.com/python/ for information on the graphs.
- **Configurable Styling**: Customize titles, axis labels, and ranges
- **Light/Dark Mode Toggle**: Switch between dark and light themes for the plotly graphs
- **Responsive Design**: Works on desktop and mobile devices
- **Download & Fullscreen**: Export graphs as PNG or view in fullscreen

## Installation

### Option 1: Quick Setup with Scripts

**On macOS/Linux:**
```bash
chmod +x deploy_setup.sh
./deploy_setup.sh
```

**On Windows:**
```cmd
deploy_setup.bat
```

### Option 2: Manual Setup

1. **Clone or download the project files**

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
   ```

3. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python3 app.py
   ```

5. **Access the application**:
   - Open your browser and go to `http://localhost:5001`
   - The app will be available on your local network at `http://[your-ip]:5001`

## Offline Capability

**This application works completely offline!**

- All dependencies are included locally
- Custom SVG icons instead of external icon libraries
- No internet connection required after installation
- Perfect for air-gapped networks or offline environments
- Test offline capability: `python3 test_offline.py`

### Custom Graphics

The application uses **external SVG files** stored in `static/images/icons/`:
- **Chart Icons**: Line charts, bar charts, scatter plots
- **UI Icons**: Upload, download, settings, info, etc.
- **Action Icons**: Generate, reset, expand, etc.

All icons are styled with `static/css/icons.css` and work completely offline.

**Icon Features:**
- **Easy Manual Updates**: Edit SVG files directly without touching HTML
- **External File References**: Icons are loaded from local file paths
- **Responsive Sizing**: Icons scale properly with text using em units
- **Consistent Styling**: All icons use the same stroke width and styling
- **Color Inheritance**: Icons inherit colors from their parent elements
- **Flexible Layout**: Icons align properly in headers, buttons, and text

**For detailed icon update instructions, see:** `SVG_UPDATE_GUIDE.md`

## Configuration

### Host Configuration
To change the hosting configuration, edit the `HOST` and `PORT` variables in `app.py`:

```python
# For localhost only
HOST = '127.0.0.1'

# For network access (default)
HOST = '0.0.0.0'

PORT = 5001  # Change port if needed
```

## Usage

### 1. Upload Data File
- Drag and drop your data file onto the upload area
- Or click "Browse Files" to select a file
- Supported formats: CSV, TXT, LOG, JSON, ZIP
- The app will automatically detect columns and data types for csvs

### 2. Configure Graph
- **Select Graph Type**: Choose from Scatter Plot, Single Line Chart, Scatter on Map, or Dual Axis Line Chart
- **Column Selection**: 
  - X-Axis: Any column from your CSV
  - Y-Axis: Numeric columns only
  - Y2-Axis: For dual axis charts (numeric columns only)
- **Styling Options**:
  - Graph Title
  - X-Axis Title
  - Y-Axis Title
  - Y2-Axis Title (for dual axis charts)
  - Light/Dark Mode Toggle for graphs
- **Axis Range**: Set custom min/max values for each axis (optional)

### 3. Generate Graph
- Click "Generate Graph" to create your visualization
- The graph will appear with full Plotly interactivity

### 4. Export Options
- **Download**: Save the graph as a PNG file
- **Fullscreen**: View the graph in fullscreen mode

## Supported File Formats

The application supports multiple file formats for data visualization:

### CSV Files
- Standard comma-separated values
- Header row (column names)
- Mixed data types (text and numeric)

### Text Files (.txt)
- Tab-separated values
- Comma-separated values
- Space-separated values
- Automatic delimiter detection

### Log Files (.log)
- Space or tab-separated data
- Common log file formats
- Automatic parsing

### JSON Files (.json)
- JSON array of objects
- JSON object with data arrays
- Structured data format

### ZIP Files (.zip)
- Archive containing CSV files
- Automatically extracts and reads first CSV file
- Useful for compressed data files

### General Requirements
- Header row with column names (for CSV, TXT, LOG)
- Mixed data types (text and numeric)
- **Maximum file size: 1 GB**

### File Size Configuration
The application is configured to handle files up to **1 GB** by default.

**Current setting in `app.py`:**
```python
MAX_FILE_SIZE_MB = 1024  # 1 GB maximum file size
```

**To change this limit:**
1. Edit the `MAX_FILE_SIZE_MB` variable in `app.py`
2. Restart the application

**Note**: Very large files (>100MB) may take longer to process and require more memory. Files approaching 1 GB may take several minutes to upload and process.

## Graph Types

### Scatter Plot
- Perfect for showing relationships between two variables
- Each point represents a data row
- Customizable point size and color

### Single Axis Line Chart
- Ideal for time series data or continuous relationships
- Lines connect data points in order
- Single Y-axis for one data series

### Dual Axis Line Chart
- Compare two data series with different scales
- Primary Y-axis on the left
- Secondary Y-axis on the right
- Different colors for each series

## Scatter On Map
- plots values as a funtion of lat / lon
- Can vary the size and color of the dots to specify value ranges

## Technical Details

### Backend
- **Framework**: Flask (Python)
- **Data Processing**: Pandas
- **Graph Generation**: Plotly
- **File Handling**: Werkzeug

### Frontend
- **Styling**: Modern CSS with dark theme
- **Interactions**: Vanilla JavaScript
- **Graph Library**: Plotly.js
- **Icons**: Font Awesome

### File Structure
```
csv-graph-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend functionality
└── uploads/              # Temporary file storage
```

## Customization

### Theme Colors
Edit `static/css/style.css` to customize the color scheme:
- Primary blue: `#2196F3`
- Success green: `#4CAF50`
- Background: `#0f1419` to `#1a1f2e`

### Graph Styling
Modify the graph generation functions in `app.py` to customize:
- Default colors
- Marker styles
- Grid appearance
- Font settings

## Troubleshooting

### Common Issues

1. **File Upload Fails**
   - Ensure the file is a valid CSV format
   - Check file size (max 16MB)
   - Verify file permissions

2. **Graph Not Generating**
   - Select required columns for your graph type
   - Ensure Y-axis columns contain numeric data
   - Check browser console for JavaScript errors

3. **Port Already in Use**
   - Change the `PORT` variable in `app.py`
   - Or kill the process using the current port

### Browser Compatibility
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Security Notes

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.
