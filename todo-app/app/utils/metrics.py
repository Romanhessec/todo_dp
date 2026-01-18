import time
import functools
import tracemalloc
import psutil
import os
from typing import Dict, Any, Callable
from datetime import datetime
import json

class PerformanceMetrics:
    """Utility class to measure performance metrics"""
    
    def __init__(self):
        self.metrics = []
        self.process = psutil.Process(os.getpid())
    
    def measure_endpoint(self, func: Callable) -> Callable:
        """Decorator to measure endpoint performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Start measurements
            start_time = time.time()
            start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            tracemalloc.start()
            
            # Execute function
            result = func(*args, **kwargs)
            
            # End measurements
            end_time = time.time()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            # Record metrics
            metric = {
                'function': func.__name__,
                'timestamp': datetime.now().isoformat(),
                'execution_time_ms': (end_time - start_time) * 1000,
                'memory_used_mb': end_memory - start_memory,
                'peak_memory_mb': peak / 1024 / 1024,
                'cpu_percent': self.process.cpu_percent()
            }
            
            self.metrics.append(metric)
            return result
        
        return wrapper
    
    def get_metrics(self) -> list:
        """Get all recorded metrics"""
        return self.metrics
    
    def save_metrics(self, filename: str):
        """Save metrics to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.metrics:
            return {}
        
        execution_times = [m['execution_time_ms'] for m in self.metrics]
        memory_used = [m['memory_used_mb'] for m in self.metrics]
        
        return {
            'total_requests': len(self.metrics),
            'avg_execution_time_ms': sum(execution_times) / len(execution_times),
            'max_execution_time_ms': max(execution_times),
            'min_execution_time_ms': min(execution_times),
            'avg_memory_mb': sum(memory_used) / len(memory_used),
            'max_memory_mb': max(memory_used)
        }


class DatabaseMetrics:
    """Track database operations"""
    
    def __init__(self):
        self.query_count = 0
        self.queries = []
    
    def record_query(self, query: str, execution_time: float):
        """Record a database query"""
        self.query_count += 1
        self.queries.append({
            'query': query,
            'execution_time_ms': execution_time * 1000,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get database metrics summary"""
        if not self.queries:
            return {'total_queries': 0}
        
        execution_times = [q['execution_time_ms'] for q in self.queries]
        
        return {
            'total_queries': self.query_count,
            'avg_query_time_ms': sum(execution_times) / len(execution_times),
            'max_query_time_ms': max(execution_times),
            'min_query_time_ms': min(execution_times)
        }
    
    def reset(self):
        """Reset metrics"""
        self.query_count = 0
        self.queries = []


# Global instances
performance_metrics = PerformanceMetrics()
db_metrics = DatabaseMetrics()
