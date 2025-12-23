"""
Statistics Module
This module implements statistical functions for data analysis.
"""

import math
from collections import Counter


class StatisticsCalculator:
    """Class for calculating statistical measures"""
    
    def __init__(self):
        pass
    
    def mean(self, values):
        try:
            if not values:
                return 0.0
            return sum(values) / len(values)
        except (TypeError, ZeroDivisionError):
            return 0.0
    
    def median(self, values):
        try:
            if not values:
                return 0.0
            sorted_values = sorted(values)
            n = len(sorted_values)
            mid = n // 2
            if n % 2 == 0:
                return (sorted_values[mid - 1] + sorted_values[mid]) / 2
            else:
                return sorted_values[mid]
        except (TypeError, IndexError):
            return 0.0
    
    def mode(self, values):
        try:
            if not values:
                return 0.0
            counter = Counter(values)
            return counter.most_common(1)[0][0]
        except (TypeError, IndexError):
            return 0.0
    
    def variance(self, values):
        try:
            if not values or len(values) < 2:
                return 0.0
            mean_val = self.mean(values)
            squared_diffs = [(x - mean_val) ** 2 for x in values]
            return sum(squared_diffs) / len(values)
        except TypeError:
            return 0.0
    
    def standard_deviation(self, values):
        try:
            return math.sqrt(self.variance(values))
        except (TypeError, ValueError):
            return 0.0
    
    def minimum(self, values):
        try:
            if not values:
                return 0.0
            return min(values)
        except (TypeError, ValueError):
            return 0.0
    
    def maximum(self, values):
        try:
            if not values:
                return 0.0
            return max(values)
        except (TypeError, ValueError):
            return 0.0
    
    def range_val(self, values):
        try:
            if not values:
                return 0.0
            return self.maximum(values) - self.minimum(values)
        except TypeError:
            return 0.0
    
    def get_all_statistics(self, values):
        return {
            'mean': self.mean(values),
            'median': self.median(values),
            'mode': self.mode(values),
            'variance': self.variance(values),
            'std_dev': self.standard_deviation(values),
            'min': self.minimum(values),
            'max': self.maximum(values),
            'range': self.range_val(values)
        }
