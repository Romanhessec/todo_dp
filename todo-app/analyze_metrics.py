import json
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt

def load_metrics(filename):
    """Load metrics from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return None

def compare_performance(non_dp_metrics, dp_metrics):
    """Compare performance metrics"""
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    comparison_data = []
    
    metrics_to_compare = [
        ('avg_execution_time_ms', 'Avg Execution Time (ms)'),
        ('max_execution_time_ms', 'Max Execution Time (ms)'),
        ('min_execution_time_ms', 'Min Execution Time (ms)'),
        ('avg_memory_mb', 'Avg Memory Usage (MB)'),
        ('max_memory_mb', 'Max Memory Usage (MB)')
    ]
    
    for key, label in metrics_to_compare:
        non_dp_value = non_dp_metrics['performance'].get(key, 0)
        dp_value = dp_metrics['performance'].get(key, 0)
        
        if non_dp_value > 0:
            improvement = ((non_dp_value - dp_value) / non_dp_value) * 100
        else:
            improvement = 0
        
        comparison_data.append([
            label,
            f"{non_dp_value:.2f}",
            f"{dp_value:.2f}",
            f"{improvement:+.2f}%"
        ])
    
    print(tabulate(comparison_data, 
                   headers=['Metric', 'Non-DP', 'DP', 'Improvement'],
                   tablefmt='grid'))

def compare_database(non_dp_metrics, dp_metrics):
    """Compare database metrics"""
    print("\n" + "="*60)
    print("DATABASE COMPARISON")
    print("="*60)
    
    comparison_data = [
        ['Total Queries', 
         non_dp_metrics['database'].get('total_queries', 0),
         dp_metrics['database'].get('total_queries', 0)],
        ['Avg Query Time (ms)',
         f"{non_dp_metrics['database'].get('avg_query_time_ms', 0):.2f}",
         f"{dp_metrics['database'].get('avg_query_time_ms', 0):.2f}"]
    ]
    
    print(tabulate(comparison_data,
                   headers=['Metric', 'Non-DP', 'DP'],
                   tablefmt='grid'))

def analyze_code_complexity():
    """Analyze code complexity using radon"""
    print("\n" + "="*60)
    print("CODE COMPLEXITY ANALYSIS")
    print("="*60)
    print("\nRun these commands to compare complexity:")
    print("\n  Non-DP branch:")
    print("    radon cc app/routes/auth.py -a")
    print("    radon mi app/routes/auth.py")
    print("\n  DP branch:")
    print("    git checkout dp-branch")
    print("    radon cc app/routes/auth.py -a")
    print("    radon mi app/routes/auth.py")

def generate_charts(non_dp_metrics, dp_metrics):
    """Generate comparison charts"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Execution time comparison
    categories = ['Avg', 'Max', 'Min']
    non_dp_times = [
        non_dp_metrics['performance'].get('avg_execution_time_ms', 0),
        non_dp_metrics['performance'].get('max_execution_time_ms', 0),
        non_dp_metrics['performance'].get('min_execution_time_ms', 0)
    ]
    dp_times = [
        dp_metrics['performance'].get('avg_execution_time_ms', 0),
        dp_metrics['performance'].get('max_execution_time_ms', 0),
        dp_metrics['performance'].get('min_execution_time_ms', 0)
    ]
    
    x = range(len(categories))
    width = 0.35
    
    axes[0, 0].bar([i - width/2 for i in x], non_dp_times, width, label='Non-DP')
    axes[0, 0].bar([i + width/2 for i in x], dp_times, width, label='DP')
    axes[0, 0].set_ylabel('Time (ms)')
    axes[0, 0].set_title('Execution Time Comparison')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(categories)
    axes[0, 0].legend()
    
    # Memory comparison
    non_dp_memory = [
        non_dp_metrics['performance'].get('avg_memory_mb', 0),
        non_dp_metrics['performance'].get('max_memory_mb', 0)
    ]
    dp_memory = [
        dp_metrics['performance'].get('avg_memory_mb', 0),
        dp_metrics['performance'].get('max_memory_mb', 0)
    ]
    
    memory_cats = ['Avg', 'Max']
    x = range(len(memory_cats))
    
    axes[0, 1].bar([i - width/2 for i in x], non_dp_memory, width, label='Non-DP')
    axes[0, 1].bar([i + width/2 for i in x], dp_memory, width, label='DP')
    axes[0, 1].set_ylabel('Memory (MB)')
    axes[0, 1].set_title('Memory Usage Comparison')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(memory_cats)
    axes[0, 1].legend()
    
    plt.tight_layout()
    plt.savefig('metrics_comparison.png')
    print("\nCharts saved to metrics_comparison.png")

def main():
    """Main analysis function"""
    print("="*60)
    print("DESIGN PATTERN METRICS COMPARISON TOOL")
    print("="*60)
    
    # Load metrics
    non_dp = load_metrics('metrics_non_dp.json')
    dp = load_metrics('metrics_dp.json')
    
    if not non_dp:
        print("\nRun tests on non-DP branch first:")
        print("  python -m pytest tests/test_metrics.py -v")
        return
    
    if not dp:
        print("\nNon-DP metrics loaded. DP metrics not found.")
        print("Switch to DP branch and run:")
        print("  python -m pytest tests/test_metrics.py -v")
        return
    
    # Compare metrics
    compare_performance(non_dp, dp)
    compare_database(non_dp, dp)
    analyze_code_complexity()
    
    # Generate charts
    try:
        generate_charts(non_dp, dp)
    except Exception as e:
        print(f"\nCould not generate charts: {e}")
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)

if __name__ == '__main__':
    main()
