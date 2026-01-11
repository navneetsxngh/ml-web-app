from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from mysql.connector import Error
import psycopg2
from psycopg2 import Error
import pandas as pd
import numpy as np
import json
import io
import base64
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production-ready configuration using environment variables
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=int(os.getenv('SESSION_LIFETIME_HOURS', 2)))
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 64 * 1024 * 1024))

# Database Configuration - Automatically loads from .env file
# Make sure you've configured your .env file with your MySQL credentials
# See ENV_SETUP_GUIDE.md or run: python setup_env.py
# For PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', '')

if DATABASE_URL:
    # Production: Use Render PostgreSQL connection string
    DB_CONFIG = DATABASE_URL
else:
    # Local development: Use individual parameters
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'database': os.getenv('DB_NAME', 'ml_webapp_db')
    }

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'json', 'xml'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Create and return a database connection"""
    try:
        if isinstance(DB_CONFIG, str):
            # Using DATABASE_URL (production)
            connection = psycopg2.connect(DB_CONFIG)
        else:
            # Using individual parameters (local)
            connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def init_database():
    """Initialize the database if it doesn't exist"""
    try:
        # For PostgreSQL, database is already created by Render
        # Just verify connection
        conn = get_db_connection()
        if conn:
            print(f"Database connection is ready.")
            conn.close()
    except Error as e:
        print(f"Error connecting to database: {e}")

def save_dataframe_to_db(df, table_name):
    """Save a pandas DataFrame to MySQL database"""
    try:
        connection = get_db_connection()
        if connection is None:
            return False
        
        cursor = connection.cursor()
        
        # Drop table if exists
        cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        
        # Create table dynamically based on DataFrame columns
        columns_sql = []
        for col in df.columns:
            # Determine SQL data type based on pandas dtype
            dtype = df[col].dtype
            if dtype == 'int64':
                sql_type = 'INT'
            elif dtype == 'float64':
                sql_type = 'DOUBLE'
            else:
                sql_type = 'TEXT'
            columns_sql.append(f"`{col}` {sql_type}")
        
        create_table_sql = f"CREATE TABLE `{table_name}` ({', '.join(columns_sql)})"
        cursor.execute(create_table_sql)
        
        # Insert data
        for _, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join([f"`{col}`" for col in df.columns])
            insert_sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
            cursor.execute(insert_sql, tuple(row))
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error saving DataFrame to database: {e}")
        return False

def load_dataframe_from_db(table_name):
    """Load a pandas DataFrame from MySQL database"""
    try:
        connection = get_db_connection()
        if connection is None:
            return None
        
        query = f"SELECT * FROM `{table_name}`"
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except Error as e:
        print(f"Error loading DataFrame from database: {e}")
        return None

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/data_source')
def data_source():
    """Data source selection page"""
    return render_template('data_source.html')

