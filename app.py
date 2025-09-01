import os
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# =============================================================================
# FILE SIZE CONFIGURATION
# =============================================================================
# To change the maximum file size limit, modify the MAX_FILE_SIZE_MB variable below:
# - For 50MB files: set MAX_FILE_SIZE_MB = 50
# - For 100MB files: set MAX_FILE_SIZE_MB = 100  
# - For 500MB files: set MAX_FILE_SIZE_MB = 500
# - For 1GB files: set MAX_FILE_SIZE_MB = 1024
# =============================================================================

app = Flask(__name__)
# File size configuration - set to 1 GB maximum
MAX_FILE_SIZE_MB = 1024  # 1 GB maximum file size
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Additional configurations for large file handling
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for large files
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuration for hosting
HOST = '0.0.0.0'  # Change to '127.0.0.1' for localhost only
PORT = 5001

ALLOWED_EXTENSIONS = {'csv', 'txt', 'log', 'json', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Determine file type and read accordingly
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(filepath)
                # Get column information
                columns = df.columns.tolist()
                numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'columns': columns,
                    'numeric_columns': numeric_columns,
                    'row_count': len(df),
                    'file_type': file_extension
                })

            elif file_extension in ['json', 'txt', "log"]:
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'filepath': filepath,
                    'file_type': file_extension
                })
                
            elif file_extension == 'zip':
                # Handle zip files - extract and read the first CSV file
                import zipfile
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                    if csv_files:
                        pass
                        #TODO store list of csv files and then process
                    else:
                        return jsonify({'error': 'No CSV file found in zip archive'}), 400
            else:
                return jsonify({'error': f'Unsupported file type: {file_extension}'}), 400
            
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
    else:
        return jsonify({'error': 'Invalid file type'}), 400


#TODO refactor this to properly sort out the file types and generate the appropriate graph / post process
@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    try:
        data = request.json
        filename = data.get('filename')
        graph_type = data.get('graph_type')
        config = data.get('config', {})
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Determine file type and read accordingly
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(filepath)
        elif file_extension == 'txt':
            # Try different delimiters for text files
            try:
                df = pd.read_csv(filepath, delimiter='\t')  # Tab-separated
            except:
                try:
                    df = pd.read_csv(filepath, delimiter=',')  # Comma-separated
                except:
                    df = pd.read_csv(filepath, delimiter='\s+')  # Space-separated
        elif file_extension == 'log':
            # Try to read log files as space or tab separated
            try:

                df = pd.read_csv(filepath, delimiter='\s+', engine='python')
            except:
                df = pd.read_csv(filepath, delimiter='\t')
        elif file_extension == 'json':
            df = pd.read_json(filepath)
        elif file_extension == 'zip':
            # Handle zip files - extract and read the first CSV file
            import zipfile
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                if csv_files:
                    with zip_ref.open(csv_files[0]) as csv_file:
                        df = pd.read_csv(csv_file)
                else:
                    return jsonify({'error': 'No CSV file found in zip archive'}), 400
        else:
            return jsonify({'error': f'Unsupported file type: {file_extension}'}), 400
        
        # Create graph based on type
        if graph_type == 'scatter':
            fig = create_scatter_plot(df, config)
        elif graph_type == 'single_line':
            fig = create_single_line_chart(df, config)
        elif graph_type == 'dual_line':
            fig = create_dual_line_chart(df, config)
        elif graph_type == 'scatter_on_map':
            fig = scatter_on_map(df, config)

        else:
            return jsonify({'error': 'Invalid graph type'}), 400
        
        # Convert to JSON for frontend
        graph_json = fig.to_json()
        return jsonify({'success': True, 'graph': graph_json})
        
    except Exception as e:
        return jsonify({'error': f'Error generating graph: {str(e)}'}), 400

def create_scatter_plot(df, config):
    x_col = config.get('x_column')
    y_cols = config.get('y_columns', [])
    title = config.get('title', 'Scatter Plot')
    x_title = config.get('x_title', x_col)
    y_title = config.get('y_title', 'Values')
    light_mode = config.get('light_mode', True)
    
    fig = go.Figure()
        
    for i, y_col in enumerate(y_cols):
        # color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.7
            ),
            name=y_col
        ))
    
    # Apply theme based on light mode setting
    template = 'plotly_white' if light_mode else 'plotly_dark'
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template=template
    )

    # Apply min/max if specified
    if config.get('x_min') is not None:
        fig.update_xaxes(range=[config['x_min'], config.get('x_max')])
    if config.get('y_min') is not None:
        fig.update_yaxes(range=[config['y_min'], config.get('y_max')])
    
    return fig

