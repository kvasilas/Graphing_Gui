import os
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import base64
import io
import datetime
import zipfile

# Initialize Dash app with dark theme and blue accent
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Graphing Tool - Dash Version"

# Global variable to store uploaded data
uploaded_data = None

# File size configuration - set to 1 GB maximum
MAX_FILE_SIZE_MB = 1024  # 1 GB maximum file size
ALLOWED_EXTENSIONS = {'csv', 'txt', 'log', 'json', 'zip'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("📊 Graphing Tool", className="text-center mb-4"),
            html.P("Upload your data file and create interactive visualizations", className="text-center text-muted mb-4")
        ])
    ]),
    
    dbc.Row([
        # Left column - Controls
        dbc.Col([
            # File Upload Section
            dbc.Card([
                dbc.CardHeader("📁 File Upload"),
                dbc.CardBody([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px',
                            'cursor': 'pointer'
                        },
                        multiple=False,
                        accept='.csv,.txt,.log,.json,.zip'
                    ),
                    html.Div(id='upload-status', className="mt-2")
                ])
            ], className="mb-3"),
            
            # Graph Configuration Section
            dbc.Card([
                dbc.CardHeader("⚙️ Graph Configuration"),
                dbc.CardBody([
                    html.Label("Graph Type:"),
                    dcc.Dropdown(
                        id='graph-type',
                        options=[
                            {'label': 'Scatter Plot', 'value': 'scatter'},
                            {'label': 'Single Line Chart', 'value': 'single_line'},
                            {'label': 'Dual Axis Line Chart', 'value': 'dual_line'},
                            {'label': 'Scatter on Map', 'value': 'scatter_on_map'}
                        ],
                        placeholder="Select graph type..."
                    ),
                    
                    html.Div(id='graph-config', className="mt-3"),
                    
                    dbc.Button("Generate Graph", id='generate-btn', color="primary", className="mt-3 w-100", disabled=True)
                ])
            ], className="mb-3"),
            
            # File Processing Section
            dbc.Card([
                dbc.CardHeader("📄 File Processing"),
                dbc.CardBody([
                    html.Label("Processing Type:"),
                    dcc.Dropdown(
                        id='process-type',
                        options=[
                            {'label': 'Generate Summary Report', 'value': 'summary'},
                            {'label': 'Filter Data', 'value': 'filter'},
                            {'label': 'Calculate Statistics', 'value': 'stats'},
                            {'label': 'Export Cleaned Data', 'value': 'clean'}
                        ],
                        placeholder="Select processing type..."
                    ),
                    
                    html.Div(id='process-config', className="mt-3"),
                    
                    dbc.Button("Process File", id='process-btn', color="success", className="mt-3 w-100", disabled=True),
                    
                    # Hidden download component
                    dcc.Download(id="download-dataframe-csv")
                ])
            ])
        ], width=4),
        
        # Right column - Graph display
        dbc.Col([
            # Notification areas
            html.Div(id='graph-notification-area', className="mb-3"),
            html.Div(id='process-notification-area', className="mb-3"),
            
            # Graph display
            dbc.Card([
                dbc.CardHeader("📈 Generated Graph"),
                dbc.CardBody([
                    dcc.Graph(id='main-graph', style={'height': '600px'}),
                    html.Div(id='graph-info', className="mt-2")
                ])
            ])
        ], width=8)
    ])
], fluid=True)

