"""
CSV Reader Module
Handles loading and parsing sales data from CSV files.
"""

import csv
import re
from typing import List, Optional, Dict
from pathlib import Path

from models import SalesRecord


def find_column_mapping(headers: List[str]) -> Dict[str, str]:
    """
    Map CSV columns to expected field names using flexible matching.
    
    Handles common variations of column names.
    
    Args:
        headers: List of column names from CSV header
        
    Returns:
        Dictionary mapping expected fields to actual column names
    """
    normalized_headers = {col.lower().strip(): col for col in headers}
    mapping = {}
    
    # Map product (try: product, product name, product_name, name)
    for key in ['product', 'product name', 'product_name', 'name']:
        if key in normalized_headers:
            mapping['product'] = normalized_headers[key]
            break
    
    # Map unit_price (try: unit_price, price, sale price, sale_price, cost, price_each, price each)
    # Note: 'sales' column might be total revenue, not unit price
    for key in ['unit_price', 'price', 'sale price', 'sale_price', 'cost', 'price_each', 'price each']:
        if key in normalized_headers:
            mapping['unit_price'] = normalized_headers[key]
            break
    
    # Map region (try: region, brand, location, area, product_category, product category, category)
    for key in ['region', 'brand', 'location', 'area', 'product_category', 'product category', 'category']:
        if key in normalized_headers:
            mapping['region'] = normalized_headers[key]
            break
    
    # Map units_sold (try: units_sold, quantity, number of ratings, number_of_ratings, 
    # number of reviews, number_of_reviews, count, qty)
    for key in ['units_sold', 'quantity', 'number of ratings', 'number_of_ratings',
                'number of reviews', 'number_of_reviews', 'count', 'qty']:
        if key in normalized_headers:
            mapping['units_sold'] = normalized_headers[key]
            break
    
    # Map date (try: date, sale date, sale_date, timestamp, time, order_date, order date, order date)
    for key in ['date', 'sale date', 'sale_date', 'timestamp', 'time', 'order_date', 'order date', 'orderdate']:
        if key in normalized_headers:
            mapping['date'] = normalized_headers[key]
            break
    
    # Map total_revenue (optional) - try sales first as it's often total revenue
    for key in ['sales', 'total_revenue', 'revenue', 'total', 'amount']:
        if key in normalized_headers:
            mapping['total_revenue'] = normalized_headers[key]
            break
    
    return mapping


def validate_minimum_columns(mapping: Dict[str, str]) -> bool:
    """
    Validate that minimum required columns are present.
    
    At minimum, we need product and unit_price to perform meaningful analysis.
    
    Args:
        mapping: Column mapping dictionary
        
    Returns:
        True if minimum columns are present
    """
    return 'product' in mapping and 'unit_price' in mapping


def parse_float(value: str, default: float = 0.0) -> float:
    """
    Safely parse a string to float, handling missing or invalid values.
    
    Args:
        value: String value to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed float value or default
    """
    try:
        # Remove commas and other formatting
        cleaned = str(value).strip().replace(',', '')
        return float(cleaned) if cleaned else default
    except (ValueError, AttributeError):
        return default


def normalize_date(date_str: str) -> str:
    """
    Normalize date string to YYYY-MM-DD format.
    Handles various date formats including DD-MM-YYYY, MM-DD-YYYY, YYYY-MM-DD.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Date string in YYYY-MM-DD format, or original if parsing fails
    """
    if not date_str or not date_str.strip():
        return ""
    
    date_str = date_str.strip()
    
    # Try to parse various date formats
    if '-' in date_str or '/' in date_str:
        parts = date_str.replace('/', '-').split('-')
        if len(parts) == 3:
            try:
                # Check if first part is 4 digits (YYYY-MM-DD format)
                if len(parts[0]) == 4:
                    # Already in YYYY-MM-DD format
                    return date_str
                # Check if third part is 4 digits (DD-MM-YYYY or MM-DD-YYYY)
                elif len(parts[2]) == 4:
                    # If first part > 12, it's DD-MM-YYYY
                    if int(parts[0]) > 12:
                        day, month, year = parts[0], parts[1], parts[2]
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        # Assume MM-DD-YYYY
                        month, day, year = parts[0], parts[1], parts[2]
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                # Handle 2-digit year (M/D/YY or DD/MM/YY format)
                elif len(parts[2]) == 2:
                    # Convert 2-digit year to 4-digit (assume 20XX for years 00-99)
                    year_2digit = int(parts[2])
                    year_4digit = 2000 + year_2digit if year_2digit < 100 else year_2digit
                    # If first part > 12, it's DD-MM-YY
                    if int(parts[0]) > 12:
                        day, month = parts[0], parts[1]
                        return f"{year_4digit}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        # Assume MM-DD-YY
                        month, day = parts[0], parts[1]
                        return f"{year_4digit}-{month.zfill(2)}-{day.zfill(2)}"
                else:
                    # Can't determine format, return as is
                    return date_str
            except (ValueError, IndexError):
                pass
    
    # If already in YYYY-MM-DD format or can't parse, return as is
    return date_str


