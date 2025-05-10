class ExcelAPIException(Exception):
    """Base exception for Excel API errors."""

class TableNotFoundException(ExcelAPIException):
    """Raised when a table is not found."""

class RowNotFoundException(ExcelAPIException):
    """Raised when a row is not found."""

class FileNotFoundAPIException(ExcelAPIException):
    """Raised when the Excel file is not found."""
