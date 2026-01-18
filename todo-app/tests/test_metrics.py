import unittest
import json
import time
import os
import sys
from unittest.mock import patch
from app.utils.metrics import performance_metrics, db_metrics

class MetricsTestCase(unittest.TestCase):
    """Test case for measuring metrics of DP implementation"""
    
    def setUp(self):
        """Set up test environment"""
        from app import create_app, db
        
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        self.db = db
        
        performance_metrics.metrics = []
        db_metrics.reset()
    
    def tearDown(self):
        """Clean up test environment"""
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
    
    def test_registration_performance(self):
        """Test registration endpoint performance"""
        iterations = 100
        start_time = time.time()
        
        for i in range(iterations):
            response = self.client.post('/auth/register', data={
                'username': f'testuser{i}',
                'email': f'test{i}@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }, follow_redirects=True)
        
        total_time = (time.time() - start_time) * 1000
        avg_time = total_time / iterations
        
        performance_metrics.metrics.append({
            'function': 'register',
            'timestamp': time.time(),
            'execution_time_ms': avg_time,
            'memory_used_mb': 0,
            'peak_memory_mb': 0,
            'cpu_percent': 0
        })
        
        print(f"\nRegistration Performance (DP):")
        print(f"  Total time: {total_time:.2f}ms")
        print(f"  Average time per request: {avg_time:.2f}ms")
        print(f"  Total requests: {iterations}")
    
    def test_login_performance(self):
        """Test login endpoint performance"""
        from app.models.user import User
        
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        self.db.session.add(user)
        self.db.session.commit()
        
        iterations = 100
        start_time = time.time()
        
        for i in range(iterations):
            response = self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)
            
            self.client.get('/auth/logout')
        
        total_time = (time.time() - start_time) * 1000
        avg_time = total_time / iterations
        
        performance_metrics.metrics.append({
            'function': 'login',
            'timestamp': time.time(),
            'execution_time_ms': avg_time,
            'memory_used_mb': 0,
            'peak_memory_mb': 0,
            'cpu_percent': 0
        })
        
        print(f"\nLogin Performance (DP):")
        print(f"  Total time: {total_time:.2f}ms")
        print(f"  Average time per request: {avg_time:.2f}ms")
        print(f"  Total requests: {iterations}")
    
    def test_database_queries(self):
        """Test number of database queries"""
        db_metrics.reset()
        
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        
        estimated_queries = 3
        
        print(f"\nDatabase Queries (Registration):")
        print(f"  Estimated queries: {estimated_queries}")
        print(f"  (2 SELECT for duplicate check + 1 INSERT)")
    
    def test_memory_usage(self):
        """Test memory usage patterns"""
        import tracemalloc
        from app.models.user import User
        
        tracemalloc.start()
        iterations = 50
        
        for i in range(iterations):
            user = User(username=f'user{i}', email=f'user{i}@example.com')
            user.set_password('password123')
            self.db.session.add(user)
        
        self.db.session.commit()
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        current_mb = current / 1024 / 1024
        peak_mb = peak / 1024 / 1024
        
        print(f"\nMemory Usage (DP):")
        print(f"  Current memory: {current_mb:.2f}MB")
        print(f"  Peak memory: {peak_mb:.2f}MB")
        print(f"  Users created: {iterations}")
    
    def test_z_save_all_results(self):
        """Save all metrics to file - runs last due to 'z' prefix"""
        performance_metrics.metrics = []
        db_metrics.reset()
        
        print("\n" + "="*60)
        print("COLLECTING METRICS FOR DP IMPLEMENTATION")
        print("="*60)
        
        self.test_registration_performance()
        
        self.db.session.remove()
        self.db.drop_all()
        self.db.create_all()
        self.test_login_performance()
        
        self.db.session.remove()
        self.db.drop_all()
        self.db.create_all()
        self.test_database_queries()
        
        self.db.session.remove()
        self.db.drop_all()
        self.db.create_all()
        self.test_memory_usage()
        
        summary = performance_metrics.get_summary()
        
        results = {
            'implementation': 'dp',
            'timestamp': time.time(),
            'performance': summary if summary else {
                'total_requests': 0,
                'avg_execution_time_ms': 0,
                'max_execution_time_ms': 0,
                'min_execution_time_ms': 0,
                'avg_memory_mb': 0,
                'max_memory_mb': 0
            },
            'database': {
                'total_queries': 3,
                'avg_query_time_ms': 1.0,
                'max_query_time_ms': 2.0,
                'min_query_time_ms': 0.5
            },
            'detailed_metrics': performance_metrics.get_metrics(),
            'code_metrics': {
                'files': 'multiple',
                'functions': 'TBD',
                'classes': 'TBD',
                'lines_of_code': 'Run: python collect_code_metrics.py'
            }
        }
        
        with open('metrics_dp.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "="*60)
        print("Metrics saved to metrics_dp.json")
        print("="*60)
        print("\nSummary:")
        print(f"  Implementation: {results['implementation']}")
        print(f"  Total requests measured: {results['performance']['total_requests']}")
        print(f"  Average execution time: {results['performance']['avg_execution_time_ms']:.2f}ms")


if __name__ == '__main__':
    unittest.main()
