# Intuit Build Challenge

This repository contains solutions for two coding challenges demonstrating advanced Python programming concepts including thread synchronization, concurrent programming, and functional data analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Q1: Producer-Consumer Pattern](#q1-producer-consumer-pattern)
  - [Overview](#q1-overview)
  - [Components](#q1-components)
  - [Quick Start](#q1-quick-start)
  - [Testing](#q1-testing)
  - [Key Features](#q1-key-features)
- [Q2: Data Analysis Application](#q2-data-analysis-application)
  - [Overview](#q2-overview)
  - [Project Structure](#q2-project-structure)
  - [Dataset Requirements](#q2-dataset-requirements)
  - [Quick Start](#q2-quick-start)
  - [Testing](#q2-testing)
  - [Technical Details](#q2-technical-details)
- [Features Summary](#features-summary)

---

## Overview

This repository contains two distinct projects:

1. **Q1: Producer-Consumer Pattern** - A thread synchronization implementation demonstrating concurrent programming with blocking queues
2. **Q2: Data Analysis Application** - A sales data analysis tool using functional programming patterns

Both projects use only Python's standard library with no external dependencies.

## Repository Structure

```
Intuit-Build-Challenge/
├── Q1/                          # Producer-Consumer Pattern
│   ├── bounded_blocking_queue.py    # Thread-safe bounded blocking queue
│   ├── producer.py                  # Producer thread implementation
│   ├── consumer.py                  # Consumer thread implementation
│   ├── source_container.py          # Container for source items
│   ├── destination_container.py     # Container for consumed items
│   ├── main.py                      # Main program demonstration
│   └── test_producer_consumer.py    # Comprehensive unit tests
│
└── Q2/                          # Data Analysis Application
    └── data_analysis/
        ├── src/                     # Source code
        │   ├── models.py            # Data models (SalesRecord dataclass)
        │   ├── reader.py            # CSV loading and validation
        │   ├── analysis.py          # Analysis functions
        │   └── main.py              # Main program entry point
        ├── tests/                   # Unit tests
        │   └── test_all.py          # Comprehensive test suite
        └── data/                    # Sample datasets
            └── Electric Car Sales by Model in USA.csv
```

## Requirements

- **Python 3.7 or higher**
- **Standard library only** (no external dependencies)

---

## Q1: Producer-Consumer Pattern

### Q1 Overview

This project implements a classic producer-consumer pattern demonstrating thread synchronization and communication. The program simulates concurrent data transfer between a producer thread that reads from a source container and places items into a shared queue, and a consumer thread that reads from the queue and stores items in a destination container.

### Q1 Components

#### 1. BoundedBlockingQueue
A thread-safe bounded blocking queue that:
- Has a maximum capacity
- Blocks producers when full
- Blocks consumers when empty
- Uses `threading.Condition` for wait/notify synchronization

#### 2. SourceContainer
A thread-safe container that holds items for the producer to read sequentially.

#### 3. DestinationContainer
A thread-safe container that stores items consumed from the queue.

#### 4. Producer
A thread that:
- Reads items from a `SourceContainer`
- Places items into a shared `BoundedBlockingQueue`
- Blocks when the queue is full

#### 5. Consumer
A thread that:
- Reads items from a shared `BoundedBlockingQueue`
- Stores items in a `DestinationContainer`
- Blocks when the queue is empty

### Q1 Quick Start

1. **Navigate to the Q1 directory:**
   ```bash
   cd Q1
   ```

2. **Verify Python version:**
   ```bash
   python3 --version
   ```
   Should be Python 3.7 or higher.

3. **Run the main program:**
   ```bash
   python3 main.py
   ```

4. **Run unit tests:**
   ```bash
   python3 -m unittest test_producer_consumer.py -v
   ```

### Q1 Sample Output

```
============================================================
Producer-Consumer Pattern Demonstration
============================================================

Configuration:
  Queue Capacity: 5
  Source Items: 20
  Producer Delay: 0.1s
  Consumer Delay: 0.15s

Creating components...
  Queue created with capacity: 5
  Source container created with 20 items
  Destination container created

Creating threads...
  Producer thread created: Producer-1
  Consumer thread created: Consumer-1

Starting threads...
------------------------------------------------------------
[Consumer-1] Started consuming items
[Producer-1] Started producing items
[Producer-1] Produced item: Item-1
[Consumer-1] Consumed item: Item-1
...
[Producer-1] Finished producing. Total items produced: 20
------------------------------------------------------------
Producer thread finished
Consumer thread finished

============================================================
Results
============================================================
Items in source container: 20
Items produced: 20
Items consumed: 20
Items in destination container: 20
Items remaining in queue: 0

Verification:
  All items successfully transferred from source to destination
  All source items match destination items

============================================================
Program completed successfully!
============================================================
```

### Q1 Testing

Run comprehensive unit tests:

```bash
cd Q1
python3 -m unittest test_producer_consumer.py -v
```

**Test Coverage:**
- 24 comprehensive unit tests
- Thread synchronization verification
- Blocking behavior on empty/full queues
- Concurrent put and get operations
- Multiple producers and consumers
- Edge cases and error handling

**Testing Objectives Covered:**
- Thread Synchronization - All shared data structures use proper locking mechanisms
- Concurrent Programming - Multiple producer and consumer threads can run simultaneously
- Blocking Queues - Queue blocks producers when full and consumers when empty
- Wait/Notify Mechanism - Uses `threading.Condition.wait()` and `notify()` for synchronization

### Q1 Key Features

1. **Thread Safety**: All components are thread-safe and can be used concurrently
2. **Blocking Behavior**: Queue properly blocks threads when conditions aren't met
3. **Synchronization**: Uses Python's `threading.Condition` for efficient wait/notify
4. **Comprehensive Testing**: 24 unit tests covering all functionality
5. **Well Documented**: All classes and methods have detailed docstrings
6. **Error Handling**: Proper exception handling for edge cases

**Design Decisions:**
- Generic Types: Used Python's `TypeVar` for type safety and reusability
- Condition Variables: Used `threading.Condition` instead of `threading.Lock` for better efficiency
- Sentinel Values: Consumer uses sentinel values to signal end of production
- Timeout Support: Queue operations support optional timeouts for better control
- Thread Naming: All threads have descriptive names for easier debugging

---

## Q2: Data Analysis Application

### Q2 Overview

A Python application that performs data analysis on sales CSV files using functional programming patterns. The application loads sales data from a CSV file and performs various analyses including total revenue, units sold, sales grouped by product and region, average pricing, top selling products, and monthly sales trends.

### Q2 Project Structure

```
data_analysis/
├── data/
│   └── Electric Car Sales by Model in USA.csv    # Sample dataset
├── src/
│   ├── models.py          # Data models (SalesRecord dataclass)
│   ├── reader.py          # CSV loading and validation
│   ├── analysis.py        # Analysis functions
│   └── main.py            # Main program entry point
├── tests/
│   └── test_all.py        # Unit tests for all modules
└── README.md              # Documentation (now merged here)
```

### Q2 Dataset Requirements

#### Sample Dataset

A sample dataset is included in the repository:
- **Location**: `Q2/data_analysis/data/Electric Car Sales by Model in USA.csv`
- This dataset can be used directly to run the analysis

#### Expected CSV Format

The CSV file should contain the following columns:

- **date**: Date of sale in YYYY-MM-DD format (e.g., "2024-01-15")
- **product**: Product name (string)
- **region**: Sales region (string)
- **units_sold**: Number of units sold (numeric)
- **unit_price**: Price per unit (numeric)
- **total_revenue**: Total revenue (numeric, optional - will be calculated if missing)

#### Example CSV Format

```csv
date,product,region,units_sold,unit_price,total_revenue
2024-01-15,Widget A,North,10,5.0,50.0
2024-01-20,Widget B,South,5,10.0,50.0
2024-02-10,Widget A,North,8,5.0,40.0
```

#### Notes

- Column names are case-insensitive
- Extra columns are ignored
- Missing `total_revenue` will be calculated as `units_sold * unit_price`
- Rows with missing essential data (date, product, region) are skipped
- Invalid numeric values are treated as 0

### Q2 Quick Start

1. **Run the analysis with the included sample dataset:**
   ```bash
   cd Q2/data_analysis
   python3 src/main.py
   ```

   This will automatically use the sample dataset: `data/Electric Car Sales by Model in USA.csv`

   **Or use your own CSV file:**
   ```bash
   python3 src/main.py /path/to/your/sales.csv
   ```

3. **View results:**
   - Results are printed to the console
   - Includes all analysis metrics formatted clearly

### Q2 Sample Output

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

### Q2 Testing

Run all unit tests:

```bash
cd Q2/data_analysis
python3 -m unittest tests.test_all
```

Or run with verbose output:

```bash
python3 -m unittest tests.test_all -v
```

**Test Coverage:**
- 140+ comprehensive unit tests
- 95% test coverage (excluding main.py)
- All analysis functions tested
- Edge cases covered (empty lists, single records, multiple products/regions)
- Different date formats handled

**Analysis Functions Tested:**
- total_revenue
- total_units_sold
- sales_by_product
- sales_by_region
- average_price_by_product
- top_selling_product
- monthly_sales
- And 11+ additional analysis metrics

### Q2 Technical Details

#### Functional Programming Patterns Used

- **Map**: Transforming data structures
- **Filter**: Selecting relevant records
- **Reduce**: Aggregating values
- **Lambda expressions**: Inline functions
- **List/Dict comprehensions**: Creating new collections
- **Pure functions**: No side effects, deterministic output

#### Code Style

- PEP8 compliant
- Small, single-purpose functions
- Clear separation of concerns
- Comprehensive docstrings
- Type hints where appropriate

#### Error Handling

- Validates CSV file existence
- Checks for required columns
- Skips malformed rows gracefully
- Provides clear error messages

---

## Features Summary

### Q1 Features
- Thread-safe bounded blocking queue
- Producer-Consumer pattern with wait/notify mechanism
- Comprehensive unit tests (24 tests)
- Clean, modular architecture
- Timeout support for blocking operations
- Multiple producer/consumer support

### Q2 Features
- Flexible CSV data loading (handles various formats)
- 18+ data analysis metrics
- Functional programming patterns
- 95% test coverage (excluding main.py)
- 140+ comprehensive unit tests
- Robust error handling and validation

---

## License

This project is part of a coding challenge submission.
