import re
import math

def extract_numeric_value(row):
    """
    Extracts the first numeric value from the row, handling percentages and strings.
    Returns None if no value is found.
    """
    for cell in row[1:]:
        if isinstance(cell, float):
            if cell is not None and not math.isnan(cell):
                if 0 < cell < 1:
                    return cell * 100
                else:
                    return cell
        elif isinstance(cell, int):
            return cell
        elif isinstance(cell, str):
            cleaned = cell.replace(',', '').strip()
            percent_match = re.match(r"(-?\d+\.?\d*)\s*%", cleaned)
            if percent_match:
                return float(percent_match.group(1))
            match = re.search(r"-?\d+\.?\d*", cleaned)
            if match:
                return float(match.group())
    return None

def clean_number(num):
    """Return int if number is whole, else round to 2 decimals."""
    if num is None:
        return None
    if isinstance(num, float):
        if num.is_integer():
            return int(num)
        return round(num, 2)
    return num