def parse_row(row: dict, mapping: Dict[str, str], row_number: int) -> Optional[SalesRecord]:
    """
    Parse a single CSV row into a SalesRecord object.
    Skips malformed rows and returns None if parsing fails.
    
    Args:
        row: Dictionary representing a CSV row
        mapping: Column mapping dictionary
        row_number: Row number for generating default date if needed
        
    Returns:
        SalesRecord object or None if row is malformed
    """
    try:
        # Get product (required)
        product_col = mapping.get('product')
        if not product_col or not row.get(product_col):
            return None
        product = str(row[product_col]).strip()
        if not product:
            return None
        
        # Get unit_price (required)
        # If we have Sales (total_revenue) and Quantity, calculate unit_price
        price_col = mapping.get('unit_price')
        revenue_col = mapping.get('total_revenue')
        units_col = mapping.get('units_sold')
        
        if price_col:
            unit_price = parse_float(row.get(price_col, '0'))
        elif revenue_col and units_col:
            # Calculate unit_price from total_revenue / units_sold
            total_rev = parse_float(row.get(revenue_col, '0'))
            units = parse_float(row.get(units_col, '1'))
            if units > 0:
                unit_price = total_rev / units
            else:
                return None
        else:
            return None
        
        if unit_price <= 0:
            return None
        
        # Get region (use brand or default)
        region_col = mapping.get('region')
        if region_col and row.get(region_col):
            region = str(row[region_col]).strip()
        else:
            region = "Unknown"
        
        # Get units_sold (use available data or default to 1)
        units_col = mapping.get('units_sold')
        if units_col and row.get(units_col):
            units_sold = parse_float(row.get(units_col, '1'))
            # If units_sold is 0 or negative, default to 1
            if units_sold <= 0:
                units_sold = 1.0
        else:
            units_sold = 1.0  # Default to 1 if not available
        
        # Get date (use available or generate default)
        date_col = mapping.get('date')
        if date_col and row.get(date_col):
            date_str = str(row[date_col]).strip()
            # Normalize date format to YYYY-MM-DD
            date = normalize_date(date_str)
            # If date is empty or invalid after normalization, use default
            if not date or len(date) < 4:
                date = f"2024-01-{min(28, row_number % 28 + 1):02d}"
        else:
            # Generate a default date based on row number
            date = f"2024-01-{min(28, row_number % 28 + 1):02d}"
        
        # Get total_revenue (optional, will be calculated if missing)
        revenue_col = mapping.get('total_revenue')
        total_revenue = parse_float(row.get(revenue_col, '0')) if revenue_col else 0.0
        
        return SalesRecord(
            date=date,
            product=product,
            region=region,
            units_sold=units_sold,
            unit_price=unit_price,
            total_revenue=total_revenue
        )
    except (KeyError, ValueError, AttributeError, TypeError):
        return None


def parse_month_column(month_str: str) -> Optional[str]:
    """
    Parse month column name to YYYY-MM format.
    Handles various formats like 'janv-12', 'Feb 2012', 'mars-12', etc.
    
    Args:
        month_str: Month column name
        
    Returns:
        Date string in YYYY-MM format or None if can't parse
    """
    month_str = month_str.strip().lower()
    
    # Month name mappings
    month_map = {
        'jan': '01', 'janv': '01', 'january': '01',
        'feb': '02', 'february': '02',
        'mar': '03', 'mars': '03', 'march': '03',
        'apr': '04', 'april': '04',
        'may': '05',
        'jun': '06', 'juin': '06', 'june': '06',
        'jul': '07', 'juil': '07', 'july': '07',
        'aug': '08', 'august': '08',
        'sep': '09', 'sept': '09', 'september': '09',
        'oct': '10', 'october': '10',
        'nov': '11', 'november': '11',
        'dec': '12', 'december': '12'
    }
    
    # Try to extract year and month
    import re
    # Look for 4-digit year
    year_match = re.search(r'20\d{2}', month_str)
    if year_match:
        year = year_match.group()
    else:
        # Look for 2-digit year
        year_match = re.search(r'\b(\d{2})\b', month_str)
        if year_match:
            year_2digit = int(year_match.group(1))
            year = f"20{year_2digit:02d}" if year_2digit < 100 else str(year_2digit)
        else:
            return None
    
    # Find month
    month = None
    for key, value in month_map.items():
        if key in month_str:
            month = value
            break
    
    if month:
        return f"{year}-{month}"
    return None


