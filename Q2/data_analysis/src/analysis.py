"""
Data Analysis Module
Implements various analysis functions using functional programming patterns.
"""

from typing import List, Dict, Tuple
from functools import reduce
from collections import defaultdict

from models import SalesRecord


def total_revenue(records: List[SalesRecord]) -> float:
    """
    Calculate total revenue across all sales records.
    
    Uses functional programming with reduce to sum revenues.
    
    Args:
        records: List of sales records
        
    Returns:
        Total revenue as float
    """
    return reduce(lambda acc, r: acc + r.total_revenue, records, 0.0)


def total_units_sold(records: List[SalesRecord]) -> float:
    """
    Calculate total units sold across all sales records.
    
    Uses functional programming with reduce to sum units.
    
    Args:
        records: List of sales records
        
    Returns:
        Total units sold as float
    """
    return reduce(lambda acc, r: acc + r.units_sold, records, 0.0)


def sales_by_product(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total revenue grouped by product.
    
    Uses dictionary comprehension and functional patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping product names to total revenue
    """
    # Group by product using defaultdict
    product_revenue = defaultdict(float)
    
    # Use map to extract product and revenue, then aggregate
    for record in records:
        product_revenue[record.product] += record.total_revenue
    
    return dict(product_revenue)


def sales_by_region(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total revenue grouped by region.
    
    Uses dictionary comprehension and functional patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping region names to total revenue
    """
    # Group by region using defaultdict
    region_revenue = defaultdict(float)
    
    # Use map to extract region and revenue, then aggregate
    for record in records:
        region_revenue[record.region] += record.total_revenue
    
    return dict(region_revenue)


def average_price_by_product(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate average unit price by product.
    
    Uses functional programming with map, filter, and comprehensions.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping product names to average unit price
    """
    # Group records by product
    product_records = defaultdict(list)
    for record in records:
        product_records[record.product].append(record)
    
    # Calculate average price for each product using functional approach
    return {
        product: sum(map(lambda r: r.unit_price, product_records[product])) 
                / len(product_records[product])
        for product in product_records
    }


def top_selling_product(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the product with the highest total revenue.
    
    Uses functional programming with max and lambda expressions.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (product_name, total_revenue)
    """
    if not records:
        return ("", 0.0)
    
    product_revenue = sales_by_product(records)
    
    # Use max with key function to find top product
    top_product = max(product_revenue.items(), key=lambda x: x[1])
    
    return top_product


def monthly_sales(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total revenue grouped by month (YYYY-MM format).
    
    Extracts month from date string and groups sales by month.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping month (YYYY-MM) to total revenue
    """
    # Extract month from date (assumes YYYY-MM-DD format)
    def extract_month(record: SalesRecord) -> str:
        """Extract YYYY-MM from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 2:
            return f"{date_parts[0]}-{date_parts[1]}"
        return record.date[:7] if len(record.date) >= 7 else "Unknown"
    
    # Group by month using functional approach
    monthly_revenue = defaultdict(float)
    
    # Use map to extract month and aggregate revenue
    for record in records:
        month = extract_month(record)
        monthly_revenue[month] += record.total_revenue
    
    return dict(monthly_revenue)


def average_revenue_per_transaction(records: List[SalesRecord]) -> float:
    """
    Calculate average revenue per transaction.
    
    Uses functional programming with reduce and len.
    
    Args:
        records: List of sales records
        
    Returns:
        Average revenue per transaction
    """
    if not records:
        return 0.0
    return total_revenue(records) / len(records)


def unique_products_count(records: List[SalesRecord]) -> int:
    """
    Count the number of unique products.
    
    Uses set comprehension for unique values.
    
    Args:
        records: List of sales records
        
    Returns:
        Number of unique products
    """
    return len({record.product for record in records})


def unique_regions_count(records: List[SalesRecord]) -> int:
    """
    Count the number of unique regions.
    
    Uses set comprehension for unique values.
    
    Args:
        records: List of sales records
        
    Returns:
        Number of unique regions
    """
    return len({record.region for record in records})


def top_n_products(records: List[SalesRecord], n: int = 5) -> List[Tuple[str, float]]:
    """
    Find top N products by revenue.
    
    Uses functional programming with sorted and lambda.
    
    Args:
        records: List of sales records
        n: Number of top products to return
        
    Returns:
        List of tuples (product_name, revenue) sorted by revenue descending
    """
    product_revenue = sales_by_product(records)
    # Use sorted with lambda to get top N
    top_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    return top_products[:n]


def best_selling_month(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the month with the highest total revenue.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (month_YYYY-MM, total_revenue)
    """
    if not records:
        return ("", 0.0)
    
    monthly = monthly_sales(records)
    return max(monthly.items(), key=lambda x: x[1])


def worst_selling_month(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the month with the lowest total revenue.
    
    Uses functional programming with min and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (month_YYYY-MM, total_revenue)
    """
    if not records:
        return ("", 0.0)
    
    monthly = monthly_sales(records)
    return min(monthly.items(), key=lambda x: x[1])


def top_region_by_revenue(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the region with the highest total revenue.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (region_name, total_revenue)
    """
    if not records:
        return ("", 0.0)
    
    region_sales = sales_by_region(records)
    return max(region_sales.items(), key=lambda x: x[1])


def top_region_by_units(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the region with the highest total units sold.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (region_name, total_units_sold)
    """
    if not records:
        return ("", 0.0)
    
    region_units = defaultdict(float)
    for record in records:
        region_units[record.region] += record.units_sold
    
    return max(region_units.items(), key=lambda x: x[1])


def average_revenue_per_region(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate average revenue per region.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping region names to average revenue
    """
    region_records = defaultdict(list)
    for record in records:
        region_records[record.region].append(record.total_revenue)
    
    return {
        region: sum(revenues) / len(revenues)
        for region, revenues in region_records.items()
    }


def revenue_concentration_top_10_percent(records: List[SalesRecord]) -> float:
    """
    Calculate what percentage of total revenue comes from top 10% of products.
    
    Uses functional programming with sorted and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Percentage (0-100) of revenue from top 10% of products
    """
    if not records:
        return 0.0
    
    product_revenue = sales_by_product(records)
    total_rev = total_revenue(records)
    
    if total_rev == 0:
        return 0.0
    
    # Sort products by revenue descending
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate how many products represent top 10%
    top_10_percent_count = max(1, len(sorted_products) // 10)
    
    # Sum revenue from top 10% products
    top_10_percent_revenue = sum(
        revenue for _, revenue in sorted_products[:top_10_percent_count]
    )
    
    return (top_10_percent_revenue / total_rev) * 100


def peak_sales_period(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the year with the highest total revenue.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (year_YYYY, total_revenue)
    """
    if not records:
        return ("", 0.0)
    
    yearly = yearly_sales(records)
    return max(yearly.items(), key=lambda x: x[1])


def average_units_per_region(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate average units sold per region.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping region names to average units sold
    """
    region_records = defaultdict(list)
    for record in records:
        region_records[record.region].append(record.units_sold)
    
    return {
        region: sum(units) / len(units)
        for region, units in region_records.items()
    }


def units_sold_by_product(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total units sold grouped by product.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping product names to total units sold
    """
    product_units = defaultdict(float)
    for record in records:
        product_units[record.product] += record.units_sold
    return dict(product_units)


def top_product_by_units(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the product with the highest units sold.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (product_name, units_sold)
    """
    if not records:
        return ("", 0.0)
    
    product_units = units_sold_by_product(records)
    top_product = max(product_units.items(), key=lambda x: x[1])
    return top_product


def most_expensive_product(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the product with the highest unit price.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (product_name, unit_price)
    """
    if not records:
        return ("", 0.0)
    
    # Get product with max unit price
    max_price_record = max(records, key=lambda r: r.unit_price)
    return (max_price_record.product, max_price_record.unit_price)


def least_expensive_product(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the product with the lowest unit price.
    
    Uses functional programming with min and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (product_name, unit_price)
    """
    if not records:
        return ("", 0.0)
    
    # Get product with min unit price
    min_price_record = min(records, key=lambda r: r.unit_price)
    return (min_price_record.product, min_price_record.unit_price)


def yearly_sales(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total revenue grouped by year.
    
    Extracts year from date string and groups sales by year.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping year (YYYY) to total revenue
    """
    def extract_year(record: SalesRecord) -> str:
        """Extract YYYY from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 1:
            return date_parts[0]
        return record.date[:4] if len(record.date) >= 4 else "Unknown"
    
    yearly_revenue = defaultdict(float)
    for record in records:
        year = extract_year(record)
        yearly_revenue[year] += record.total_revenue
    
    return dict(yearly_revenue)


def average_units_per_transaction(records: List[SalesRecord]) -> float:
    """
    Calculate average units sold per transaction.
    
    Uses functional programming with reduce and len.
    
    Args:
        records: List of sales records
        
    Returns:
        Average units per transaction
    """
    if not records:
        return 0.0
    return total_units_sold(records) / len(records)


def monthly_units_sold(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total units sold grouped by month (YYYY-MM format).
    
    Extracts month from date string and groups units by month.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping month (YYYY-MM) to total units sold
    """
    def extract_month(record: SalesRecord) -> str:
        """Extract YYYY-MM from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 2:
            return f"{date_parts[0]}-{date_parts[1]}"
        return record.date[:7] if len(record.date) >= 7 else "Unknown"
    
    monthly_units = defaultdict(float)
    for record in records:
        month = extract_month(record)
        monthly_units[month] += record.units_sold
    
    return dict(monthly_units)


def yearly_units_sold(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total units sold grouped by year.
    
    Extracts year from date string and groups units by year.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping year (YYYY) to total units sold
    """
    def extract_year(record: SalesRecord) -> str:
        """Extract YYYY from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 1:
            return date_parts[0]
        return record.date[:4] if len(record.date) >= 4 else "Unknown"
    
    yearly_units = defaultdict(float)
    for record in records:
        year = extract_year(record)
        yearly_units[year] += record.units_sold
    
    return dict(yearly_units)


def units_sold_by_region(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate total units sold grouped by region.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping region names to total units sold
    """
    region_units = defaultdict(float)
    for record in records:
        region_units[record.region] += record.units_sold
    return dict(region_units)


def best_selling_month_by_units(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the month with the highest total units sold.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (month_YYYY-MM, total_units_sold)
    """
    if not records:
        return ("", 0.0)
    
    monthly = monthly_units_sold(records)
    return max(monthly.items(), key=lambda x: x[1])


def worst_selling_month_by_units(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the month with the lowest total units sold.
    
    Uses functional programming with min and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (month_YYYY-MM, total_units_sold)
    """
    if not records:
        return ("", 0.0)
    
    monthly = monthly_units_sold(records)
    return min(monthly.items(), key=lambda x: x[1])


def peak_sales_period_by_units(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the year with the highest total units sold.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (year_YYYY, total_units_sold)
    """
    if not records:
        return ("", 0.0)
    
    yearly = yearly_units_sold(records)
    return max(yearly.items(), key=lambda x: x[1])


def units_concentration_top_10_percent(records: List[SalesRecord]) -> float:
    """
    Calculate what percentage of total units sold comes from top 10% of products.
    
    Uses functional programming with sorted and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Percentage (0-100) of units from top 10% of products
    """
    if not records:
        return 0.0
    
    product_units = units_sold_by_product(records)
    total_units = total_units_sold(records)
    
    if total_units == 0:
        return 0.0
    
    # Sort products by units descending
    sorted_products = sorted(product_units.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate how many products represent top 10%
    top_10_percent_count = max(1, len(sorted_products) // 10)
    
    # Sum units from top 10% products
    top_10_percent_units = sum(
        units for _, units in sorted_products[:top_10_percent_count]
    )
    
    return (top_10_percent_units / total_units) * 100


def top_n_products_by_units(records: List[SalesRecord], n: int = 5) -> List[Tuple[str, float]]:
    """
    Find top N products by units sold.
    
    Uses functional programming with sorted and lambda.
    
    Args:
        records: List of sales records
        n: Number of top products to return
        
    Returns:
        List of tuples (product_name, units_sold) sorted by units descending
    """
    product_units = units_sold_by_product(records)
    top_products = sorted(product_units.items(), key=lambda x: x[1], reverse=True)
    return top_products[:n]


def top_product_by_year(records: List[SalesRecord]) -> Dict[str, Tuple[str, float]]:
    """
    Find the top-selling product (by units sold) for each year.
    
    Groups sales by year and product, then finds the product with
    the highest units sold for each year.
    
    Uses functional programming with defaultdict and max.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping year (YYYY) to tuple of (product_name, units_sold)
    """
    if not records:
        return {}
    
    # Extract year from date (assumes YYYY-MM-DD format)
    def extract_year(record: SalesRecord) -> str:
        """Extract YYYY from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 1:
            return date_parts[0]
        return record.date[:4] if len(record.date) >= 4 else "Unknown"
    
    # Group units sold by year and product
    year_product_units = defaultdict(lambda: defaultdict(float))
    for record in records:
        year = extract_year(record)
        year_product_units[year][record.product] += record.units_sold
    
    # Find top product for each year using max with lambda
    result = {}
    for year, product_units in year_product_units.items():
        top_product = max(product_units.items(), key=lambda x: x[1])
        result[year] = (top_product[0], top_product[1])
    
    return result


def top_n_products_by_year(records: List[SalesRecord], n: int = 5) -> Dict[str, List[Tuple[str, float]]]:
    """
    Find the top N products (by units sold) for each year.
    
    Groups sales by year and product, then finds the top N products
    with the highest units sold for each year.
    
    Uses functional programming with defaultdict, sorted, and lambda.
    
    Args:
        records: List of sales records
        n: Number of top products to return per year
        
    Returns:
        Dictionary mapping year (YYYY) to list of tuples (product_name, units_sold)
    """
    if not records:
        return {}
    
    # Extract year from date (assumes YYYY-MM-DD format)
    def extract_year(record: SalesRecord) -> str:
        """Extract YYYY from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 1:
            return date_parts[0]
        return record.date[:4] if len(record.date) >= 4 else "Unknown"
    
    # Group units sold by year and product
    year_product_units = defaultdict(lambda: defaultdict(float))
    for record in records:
        year = extract_year(record)
        year_product_units[year][record.product] += record.units_sold
    
    # Find top N products for each year using sorted with lambda
    result = {}
    for year, product_units in year_product_units.items():
        top_products = sorted(product_units.items(), key=lambda x: x[1], reverse=True)[:n]
        result[year] = top_products
    
    return result


def bottom_n_products_by_units(records: List[SalesRecord], n: int = 5) -> List[Tuple[str, float]]:
    """
    Find bottom N products by units sold.
    
    Uses functional programming with sorted and lambda.
    
    Args:
        records: List of sales records
        n: Number of bottom products to return
        
    Returns:
        List of tuples (product_name, units_sold) sorted by units ascending
    """
    product_units = units_sold_by_product(records)
    bottom_products = sorted(product_units.items(), key=lambda x: x[1])
    return bottom_products[:n]


def year_over_year_growth(records: List[SalesRecord]) -> Dict[str, float]:
    """
    Calculate year-over-year growth percentage for total units sold.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping year to growth percentage (previous year as base)
    """
    yearly = yearly_units_sold(records)
    if len(yearly) < 2:
        return {}
    
    sorted_years = sorted(yearly.keys())
    growth = {}
    
    for i in range(1, len(sorted_years)):
        current_year = sorted_years[i]
        previous_year = sorted_years[i-1]
        current_units = yearly[current_year]
        previous_units = yearly[previous_year]
        
        if previous_units > 0:
            growth_pct = ((current_units - previous_units) / previous_units) * 100
            growth[current_year] = growth_pct
        else:
            growth[current_year] = 0.0 if current_units == 0 else 100.0
    
    return growth


def total_transactions_count(records: List[SalesRecord]) -> int:
    """
    Count the total number of sales transactions/records.
    
    Args:
        records: List of sales records
        
    Returns:
        Total number of transactions
    """
    return len(records)


def average_units_per_product(records: List[SalesRecord]) -> float:
    """
    Calculate average units sold per product.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Average units sold per product
    """
    if not records:
        return 0.0
    
    product_units = units_sold_by_product(records)
    if not product_units:
        return 0.0
    
    total_units = sum(product_units.values())
    num_products = len(product_units)
    
    return total_units / num_products if num_products > 0 else 0.0


def products_in_all_years(records: List[SalesRecord]) -> List[str]:
    """
    Find products that have sales in all available years.
    
    Uses functional programming with set operations.
    
    Args:
        records: List of sales records
        
    Returns:
        List of product names that appear in all years
    """
    if not records:
        return []
    
    def extract_year(record: SalesRecord) -> str:
        """Extract YYYY from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 1:
            return date_parts[0]
        return record.date[:4] if len(record.date) >= 4 else "Unknown"
    
    # Get all years
    all_years = {extract_year(r) for r in records}
    
    # Get products per year
    products_by_year = defaultdict(set)
    for record in records:
        year = extract_year(record)
        products_by_year[year].add(record.product)
    
    # Find products that appear in all years
    if not products_by_year:
        return []
    
    common_products = set.intersection(*products_by_year.values())
    return sorted(list(common_products))


def top_growth_year(records: List[SalesRecord]) -> Tuple[str, float]:
    """
    Find the year with the highest year-over-year growth.
    
    Uses functional programming with max and lambda.
    
    Args:
        records: List of sales records
        
    Returns:
        Tuple of (year, growth_percentage)
    """
    growth = year_over_year_growth(records)
    if not growth:
        return ("", 0.0)
    
    return max(growth.items(), key=lambda x: x[1])


def products_by_year_count(records: List[SalesRecord]) -> Dict[str, int]:
    """
    Count how many products were sold in each year.
    
    Uses functional programming patterns.
    
    Args:
        records: List of sales records
        
    Returns:
        Dictionary mapping year to number of unique products
    """
    def extract_year(record: SalesRecord) -> str:
        """Extract YYYY from date string."""
        date_parts = record.date.split('-')
        if len(date_parts) >= 1:
            return date_parts[0]
        return record.date[:4] if len(record.date) >= 4 else "Unknown"
    
    products_by_year = defaultdict(set)
    for record in records:
        year = extract_year(record)
        products_by_year[year].add(record.product)
    
    return {year: len(products) for year, products in products_by_year.items()}

