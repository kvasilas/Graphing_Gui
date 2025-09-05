// Global variables
let uploadedFile = null;
let csvData = null;
let currentGraph = null;

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('uploadSection');
const configSection = document.getElementById('configSection');
const graphSection = document.getElementById('graphSection');
const loadingOverlay = document.getElementById('loadingOverlay');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeDragAndDrop();
    initializeFileInput();
    updateToggleText(); // Initialize toggle text for default light mode
});

// Drag and Drop functionality
function initializeDragAndDrop() {
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
}

// File input functionality
function initializeFileInput() {
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

// Handle file upload
async function handleFileUpload(file) {
    const allowedExtensions = ['.csv', '.txt', '.log', '.json', '.zip'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
        showNotification('Please select a supported file type: CSV, TXT, LOG, JSON, or ZIP', 'error');
        return;
    }

    // Check file size and show warning for large files
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(1);
    if (file.size > 100 * 1024 * 1024) { // 100MB
        showNotification(`Large file detected (${fileSizeMB} MB). Upload may take longer than usual.`, 'warning');
    }
    if (file.size > 500 * 1024 * 1024) { // 500MB
        showNotification(`Very large file detected (${fileSizeMB} MB). Processing may take several minutes.`, 'warning');
    }

    showLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            uploadedFile = result.filename;
            if (result.file_type === 'csv') {
                csvData = result;
                const fileType = result.file_type ? result.file_type.toUpperCase() : 'CSV';
                showNotification(`${fileType} file uploaded successfully! Found ${result.row_count} rows and ${result.columns.length} columns.`, 'success');
                showConfigSection();
                populateColumnDropdowns();
            } else {
                // For non-CSV files, store basic file info
                csvData = {
                    filename: result.filename,
                    file_type: result.file_type,
                    columns: [], // Empty for non-CSV files
                    numeric_columns: []
                };
                const fileType = result.file_type ? result.file_type.toUpperCase() : 'FILE';
                showNotification(`${fileType} file uploaded successfully!`, 'success');
                showConfigSection();
            }
        } else {
            showNotification(result.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showNotification('Error uploading file: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Show configuration section
function showConfigSection() {
    uploadSection.style.display = 'none';
    configSection.style.display = 'block';
    graphSection.style.display = 'none';
    
    // Initialize toggle text
    updateToggleText();
    
    // Ensure instructions are shown initially (after elements are created)
    setTimeout(() => {
        updateConfigFields();
    }, 100);
}

// Populate column dropdowns
function populateColumnDropdowns() {
    const columnFields = document.getElementById('columnFields');
    columnFields.innerHTML = '';

    // Create X-axis dropdown
    const xGroup = createFormGroup('X-Axis Column', 'xColumn', csvData.columns);
    columnFields.appendChild(xGroup);

    // Create Y-axis multi-select dropdown
    const yGroup = createMultiSelectGroup('Y-Axis Columns', 'yColumns', csvData.numeric_columns);
    columnFields.appendChild(yGroup);

    // Create Y2-axis multi-select dropdown (hidden by default)
    const y2Group = createMultiSelectGroup('Y2-Axis Columns', 'y2Columns', csvData.numeric_columns);
    y2Group.style.display = 'none';
    y2Group.id = 'y2Group';
    columnFields.appendChild(y2Group);
}

// Populate map dropdowns
function populateMapDropdowns() {
    if (!csvData || !csvData.columns) return;
    
    // Populate latitude dropdown
    const latitudeSelect = document.getElementById('latitudeColumn');
    latitudeSelect.innerHTML = '<option value="">Select Latitude Column</option>';
    csvData.columns.forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        latitudeSelect.appendChild(option);
    });
    
    // Populate longitude dropdown
    const longitudeSelect = document.getElementById('longitudeColumn');
    longitudeSelect.innerHTML = '<option value="">Select Longitude Column</option>';
    csvData.columns.forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        longitudeSelect.appendChild(option);
    });
    
    // Populate hover columns multi-select
    const hoverSelect = document.getElementById('hoverColumns');
    hoverSelect.innerHTML = '';
    csvData.columns.forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        hoverSelect.appendChild(option);
    });
    
    // Populate color column dropdown
    const colorSelect = document.getElementById('colorColumn');
    colorSelect.innerHTML = '<option value="">Select Color Column (Optional)</option>';
    csvData.columns.forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        colorSelect.appendChild(option);
    });
    
    // Populate size column dropdown
    const sizeSelect = document.getElementById('sizeColumn');
    sizeSelect.innerHTML = '<option value="">Select Size Column (Optional)</option>';
    csvData.columns.forEach(column => {
        const option = document.createElement('option');
        option.value = column;
        option.textContent = column;
        sizeSelect.appendChild(option);
    });
}