@app.route('/create_csv', methods=['GET', 'POST'])
def create_csv():
    """Manual CSV creation interface"""
    if request.method == 'POST':
        try:
            data = request.json
            columns = data.get('columns', [])
            rows = data.get('rows', [])
            
            if not columns or not rows:
                return jsonify({'success': False, 'message': 'No data provided'})
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=columns)
            
            # Save to database
            table_name = f"user_data_{session.get('session_id', 'default')}"
            if save_dataframe_to_db(df, table_name):
                session['table_name'] = table_name
                session['columns'] = list(df.columns)
                return jsonify({'success': True, 'message': 'Data saved successfully'})
            else:
                return jsonify({'success': False, 'message': 'Database error'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('create_csv.html')

@app.route('/upload_data', methods=['GET', 'POST'])
def upload_data():
    """File upload interface"""
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'success': False, 'message': 'No file uploaded'})
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'success': False, 'message': 'No file selected'})
            
            if not allowed_file(file.filename):
                return jsonify({'success': False, 'message': 'Invalid file type. Only CSV, JSON, and XML are allowed.'})
            
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            
            # Read file based on type
            if file_ext == 'csv':
                df = pd.read_csv(file)
            elif file_ext == 'json':
                df = pd.read_json(file)
            elif file_ext == 'xml':
                df = pd.read_xml(file)
            
            # Generate unique table name
            import time
            table_name = f"user_data_{int(time.time())}"
            
            # Save to database
            if save_dataframe_to_db(df, table_name):
                session['table_name'] = table_name
                session['columns'] = list(df.columns)
                return jsonify({'success': True, 'message': 'File uploaded successfully'})
            else:
                return jsonify({'success': False, 'message': 'Database error'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error processing file: {str(e)}'})
    
    return render_template('upload_data.html')

@app.route('/visualization')
def visualization():
    """Data visualization and inspection page"""
    if 'table_name' not in session:
        return redirect(url_for('data_source'))
    
    df = load_dataframe_from_db(session['table_name'])
    if df is None:
        return redirect(url_for('data_source'))
    
    # Prepare data info
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    
    return render_template('visualization.html',
                         columns=list(df.columns),
                         head_html=df.head(10).to_html(classes='table table-striped', index=False),
                         info=info_str,
                         dtypes=df.dtypes.to_dict(),
                         describe_html=df.describe().to_html(classes='table table-striped'))

@app.route('/get_value_counts', methods=['POST'])
def get_value_counts():
    """Get value counts for selected columns"""
    try:
        data = request.json
        columns = data.get('columns', [])
        
        if 'table_name' not in session:
            return jsonify({'success': False, 'message': 'No data loaded'})
        
        df = load_dataframe_from_db(session['table_name'])
        if df is None:
            return jsonify({'success': False, 'message': 'Error loading data'})
        
        results = {}
        for col in columns:
            if col in df.columns:
                value_counts = df[col].value_counts().to_dict()
                results[col] = value_counts
        
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/preprocessing', methods=['GET', 'POST'])
def preprocessing():
    """Data preprocessing page"""
    if 'table_name' not in session:
        return redirect(url_for('data_source'))
    
    df = load_dataframe_from_db(session['table_name'])
    if df is None:
        return redirect(url_for('data_source'))
    
    # Get numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    return render_template('preprocessing.html',
                         numeric_columns=numeric_cols,
                         categorical_columns=categorical_cols,
                         all_columns=list(df.columns))

@app.route('/handle_missing', methods=['POST'])
def handle_missing():
    """Handle missing values"""
    try:
        data = request.json
        method = data.get('method')
        
        if 'table_name' not in session:
            return jsonify({'success': False, 'message': 'No data loaded'})
        
        df = load_dataframe_from_db(session['table_name'])
        if df is None:
            return jsonify({'success': False, 'message': 'Error loading data'})
        
        if method == 'drop':
            df = df.dropna()
        elif method in ['mean', 'median', 'mode']:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if method == 'mean':
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            elif method == 'median':
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            elif method == 'mode':
                for col in df.columns:
                    if df[col].isna().any():
                        mode_val = df[col].mode()
                        if len(mode_val) > 0:
                            df[col].fillna(mode_val[0], inplace=True)
        
        # Save processed data
        if save_dataframe_to_db(df, session['table_name']):
            return jsonify({'success': True, 'message': f'Missing values handled using {method}'})
        else:
            return jsonify({'success': False, 'message': 'Database error'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/visualize_outliers', methods=['POST'])
def visualize_outliers():
    """Visualize outliers using boxplots"""
    try:
        data = request.json
        columns = data.get('columns', [])
        
        if 'table_name' not in session:
            return jsonify({'success': False, 'message': 'No data loaded'})
        
        df = load_dataframe_from_db(session['table_name'])
        if df is None:
            return jsonify({'success': False, 'message': 'Error loading data'})
        
        # Create boxplot
        fig, ax = plt.subplots(figsize=(10, 6))
        df[columns].boxplot(ax=ax)
        ax.set_title('Outlier Detection - Before Handling')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Convert plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return jsonify({'success': True, 'image': image_base64})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/handle_outliers', methods=['POST'])
def handle_outliers():
    """Handle outliers using capping or trimming"""
    try:
        data = request.json
        columns = data.get('columns', [])
        method = data.get('method')  # 'capping' or 'trimming'
        
        if 'table_name' not in session:
            return jsonify({'success': False, 'message': 'No data loaded'})
        
        df = load_dataframe_from_db(session['table_name'])
        if df is None:
            return jsonify({'success': False, 'message': 'Error loading data'})
        
        # Before handling image
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        df[columns].boxplot(ax=ax1)
        ax1.set_title('Before Handling Outliers')
        ax1.set_xlabel('Columns')
        ax1.set_ylabel('Values')
        ax1.tick_params(axis='x', rotation=45)
        
        # Handle outliers
        df_processed = df.copy()
        for col in columns:
            if col in df_processed.columns and df_processed[col].dtype in [np.int64, np.float64]:
                Q1 = df_processed[col].quantile(0.25)
                Q3 = df_processed[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                if method == 'capping':
                    # Winsorizing
                    df_processed[col] = df_processed[col].clip(lower_bound, upper_bound)
                elif method == 'trimming':
                    # Remove outliers
                    df_processed = df_processed[
                        (df_processed[col] >= lower_bound) & 
                        (df_processed[col] <= upper_bound)
                    ]
        
        # After handling image
        df_processed[columns].boxplot(ax=ax2)
        ax2.set_title('After Handling Outliers')
        ax2.set_xlabel('Columns')
        ax2.set_ylabel('Values')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Convert plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        # Save processed data
        if save_dataframe_to_db(df_processed, session['table_name']):
            return jsonify({'success': True, 'image': image_base64, 'message': f'Outliers handled using {method}'})
        else:
            return jsonify({'success': False, 'message': 'Database error'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/encode_data', methods=['POST'])
def encode_data():
    """Encode categorical columns"""
    try:
        data = request.json
        columns = data.get('columns', [])
        method = data.get('method')  # 'label' or 'ordinal'
        
        if 'table_name' not in session:
            return jsonify({'success': False, 'message': 'No data loaded'})
        
        df = load_dataframe_from_db(session['table_name'])
        if df is None:
            return jsonify({'success': False, 'message': 'Error loading data'})
        
        encoders = {}
        for col in columns:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                encoders[col] = le
        
        # Store encoders in session for later use
        session['encoders'] = {col: list(encoders[col].classes_) for col in encoders}
        
        # Save processed data
        if save_dataframe_to_db(df, session['table_name']):
            return jsonify({'success': True, 'message': f'{len(columns)} columns encoded using {method} encoding'})
        else:
            return jsonify({'success': False, 'message': 'Database error'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/scale_data', methods=['POST'])
def scale_data():
    """Scale numerical columns"""
    try:
        data = request.json
        columns = data.get('columns', [])
        method = data.get('method')  # 'standard' or 'minmax'
        
        if 'table_name' not in session:
            return jsonify({'success': False, 'message': 'No data loaded'})
        
        df = load_dataframe_from_db(session['table_name'])
        if df is None:
            return jsonify({'success': False, 'message': 'Error loading data'})
        
        if method == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
        df[columns] = scaler.fit_transform(df[columns])
        
        # Store scaler parameters
        session['scaler_type'] = method
        session['scaler_columns'] = columns
        
        # Save processed data
        if save_dataframe_to_db(df, session['table_name']):
            return jsonify({'success': True, 'message': f'{len(columns)} columns scaled using {method} scaler'})
        else:
            return jsonify({'success': False, 'message': 'Database error'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/training', methods=['GET', 'POST'])
def training():
    """Model training page"""
    if 'table_name' not in session:
        return redirect(url_for('data_source'))
    
    df = load_dataframe_from_db(session['table_name'])
    if df is None:
        return redirect(url_for('data_source'))
    
    columns = list(df.columns)
    
    if request.method == 'POST':
        try:
            data = request.json
            algorithm = data.get('algorithm')
            target = data.get('target')
            test_size = float(data.get('test_size', 0.2))
            random_state = int(data.get('random_state', 42))
            
            # Prepare data
            X = df.drop(columns=[target])
            y = df[target]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            # Train model
            if algorithm == 'linear':
                model = LinearRegression()
            elif algorithm == 'ridge':
                model = Ridge()
            elif algorithm == 'lasso':
                model = Lasso()
            elif algorithm == 'logistic':
                model = LogisticRegression(max_iter=1000)
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            metrics = {}
            if algorithm in ['linear', 'ridge', 'lasso']:
                metrics['r2_score'] = float(r2_score(y_test, y_pred))
                metrics['mse'] = float(mean_squared_error(y_test, y_pred))
                metrics['mae'] = float(mean_absolute_error(y_test, y_pred))
                metrics['rmse'] = float(np.sqrt(metrics['mse']))
            else:
                metrics['accuracy'] = float(accuracy_score(y_test, y_pred.round()))
            
            # Store model info in session
            session['model_type'] = algorithm
            session['target_column'] = target
            session['feature_columns'] = list(X.columns)
            session['model_trained'] = True
            
            # Store model coefficients or feature importance
            if hasattr(model, 'coef_'):
                session['model_coef'] = model.coef_.tolist()
            if hasattr(model, 'intercept_'):
                session['model_intercept'] = float(model.intercept_)
            
            return jsonify({'success': True, 'metrics': metrics})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('training.html', columns=columns)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction interface"""
    if not session.get('model_trained'):
        return redirect(url_for('training'))
    
    feature_columns = session.get('feature_columns', [])
    
    if request.method == 'POST':
        try:
            data = request.json
            input_values = data.get('values', {})
            
            # Prepare input data
            input_df = pd.DataFrame([input_values])
            
            # Recreate model (in production, you'd save/load the actual model)
            df = load_dataframe_from_db(session['table_name'])
            target = session['target_column']
            X = df.drop(columns=[target])
            y = df[target]
            
            algorithm = session['model_type']
            if algorithm == 'linear':
                model = LinearRegression()
            elif algorithm == 'ridge':
                model = Ridge()
            elif algorithm == 'lasso':
                model = Lasso()
            elif algorithm == 'logistic':
                model = LogisticRegression(max_iter=1000)
            
            model.fit(X, y)
            
            # Make prediction
            prediction = model.predict(input_df)
            
            return jsonify({
                'success': True, 
                'prediction': float(prediction[0])
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('predict.html', feature_columns=feature_columns)

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Get port from environment variable (for cloud platforms like Render)
    port = int(os.getenv('PORT', 5000))
    
    # Run the app
    # Debug mode is disabled in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)