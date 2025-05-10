
import math
import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.processor.excel_processor import ExcelProcessor
from src.utils.filter import extract_numeric_value, clean_number
from src.utils.config_loader import read_base_config
from src.utils.exceptions import TableNotFoundException, RowNotFoundException, FileNotFoundAPIException

# Load config once
CONFIG = read_base_config()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app with config
app = FastAPI(
    title=CONFIG["title"],
    description=CONFIG["description"],
    version=CONFIG["version"],
    docs_url=CONFIG.get("docs_url", "/docs"),
    redoc_url=CONFIG.get("redoc_url", "/redoc")
)

# Add CORS middleware using config
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.get("allow_origins", ["*"]),
    allow_credentials=CONFIG.get("allow_credentials", True),
    allow_methods=CONFIG.get("allow_methods", ["*"]),
    allow_headers=CONFIG.get("allow_headers", ["*"]),
)

# Excel Processor instance (single responsibility)
excel_processor = ExcelProcessor(CONFIG["excel_file_path"])

# Exception handlers (single responsibility)
@app.exception_handler(TableNotFoundException)
async def table_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(RowNotFoundException)
async def row_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(FileNotFoundAPIException)
async def file_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

# API Endpoints
@app.get("/list_tables", summary="List all table names in the Excel file")
def list_tables():
    try:
        tables = excel_processor.get_tables()
        if not tables:
            return {"tables": [], "message": "Excel file is empty or contains no tables."}
        table_names = [t["name"] for t in tables]
        logger.info(f"Tables found: {table_names}")
        return {"tables": table_names}
    except FileNotFoundError as e:
        raise FileNotFoundAPIException("Excel file not found.") from e
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error_type": type(e).__name__, "error_message": str(e)}
        )

@app.get("/get_table_details", summary="Get row names for all tables with a given name")
def get_table_details(table_name: str = Query(..., description="Name of the table")):
    try:
        tables = excel_processor.get_tables()
        if not tables:
            return {"tables": [], "message": "Excel file is empty or contains no tables."}
        # matching_tables = [t for t in tables if t["name"] == table_name]
        matching_tables = [t for t in tables if t["name"].lower() == table_name.lower()]
        if not matching_tables:
            raise TableNotFoundException(f"Table '{table_name}' not found.")
        all_row_names = []
        for t in matching_tables:
            row_names = []
            for row in t["rows"]:
                val = row[0]
                if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
                    val = None
                row_names.append(val)
            all_row_names.append(row_names)
        return {
            "table_name": table_name,
            "instances": len(matching_tables),
            "row_names": all_row_names
        }
    except FileNotFoundError as e:
        raise FileNotFoundAPIException("Excel file not found.") from e
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error_type": type(e).__name__, "error_message": str(e)}
        )

@app.get("/row_sum", summary="Sum the first numeric value in a given row of a table (searches all instances)")
def row_sum(
    table_name: str = Query(..., description="Name of the table"),
    row_name: str = Query(..., description="Name of the row (must match a row name from /get_table_details)")
):
    try:
        tables = excel_processor.get_tables()
        if not tables:
            return {"tables": [], "message": "Excel file is empty or contains no tables."}
        matching_tables = [t for t in tables if t["name"].lower() == table_name.lower()]
        if not matching_tables:
            raise TableNotFoundException(f"Table '{table_name}' not found.")
        for idx, t in enumerate(matching_tables):
            for row in t["rows"]:
                if str(row[0]).strip().lower() == str(row_name).strip().lower():
                    value = extract_numeric_value(row)
                    return {
                        "table_name": table_name,
                        "instance": idx,
                        "row_name": row_name,
                        "sum": clean_number(value),
                    }
        raise RowNotFoundException(f"Row '{row_name}' not found in any instance of table '{table_name}'.")
    except FileNotFoundError as e:
        raise FileNotFoundAPIException("Excel file not found.") from e
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error_type": type(e).__name__, "error_message": str(e)}
        )

@app.get("/row_max", summary="Get the maximum numeric value in a given row of a table")
def row_max(
    table_name: str = Query(..., description="Name of the table"),
    row_name: str = Query(..., description="Name of the row")
):
    try:
        tables = excel_processor.get_tables()
        if not tables:
            return {"tables": [], "message": "Excel file is empty or contains no tables."}
        matching_tables = [t for t in tables if t["name"] == table_name]
        if not matching_tables:
            raise TableNotFoundException(f"Table '{table_name}' not found.")
        max_value = None
        for t in matching_tables:
            for row in t["rows"]:
                if str(row[0]).strip().lower() == str(row_name).strip().lower():
                    nums = [
                        cell for cell in row[1:]
                        if isinstance(cell, (int, float)) and cell is not None and not (isinstance(cell, float) and (math.isnan(cell) or math.isinf(cell)))
                    ]
                    if nums:
                        row_max_val = max(nums)
                        if max_value is None or row_max_val > max_value:
                            max_value = row_max_val
        if max_value is None:
            raise RowNotFoundException(f"No numeric values found in row '{row_name}' of table '{table_name}'.")
        return {
            "table_name": table_name,
            "row_name": row_name,
            "max": clean_number(max_value)
        }
    except FileNotFoundError as e:
        raise FileNotFoundAPIException("Excel file not found.") from e
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error_type": type(e).__name__, "error_message": str(e)}
        )

@app.get("/row_min", summary="Get the minimum numeric value in a given row of a table")
def row_min(
    table_name: str = Query(..., description="Name of the table"),
    row_name: str = Query(..., description="Name of the row")
):
    try:
        tables = excel_processor.get_tables()
        if not tables:
            return {"tables": [], "message": "Excel file is empty or contains no tables."}
        matching_tables = [t for t in tables if t["name"] == table_name]
        if not matching_tables:
            raise TableNotFoundException(f"Table '{table_name}' not found.")
        min_value = None
        for t in matching_tables:
            for row in t["rows"]:
                if str(row[0]).strip().lower() == str(row_name).strip().lower():
                    nums = [
                        cell for cell in row[1:]
                        if isinstance(cell, (int, float)) and cell is not None and not (isinstance(cell, float) and (math.isnan(cell) or math.isinf(cell)))
                    ]
                    if nums:
                        row_min_val = min(nums)
                        if min_value is None or row_min_val < min_value:
                            min_value = row_min_val
        if min_value is None:
            raise RowNotFoundException(f"No numeric values found in row '{row_name}' of table '{table_name}'.")
        return {
            "table_name": table_name,
            "row_name": row_name,
            "min": clean_number(min_value)
        }
    except FileNotFoundError as e:
        raise FileNotFoundAPIException("Excel file not found.") from e
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error_type": type(e).__name__, "error_message": str(e)}
        )

@app.get("/", include_in_schema=False)
def root():
    return {"message": f"{CONFIG['title']} v{CONFIG['version']} is running."}