def is_pivot_table_format(headers: List[str]) -> bool:
    """
    Check if CSV is in pivot table format (product rows, time period columns).
    
    Args:
        headers: List of column names
        
    Returns:
        True if appears to be pivot table format
    """
    # Check for common pivot table indicators:
    # 1. Has Make/Model or similar product identifier columns
    # 2. Has many date-like columns (month names, years)
    normalized = [h.lower().strip() for h in headers]
    
    has_product_cols = any(col in ['make', 'model', 'product', 'name'] for col in normalized)
    date_like_cols = sum(1 for h in headers if parse_month_column(h) is not None)
    
    # If we have product columns and many date-like columns, it's likely pivot format
    return has_product_cols and date_like_cols >= 3


def load_pivot_table_data(csv_path: str) -> List[SalesRecord]:
    """
    Load data from pivot table format CSV (product rows, time period columns).
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of SalesRecord objects
    """
    records: List[SalesRecord] = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        
        # Find product identifier columns
        normalized_headers = {h.lower().strip(): h for h in headers}
        make_col = None
        model_col = None
        
        for key in ['make', 'brand']:
            if key in normalized_headers:
                make_col = normalized_headers[key]
                break
        
        for key in ['model', 'product', 'name']:
            if key in normalized_headers:
                model_col = normalized_headers[key]
                break
        
        if not make_col or not model_col:
            raise ValueError("Pivot table format requires Make and Model columns")
        
        # Process each row (each row is a product)
        for row_num, row in enumerate(reader, start=2):
            make = str(row.get(make_col, '')).strip()
            model = str(row.get(model_col, '')).strip()
            
            if not make or not model:
                continue
            
            product = f"{make} {model}"
            region = "USA"  # Default region for this dataset
            
            # Process each date column
            prev_value = 0.0
            for col in headers:
                if col in [make_col, model_col, 'Logo']:
                    continue
                
                # Try to parse as date
                date_str = parse_month_column(col)
                if not date_str:
                    continue
                
                # Get value for this month
                value_str = row.get(col, '').strip()
                if not value_str or value_str == '':
                    continue
                
                # Parse value (handle comma-separated numbers)
                try:
                    value = parse_float(value_str)
                    if value <= 0:
                        continue
                    
                    # Calculate incremental units (current - previous)
                    # If value is less than previous, use the value as-is (might be reset)
                    units_sold = max(0, value - prev_value) if value >= prev_value else value
                    prev_value = value
                    
                    # Use a default unit price (since not provided)
                    # Could be calculated from average or set to 1
                    unit_price = 1.0  # Default since price not available
                    total_revenue = units_sold * unit_price
                    
                    # Create date with day 01
                    date = f"{date_str}-01"
                    
                    record = SalesRecord(
                        date=date,
                        product=product,
                        region=region,
                        units_sold=units_sold,
                        unit_price=unit_price,
                        total_revenue=total_revenue
                    )
                    records.append(record)
                except (ValueError, TypeError):
                    continue
    
    return records


def load_sales_data(csv_path: str) -> List[SalesRecord]:
    """
    Load sales data from a CSV file.
    
    Validates required columns, skips malformed rows, and converts
    data to SalesRecord objects. Handles various CSV formats flexibly.
    Automatically detects pivot table format and handles it appropriately.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of SalesRecord objects
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV is missing minimum required columns
    """
    file_path = Path(csv_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # First, check if it's pivot table format
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        
        if not headers:
            raise ValueError("CSV file appears to be empty or has no headers")
        
        # Check if pivot table format
        if is_pivot_table_format(headers):
            return load_pivot_table_data(csv_path)
    
    # Standard format processing
    records: List[SalesRecord] = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        
        # Create flexible column mapping
        mapping = find_column_mapping(headers)
        
        if not validate_minimum_columns(mapping):
            raise ValueError(
                f"CSV missing minimum required columns. Need at least: product and price. "
                f"Found columns: {headers}"
            )
        
        # Process each row, filtering out None values (malformed rows)
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (row 1 is header)
            record = parse_row(row, mapping, row_num)
            if record is not None:
                records.append(record)
    
    return records
