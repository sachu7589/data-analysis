# CSV Analysis Web Application

A Flask web application for analyzing CSV data with interactive visualizations and statistical insights. Upload your CSV files and get comprehensive data analysis including distributions, correlations, missing values, and outlier detection.

## Features

- **📊 Data Overview**: View basic statistics, data types, and sample data
- **📈 Distribution Analysis**: Visualize data distributions with histograms
- **❓ Missing Values Analysis**: Identify and analyze missing data patterns with visualizations
- **🔍 Outlier Analysis**: Detect and visualize statistical outliers using boxplots and IQR method
- **🔗 Correlation Analysis**: Explore relationships between variables with heatmaps
- **📱 Responsive UI**: Modern Bootstrap 5 interface with Font Awesome icons
- **📁 File Upload**: Support for CSV and Excel files

## Tech Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Data Processing**: Pandas 2.1.1, NumPy 1.24.3
- **Visualization**: Matplotlib 3.7.2, Seaborn 0.12.2
- **Frontend**: Bootstrap 5, Font Awesome
- **File Support**: openpyxl 3.1.2 (Excel files)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sachu7589/data-analysis.git
   cd analysis-project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Upload your CSV file:**
   - Click "Choose File" and select your CSV file
   - Click "Upload and Analyze"
   - The application will automatically redirect to the dashboard

4. **Explore the analysis:**
   - **Dashboard**: Overview of your dataset
   - **Data Overview**: Detailed statistics and sample data
   - **Distribution Analysis**: Histograms for numeric columns
   - **Missing Values**: Analysis of missing data patterns
   - **Outlier Analysis**: Boxplots and outlier detection
   - **Correlation Analysis**: Correlation matrix and heatmap

## Project Structure

```
analysis-project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── uploads/          # Uploaded files storage
│   └── plots/            # Generated plots storage
└── templates/
    ├── index.html        # Upload page
    ├── dashboard.html    # Main dashboard
    ├── data_overview.html
    ├── distribution_analysis.html
    ├── missing_values.html
    ├── outlier_analysis.html
    └── correlation_analysis.html
```

## API Endpoints

- `GET /` - Upload page
- `POST /` - File upload and processing
- `GET /dashboard` - Main dashboard
- `GET /data-overview` - Detailed data statistics
- `GET /distribution-analysis` - Distribution plots
- `GET /missing-values` - Missing values analysis
- `GET /outlier-analysis` - Outlier detection
- `GET /correlation-analysis` - Correlation matrix

## Supported File Formats

- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`) via openpyxl

## Data Requirements

- **Correlation Analysis**: Requires at least 2 numeric columns
- **Distribution/Outlier Analysis**: Requires at least 1 numeric column
- **Missing Values**: Works with any data type

## Development

To run in development mode with auto-reload:
```bash
python app.py
```

The application runs on `http://localhost:5000` with debug mode enabled.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

- **Port already in use**: Change the port in `app.py` or kill the existing process
- **File upload issues**: Ensure the `static/uploads` directory exists and has write permissions
- **Memory issues**: For large files, consider chunking or sampling the data
