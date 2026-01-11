# Machine Learning Web Application - Setup & Execution Guide

## Project Overview
This is a full-stack Machine Learning web application built with Flask, MySQL, and modern frontend technologies. It provides an end-to-end workflow for data processing, visualization, preprocessing, model training, and predictions.

## Technology Stack
- **Backend**: Python 3.8+, Flask
- **Database**: MySQL 8.0+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-Learn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## File Structure
```
ml_web_app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── create_csv.js      # Manual CSV creation logic
│   │   ├── upload_data.js     # File upload logic
│   │   ├── visualization.js   # Data visualization logic
│   │   ├── preprocessing.js   # Preprocessing logic
│   │   ├── training.js        # Model training logic
│   │   └── predict.js         # Prediction logic
│   └── images/                # (Optional) For storing images
└── templates/
    ├── index.html             # Landing page
    ├── data_source.html       # Data source selection
    ├── create_csv.html        # Manual CSV creation
    ├── upload_data.html       # File upload
    ├── visualization.html     # Data visualization
    ├── preprocessing.html     # Data preprocessing
    ├── training.html          # Model training
    └── predict.html           # Prediction interface
```

## Prerequisites

### 1. Python Installation
- Python 3.8 or higher
- Check version: `python --version` or `python3 --version`

### 2. MySQL Installation
- MySQL Workbench 8.0 or higher
- MySQL Server running on localhost (default port 3306)

### 3. pip (Python Package Manager)
- Usually comes with Python installation
- Upgrade pip: `python -m pip install --upgrade pip`

## Step-by-Step Setup Instructions

### Step 1: Install MySQL and Create Database User

1. **Install MySQL Workbench** (if not already installed):
   - Download from: https://dev.mysql.com/downloads/workbench/
   - Follow the installation wizard

2. **Start MySQL Server**:
   - Open MySQL Workbench
   - Connect to your local MySQL instance
   - Default connection: localhost:3306

