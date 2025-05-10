import os
import re
import math
import pandas as pd 

from typing import List, Dict, Any

class FileHandler:
    """
    Handles file reading and checking.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath

    def file_exists(self) -> bool:
        """Checks if the file exists."""
        return os.path.exists(self.filepath)

    def read_excel(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Excel file '{self.filepath}' not found.")
        ext = os.path.splitext(self.filepath)[1].lower()
        if ext not in [".xls", ".xlsx"]:
            raise ValueError("Unsupported file extension. Only .xls and .xlsx are supported.")
        try:
            return pd.read_excel(self.filepath, header=None)
        except Exception as e:
            raise RuntimeError(f"Failed to read the Excel file: {str(e)}")


class TableExtractor:
    """
    Extracts tables from the Excel data.
    """
    @staticmethod
    def is_table_header(cell: Any) -> bool:
        """Identifies if a cell is a valid table header."""
        return isinstance(cell, str) and cell.strip() and cell.isupper() and len(cell.strip()) > 2
    
    def extract_tables(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extracts tables from the provided dataframe."""
        tables = []
        current_table = None
        current_data = []
        for _, row in df.iterrows():
            first_cell = row.iloc[0]
            if self.is_table_header(first_cell):
                if current_table and current_data:
                    tables.append({"name": current_table, "rows": current_data})
                current_table = first_cell.strip()
                current_data = []
            elif not row.isnull().all():
                current_data.append(row.tolist())
        if current_table and current_data:
            tables.append({"name": current_table, "rows": current_data})
        return tables


class JsonCleaner:
    """
    Cleans NaN and infinite values from a data structure.
    """
    @staticmethod
    def clean_json(obj: Any) -> Any:
        """Recursively replace NaN and inf with None for JSON serialization."""
        if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        elif isinstance(obj, list):
            return [JsonCleaner.clean_json(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: JsonCleaner.clean_json(v) for k, v in obj.items()}
        else:
            return obj


class ExcelProcessor:
    """
    Processes Excel file data, extracts tables, and cleans JSON data.
    """
    def __init__(self, filepath: str):
        self.file_handler = FileHandler(filepath)
        self.table_extractor = TableExtractor()

    def get_tables(self) -> List[Dict[str, Any]]:
        """Gets tables from the Excel file."""
        try:
            df = self.file_handler.read_excel()
            return self.table_extractor.extract_tables(df)
        except FileNotFoundError as fnf_error:
            raise fnf_error
        except Exception as e:
            raise f"Error processing Excel file: {str(e)}"
        
    def process(self) -> List[Dict[str, Any]]:
        """Clean and return the tables in JSON-friendly format."""
        tables = self.get_tables()
        cleaned_tables = [JsonCleaner.clean_json(table) for table in tables]
        return cleaned_tables
