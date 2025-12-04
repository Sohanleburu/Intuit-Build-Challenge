# Sales Data Analysis Application

A Python application that performs data analysis on sales CSV files using functional programming patterns.

## 📋 Overview

This application loads sales data from a CSV file and performs various analyses including:
- Total revenue and units sold
- Sales grouped by product and region
- Average pricing by product
- Top selling products
- Monthly sales trends

## 📁 Project Structure

```
data_analysis/
├── data/
│   └── sales.csv          # Your sales data CSV file (download manually)
├── src/
│   ├── models.py          # Data models (SalesRecord dataclass)
│   ├── reader.py          # CSV loading and validation
│   ├── analysis.py        # Analysis functions
│   └── main.py            # Main program entry point
├── tests/
│   └── test_all.py        # Unit tests for all modules
└── README.md              # This file
```

## 📊 Dataset Requirements

### Expected CSV Format

The CSV file should contain the following columns:

- **date**: Date of sale in YYYY-MM-DD format (e.g., "2024-01-15")
- **product**: Product name (string)
- **region**: Sales region (string)
- **units_sold**: Number of units sold (numeric)
- **unit_price**: Price per unit (numeric)
- **total_revenue**: Total revenue (numeric, optional - will be calculated if missing)

### Example CSV

```csv
date,product,region,units_sold,unit_price,total_revenue
2024-01-15,Widget A,North,10,5.0,50.0
2024-01-20,Widget B,South,5,10.0,50.0
2024-02-10,Widget A,North,8,5.0,40.0
```

### Notes

- Column names are case-insensitive
- Extra columns are ignored
- Missing `total_revenue` will be calculated as `units_sold * unit_price`
- Rows with missing essential data (date, product, region) are skipped
- Invalid numeric values are treated as 0

## 🚀 How to Run

### Prerequisites

- Python 3.7 or higher
- Standard library only (no external dependencies)

### Steps

1. **Download your sales CSV file**
   - Get a CSV file from Kaggle, GitHub, or any public dataset
   - Ensure it has the required columns (see above)
   - Place it in the `data/` folder as `sales.csv`

2. **Run the analysis**
   ```bash
   cd data_analysis/src
   python3 main.py
   ```

   Or specify a custom CSV path:
   ```bash
   python3 main.py /path/to/your/sales.csv
   ```

3. **View results**
   - Results are printed to the console
   - Includes all analysis metrics formatted clearly

## 🧪 How to Run Tests

Run all unit tests using:

```bash
cd data_analysis
python3 -m unittest tests.test_all
```

Or run with verbose output:

```bash
python3 -m unittest tests.test_all -v
```

### Test Coverage

All analysis functions are tested:
- ✅ total_revenue
- ✅ total_units_sold
- ✅ sales_by_product
- ✅ sales_by_region
- ✅ average_price_by_product
- ✅ top_selling_product
- ✅ monthly_sales

Tests include edge cases:
- Empty lists
- Single records
- Multiple products/regions
- Different date formats

## 📈 Sample Output

```
Loading sales data from: /path/to/data/sales.csv
Successfully loaded 8 sales records

======================================================================
SALES DATA ANALYSIS RESULTS
======================================================================

1. TOTAL REVENUE
----------------------------------------------------------------------
   Total Revenue: $555.00

2. TOTAL UNITS SOLD
----------------------------------------------------------------------
   Total Units Sold: 86

3. SALES BY PRODUCT
----------------------------------------------------------------------
   Widget C: $150.00
   Widget B: $230.00
   Widget A: $215.00

4. SALES BY REGION
----------------------------------------------------------------------
   East: $170.00
   North: $240.00
   South: $125.00
   West: $60.00

5. AVERAGE PRICE BY PRODUCT
----------------------------------------------------------------------
   Widget A: $5.00
   Widget B: $10.00
   Widget C: $7.50

6. TOP SELLING PRODUCT
----------------------------------------------------------------------
   Product: Widget B
   Revenue: $230.00

7. MONTHLY SALES
----------------------------------------------------------------------
   2024-01: $100.00
   2024-02: $160.00
   2024-03: $225.00
   2024-04: $110.00

======================================================================
```

## 🔧 Technical Details

### Functional Programming Patterns Used

- **Map**: Transforming data structures
- **Filter**: Selecting relevant records
- **Reduce**: Aggregating values
- **Lambda expressions**: Inline functions
- **List/Dict comprehensions**: Creating new collections
- **Pure functions**: No side effects, deterministic output

### Code Style

- PEP8 compliant
- Small, single-purpose functions
- Clear separation of concerns
- Comprehensive docstrings
- Type hints where appropriate

### Error Handling

- Validates CSV file existence
- Checks for required columns
- Skips malformed rows gracefully
- Provides clear error messages

## 📝 License

This is a sample implementation for educational purposes.