# Callback for file upload
@app.callback(
    [Output('upload-status', 'children'),
     Output('graph-config', 'children'),
     Output('generate-btn', 'disabled'),
     Output('process-btn', 'disabled')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_upload_status(contents, filename):
    global uploaded_data
    
    if contents is None:
        return "", "", True, True
    
    try:
        print(f"DEBUG: Upload triggered with filename: {filename}")
        print(f"DEBUG: Contents type: {type(contents)}")
        
        # Parse uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        print(f"DEBUG: Content type: {content_type}")
        print(f"DEBUG: Decoded size: {len(decoded)} bytes")
        
        if filename and allowed_file(filename):
            file_extension = filename.rsplit('.', 1)[1].lower()
            print(f"DEBUG: Processing {file_extension} file")
            
            if file_extension == 'csv':
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                print(f"DEBUG: CSV loaded with {len(df)} rows, {len(df.columns)} columns")
            elif file_extension == 'txt':
                # Try different delimiters for text files
                try:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter='\t')
                    print(f"DEBUG: TXT loaded with tab delimiter")
                except Exception as e1:
                    try:
                        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=',')
                        print(f"DEBUG: TXT loaded with comma delimiter")
                    except Exception as e2:
                        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter='\s+')
                        print(f"DEBUG: TXT loaded with space delimiter")
            elif file_extension == 'log':
                # Try to read log files as space or tab separated
                try:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter='\s+', engine='python')
                    print(f"DEBUG: LOG loaded with space delimiter")
                except Exception as e:
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter='\t')
                    print(f"DEBUG: LOG loaded with tab delimiter")
            elif file_extension == 'json':
                df = pd.read_json(io.StringIO(decoded.decode('utf-8')))
                print(f"DEBUG: JSON loaded with {len(df)} rows, {len(df.columns)} columns")
            elif file_extension == 'zip':
                # Handle zip files - extract and read the first CSV file
                with zipfile.ZipFile(io.BytesIO(decoded)) as zip_ref:
                    csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                    if csv_files:
                        with zip_ref.open(csv_files[0]) as csv_file:
                            df = pd.read_csv(csv_file)
                        print(f"DEBUG: ZIP CSV loaded with {len(df)} rows, {len(df.columns)} columns")
                    else:
                        return dbc.Alert("❌ No CSV file found in zip archive.", color="danger"), "", True, True
            
            uploaded_data = df
            columns = df.columns.tolist()
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            
            # Create configuration elements
            config_elements = [
                html.Label("X-Axis Column:"),
                dcc.Dropdown(id='x-column', options=[{'label': col, 'value': col} for col in columns], placeholder="Select X-axis column..."),
                
                html.Label("Y-Axis Column(s):", className="mt-2"),
                dcc.Dropdown(id='y-columns', options=[{'label': col, 'value': col} for col in columns], multi=True, placeholder="Select Y-axis column(s)..."),
                
                html.Label("Title:", className="mt-2"),
                dbc.Input(id='graph-title', placeholder="Enter graph title...", value="My Graph")
            ]
            
            status = dbc.Alert(f"✅ File uploaded successfully! Found {len(df)} rows and {len(df.columns)} columns.", color="success")
            return status, config_elements, False, False
            
        else:
            print(f"DEBUG: File not allowed - filename: {filename}")
            return dbc.Alert("❌ Please upload a supported file type (CSV, TXT, LOG, JSON, ZIP).", color="danger"), "", True, True
            
    except Exception as e:
        print(f"DEBUG: Upload error: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return dbc.Alert(f"❌ Error uploading file: {str(e)}", color="danger"), "", True, True

# Callback for graph generation
@app.callback(
    [Output('main-graph', 'figure'),
     Output('graph-info', 'children'),
     Output('graph-notification-area', 'children')],
    [Input('generate-btn', 'n_clicks')],
    [State('graph-type', 'value'),
     State('x-column', 'value'),
     State('y-columns', 'value'),
     State('graph-title', 'value')],
    prevent_initial_call=True
)
def generate_graph(n_clicks, graph_type, x_col, y_cols, title):
    global uploaded_data
    
    if n_clicks is None or uploaded_data is None:
        raise PreventUpdate
    
    try:
        df = uploaded_data.copy()
        
        if not x_col or not y_cols:
            return {}, "", dbc.Alert("❌ Please select X-axis and Y-axis columns.", color="warning")
        
        # Create graph based on type
        if graph_type == 'scatter':
            fig = create_scatter_plot(df, x_col, y_cols, title)
        elif graph_type == 'single_line':
            fig = create_single_line_chart(df, x_col, y_cols, title)
        elif graph_type == 'dual_line':
            fig = create_dual_line_chart(df, x_col, y_cols, title)
        elif graph_type == 'scatter_on_map':
            result = scatter_on_map(df, x_col, y_cols, title)
            if result == "Success":
                return {}, "", dbc.Alert("✅ Scatter map generated successfully! Check the new window that opened.", color="success", duration=5000)
            else:
                return {}, "", dbc.Alert("❌ Failed to generate scatter map.", color="danger")
        else:
            return {}, "", dbc.Alert("❌ Invalid graph type.", color="danger")
        
        # Return the graph and info
        info = dbc.Alert(f"✅ Graph generated successfully! Showing {len(df)} data points.", color="success")
        return fig, info, ""
        
    except Exception as e:
        return {}, "", dbc.Alert(f"❌ Error generating graph: {str(e)}", color="danger")

# Callback for processing configuration
@app.callback(
    Output('process-config', 'children'),
    [Input('process-type', 'value')]
)
def update_process_config(process_type):
    global uploaded_data
    
    if not process_type:
        return ""
    
    if process_type == 'summary':
        return [
            html.Label("Summary Type:"),
            dcc.Dropdown(
                id='summary-type',
                options=[
                    {'label': 'Basic Statistics', 'value': 'basic'},
                    {'label': 'Data Quality Report', 'value': 'quality'},
                    {'label': 'Column Analysis', 'value': 'columns'}
                ],
                placeholder="Select summary type..."
            )
        ]
    elif process_type == 'filter':
        # Get column options from uploaded data
        column_options = []
        if uploaded_data is not None:
            column_options = [{'label': col, 'value': col} for col in uploaded_data.columns]
        
        return [
            html.Label("Filter Column:"),
            dcc.Dropdown(
                id='filter-column', 
                options=column_options,
                placeholder="Select column to filter..."
            ),
            html.Label("Filter Value:", className="mt-2"),
            dbc.Input(id='filter-value', placeholder="Enter filter value...")
        ]
    elif process_type == 'stats':
        return [
            html.Label("Statistical Operations:"),
            dcc.Checklist(
                id='stats-ops',
                options=[
                    {'label': 'Mean', 'value': 'mean'},
                    {'label': 'Median', 'value': 'median'},
                    {'label': 'Standard Deviation', 'value': 'std'},
                    {'label': 'Min/Max', 'value': 'minmax'}
                ],
                value=['mean', 'median']
            )
        ]
    elif process_type == 'clean':
        return [
            html.Label("Cleaning Options:"),
            dcc.Checklist(
                id='clean-ops',
                options=[
                    {'label': 'Remove Duplicates', 'value': 'duplicates'},
                    {'label': 'Remove Empty Rows', 'value': 'empty'},
                    {'label': 'Standardize Text', 'value': 'text'},
                    {'label': 'Convert Data Types', 'value': 'types'}
                ],
                value=['duplicates', 'empty']
            )
        ]
    
    return ""

# Callback for file processing and download
@app.callback(
    [Output('download-dataframe-csv', 'data'),
     Output('process-notification-area', 'children')],
    [Input('process-btn', 'n_clicks')],
    [State('process-type', 'value'),
     State('summary-type', 'value'),
     State('filter-column', 'value'),
     State('filter-value', 'value'),
     State('stats-ops', 'value'),
     State('clean-ops', 'value')],
    prevent_initial_call=True
)
def process_file(n_clicks, process_type, summary_type, filter_col, filter_val, stats_ops, clean_ops):
    global uploaded_data
    
    if n_clicks is None or uploaded_data is None:
        raise PreventUpdate
    
    try:
        df = uploaded_data.copy()
        filename = f"processed_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if process_type == 'summary':
            processed_df = generate_summary_report(df, summary_type)
            message = f"✅ Summary report generated successfully! {len(processed_df)} rows processed."
            
        elif process_type == 'filter':
            if not filter_col or not filter_val:
                return None, dbc.Alert("❌ Please select a column and enter a filter value.", color="warning")
            processed_df = filter_data(df, filter_col, filter_val)
            message = f"✅ Data filtered successfully! {len(processed_df)} rows remaining (from {len(df)} original)."
            
        elif process_type == 'stats':
            processed_df = calculate_statistics(df, stats_ops)
            message = f"✅ Statistics calculated successfully! Generated {len(processed_df)} statistical measures."
            
        elif process_type == 'clean':
            processed_df = clean_data(df, clean_ops)
            message = f"✅ Data cleaned successfully! {len(processed_df)} rows remaining (from {len(df)} original)."
        
        else:
            return None, dbc.Alert("❌ Invalid processing type.", color="danger")
        
        # Convert DataFrame to CSV for download
        csv_string = processed_df.to_csv(index=False)
        
        return dict(content=csv_string, filename=filename), dbc.Alert(message, color="success", duration=5000)
        
    except Exception as e:
        return None, dbc.Alert(f"❌ Error processing file: {str(e)}", color="danger")

# Graph creation functions (keeping existing logic)
def create_scatter_plot(df, x_col, y_cols, title):
    fig = go.Figure()
    
    for i, y_col in enumerate(y_cols):
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
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title='Values',
        template='plotly_dark'
    )
    
    return fig