// Create form group
function createFormGroup(label, id, options) {
    const group = document.createElement('div');
    group.className = 'form-group';
    
    const labelElement = document.createElement('label');
    labelElement.textContent = label;
    labelElement.setAttribute('for', id);
    
    const select = document.createElement('select');
    select.id = id;
    select.className = 'form-select';
    
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = `Select ${label}`;
    select.appendChild(defaultOption);
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
    
    group.appendChild(labelElement);
    group.appendChild(select);
    
    return group;
}

// Create multi-select form group
function createMultiSelectGroup(label, id, options) {
    const group = document.createElement('div');
    group.className = 'form-group';
    
    const labelElement = document.createElement('label');
    labelElement.textContent = label;
    labelElement.setAttribute('for', id);
    
    const container = document.createElement('div');
    container.className = 'multi-select-container';
    
    const select = document.createElement('select');
    select.id = id;
    select.className = 'form-select multi-select';
    select.multiple = true;
    select.size = 4;
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = option;
        select.appendChild(optionElement);
    });
    
    const helpText = document.createElement('small');
    helpText.className = 'help-text';
    helpText.textContent = 'Hold Ctrl/Cmd to select multiple columns';
    helpText.style.color = '#b0b8c1';
    helpText.style.fontSize = '0.85rem';
    helpText.style.marginTop = '5px';
    helpText.style.display = 'block';
    
    container.appendChild(select);
    container.appendChild(helpText);
    
    group.appendChild(labelElement);
    group.appendChild(container);
    
    return group;
}

// Update configuration fields based on graph type
function updateConfigFields() {
    const graphType = document.getElementById('graphType').value;
    const instructionsCard = document.getElementById('instructionsCard');
    const columnSelection = document.getElementById('columnSelection');
    const stylingConfig = document.getElementById('stylingConfig');
    const axisRangeConfig = document.getElementById('axisRangeConfig');
    
    const scatterMapConfig = document.getElementById('scatterMapConfig');
    const y2Group = document.getElementById('y2Group');
    const y2TitleGroup = document.getElementById('y2TitleGroup');
    const y2MinGroup = document.getElementById('y2MinGroup');
    const y2MaxGroup = document.getElementById('y2MaxGroup');
    const generateBtn = document.getElementById('generateBtn');

    if (!graphType) {
        // Show instructions, hide all config sections
        instructionsCard.style.display = 'block';
        columnSelection.style.display = 'none';
        stylingConfig.style.display = 'none';
        axisRangeConfig.style.display = 'none';
        scatterMapConfig.style.display = 'none';

        return;
    }

    // Hide instructions
    instructionsCard.style.display = 'none';

    // Handle specific parser types
    if (graphType === 'scatter_on_map') {
        columnSelection.style.display = 'none';
        stylingConfig.style.display = 'none';
        axisRangeConfig.style.display = 'none';
        scatterMapConfig.style.display = 'block';
        populateMapDropdowns();

    } else {
        // Show standard config sections for other graph types
        columnSelection.style.display = 'block';
        stylingConfig.style.display = 'block';
        axisRangeConfig.style.display = 'block';
        scatterMapConfig.style.display = 'none';

    }

    // Reset dual axis specific visibility (with null checks)
    if (y2Group) y2Group.style.display = 'none';
    if (y2TitleGroup) y2TitleGroup.style.display = 'none';
    if (y2MinGroup) y2MinGroup.style.display = 'none';
    if (y2MaxGroup) y2MaxGroup.style.display = 'none';

    if (graphType === 'dual_line') {
        if (y2Group) y2Group.style.display = 'block';
        if (y2TitleGroup) y2TitleGroup.style.display = 'block';
        if (y2MinGroup) y2MinGroup.style.display = 'block';
        if (y2MaxGroup) y2MaxGroup.style.display = 'block';
    }


}

