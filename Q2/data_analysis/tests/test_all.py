"""
Unit Tests for Sales Data Analysis Application
Comprehensive tests for all modules: analysis, reader, and models.
"""

import sys
import unittest
import tempfile
import os
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from models import SalesRecord
from analysis import (
    total_revenue,
    total_units_sold,
    sales_by_product,
    sales_by_region,
    average_price_by_product,
    top_selling_product,
    monthly_sales,
    average_revenue_per_transaction,
    unique_products_count,
    unique_regions_count,
    top_n_products,
    units_sold_by_product,
    top_product_by_units,
    most_expensive_product,
    least_expensive_product,
    yearly_sales,
    average_units_per_transaction,
    best_selling_month,
    worst_selling_month,
    top_region_by_revenue,
    top_region_by_units,
    average_revenue_per_region,
    revenue_concentration_top_10_percent,
    peak_sales_period,
    average_units_per_region,
    monthly_units_sold,
    yearly_units_sold,
    units_sold_by_region,
    best_selling_month_by_units,
    worst_selling_month_by_units,
    peak_sales_period_by_units,
    units_concentration_top_10_percent,
    top_n_products_by_units,
    top_product_by_year,
    top_n_products_by_year,
    year_over_year_growth,
    total_transactions_count,
    average_units_per_product,
    products_in_all_years,
    top_growth_year,
    products_by_year_count
)
from reader import (
    find_column_mapping,
    validate_minimum_columns,
    parse_float,
    normalize_date,
    parse_row,
    load_sales_data,
    parse_month_column,
    is_pivot_table_format,
    load_pivot_table_data
)
from main import print_analysis_results