def create_single_line_chart(df, config):
    x_col = config.get('x_column')
    y_cols = config.get('y_columns', [])
    title = config.get('title', 'Line Chart')
    x_title = config.get('x_title', x_col)
    y_title = config.get('y_title', 'Values')
    light_mode = config.get('light_mode', True)
    
    fig = go.Figure()
        
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=6),
            name=y_col
        ))
    
    # Apply theme based on light mode setting
    template = 'plotly_white' if light_mode else 'plotly_dark'
    fig.update_layout(
        title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            template=template
    )
    
    # Apply min/max if specified
    if config.get('x_min') is not None:
        fig.update_xaxes(range=[config['x_min'], config.get('x_max')])
    if config.get('y_min') is not None:
        fig.update_yaxes(range=[config['y_min'], config.get('y_max')])
    
    return fig

def create_dual_line_chart(df, config):
    x_col = config.get('x_column')
    y1_cols = config.get('y1_columns', [])
    y2_cols = config.get('y2_columns', [])
    title = config.get('title', 'Dual Axis Line Chart')
    x_title = config.get('x_title', x_col)
    y1_title = config.get('y1_title', 'Left Y-Axis')
    y2_title = config.get('y2_title', 'Right Y-Axis')
    light_mode = config.get('light_mode', True)
    
    fig = go.Figure()

    #needed to allow for each access to have a unique color. 
    marker_styles = ["circle", "x", "square", "diamond","triangle-up", "pentagon", "hexagon", "star" "triangle-down", "triangle-left", "triangle-right", "star"]
        
    # First y-axis traces (left axis)
    for i, y1_col in enumerate(y1_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y1_col],
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8, symbol=marker_styles[i % len(marker_styles)]),
            name=y1_col,
            yaxis='y',
            marker_color='blue'
        ))
    
    # Second y-axis traces (right axis)
    for i, y2_col in enumerate(y2_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y2_col],
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8, symbol=marker_styles[i % len(marker_styles)]),
            name=y2_col,
            yaxis='y2',
            marker_color='red'
        ))
    
    # Apply theme based on light mode setting
    template = 'plotly_white' if light_mode else 'plotly_dark'
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        template=template,
        yaxis=dict(
            title=y1_title,
            side='left',
            color='blue'
        ),
        yaxis2=dict(
            title=y2_title,
            side='right',
            overlaying='y',
            color='red'
        )
    )
    
    # Apply min/max if specified
    if config.get('x_min') is not None:
        fig.update_xaxes(range=[config['x_min'], config.get('x_max')])
    if config.get('y1_min') is not None:
        fig.update_yaxes(range=[config['y1_min'], config.get('y1_max')])
    if config.get('y2_min') is not None:
        fig.update_layout(yaxis2=dict(range=[config['y2_min'], config.get('y2_max')]))
    
    return fig

def scatter_on_map(df, config):
    title = config.get('title', 'Scatter Plot on Map')
    map_type = config.get('map_type', 'satellite')
    lat_col = config.get('latitude_column')
    lon_col = config.get('longitude_column')
    hover_cols = config.get('hover_columns', [])
    color_col = config.get('color_column')
    size_col = config.get('size_column')
    
    #TODO impliment my own scatter on map functionality here.
    # Create hover text from selected columns
    hover_text = []
    for i in range(len(df)):
        text_parts = []
        for col in hover_cols:
            if col in df.columns:
                text_parts.append(f"{col}: {df[col].iloc[i]}")
        hover_text.append('<br>'.join(text_parts)) if text_parts else hover_text.append('')
    
    # Create the scatter mapbox
    fig = go.Figure()
    
    scatter_kwargs = {
        'lat': df[lat_col],
        'lon': df[lon_col],
        'mode': 'markers',
        'marker': dict(
            size=8,
            opacity=0.7
        ),
        'name': 'Data Points',
        'text': hover_text if hover_text else None,
        'hovertemplate': '%{text}<extra></extra>' if hover_text else None
    }
    
    # Add color if specified
    if color_col and color_col in df.columns:
        scatter_kwargs['marker']['color'] = df[color_col]
        scatter_kwargs['marker']['colorscale'] = 'Viridis'
        scatter_kwargs['marker']['showscale'] = True
        scatter_kwargs['marker']['colorbar'] = dict(title=color_col)
    
    # Add size if specified
    if size_col and size_col in df.columns:
        scatter_kwargs['marker']['size'] = df[size_col]
    
    fig.add_trace(go.Scattermapbox(**scatter_kwargs))
    
    # Update layout
    fig.update_layout(
        title=title,
        mapbox=dict(
            style=map_type,
            center=dict(
                lat=df[lat_col].mean(),
                lon=df[lon_col].mean()
            ),
            zoom=3
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=600
    )
    
    return fig

def csv_joiner(filepath, config):
    pass


    
    #NOTE import the class here
    
def ping_plotter(filepath, config):
    pass

def iperf_udp_plotter(filepath, config):
    pass

def iperf_tcp_plotter(filepath, config):
    pass

if __name__ == '__main__':
    print(f"Starting server on {HOST}:{PORT}")
    print(f"Access the application at: http://{'localhost' if HOST == '0.0.0.0' else HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=True)