def create_single_line_chart(df, x_col, y_cols, title):
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
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title='Values',
        template='plotly_dark'
    )
    
    return fig

def create_dual_line_chart(df, x_col, y_cols, title):
    fig = go.Figure()
    
    # Split y_cols into two groups for dual axis
    mid_point = len(y_cols) // 2
    y1_cols = y_cols[:mid_point] if mid_point > 0 else y_cols[:1]
    y2_cols = y_cols[mid_point:] if mid_point > 0 else y_cols[1:] if len(y_cols) > 1 else []
    
    # Marker styles for different traces
    marker_styles = ["circle", "x", "square", "diamond", "triangle-up", "pentagon", "hexagon", "star", "triangle-down", "triangle-left", "triangle-right"]
    
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
            marker_color='#1f77b4'  # Blue color
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
            marker_color='#ff7f0e'  # Orange color
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        template='plotly_dark',
        yaxis=dict(
            title='Left Y-Axis',
            side='left',
            color='#1f77b4'
        ),
        yaxis2=dict(
            title='Right Y-Axis',
            side='right',
            overlaying='y',
            color='#ff7f0e'
        )
    )
    
    return fig

def scatter_on_map(df, x_col, y_cols, title):
    # For scatter on map, we'll use the first two columns as lat/lon
    # and the first y column as the value to display
    if len(df.columns) < 2:
        return "Error: Need at least 2 columns for map visualization"
    
    # Use first two columns as latitude and longitude
    lat_col = df.columns[0]
    lon_col = df.columns[1]
    value_col = y_cols[0] if y_cols else df.columns[2] if len(df.columns) > 2 else lat_col
    
    # Create scatter map using go.Scattermap
    fig = go.Figure(go.Scattermap(
        lat=df[lat_col],
        lon=df[lon_col],
        mode='markers',
        marker=dict(
            size=10,
            color=df[value_col],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title=value_col)
        ),
        text=df[value_col],
        hovertemplate=f'<b>{value_col}</b><br>' +
                     f'Lat: %{{lat}}<br>' +
                     f'Lon: %{{lon}}<br>' +
                     f'Value: %{{text}}<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        map=dict(
            style="open-street-map",
            center=dict(lat=df[lat_col].mean(), lon=df[lon_col].mean()),
            zoom=10
        ),
        template='plotly_dark'
    )
    
    # Show the figure in a new window
    fig.show()
    
    return "Success"

