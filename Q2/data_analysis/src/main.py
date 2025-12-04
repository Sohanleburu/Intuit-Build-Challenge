"""
Main Program
Orchestrates loading sales data and running all analyses.
"""

import sys
from pathlib import Path

from reader import load_sales_data
from analysis import (
    total_units_sold,
    units_sold_by_product,
    units_sold_by_region,
    top_product_by_units,
    monthly_units_sold,
    yearly_units_sold,
    unique_products_count,
    unique_regions_count,
    top_n_products_by_units,
    best_selling_month_by_units,
    worst_selling_month_by_units,
    units_concentration_top_10_percent,
    peak_sales_period_by_units,
    top_product_by_year,
    top_n_products_by_year,
    year_over_year_growth,
    total_transactions_count,
    average_units_per_product,
    products_in_all_years,
    top_growth_year,
    products_by_year_count
)


def print_analysis_results(records: list) -> None:
    """
    Run all analysis functions and print results to console.
    
    Args:
        records: List of sales records to analyze
    """
    print("=" * 70)
    print("SALES DATA ANALYSIS RESULTS")
    print("=" * 70)
    print()
    
    # Total Units Sold
    print("1. TOTAL UNITS SOLD")
    print("-" * 70)
    units = total_units_sold(records)
    print(f"   Total Units Sold: {units:,.0f}")
    print()
    
    # Units Sold by Product
    print("2. UNITS SOLD BY PRODUCT")
    print("-" * 70)
    units_by_product = units_sold_by_product(records)
    for product, units in sorted(units_by_product.items(), key=lambda x: x[1], reverse=True):
        print(f"   {product}: {units:,.0f} units")
    print()
    
    # Units Sold by Region
    print("3. UNITS SOLD BY REGION")
    print("-" * 70)
    units_by_region = units_sold_by_region(records)
    for region, units in sorted(units_by_region.items(), key=lambda x: x[1], reverse=True):
        print(f"   {region}: {units:,.0f} units")
    print()
    
    # Top Product by Units
    print("4. TOP PRODUCT BY UNITS SOLD")
    print("-" * 70)
    top_units_product, top_units = top_product_by_units(records)
    print(f"   Product: {top_units_product}")
    print(f"   Units Sold: {top_units:,.0f}")
    print()
    
    # Monthly Units Sold
    print("5. MONTHLY UNITS SOLD")
    print("-" * 70)
    monthly = monthly_units_sold(records)
    for month, units in sorted(monthly.items()):
        print(f"   {month}: {units:,.0f} units")
    print()
    
    # Yearly Units Sold
    print("6. YEARLY UNITS SOLD")
    print("-" * 70)
    yearly = yearly_units_sold(records)
    for year, units in sorted(yearly.items()):
        print(f"   {year}: {units:,.0f} units")
    print()
    
    # Total Car Models
    print("7. TOTAL CAR MODELS")
    print("-" * 70)
    total_models = unique_products_count(records)
    print(f"   Total Car Models: {total_models}")
    print()
    
    # Top 5 Products by Units (Total)
    print("8. TOP 5 PRODUCTS BY UNITS SOLD (TOTAL)")
    print("-" * 70)
    top_5 = top_n_products_by_units(records, 5)
    for i, (product, units) in enumerate(top_5, 1):
        print(f"   {i}. {product}: {units:,.0f} units")
    print()
    
    # Top 5 Products by Year
    print("9. TOP 5 PRODUCTS BY UNITS SOLD (BY YEAR)")
    print("-" * 70)
    top_5_by_year = top_n_products_by_year(records, 5)
    for year in sorted(top_5_by_year.keys()):
        print(f"   {year}:")
        for i, (product, units) in enumerate(top_5_by_year[year], 1):
            print(f"      {i}. {product}: {units:,.0f} units")
    print()
    
    # Best/Worst Selling Months
    print("10. BEST AND WORST SELLING MONTHS")
    print("-" * 70)
    best_month, best_month_units = best_selling_month_by_units(records)
    worst_month, worst_month_units = worst_selling_month_by_units(records)
    print(f"   Best Month: {best_month} ({best_month_units:,.0f} units)")
    print(f"   Worst Month: {worst_month} ({worst_month_units:,.0f} units)")
    print()
    
    # Units Concentration
    print("11. UNITS CONCENTRATION")
    print("-" * 70)
    concentration = units_concentration_top_10_percent(records)
    print(f"   Top 10% of Products Account for: {concentration:.2f}% of Total Units Sold")
    print()
    
    # Peak Sales Period
    print("12. PEAK SALES PERIOD")
    print("-" * 70)
    peak_year, peak_year_units = peak_sales_period_by_units(records)
    print(f"   Peak Year: {peak_year} ({peak_year_units:,.0f} units)")
    print()
    
    # Top Product by Year
    print("13. TOP-SELLING PRODUCT BY YEAR")
    print("-" * 70)
    top_by_year = top_product_by_year(records)
    for year in sorted(top_by_year.keys()):
        product, units = top_by_year[year]
        print(f"   {year}: {product} ({units:,.0f} units)")
    print()
    
    # Year-over-Year Growth
    print("14. YEAR-OVER-YEAR GROWTH")
    print("-" * 70)
    growth = year_over_year_growth(records)
    for year in sorted(growth.keys()):
        growth_pct = growth[year]
        print(f"   {year}: {growth_pct:+.2f}%")
    print()
    
    # Top Growth Year
    print("15. TOP GROWTH YEAR")
    print("-" * 70)
    top_growth_yr, top_growth_pct = top_growth_year(records)
    if top_growth_yr:
        print(f"   Year: {top_growth_yr}")
        print(f"   Growth: {top_growth_pct:+.2f}%")
    print()
    
    # Additional Statistics
    print("16. ADDITIONAL STATISTICS")
    print("-" * 70)
    total_trans = total_transactions_count(records)
    avg_units_per_prod = average_units_per_product(records)
    print(f"   Total Transactions: {total_trans:,}")
    print(f"   Average Units per Product: {avg_units_per_prod:,.2f}")
    print()
    
    # Products in All Years
    print("17. PRODUCTS SOLD IN ALL YEARS")
    print("-" * 70)
    products_all_years = products_in_all_years(records)
    if products_all_years:
        for product in products_all_years:
            print(f"   {product}")
    else:
        print("   No products sold in all years")
    print()
    
    # Products Count by Year
    print("18. NUMBER OF PRODUCTS BY YEAR")
    print("-" * 70)
    products_count = products_by_year_count(records)
    for year in sorted(products_count.keys()):
        count = products_count[year]
        print(f"   {year}: {count} products")
    print()
    
    print("=" * 70)


def main() -> None:
    """
    Main entry point for the sales data analysis application.
    """
    # Default CSV path - try sales.csv first, then any CSV in data folder
    data_dir = Path(__file__).parent.parent / "data"
    default_csv = data_dir / "sales.csv"
    
    # If sales.csv doesn't exist, look for any CSV file in data folder
    if not default_csv.exists():
        csv_files = list(data_dir.glob("*.csv"))
        if csv_files:
            default_csv = csv_files[0]  # Use first CSV found
    
    # Allow CSV path to be passed as command-line argument
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = str(default_csv)
    
    try:
        # Load sales data
        print(f"Loading sales data from: {csv_path}")
        records = load_sales_data(csv_path)
        print(f"Successfully loaded {len(records)} sales records")
        print()
        
        if not records:
            print("Warning: No valid records found in CSV file.")
            return
        
        # Run all analyses and print results
        print_analysis_results(records)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure the CSV file exists at the specified path.")
        print("Expected location: data/sales.csv")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