// Update toggle text based on current state
function updateToggleText() {
    const lightMode = document.getElementById('lightMode');
    const toggleText = document.getElementById('toggleText');
    
    if (lightMode.checked) {
        toggleText.textContent = 'Light Mode';
    } else {
        toggleText.textContent = 'Dark Mode';
    }
}

// Generate graph
async function generateGraph() {
    const graphType = document.getElementById('graphType').value;
    
    if (!graphType) {
        showNotification('Please select a graph type', 'error');
        return;
    }

    const config = getGraphConfig();
    
    if (!validateConfig(config, graphType)) {
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/generate_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: uploadedFile,
                graph_type: graphType,
                config: config
            })
        });

        const result = await response.json();

        if (result.success) {
            if (result.message) {
                // For scatter maps, show the success message
                showNotification(result.message, 'success');
            } else if (result.graph) {
                // For regular graphs, display the graph
                currentGraph = JSON.parse(result.graph);
                displayGraph(currentGraph);
                showNotification('Graph generated successfully!', 'success');
            }
        } else {
            showNotification(result.error || 'Failed to generate graph', 'error');
        }
    } catch (error) {
        showNotification('Error generating graph: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Get graph configuration from form
function getGraphConfig() {
    const graphType = document.getElementById('graphType').value;
    

    
    // Handle Scatter on Map configuration
    if (graphType === 'scatter_on_map') {
        return {
            title: document.getElementById('mapTitle').value,
            map_type: document.getElementById('mapType').value,
            latitude_column: document.getElementById('latitudeColumn').value,
            longitude_column: document.getElementById('longitudeColumn').value,
            hover_columns: getSelectedValues('hoverColumns'),
            color_column: document.getElementById('colorColumn').value,
            size_column: document.getElementById('sizeColumn').value,
            light_mode: document.getElementById('lightMode').checked
        };
    }
    
    // Standard configuration for other graph types
    const config = {
        title: document.getElementById('title').value,
        x_title: document.getElementById('xTitle').value,
        y_title: document.getElementById('yTitle').value,
        x_column: document.getElementById('xColumn').value,
        y_columns: getSelectedValues('yColumns'),
        x_min: getNumberValue('xMin'),
        x_max: getNumberValue('xMax'),
        y_min: getNumberValue('yMin'),
        y_max: getNumberValue('yMax'),
        light_mode: document.getElementById('lightMode').checked
    };

    if (graphType === 'dual_line') {
        config.y1_columns = config.y_columns;
        config.y2_columns = getSelectedValues('y2Columns');
        config.y1_title = config.y_title;
        config.y2_title = document.getElementById('y2Title').value;
        config.y1_min = getNumberValue('yMin');
        config.y1_max = getNumberValue('yMax');
        config.y2_min = getNumberValue('y2Min');
        config.y2_max = getNumberValue('y2Max');
    }

    return config;
}

// Get selected values from multi-select
function getSelectedValues(id) {
    const select = document.getElementById(id);
    const selectedOptions = Array.from(select.selectedOptions);
    return selectedOptions.map(option => option.value);
}

// Get number value from input
function getNumberValue(id) {
    const value = document.getElementById(id).value;
    return value === '' ? null : parseFloat(value);
}

// Validate configuration
function validateConfig(config, graphType) {

    
    // Handle Scatter on Map validation
    if (graphType === 'scatter_on_map') {
        if (!config.latitude_column) {
            showNotification('Please select a latitude column', 'error');
            return false;
        }
        
        if (!config.longitude_column) {
            showNotification('Please select a longitude column', 'error');
            return false;
        }
        
        return true;
    }
    
    // Standard validation for other graph types
    if (!config.x_column) {
        showNotification('Please select an X-axis column', 'error');
        return false;
    }

    if (!config.y_columns || config.y_columns.length === 0) {
        showNotification('Please select at least one Y-axis column', 'error');
        return false;
    }

    if (graphType === 'dual_line' && (!config.y2_columns || config.y2_columns.length === 0)) {
        showNotification('Please select at least one Y2-axis column for dual axis chart', 'error');
        return false;
    }

    return true;
}

// Display graph
function displayGraph(graphData) {
    const graphDisplay = document.getElementById('graphDisplay');
    
    // Clear previous graph
    graphDisplay.innerHTML = '';
    
    // Show graph section
    graphSection.style.display = 'block';
    
    // Render the graph
    Plotly.newPlot(graphDisplay, graphData.data, graphData.layout, {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    });
}

// Download graph
function downloadGraph() {
    if (!currentGraph) {
        showNotification('No graph to download', 'error');
        return;
    }

    const graphDisplay = document.getElementById('graphDisplay');
    Plotly.downloadImage(graphDisplay, {
        format: 'png',
        filename: 'csv_graph',
        height: 600,
        width: 800
    });
}

// Fullscreen graph
function fullscreenGraph() {
    if (!currentGraph) {
        showNotification('No graph to display', 'error');
        return;
    }

    const graphDisplay = document.getElementById('graphDisplay');
    Plotly.relayout(graphDisplay, {
        autosize: true
    });
}

// Reset application
function resetApp() {
    uploadedFile = null;
    csvData = null;
    currentGraph = null;
    
    // Reset form
    document.getElementById('graphType').value = '';
    document.getElementById('title').value = '';
    document.getElementById('xTitle').value = '';
    document.getElementById('yTitle').value = '';
    document.getElementById('y2Title').value = '';
    document.getElementById('xMin').value = '';
    document.getElementById('xMax').value = '';
    document.getElementById('yMin').value = '';
    document.getElementById('yMax').value = '';
    document.getElementById('y2Min').value = '';
    document.getElementById('y2Max').value = '';
    document.getElementById('lightMode').checked = false;
    

    
    // Reset Scatter on Map fields
    document.getElementById('mapTitle').value = '';
    document.getElementById('mapType').value = 'satellite';
    document.getElementById('latitudeColumn').selectedIndex = 0;
    document.getElementById('longitudeColumn').selectedIndex = 0;
    document.getElementById('hoverColumns').selectedIndex = -1;
    document.getElementById('colorColumn').selectedIndex = 0;
    document.getElementById('sizeColumn').selectedIndex = 0;
    
    // Reset file input
    fileInput.value = '';
    
    // Show upload section and instructions
    uploadSection.style.display = 'block';
    configSection.style.display = 'none';
    graphSection.style.display = 'none';
    
    // Update toggle text
    updateToggleText();
    
    showNotification('Application reset successfully', 'success');
}

// Show loading overlay
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// Show notification
function showNotification(message, type = 'info') {
    // Print to terminal (browser console)
    switch (type) {
        case 'success':
            console.log(`[SUCCESS] ${message}`);
            break;
        case 'error':
            console.error(`[ERROR] ${message}`);
            break;
        case 'warning':
            console.warn(`[WARNING] ${message}`);
            break;
        default:
            console.info(`[INFO] ${message}`);
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        max-width: 300px;
        word-wrap: break-word;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.background = 'linear-gradient(45deg, #4CAF50, #45a049)';
            break;
        case 'error':
            notification.style.background = 'linear-gradient(45deg, #f44336, #d32f2f)';
            break;
        case 'warning':
            notification.style.background = 'linear-gradient(45deg, #ff9800, #f57c00)';
            break;
        default:
            notification.style.background = 'linear-gradient(45deg, #2196F3, #1976D2)';
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