# Data processing functions
def generate_summary_report(df, summary_type):
    """Generate different types of summary reports"""
    if summary_type == 'basic':
        # Basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        summary = df[numeric_cols].describe()
        return summary.reset_index()
    
    elif summary_type == 'quality':
        # Data quality report
        quality_report = []
        for col in df.columns:
            total_rows = len(df)
            null_count = df[col].isnull().sum()
            null_percent = (null_count / total_rows) * 100
            unique_count = df[col].nunique()
            
            quality_report.append({
                'Column': col,
                'Total_Rows': total_rows,
                'Null_Count': null_count,
                'Null_Percentage': round(null_percent, 2),
                'Unique_Values': unique_count,
                'Data_Type': str(df[col].dtype)
            })
        
        return pd.DataFrame(quality_report)
    
    elif summary_type == 'columns':
        # Column analysis
        col_analysis = []
        for col in df.columns:
            col_analysis.append({
                'Column': col,
                'Data_Type': str(df[col].dtype),
                'Sample_Values': ', '.join([str(x) for x in df[col].head(3).tolist()]),
                'Unique_Count': df[col].nunique()
            })
        
        return pd.DataFrame(col_analysis)

def filter_data(df, column, value):
    """Filter data based on column and value"""
    try:
        # Try to convert value to numeric if the column is numeric
        if df[column].dtype in ['int64', 'float64']:
            value = float(value)
        
        filtered_df = df[df[column] == value]
        return filtered_df
    except:
        # If conversion fails, treat as string
        filtered_df = df[df[column].astype(str) == str(value)]
        return filtered_df

def calculate_statistics(df, operations):
    """Calculate statistical measures"""
    numeric_cols = df.select_dtypes(include=['number']).columns
    stats_data = []
    
    for col in numeric_cols:
        col_stats = {'Column': col}
        
        if 'mean' in operations:
            col_stats['Mean'] = df[col].mean()
        if 'median' in operations:
            col_stats['Median'] = df[col].median()
        if 'std' in operations:
            col_stats['Standard_Deviation'] = df[col].std()
        if 'minmax' in operations:
            col_stats['Min'] = df[col].min()
            col_stats['Max'] = df[col].max()
        
        stats_data.append(col_stats)
    
    return pd.DataFrame(stats_data)

def clean_data(df, operations):
    """Clean data based on selected operations"""
    cleaned_df = df.copy()
    
    if 'duplicates' in operations:
        cleaned_df = cleaned_df.drop_duplicates()
    
    if 'empty' in operations:
        cleaned_df = cleaned_df.dropna()
    
    if 'text' in operations:
        # Standardize text columns (convert to lowercase, strip whitespace)
        text_cols = cleaned_df.select_dtypes(include=['object']).columns
        for col in text_cols:
            cleaned_df[col] = cleaned_df[col].astype(str).str.lower().str.strip()
    
    if 'types' in operations:
        # Try to convert columns to appropriate data types
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                # Try to convert to numeric
                try:
                    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='ignore')
                except:
                    pass
    
    return cleaned_df

if __name__ == '__main__':
    print("Starting Dash Graphing Tool...")
    print("Access the application at: http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
