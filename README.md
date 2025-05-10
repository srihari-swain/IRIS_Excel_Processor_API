# Excel Process FastAPI
A FastAPI-based REST API for extracting and analyzing data from Excel files.

## Author Information
- **Developer:** Srihari Swain
- **Email:** srihariswain2001@gmail.com
- **GitHub:** https://github.com/srihari-swain

## Project Timeline
- **Development Time:** Approximately 10 hours

## Overview
This project provides a robust API for interacting with Excel files, allowing users to:
- List all tables in an Excel file
- Get details about specific tables
- Calculate sum, max, and min values for specific rows in tables

The system is designed with clean architecture principles, separating concerns between file handling, data processing, and API endpoints.

## Project Structure
```
├── __init__.py
└── src
    ├── comms
    │   ├── client
    │   │   └── streamlit
    │   │       └── app.py
    │   └── server
    │       └── rest_api
    │           └── api.py
    ├── configs
    │   └── config.json
    ├── Data
    │   └── capbudg.xls
    ├── main.py
    ├── processor
    │   └── excel_processor.py
    └── utils
        ├── config_loader.py
        ├── exceptions.py
        ├── filter.py
```

## API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | Root endpoint showing API is running | None |
| `/list_tables` | GET | List all tables in the Excel file | None |
| `/get_table_details` | GET | Get details for a specific table | `table_name` |
| `/row_sum` | GET | Get the sum of numeric values in a row | `table_name`, `row_name` |
| `/row_max` | GET | Get the maximum numeric value in a row | `table_name`, `row_name` |
| `/row_min` | GET | Get the minimum numeric value in a row | `table_name`, `row_name` |

## Error Handling
The API includes comprehensive error handling for various scenarios:
- File not found errors
- Table not found errors
- Row not found errors
- Invalid file format errors 
- Unexpected exceptions

Each error is returned with an appropriate HTTP status code and a descriptive message.

## Configuration
The API loads configuration from a JSON file located at `src/configs/config.json`. This file includes important settings for the application:

```json
{
    "title": "IRIS-Excel-API",
    "description": "",
    "version": "0.0.1",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "excel_file_path": "src/Data/capbudg.xls",
    "app": "src.comms.server.rest_api.api:app",
    "host": "0.0.0.0",
    "port": 9090,
    "reload": false,
    "workers": 1,
    "allow_origins": ["*"],
    "allow_credentials": true,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}
```

### Configuration Parameters:
- `title`: Title of the API shown in documentation
- `description`: Description of the API shown in documentation
- `version`: API version number
- `excel_file_path`: Path to the Excel file to be processed
- `allow_origins`, `allow_credentials`, `allow_methods`, `allow_headers`: CORS settings
- `docs_url`: URL path for Swagger UI documentation
- `redoc_url`: URL path for ReDoc documentation

To use a different Excel file, simply update the `excel_file_path` parameter in the config.json file.

## Installation and Setup

### Prerequisites
- Python 
- pip (Python package installer)

### Setting Up the Environment
1. Clone the repository:
```bash
git clone https://github.com/srihari-swain/IRIS_Excel_Processor_API.git
cd IRIS_Excel_Processor_API
```

2. Create a Python virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application
To run the application, use the FastAPI server:
```bash
python src/main.py
```

This will start the API server with hot-reloading enabled for development.

## API Documentation
The API documentation is available at:
- Swagger UI: `/docs` (or custom URL from config)
- ReDoc: `/redoc` (or custom URL from config)

## Streamlit Client
The project includes a Streamlit web interface for easier interaction with the API.

### Running the Streamlit App
1. Make sure the FastAPI server is running first
2. Open a new terminal and activate your virtual environment
3. Run the Streamlit app:
```bash
streamlit run src/comms/client/streamlit/app.py
```

This will start the web interface and automatically open it in your default web browser.





Below is a screenshot of the Streamlit app in action, which provides a convenient way to interact with the API without needing to make API requests manually.

![alt text](<Screenshot from 2025-05-10 19-58-13.png>)
