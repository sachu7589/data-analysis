import os
import matplotlib
matplotlib.use('Agg')  # Set backend for headless environment
from flask import Flask, render_template, request, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
PLOTS_FOLDER = 'static/plots'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOTS_FOLDER, exist_ok=True)

# Global variable to store current dataset
current_df = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_df
    if request.method == 'POST':
        file = request.files['csv_file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            
            # Load CSV
            current_df = pd.read_csv(filepath)
            
            # Basic info for dashboard
            basic_info = {
                'rows': len(current_df),
                'columns': len(current_df.columns),
                'memory_usage': current_df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
                'file_name': file.filename
            }
            
            # Convert data types to strings for template
            data_types_str = {col: str(dtype) for col, dtype in current_df.dtypes.to_dict().items()}
            
            return render_template('dashboard.html', 
                                 basic_info=basic_info,
                                 columns=list(current_df.columns),
                                 data_types=data_types_str)
    
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    global current_df
    if current_df is None:
        return render_template('index.html')
    
    # Basic info for dashboard
    basic_info = {
        'rows': len(current_df),
        'columns': len(current_df.columns),
        'memory_usage': current_df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
        'file_name': 'Current Dataset'
    }
    
    # Convert data types to strings for template
    data_types_str = {col: str(dtype) for col, dtype in current_df.dtypes.to_dict().items()}
    
    return render_template('dashboard.html', 
                         basic_info=basic_info,
                         columns=list(current_df.columns),
                         data_types=data_types_str)

@app.route('/missing-values')
def missing_values():
    global current_df
    if current_df is None:
        return jsonify({'error': 'No data loaded'})
    
    missing_data = {
        'total_missing': current_df.isnull().sum().sum(),
        'missing_percentage': (current_df.isnull().sum().sum() / (current_df.shape[0] * current_df.shape[1])) * 100,
        'columns_missing': current_df.isnull().sum().to_dict(),
        'columns_missing_pct': (current_df.isnull().sum() / len(current_df) * 100).to_dict()
    }
    
    # Create missing values plot
    plt.figure(figsize=(10, 6))
    missing_counts = current_df.isnull().sum()
    missing_counts = missing_counts[missing_counts > 0]
    if len(missing_counts) > 0:
        plt.bar(missing_counts.index, missing_counts.values)
        plt.title('Missing Values by Column')
        plt.xticks(rotation=45)
        plt.ylabel('Count of Missing Values')
        plt.tight_layout()
        
        # Save plot
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        missing_data['plot'] = plot_url
    
    return render_template('missing_values.html', missing_data=missing_data)

@app.route('/data-overview')
def data_overview():
    global current_df
    if current_df is None:
        return jsonify({'error': 'No data loaded'})
    
    # Summary statistics
    summary_stats = current_df.describe().round(2)
    
    # Data types info
    dtype_info = current_df.dtypes.value_counts().to_dict()
    
    # Sample data
    sample_data = current_df.head(10).to_dict('records')
    
    return render_template('data_overview.html', 
                         summary_stats=summary_stats.to_html(classes='table table-striped'),
                         dtype_info=dtype_info,
                         sample_data=sample_data)

@app.route('/correlation-analysis')
def correlation_analysis():
    global current_df
    if current_df is None:
        return jsonify({'error': 'No data loaded'})
    
    # Get numeric columns only
    numeric_df = current_df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) < 2:
        return render_template('correlation_analysis.html', error="Need at least 2 numeric columns for correlation analysis")
    
    # Correlation matrix
    corr_matrix = numeric_df.corr().round(3)
    
    # Create correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('correlation_analysis.html', 
                         corr_matrix=corr_matrix.to_html(classes='table table-striped'),
                         plot_url=plot_url)

@app.route('/distribution-analysis')
def distribution_analysis():
    global current_df
    if current_df is None:
        return jsonify({'error': 'No data loaded'})
    
    numeric_df = current_df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) == 0:
        return render_template('distribution_analysis.html', error="No numeric columns found")
    
    plots = []
    
    # Histograms for each numeric column
    for col in numeric_df.columns:
        plt.figure(figsize=(8, 6))
        plt.hist(numeric_df[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
        plt.title(f'Distribution of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        plots.append({'title': f'{col} Distribution', 'url': plot_url})
    
    return render_template('distribution_analysis.html', plots=plots)

@app.route('/outlier-analysis')
def outlier_analysis():
    global current_df
    if current_df is None:
        return jsonify({'error': 'No data loaded'})
    
    numeric_df = current_df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) == 0:
        return render_template('outlier_analysis.html', error="No numeric columns found")
    
    plots = []
    outlier_info = {}
    
    for col in numeric_df.columns:
        # Box plot
        plt.figure(figsize=(8, 6))
        plt.boxplot(numeric_df[col].dropna())
        plt.title(f'Boxplot of {col}')
        plt.ylabel(col)
        plt.tight_layout()
        
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        plots.append({'title': f'{col} Boxplot', 'url': plot_url})
        
        # Outlier detection using IQR method
        Q1 = numeric_df[col].quantile(0.25)
        Q3 = numeric_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = numeric_df[(numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)][col]
        
        outlier_info[col] = {
            'count': len(outliers),
            'percentage': (len(outliers) / len(numeric_df[col].dropna())) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    
    return render_template('outlier_analysis.html', plots=plots, outlier_info=outlier_info)

if __name__ == '__main__':
    app.run(debug=True)