class TestAnalysisFunctions(unittest.TestCase):
    """Test cases for all analysis functions."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_records = [
            SalesRecord(
                date="2024-01-15",
                product="Widget A",
                region="North",
                units_sold=10.0,
                unit_price=5.0,
                total_revenue=50.0
            ),
            SalesRecord(
                date="2024-01-20",
                product="Widget B",
                region="South",
                units_sold=5.0,
                unit_price=10.0,
                total_revenue=50.0
            ),
            SalesRecord(
                date="2024-02-10",
                product="Widget A",
                region="North",
                units_sold=8.0,
                unit_price=5.0,
                total_revenue=40.0
            ),
            SalesRecord(
                date="2024-02-15",
                product="Widget B",
                region="East",
                units_sold=12.0,
                unit_price=10.0,
                total_revenue=120.0
            ),
        ]
    
    def test_total_revenue(self):
        """Test total revenue calculation."""
        result = total_revenue(self.sample_records)
        expected = 50.0 + 50.0 + 40.0 + 120.0
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_total_revenue_empty_list(self):
        """Test total revenue with empty list."""
        result = total_revenue([])
        self.assertEqual(result, 0.0)
    
    def test_total_units_sold(self):
        """Test total units sold calculation."""
        result = total_units_sold(self.sample_records)
        expected = 10.0 + 5.0 + 8.0 + 12.0
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_total_units_sold_empty_list(self):
        """Test total units sold with empty list."""
        result = total_units_sold([])
        self.assertEqual(result, 0.0)
    
    def test_sales_by_product(self):
        """Test sales grouped by product."""
        result = sales_by_product(self.sample_records)
        
        self.assertIn("Widget A", result)
        self.assertIn("Widget B", result)
        self.assertAlmostEqual(result["Widget A"], 90.0, places=2)
        self.assertAlmostEqual(result["Widget B"], 170.0, places=2)
    
    def test_sales_by_product_empty_list(self):
        """Test sales by product with empty list."""
        result = sales_by_product([])
        self.assertEqual(result, {})
    
    def test_sales_by_region(self):
        """Test sales grouped by region."""
        result = sales_by_region(self.sample_records)
        
        self.assertIn("North", result)
        self.assertIn("South", result)
        self.assertIn("East", result)
        self.assertAlmostEqual(result["North"], 90.0, places=2)
        self.assertAlmostEqual(result["South"], 50.0, places=2)
        self.assertAlmostEqual(result["East"], 120.0, places=2)
    
    def test_sales_by_region_empty_list(self):
        """Test sales by region with empty list."""
        result = sales_by_region([])
        self.assertEqual(result, {})
    
    def test_average_price_by_product(self):
        """Test average price by product."""
        result = average_price_by_product(self.sample_records)
        
        self.assertIn("Widget A", result)
        self.assertIn("Widget B", result)
        self.assertAlmostEqual(result["Widget A"], 5.0, places=2)
        self.assertAlmostEqual(result["Widget B"], 10.0, places=2)
    
    def test_average_price_by_product_empty_list(self):
        """Test average price by product with empty list."""
        result = average_price_by_product([])
        self.assertEqual(result, {})
    
    def test_top_selling_product(self):
        """Test finding top selling product."""
        product, revenue = top_selling_product(self.sample_records)
        
        self.assertEqual(product, "Widget B")
        self.assertAlmostEqual(revenue, 170.0, places=2)
    
    def test_top_selling_product_empty_list(self):
        """Test top selling product with empty list."""
        product, revenue = top_selling_product([])
        self.assertEqual(product, "")
        self.assertEqual(revenue, 0.0)
    
    def test_monthly_sales(self):
        """Test monthly sales grouping."""
        result = monthly_sales(self.sample_records)
        
        self.assertIn("2024-01", result)
        self.assertIn("2024-02", result)
        self.assertAlmostEqual(result["2024-01"], 100.0, places=2)
        self.assertAlmostEqual(result["2024-02"], 160.0, places=2)
    
    def test_monthly_sales_empty_list(self):
        """Test monthly sales with empty list."""
        result = monthly_sales([])
        self.assertEqual(result, {})
    
    def test_monthly_sales_date_format(self):
        """Test monthly sales with different date formats."""
        records = [
            SalesRecord(
                date="2024-03-05",
                product="Test",
                region="North",
                units_sold=1.0,
                unit_price=1.0,
                total_revenue=1.0
            )
        ]
        result = monthly_sales(records)
        self.assertIn("2024-03", result)
    
    def test_average_revenue_per_transaction(self):
        """Test average revenue per transaction calculation."""
        result = average_revenue_per_transaction(self.sample_records)
        expected = (50.0 + 50.0 + 40.0 + 120.0) / 4
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_average_revenue_per_transaction_empty(self):
        """Test average revenue per transaction with empty list."""
        result = average_revenue_per_transaction([])
        self.assertEqual(result, 0.0)
    
    def test_unique_products_count(self):
        """Test counting unique products."""
        result = unique_products_count(self.sample_records)
        self.assertEqual(result, 2)  # Widget A and Widget B
    
    def test_unique_products_count_empty(self):
        """Test unique products count with empty list."""
        result = unique_products_count([])
        self.assertEqual(result, 0)
    
    def test_unique_regions_count(self):
        """Test counting unique regions."""
        result = unique_regions_count(self.sample_records)
        self.assertEqual(result, 3)  # North, South, East
    
    def test_unique_regions_count_empty(self):
        """Test unique regions count with empty list."""
        result = unique_regions_count([])
        self.assertEqual(result, 0)
    
    def test_top_n_products(self):
        """Test finding top N products."""
        result = top_n_products(self.sample_records, 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "Widget B")  # Highest revenue
        self.assertEqual(result[1][0], "Widget A")
    
    def test_top_n_products_more_than_available(self):
        """Test top N products when N exceeds available products."""
        result = top_n_products(self.sample_records, 10)
        self.assertEqual(len(result), 2)  # Only 2 products available
    
    def test_units_sold_by_product(self):
        """Test units sold grouped by product."""
        result = units_sold_by_product(self.sample_records)
        self.assertIn("Widget A", result)
        self.assertIn("Widget B", result)
        self.assertAlmostEqual(result["Widget A"], 18.0, places=2)
        self.assertAlmostEqual(result["Widget B"], 17.0, places=2)
    
    def test_units_sold_by_product_empty(self):
        """Test units sold by product with empty list."""
        result = units_sold_by_product([])
        self.assertEqual(result, {})
    
    def test_top_product_by_units(self):
        """Test finding top product by units sold."""
        product, units = top_product_by_units(self.sample_records)
        self.assertEqual(product, "Widget A")
        self.assertAlmostEqual(units, 18.0, places=2)
    
    def test_top_product_by_units_empty(self):
        """Test top product by units with empty list."""
        product, units = top_product_by_units([])
        self.assertEqual(product, "")
        self.assertEqual(units, 0.0)
    
    def test_most_expensive_product(self):
        """Test finding most expensive product."""
        product, price = most_expensive_product(self.sample_records)
        self.assertEqual(product, "Widget B")
        self.assertEqual(price, 10.0)
    
    def test_most_expensive_product_empty(self):
        """Test most expensive product with empty list."""
        product, price = most_expensive_product([])
        self.assertEqual(product, "")
        self.assertEqual(price, 0.0)
    
    def test_least_expensive_product(self):
        """Test finding least expensive product."""
        product, price = least_expensive_product(self.sample_records)
        self.assertEqual(product, "Widget A")
        self.assertEqual(price, 5.0)
    
    def test_least_expensive_product_empty(self):
        """Test least expensive product with empty list."""
        product, price = least_expensive_product([])
        self.assertEqual(product, "")
        self.assertEqual(price, 0.0)
    
    def test_yearly_sales(self):
        """Test yearly sales grouping."""
        result = yearly_sales(self.sample_records)
        self.assertIn("2024", result)
        self.assertAlmostEqual(result["2024"], 260.0, places=2)
    
    def test_yearly_sales_empty(self):
        """Test yearly sales with empty list."""
        result = yearly_sales([])
        self.assertEqual(result, {})
    
    def test_average_units_per_transaction(self):
        """Test average units per transaction calculation."""
        result = average_units_per_transaction(self.sample_records)
        expected = (10.0 + 5.0 + 8.0 + 12.0) / 4
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_average_units_per_transaction_empty(self):
        """Test average units per transaction with empty list."""
        result = average_units_per_transaction([])
        self.assertEqual(result, 0.0)
    
    def test_best_selling_month(self):
        """Test finding best selling month."""
        month, revenue = best_selling_month(self.sample_records)
        self.assertEqual(month, "2024-02")
        self.assertAlmostEqual(revenue, 160.0, places=2)
    
    def test_best_selling_month_empty(self):
        """Test best selling month with empty list."""
        month, revenue = best_selling_month([])
        self.assertEqual(month, "")
        self.assertEqual(revenue, 0.0)
    
    def test_worst_selling_month(self):
        """Test finding worst selling month."""
        month, revenue = worst_selling_month(self.sample_records)
        self.assertEqual(month, "2024-01")
        self.assertAlmostEqual(revenue, 100.0, places=2)
    
    def test_worst_selling_month_empty(self):
        """Test worst selling month with empty list."""
        month, revenue = worst_selling_month([])
        self.assertEqual(month, "")
        self.assertEqual(revenue, 0.0)
    
    def test_top_region_by_revenue(self):
        """Test finding top region by revenue."""
        region, revenue = top_region_by_revenue(self.sample_records)
        self.assertEqual(region, "East")
        self.assertAlmostEqual(revenue, 120.0, places=2)
    
    def test_top_region_by_revenue_empty(self):
        """Test top region by revenue with empty list."""
        region, revenue = top_region_by_revenue([])
        self.assertEqual(region, "")
        self.assertEqual(revenue, 0.0)
    
    def test_top_region_by_units(self):
        """Test finding top region by units sold."""
        region, units = top_region_by_units(self.sample_records)
        self.assertEqual(region, "North")  # North: 10 + 8 = 18 units
        self.assertAlmostEqual(units, 18.0, places=2)
    
    def test_top_region_by_units_empty(self):
        """Test top region by units with empty list."""
        region, units = top_region_by_units([])
        self.assertEqual(region, "")
        self.assertEqual(units, 0.0)
    
    def test_average_revenue_per_region(self):
        """Test calculating average revenue per region."""
        result = average_revenue_per_region(self.sample_records)
        self.assertIn("North", result)
        self.assertIn("South", result)
        self.assertIn("East", result)
        # North: (50.0 + 40.0) / 2 = 45.0
        self.assertAlmostEqual(result["North"], 45.0, places=2)
        # South: 50.0 / 1 = 50.0
        self.assertAlmostEqual(result["South"], 50.0, places=2)
        # East: 120.0 / 1 = 120.0
        self.assertAlmostEqual(result["East"], 120.0, places=2)
    
    def test_average_revenue_per_region_empty(self):
        """Test average revenue per region with empty list."""
        result = average_revenue_per_region([])
        self.assertEqual(result, {})
    
    def test_revenue_concentration_top_10_percent(self):
        """Test revenue concentration calculation."""
        # With 2 products, top 10% = 1 product (Widget B with 170.0 revenue)
        # Total revenue = 260.0
        # Concentration = 170.0 / 260.0 * 100 = 65.38%
        result = revenue_concentration_top_10_percent(self.sample_records)
        self.assertGreater(result, 0.0)
        self.assertLessEqual(result, 100.0)
    
    def test_revenue_concentration_top_10_percent_empty(self):
        """Test revenue concentration with empty list."""
        result = revenue_concentration_top_10_percent([])
        self.assertEqual(result, 0.0)
    
    def test_peak_sales_period(self):
        """Test finding peak sales period (year)."""
        year, revenue = peak_sales_period(self.sample_records)
        self.assertEqual(year, "2024")
        self.assertAlmostEqual(revenue, 260.0, places=2)
    
    def test_peak_sales_period_empty(self):
        """Test peak sales period with empty list."""
        year, revenue = peak_sales_period([])
        self.assertEqual(year, "")
        self.assertEqual(revenue, 0.0)
    
    def test_average_units_per_region(self):
        """Test calculating average units per region."""
        result = average_units_per_region(self.sample_records)
        self.assertIn("North", result)
        self.assertIn("South", result)
        self.assertIn("East", result)
        # North: (10.0 + 8.0) / 2 = 9.0
        self.assertAlmostEqual(result["North"], 9.0, places=2)
        # South: 5.0 / 1 = 5.0
        self.assertAlmostEqual(result["South"], 5.0, places=2)
        # East: 12.0 / 1 = 12.0
        self.assertAlmostEqual(result["East"], 12.0, places=2)
    
    def test_average_units_per_region_empty(self):
        """Test average units per region with empty list."""
        result = average_units_per_region([])
        self.assertEqual(result, {})
    
    def test_monthly_units_sold(self):
        """Test monthly units sold calculation."""
        result = monthly_units_sold(self.sample_records)
        self.assertIn("2024-01", result)
        self.assertIn("2024-02", result)
        self.assertAlmostEqual(result["2024-01"], 15.0, places=2)
        self.assertAlmostEqual(result["2024-02"], 20.0, places=2)
    
    def test_monthly_units_sold_empty(self):
        """Test monthly units sold with empty list."""
        result = monthly_units_sold([])
        self.assertEqual(result, {})
    
    def test_yearly_units_sold(self):
        """Test yearly units sold calculation."""
        result = yearly_units_sold(self.sample_records)
        self.assertIn("2024", result)
        self.assertAlmostEqual(result["2024"], 35.0, places=2)
    
    def test_yearly_units_sold_empty(self):
        """Test yearly units sold with empty list."""
        result = yearly_units_sold([])
        self.assertEqual(result, {})
    
    def test_units_sold_by_region(self):
        """Test units sold by region."""
        result = units_sold_by_region(self.sample_records)
        self.assertIn("North", result)
        self.assertIn("South", result)
        self.assertIn("East", result)
        self.assertAlmostEqual(result["North"], 18.0, places=2)
        self.assertAlmostEqual(result["South"], 5.0, places=2)
        self.assertAlmostEqual(result["East"], 12.0, places=2)
    
    def test_units_sold_by_region_empty(self):
        """Test units sold by region with empty list."""
        result = units_sold_by_region([])
        self.assertEqual(result, {})
    
    def test_best_selling_month_by_units(self):
        """Test finding best selling month by units."""
        month, units = best_selling_month_by_units(self.sample_records)
        self.assertEqual(month, "2024-02")
        self.assertAlmostEqual(units, 20.0, places=2)
    
    def test_best_selling_month_by_units_empty(self):
        """Test best selling month by units with empty list."""
        month, units = best_selling_month_by_units([])
        self.assertEqual(month, "")
        self.assertEqual(units, 0.0)
    
    def test_worst_selling_month_by_units(self):
        """Test finding worst selling month by units."""
        month, units = worst_selling_month_by_units(self.sample_records)
        self.assertEqual(month, "2024-01")
        self.assertAlmostEqual(units, 15.0, places=2)
    
    def test_worst_selling_month_by_units_empty(self):
        """Test worst selling month by units with empty list."""
        month, units = worst_selling_month_by_units([])
        self.assertEqual(month, "")
        self.assertEqual(units, 0.0)
    
    def test_peak_sales_period_by_units(self):
        """Test finding peak sales period by units."""
        year, units = peak_sales_period_by_units(self.sample_records)
        self.assertEqual(year, "2024")
        self.assertAlmostEqual(units, 35.0, places=2)
    
    def test_peak_sales_period_by_units_empty(self):
        """Test peak sales period by units with empty list."""
        year, units = peak_sales_period_by_units([])
        self.assertEqual(year, "")
        self.assertEqual(units, 0.0)
    
    def test_units_concentration_top_10_percent(self):
        """Test units concentration calculation."""
        result = units_concentration_top_10_percent(self.sample_records)
        self.assertGreater(result, 0.0)
        self.assertLessEqual(result, 100.0)
    
    def test_units_concentration_top_10_percent_empty(self):
        """Test units concentration with empty list."""
        result = units_concentration_top_10_percent([])
        self.assertEqual(result, 0.0)
    
    def test_top_n_products_by_units(self):
        """Test finding top N products by units."""
        result = top_n_products_by_units(self.sample_records, 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "Widget A")
        self.assertAlmostEqual(result[0][1], 18.0, places=2)
    
    def test_top_n_products_by_units_empty(self):
        """Test top N products by units with empty list."""
        result = top_n_products_by_units([], 5)
        self.assertEqual(result, [])
    
    def test_top_product_by_year(self):
        """Test finding top product by year."""
        result = top_product_by_year(self.sample_records)
        self.assertIn("2024", result)
        product, units = result["2024"]
        self.assertEqual(product, "Widget A")
        self.assertAlmostEqual(units, 18.0, places=2)
    
    def test_top_product_by_year_empty(self):
        """Test top product by year with empty list."""
        result = top_product_by_year([])
        self.assertEqual(result, {})
    
    def test_top_n_products_by_year(self):
        """Test finding top N products by year."""
        result = top_n_products_by_year(self.sample_records, 2)
        self.assertIn("2024", result)
        top_products = result["2024"]
        self.assertEqual(len(top_products), 2)
        self.assertEqual(top_products[0][0], "Widget A")
    
    def test_top_n_products_by_year_empty(self):
        """Test top N products by year with empty list."""
        result = top_n_products_by_year([], 5)
        self.assertEqual(result, {})
    
    def test_year_over_year_growth(self):
        """Test year-over-year growth calculation."""
        # Create records with multiple years
        multi_year_records = [
            SalesRecord(date="2023-01-15", product="A", region="North", units_sold=100.0, unit_price=5.0, total_revenue=500.0),
            SalesRecord(date="2024-01-15", product="A", region="North", units_sold=150.0, unit_price=5.0, total_revenue=750.0),
            SalesRecord(date="2025-01-15", product="A", region="North", units_sold=200.0, unit_price=5.0, total_revenue=1000.0),
        ]
        result = year_over_year_growth(multi_year_records)
        self.assertIn("2024", result)
        self.assertIn("2025", result)
        # 2024: (150-100)/100 * 100 = 50%
        self.assertAlmostEqual(result["2024"], 50.0, places=2)
        # 2025: (200-150)/150 * 100 = 33.33%
        self.assertAlmostEqual(result["2025"], 33.33, places=1)
    
    def test_year_over_year_growth_empty(self):
        """Test year-over-year growth with empty list."""
        result = year_over_year_growth([])
        self.assertEqual(result, {})
    
    def test_year_over_year_growth_single_year(self):
        """Test year-over-year growth with single year."""
        single_year = [
            SalesRecord(date="2024-01-15", product="A", region="North", units_sold=100.0, unit_price=5.0, total_revenue=500.0),
        ]
        result = year_over_year_growth(single_year)
        self.assertEqual(result, {})
    
    def test_total_transactions_count(self):
        """Test total transactions count."""
        result = total_transactions_count(self.sample_records)
        self.assertEqual(result, 4)
    
    def test_total_transactions_count_empty(self):
        """Test total transactions count with empty list."""
        result = total_transactions_count([])
        self.assertEqual(result, 0)
    
    def test_average_units_per_product(self):
        """Test average units per product."""
        result = average_units_per_product(self.sample_records)
        # Total units: 35, Products: 2, Average: 17.5
        self.assertAlmostEqual(result, 17.5, places=2)
    
    def test_average_units_per_product_empty(self):
        """Test average units per product with empty list."""
        result = average_units_per_product([])
        self.assertEqual(result, 0.0)
    
    def test_products_in_all_years(self):
        """Test finding products sold in all years."""
        multi_year_records = [
            SalesRecord(date="2023-01-15", product="A", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2023-02-15", product="B", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2024-01-15", product="A", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2024-02-15", product="B", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
        ]
        result = products_in_all_years(multi_year_records)
        self.assertIn("A", result)
        self.assertIn("B", result)
    
    def test_products_in_all_years_empty(self):
        """Test products in all years with empty list."""
        result = products_in_all_years([])
        self.assertEqual(result, [])
    
    def test_products_in_all_years_partial(self):
        """Test products in all years when some products missing in some years."""
        multi_year_records = [
            SalesRecord(date="2023-01-15", product="A", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2023-02-15", product="B", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2024-01-15", product="A", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            # B is missing in 2024
        ]
        result = products_in_all_years(multi_year_records)
        self.assertIn("A", result)
        self.assertNotIn("B", result)
    
    def test_top_growth_year(self):
        """Test finding top growth year."""
        multi_year_records = [
            SalesRecord(date="2023-01-15", product="A", region="North", units_sold=100.0, unit_price=5.0, total_revenue=500.0),
            SalesRecord(date="2024-01-15", product="A", region="North", units_sold=150.0, unit_price=5.0, total_revenue=750.0),
            SalesRecord(date="2025-01-15", product="A", region="North", units_sold=300.0, unit_price=5.0, total_revenue=1500.0),
        ]
        year, growth = top_growth_year(multi_year_records)
        self.assertEqual(year, "2025")
        # 2025: (300-150)/150 * 100 = 100%
        self.assertAlmostEqual(growth, 100.0, places=2)
    
    def test_top_growth_year_empty(self):
        """Test top growth year with empty list."""
        year, growth = top_growth_year([])
        self.assertEqual(year, "")
        self.assertEqual(growth, 0.0)
    
    def test_products_by_year_count(self):
        """Test counting products by year."""
        multi_year_records = [
            SalesRecord(date="2023-01-15", product="A", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2023-02-15", product="B", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2024-01-15", product="A", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
            SalesRecord(date="2024-02-15", product="C", region="North", units_sold=10.0, unit_price=5.0, total_revenue=50.0),
        ]
        result = products_by_year_count(multi_year_records)
        self.assertEqual(result["2023"], 2)
        self.assertEqual(result["2024"], 2)


class TestReaderFunctions(unittest.TestCase):
    """Test cases for reader functions."""
    
    def test_find_column_mapping_standard_columns(self):
        """Test column mapping with standard column names."""
        headers = ['date', 'product', 'region', 'units_sold', 'unit_price']
        mapping = find_column_mapping(headers)
        
        self.assertEqual(mapping['product'], 'product')
        self.assertEqual(mapping['unit_price'], 'unit_price')
        self.assertEqual(mapping['region'], 'region')
        self.assertEqual(mapping['units_sold'], 'units_sold')
        self.assertEqual(mapping['date'], 'date')
    
    def test_find_column_mapping_variations(self):
        """Test column mapping with various column name formats."""
        headers = ['Product Name', 'Sale Price', 'Brand', 'Quantity', 'Order Date']
        mapping = find_column_mapping(headers)
        
        self.assertEqual(mapping['product'], 'Product Name')
        self.assertEqual(mapping['unit_price'], 'Sale Price')
        self.assertEqual(mapping['region'], 'Brand')
        self.assertEqual(mapping['units_sold'], 'Quantity')
        self.assertEqual(mapping['date'], 'Order Date')
    
    def test_find_column_mapping_case_insensitive(self):
        """Test that column mapping is case-insensitive."""
        headers = ['PRODUCT', 'PRICE', 'REGION']
        mapping = find_column_mapping(headers)
        
        self.assertEqual(mapping['product'], 'PRODUCT')
        self.assertEqual(mapping['unit_price'], 'PRICE')
        self.assertEqual(mapping['region'], 'REGION')
    
    def test_find_column_mapping_missing_columns(self):
        """Test column mapping when some columns are missing."""
        headers = ['product', 'price']
        mapping = find_column_mapping(headers)
        
        self.assertIn('product', mapping)
        self.assertIn('unit_price', mapping)
        self.assertNotIn('region', mapping)
        self.assertNotIn('units_sold', mapping)
        self.assertNotIn('date', mapping)
    
    def test_validate_minimum_columns_valid(self):
        """Test validation with valid minimum columns."""
        mapping = {'product': 'product', 'unit_price': 'price'}
        self.assertTrue(validate_minimum_columns(mapping))
    
    def test_validate_minimum_columns_missing_product(self):
        """Test validation when product is missing."""
        mapping = {'unit_price': 'price'}
        self.assertFalse(validate_minimum_columns(mapping))
    
    def test_validate_minimum_columns_missing_price(self):
        """Test validation when unit_price is missing."""
        mapping = {'product': 'product'}
        self.assertFalse(validate_minimum_columns(mapping))
    
    def test_parse_float_valid(self):
        """Test parsing valid float values."""
        self.assertEqual(parse_float("10.5"), 10.5)
        self.assertEqual(parse_float("100"), 100.0)
        self.assertEqual(parse_float("0"), 0.0)
    
    def test_parse_float_with_commas(self):
        """Test parsing float values with commas."""
        self.assertEqual(parse_float("1,000.50"), 1000.5)
        self.assertEqual(parse_float("10,000"), 10000.0)
    
    def test_parse_float_invalid(self):
        """Test parsing invalid values returns default."""
        self.assertEqual(parse_float("invalid"), 0.0)
        self.assertEqual(parse_float(""), 0.0)
        self.assertEqual(parse_float(None), 0.0)
    
    def test_parse_float_custom_default(self):
        """Test parsing with custom default value."""
        self.assertEqual(parse_float("invalid", default=99.0), 99.0)
    
    def test_normalize_date_yyyy_mm_dd(self):
        """Test normalizing date already in YYYY-MM-DD format."""
        self.assertEqual(normalize_date("2024-01-15"), "2024-01-15")
        self.assertEqual(normalize_date("2022-12-31"), "2022-12-31")
    
    def test_normalize_date_dd_mm_yyyy(self):
        """Test normalizing date from DD-MM-YYYY format."""
        self.assertEqual(normalize_date("15-01-2024"), "2024-01-15")
        self.assertEqual(normalize_date("31-12-2022"), "2022-12-31")
    
    def test_normalize_date_with_slashes(self):
        """Test normalizing date with slashes."""
        self.assertEqual(normalize_date("15/01/2024"), "2024-01-15")
        self.assertEqual(normalize_date("31/12/2022"), "2022-12-31")
    
    def test_normalize_date_empty(self):
        """Test normalizing empty date."""
        self.assertEqual(normalize_date(""), "")
        self.assertEqual(normalize_date("   "), "")
    
    def test_parse_row_valid(self):
        """Test parsing a valid row."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'region': 'North',
            'units_sold': '5',
            'date': '2024-01-15'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'region': 'region',
            'units_sold': 'units_sold',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.product, 'Widget A')
        self.assertEqual(result.unit_price, 10.5)
        self.assertEqual(result.region, 'North')
        self.assertEqual(result.units_sold, 5.0)
        self.assertEqual(result.date, '2024-01-15')
    
    def test_parse_row_missing_product(self):
        """Test parsing row with missing product."""
        row = {'unit_price': '10.5'}
        mapping = {'product': 'product', 'unit_price': 'unit_price'}
        
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)
    
    def test_parse_row_missing_price(self):
        """Test parsing row with missing price."""
        row = {'product': 'Widget A'}
        mapping = {'product': 'product', 'unit_price': 'unit_price'}
        
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)
    
    def test_parse_row_missing_price_col_in_mapping(self):
        """Test parsing row when price column is missing from mapping."""
        row = {'product': 'Widget A', 'price': '10.5'}
        mapping = {'product': 'product'}  # unit_price not in mapping
        
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)  # Should return None when price_col is missing
    
    def test_parse_row_invalid_price(self):
        """Test parsing row with invalid price."""
        row = {'product': 'Widget A', 'unit_price': '0'}
        mapping = {'product': 'product', 'unit_price': 'unit_price'}
        
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)
    
    def test_parse_row_default_region(self):
        """Test parsing row with missing region uses default."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'units_sold': '5',
            'date': '2024-01-15'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'units_sold': 'units_sold',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.region, "Unknown")
    
    def test_parse_row_default_units(self):
        """Test parsing row with missing units defaults to 1."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'date': '2024-01-15'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.units_sold, 1.0)
    
    def test_parse_row_date_conversion(self):
        """Test parsing row converts date format."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'date': '15-01-2024'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.date, "2024-01-15")
    
    def test_load_sales_data_valid_csv(self):
        """Test loading data from a valid CSV file."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("date,product,region,units_sold,unit_price\n")
            f.write("2024-01-15,Widget A,North,10,5.0\n")
            f.write("2024-01-20,Widget B,South,5,10.0\n")
            temp_path = f.name
        
        try:
            records = load_sales_data(temp_path)
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0].product, "Widget A")
            self.assertEqual(records[1].product, "Widget B")
        finally:
            os.unlink(temp_path)
    
    def test_load_sales_data_file_not_found(self):
        """Test loading data from non-existent file raises error."""
        with self.assertRaises(FileNotFoundError):
            load_sales_data("nonexistent_file.csv")
    
    def test_load_sales_data_missing_columns(self):
        """Test loading data with missing required columns raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,value\n")
            f.write("test,123\n")
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                load_sales_data(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_sales_data_malformed_rows(self):
        """Test loading data skips malformed rows."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("date,product,region,units_sold,unit_price\n")
            f.write("2024-01-15,Widget A,North,10,5.0\n")
            f.write(",Widget B,South,5,10.0\n")  # Missing date - will get default date
            f.write("2024-01-20,,North,5,10.0\n")  # Missing product - skipped
            f.write("2024-01-25,Widget C,North,10,0\n")  # Invalid price - skipped
            f.write("2024-01-30,Widget D,North,10,15.0\n")  # Valid row
            temp_path = f.name
        
        try:
            records = load_sales_data(temp_path)
            # Should have 3 valid records (Widget A, Widget B with default date, Widget D)
            self.assertEqual(len(records), 3)
            self.assertEqual(records[0].product, "Widget A")
            self.assertEqual(records[1].product, "Widget B")
            self.assertEqual(records[2].product, "Widget D")
        finally:
            os.unlink(temp_path)
    
    def test_load_sales_data_various_column_names(self):
        """Test loading data with various column name formats."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("order_date,product_name,product_category,quantity,price_each\n")
            f.write("01-01-2024,Widget A,Laptop,10,5.0\n")
            f.write("15-01-2024,Widget B,Desktop,5,10.0\n")
            temp_path = f.name
        
        try:
            records = load_sales_data(temp_path)
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0].product, "Widget A")
            self.assertEqual(records[0].region, "Laptop")
            self.assertEqual(records[0].units_sold, 10.0)
            self.assertEqual(records[0].unit_price, 5.0)
            # Check date was converted
            self.assertEqual(records[0].date, "2024-01-01")
        finally:
            os.unlink(temp_path)
    
    def test_find_column_mapping_total_revenue(self):
        """Test column mapping for total_revenue field."""
        headers = ['product', 'price', 'revenue']
        mapping = find_column_mapping(headers)
        self.assertIn('total_revenue', mapping)
        self.assertEqual(mapping['total_revenue'], 'revenue')
    
    def test_normalize_date_mm_dd_yyyy(self):
        """Test normalizing date from MM-DD-YYYY format."""
        # When first part is <= 12, assume MM-DD-YYYY
        self.assertEqual(normalize_date("01-15-2024"), "2024-01-15")
        self.assertEqual(normalize_date("12-31-2022"), "2022-12-31")
    
    def test_normalize_date_invalid_format(self):
        """Test normalizing date with invalid format returns original."""
        # Date with only 2 parts or invalid format
        self.assertEqual(normalize_date("2024-01"), "2024-01")
        self.assertEqual(normalize_date("invalid-date"), "invalid-date")
        # Date with 3 parts but third part is 2 digits - should convert to 4-digit year
        self.assertEqual(normalize_date("15-01-24"), "2024-01-15")
    
    def test_normalize_date_exception_handling(self):
        """Test normalize_date handles exceptions gracefully."""
        # Test with non-numeric parts
        result = normalize_date("abc-def-ghij")
        # Should return original string when parsing fails
        self.assertIsInstance(result, str)
    
    def test_parse_row_empty_product(self):
        """Test parsing row with empty product string."""
        row = {'product': '   ', 'unit_price': '10.5'}
        mapping = {'product': 'product', 'unit_price': 'unit_price'}
        
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)
    
    def test_parse_row_zero_units_sold(self):
        """Test parsing row with zero units_sold defaults to 1."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'units_sold': '0',
            'date': '2024-01-15'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'units_sold': 'units_sold',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.units_sold, 1.0)
    
    def test_parse_row_negative_units_sold(self):
        """Test parsing row with negative units_sold defaults to 1."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'units_sold': '-5',
            'date': '2024-01-15'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'units_sold': 'units_sold',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.units_sold, 1.0)
    
    def test_parse_row_invalid_date_after_normalization(self):
        """Test parsing row with invalid date after normalization uses default."""
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'date': 'abc'  # Invalid date that normalizes to short string
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'date': 'date'
        }
        
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        # Should have a default date
        self.assertTrue(len(result.date) >= 7)  # At least YYYY-MM format
    
    def test_parse_row_exception_handling(self):
        """Test parse_row handles exceptions gracefully."""
        # Row with invalid data types that cause exceptions
        row = {
            'product': None,  # Will cause AttributeError in strip()
            'unit_price': '10.5'
        }
        mapping = {'product': 'product', 'unit_price': 'unit_price'}
        
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)
    
    def test_parse_row_keyerror_exception(self):
        """Test parse_row handles KeyError exceptions."""
        # Row missing a key that's expected
        row = {'product': 'Widget A'}
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'region': 'region',
            'units_sold': 'units_sold',
            'date': 'date'
        }
        # This will cause KeyError when trying to access row['unit_price']
        # but mapping says it should exist
        result = parse_row(row, mapping, 1)
        # Should handle gracefully and return None
        self.assertIsNone(result)
    
    def test_parse_row_exception_in_salesrecord_creation(self):
        """Test parse_row handles exceptions during SalesRecord creation."""
        # Test with data that might cause issues during SalesRecord creation
        # Using a row where date normalization might cause issues
        row = {
            'product': 'Widget A',
            'unit_price': '10.5',
            'date': '2024-01-15',
            'units_sold': '5',
            'region': 'North'
        }
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price',
            'date': 'date',
            'units_sold': 'units_sold',
            'region': 'region'
        }
        result = parse_row(row, mapping, 1)
        # Normal case should work
        self.assertIsNotNone(result)
    
    def test_parse_row_attribute_error(self):
        """Test parse_row handles AttributeError when accessing row values."""
        # Create a row-like object that raises AttributeError
        class BadRow:
            def get(self, key, default=None):
                raise AttributeError("Cannot access attribute")
        
        bad_row = BadRow()
        mapping = {
            'product': 'product',
            'unit_price': 'unit_price'
        }
        
        result = parse_row(bad_row, mapping, 1)
        # Should handle AttributeError and return None
        self.assertIsNone(result)
    
    def test_load_sales_data_empty_headers(self):
        """Test loading data with empty CSV file raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Empty file with no headers
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError) as context:
                load_sales_data(temp_path)
            self.assertIn("empty", str(context.exception).lower())
        finally:
            os.unlink(temp_path)
    
    def test_parse_month_column_valid(self):
        """Test parsing valid month column names."""
        self.assertEqual(parse_month_column("Jan 2012"), "2012-01")
        self.assertEqual(parse_month_column("February 2013"), "2013-02")
        self.assertEqual(parse_month_column("janv-12"), "2012-01")
        self.assertEqual(parse_month_column("mars-13"), "2013-03")
    
    def test_parse_month_column_invalid(self):
        """Test parsing invalid month column names."""
        self.assertIsNone(parse_month_column("Invalid"))
        self.assertIsNone(parse_month_column(""))
        self.assertIsNone(parse_month_column("Random Text"))
    
    def test_is_pivot_table_format_true(self):
        """Test detecting pivot table format."""
        headers = ['Make', 'Model', 'Jan 2012', 'Feb 2012', 'Mar 2012']
        self.assertTrue(is_pivot_table_format(headers))
    
    def test_is_pivot_table_format_false(self):
        """Test detecting non-pivot table format."""
        headers = ['date', 'product', 'units_sold']
        self.assertFalse(is_pivot_table_format(headers))
    
    def test_is_pivot_table_format_insufficient_dates(self):
        """Test pivot table format with insufficient date columns."""
        headers = ['Make', 'Model', 'Jan 2012']
        self.assertFalse(is_pivot_table_format(headers))
    
    def test_load_pivot_table_data(self):
        """Test loading pivot table format CSV."""
        csv_content = """Make,Model,janv-12,Feb 2012,mars-12
Chevrolet,Volt,100,200,300
Toyota,Prius PHV,50,150,250
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            records = load_pivot_table_data(temp_path)
            self.assertGreater(len(records), 0)
            # Check first record - product combines Make and Model, region is USA
            self.assertEqual(records[0].product, "Chevrolet Volt")
            self.assertEqual(records[0].region, "USA")
        finally:
            os.unlink(temp_path)
    
    def test_load_pivot_table_data_no_make_column(self):
        """Test loading pivot table without Make column."""
        csv_content = """Model,janv-12,Feb 2012
