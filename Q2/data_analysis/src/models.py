"""
Data Models
Defines the data structure for sales records.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SalesRecord:
    """
    Represents a single sales record from the CSV file.
    
    Attributes:
        date: Date of the sale (YYYY-MM-DD format)
        product: Name of the product
        region: Sales region
        units_sold: Number of units sold
        unit_price: Price per unit
        total_revenue: Total revenue (calculated if not provided)
    """
    date: str
    product: str
    region: str
    units_sold: float
    unit_price: float
    total_revenue: float
    
    def __post_init__(self):
        """
        Calculate total_revenue if not provided or if it's zero.
        Ensures total_revenue is always accurate.
        """
        if self.total_revenue == 0 or self.total_revenue is None:
            self.total_revenue = self.units_sold * self.unit_price

