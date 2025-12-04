# Intuit Build Challenge

This repository contains solutions for two coding challenges:

1. **Q1: Producer-Consumer Pattern** - Thread synchronization implementation
2. **Q2: Data Analysis Application** - Sales data analysis with functional programming

## Repository Structure

```
Intuit-Build-Challenge/
├── Q1/                          # Producer-Consumer Pattern
│   ├── bounded_blocking_queue.py
│   ├── producer.py
│   ├── consumer.py
│   ├── source_container.py
│   ├── destination_container.py
│   ├── main.py
│   ├── test_producer_consumer.py
│   └── README.md                # Detailed Q1 documentation
│
└── Q2/                          # Data Analysis Application
    └── data_analysis/
        ├── src/                 # Source code
        │   ├── models.py
        │   ├── reader.py
        │   ├── analysis.py
        │   └── main.py
        ├── tests/               # Unit tests
        │   └── test_all.py
        ├── data/                # Sample datasets
        │   └── Electric Car Sales by Model in USA.csv
        └── README.md            # Detailed Q2 documentation
```

## Quick Start

### Q1: Producer-Consumer Pattern

Navigate to the `Q1/` directory and see the [Q1 README](Q1/README.md) for detailed instructions.

**Quick run:**
```bash
cd Q1
python3 main.py
```

### Q2: Data Analysis Application

Navigate to the `Q2/data_analysis/` directory and see the [Q2 README](Q2/data_analysis/README.md) for detailed instructions.

**Quick run:**
```bash
cd Q2/data_analysis
python3 src/main.py
```

**Run tests:**
```bash
cd Q2/data_analysis
python3 -m unittest tests.test_all
```

## Features

### Q1 Features
- ✅ Thread-safe bounded blocking queue
- ✅ Producer-Consumer pattern with wait/notify mechanism
- ✅ Comprehensive unit tests
- ✅ Clean, modular architecture

### Q2 Features
- ✅ Flexible CSV data loading (handles various formats)
- ✅ 18+ data analysis metrics
- ✅ Functional programming patterns
- ✅ 95% test coverage (excluding main.py)
- ✅ 140 comprehensive unit tests

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## License

This project is part of a coding challenge submission.