3. **Configure MySQL Credentials**:
   - Open `app.py` in a text editor
   - Find the `DB_CONFIG` dictionary (around line 25):
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',              # CHANGE THIS to your MySQL username
       'password': 'password',      # CHANGE THIS to your MySQL password
       'database': 'ml_webapp_db'
   }
   ```
   - Update `user` and `password` with your MySQL credentials

4. **Note**: The application will automatically create the database `ml_webapp_db` on first run.

### Step 2: Set Up Python Virtual Environment (Recommended)

1. **Navigate to project directory**:
   ```bash
   cd /path/to/ml_web_app
   ```

2. **Create virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

### Step 3: Install Python Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- mysql-connector-python (MySQL database connector)
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib (visualization)
- seaborn (statistical visualization)
- scikit-learn (machine learning)
- lxml (XML processing)

**Installation may take 2-5 minutes depending on your internet connection.**

### Step 4: Verify Installation

```bash
pip list
```

You should see all packages from requirements.txt installed.

### Step 5: Run the Application

1. **Make sure MySQL Server is running**

2. **Run the Flask application**:
   ```bash
   # Windows
   python app.py
   
   # macOS/Linux
   python3 app.py
   ```

3. **You should see output like**:
   ```
   Database 'ml_webapp_db' is ready.
   * Serving Flask app 'app'
   * Debug mode: on
   * Running on http://0.0.0.0:5000
   ```

4. **Open your web browser and navigate to**:
   ```
   http://localhost:5000
   ```

## Using the Application

### Workflow Overview

1. **Landing Page** (index.html)
   - Introduction to the application
   - Click "Get Started" to begin

2. **Data Source Selection** (data_source.html)
   - Choose to create CSV manually OR upload a file
   
3a. **Create CSV Manually** (create_csv.html)
   - Enter column names (comma-separated)
   - Add rows of data
   - Data is saved to MySQL
   
3b. **Upload Data File** (upload_data.html)
   - Drag and drop or browse for file
   - Supports: CSV, JSON, XML (max 64MB)
   - Data is saved to MySQL

4. **Data Visualization** (visualization.html)
   - View dataset preview (first 10 rows)
   - See DataFrame info and data types
   - View statistical summary
   - Check value counts for selected columns

5. **Data Preprocessing** (preprocessing.html)
   - **Handle Missing Values**: Drop, fill with mean/median/mode
   - **Manage Outliers**: Visualize with boxplots, use capping or trimming
   - **Encode Categories**: Label or ordinal encoding
   - **Scale Features**: StandardScaler or MinMaxScaler

6. **Model Training** (training.html)
   - Select algorithm: Linear, Ridge, Lasso, or Logistic Regression
   - Choose target variable
   - Set test size and random state
   - View performance metrics

7. **Make Predictions** (predict.html)
   - Enter values for each feature
   - Get instant predictions
   - Make multiple predictions

## Features

### Data Handling
- ✅ Multiple file format support (CSV, JSON, XML)
- ✅ Manual data entry interface
- ✅ Automatic MySQL table creation
- ✅ Session-based data persistence

### Visualization
- ✅ DataFrame preview and info
- ✅ Statistical summaries
- ✅ Value count analysis
- ✅ Boxplot visualizations

### Preprocessing
- ✅ Missing value handling
- ✅ Outlier detection and handling
- ✅ Categorical encoding
- ✅ Feature scaling
- ✅ Before/after visualizations

### Machine Learning
- ✅ Multiple algorithms (Linear, Ridge, Lasso, Logistic Regression)
- ✅ Configurable train/test split
- ✅ Performance metrics (R², MSE, MAE, RMSE, Accuracy)
- ✅ Real-time predictions

### UI/UX
- ✅ Modern, colorful design
- ✅ Responsive layout
- ✅ Loading indicators
- ✅ Error handling with user-friendly messages
- ✅ "Select All" checkboxes for bulk operations

## Troubleshooting

### Database Connection Issues

**Error**: `Access denied for user 'root'@'localhost'`
- **Solution**: Update the `DB_CONFIG` in `app.py` with correct MySQL credentials

**Error**: `Can't connect to MySQL server`
- **Solution**: Ensure MySQL Server is running
- Start MySQL from MySQL Workbench or Services

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`
- **Solution**: Make sure virtual environment is activated and run `pip install -r requirements.txt`

### Port Already in Use

**Error**: `Address already in use`
- **Solution**: Change the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000
  ```

### File Upload Issues

**Error**: File size exceeds limit
- **Solution**: The limit is set to 64MB. For larger files, update `MAX_CONTENT_LENGTH` in `app.py`

### Visualization Issues

**Error**: Plots not displaying
- **Solution**: This is usually due to matplotlib backend issues. The app uses 'Agg' backend and base64 encoding, which should work in all environments.

## Security Notes

⚠️ **Important**: This application is designed for educational and development purposes.

For production deployment:
1. Change `app.secret_key` to a strong random value
2. Use environment variables for database credentials
3. Enable HTTPS
4. Implement user authentication
5. Add input validation and sanitization
6. Set `debug=False` in `app.run()`

## Sample Data

You can test the application with this sample CSV data:

```csv
Age,Gender,Salary,Experience,Purchased
25,Male,40000,1,No
30,Female,50000,3,Yes
35,Male,60000,5,Yes
28,Female,45000,2,No
40,Male,75000,10,Yes
```

Or create JSON/XML files with similar structure.

## Advanced Configuration

### Changing Database Name
Edit `DB_CONFIG` in `app.py`:
```python
'database': 'your_custom_db_name'
```

### Adjusting Session Lifetime
Edit in `app.py`:
```python
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=4)  # Changed from 2
```

### Adding More ML Algorithms
Add to the training route in `app.py` and update `training.html` and `training.js`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure MySQL credentials are correct
4. Check the terminal/console for error messages

## License

This project is created for educational purposes.

---

**Enjoy building your Machine Learning models! 🚀**