Volt,100,200
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                load_pivot_table_data(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_normalize_date_with_2_digit_year(self):
        """Test date normalization with 2-digit year."""
        result = normalize_date("15-01-24")
        self.assertEqual(result, "2024-01-15")
    
    def test_normalize_date_yyyy_mm_dd_already_normalized(self):
        """Test date that's already in YYYY-MM-DD format."""
        result = normalize_date("2024-01-15")
        self.assertEqual(result, "2024-01-15")
    
    def test_parse_row_with_calculated_unit_price(self):
        """Test parse_row calculates unit_price from revenue and units."""
        row = {
            'product': 'Widget A',
            'total_revenue': '100.0',
            'units_sold': '10.0',
            'region': 'North'
        }
        mapping = {
            'product': 'product',
            'total_revenue': 'total_revenue',
            'units_sold': 'units_sold',
            'region': 'region'
        }
        result = parse_row(row, mapping, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.unit_price, 10.0)
    
    def test_parse_row_zero_units_in_calculation(self):
        """Test parse_row handles zero units when calculating price."""
        row = {
            'product': 'Widget A',
            'total_revenue': '100.0',
            'units_sold': '0',
            'region': 'North'
        }
        mapping = {
            'product': 'product',
            'total_revenue': 'total_revenue',
            'units_sold': 'units_sold',
            'region': 'region'
        }
        result = parse_row(row, mapping, 1)
        self.assertIsNone(result)
    
    def test_find_column_mapping_total_revenue_variations(self):
        """Test finding total_revenue column with various names."""
        headers = ['Sales', 'Product', 'Price']
        mapping = find_column_mapping(headers)
        self.assertEqual(mapping.get('total_revenue'), 'Sales')
        
        headers2 = ['Revenue', 'Product', 'Price']
        mapping2 = find_column_mapping(headers2)
        self.assertEqual(mapping2.get('total_revenue'), 'Revenue')
    
    def test_load_sales_data_pivot_table_detection(self):
        """Test that load_sales_data detects and handles pivot tables."""
        csv_content = """Make,Model,janv-12,Feb 2012,mars-12
Chevrolet,Volt,100,200,300
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            records = load_sales_data(temp_path)
            self.assertGreater(len(records), 0)
        finally:
            os.unlink(temp_path)


class TestMainFunctions(unittest.TestCase):
    """Test cases for main module functions."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_records = [
            SalesRecord(
                date="2024-01-15",
                product="Widget A",
                region="North",
                units_sold=10.0,
                unit_price=5.0,
                total_revenue=50.0
            ),
            SalesRecord(
                date="2024-01-20",
                product="Widget B",
                region="South",
                units_sold=5.0,
                unit_price=10.0,
                total_revenue=50.0
            ),
        ]
    
    def test_print_analysis_results(self):
        """Test that print_analysis_results runs without errors."""
        import io
        import sys
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            print_analysis_results(self.sample_records)
            output = captured_output.getvalue()
            
            # Check that output contains expected sections
            self.assertIn("TOTAL UNITS SOLD", output)
            self.assertIn("UNITS SOLD BY PRODUCT", output)
            self.assertIn("TOP PRODUCT BY UNITS SOLD", output)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_print_analysis_results_empty_list(self):
        """Test print_analysis_results with empty list."""
        import io
        import sys
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            print_analysis_results([])
            output = captured_output.getvalue()
            self.assertIn("TOTAL UNITS SOLD", output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()

