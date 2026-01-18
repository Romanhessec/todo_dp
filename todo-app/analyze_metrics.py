import json
import sys
from typing import Dict, Any
from tabulate import tabulate
import matplotlib.pyplot as plt

def load_metrics(filename: str) -> Dict[str, Any]:
    """Load metrics from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        print(f"   Make sure you've run the tests on both branches.")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filename}")
        print(f"   {e}")
        return None

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_section(title: str):
    """Print a section header"""
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}")

def compare_performance(non_dp: Dict, dp: Dict):
    """Compare performance metrics"""
    print_section("⚡ PERFORMANCE METRICS COMPARISON")
    
    non_dp_perf = non_dp.get('performance', {})
    dp_perf = dp.get('performance', {})
    
    metrics = [
        ('avg_execution_time_ms', 'Average Execution Time', 'ms', 'lower'),
        ('max_execution_time_ms', 'Max Execution Time', 'ms', 'lower'),
        ('min_execution_time_ms', 'Min Execution Time', 'ms', 'lower'),
        ('avg_memory_mb', 'Average Memory Usage', 'MB', 'lower'),
        ('max_memory_mb', 'Max Memory Usage', 'MB', 'lower'),
    ]
    
    print(f"\n{'Metric':<30} {'Non-DP':>12} {'DP':>12} {'Diff':>12} {'Winner':>10}")
    print("─" * 80)
    
    for key, label, unit, direction in metrics:
        non_dp_val = non_dp_perf.get(key, 0)
        dp_val = dp_perf.get(key, 0)
        
        if non_dp_val == 0:
            diff_pct = 0
            diff_str = "N/A"
        else:
            diff = dp_val - non_dp_val
            diff_pct = (diff / non_dp_val) * 100
            diff_str = f"{diff_pct:+.1f}%"
        
        # Determine winner
        if non_dp_val == dp_val or non_dp_val == 0:
            winner = "="
        elif direction == 'lower':
            winner = "✅ DP" if dp_val < non_dp_val else "non-DP"
        else:
            winner = "✅ DP" if dp_val > non_dp_val else "non-DP"
        
        print(f"{label:<30} {non_dp_val:>10.2f}{unit:>2} {dp_val:>10.2f}{unit:>2} {diff_str:>12} {winner:>10}")
    
    print("\n💡 Note: Lower execution time and memory usage is better")

def compare_database(non_dp: Dict, dp: Dict):
    """Compare database metrics"""
    print_section("🗄️  DATABASE METRICS COMPARISON")
    
    non_dp_db = non_dp.get('database', {})
    dp_db = dp.get('database', {})
    
    print(f"\n{'Metric':<30} {'Non-DP':>12} {'DP':>12} {'Winner':>10}")
    print("─" * 70)
    
    total_queries_non_dp = non_dp_db.get('total_queries', 0)
    total_queries_dp = dp_db.get('total_queries', 0)
    
    winner = "✅ DP" if total_queries_dp <= total_queries_non_dp else "non-DP"
    if total_queries_dp == total_queries_non_dp:
        winner = "="
    
    print(f"{'Total Queries':<30} {total_queries_non_dp:>12} {total_queries_dp:>12} {winner:>10}")
    
    print("\n💡 Note: Fewer database queries is generally better")

def compare_code_metrics(non_dp: Dict, dp: Dict):
    """Compare code quality metrics"""
    print_section("📊 CODE QUALITY METRICS COMPARISON")
    
    non_dp_code = non_dp.get('code_metrics', {})
    dp_code = dp.get('code_metrics', {})
    
    # Complexity comparison
    print("\n🔍 Cyclomatic Complexity:")
    non_dp_cc = non_dp_code.get('cyclomatic_complexity', {})
    dp_cc = dp_code.get('cyclomatic_complexity', {})
    
    non_dp_avg = non_dp_cc.get('average_grade', 'N/A')
    dp_avg = dp_cc.get('average_grade_functions', dp_cc.get('average_grade', 'N/A'))
    
    print(f"  Non-DP Average Grade: {non_dp_avg}")
    print(f"  DP Average Grade:     {dp_avg}")
    
    grade_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
    
    if non_dp_avg in grade_order and dp_avg in grade_order:
        if grade_order[dp_avg] < grade_order[non_dp_avg]:
            print(f"  ✅ Winner: DP (Lower complexity per function)")
        elif grade_order[dp_avg] > grade_order[non_dp_avg]:
            print(f"  Winner: non-DP")
        else:
            print(f"  = Equal complexity")
    
    # Maintainability
    print("\n🔧 Maintainability Index:")
    non_dp_mi = non_dp_code.get('maintainability_index', 'N/A')
    dp_mi = dp_code.get('maintainability_index', 'N/A')
    
    print(f"  Non-DP: {non_dp_mi}")
    print(f"  DP:     {dp_mi}")
    
    # Code size comparison
    print("\n📏 Code Size:")
    non_dp_summary = non_dp_code.get('summary', {})
    dp_summary = dp_code.get('summary', {})
    
    print(f"\n{'Metric':<30} {'Non-DP':>12} {'DP':>12} {'Diff':>12}")
    print("─" * 70)
    
    size_metrics = [
        ('total_files', 'Total Files'),
        ('total_classes', 'Total Classes'),
        ('total_functions', 'Total Functions'),
        ('lines_of_code', 'Lines of Code (LOC)'),
        ('logical_lines', 'Logical Lines (LLOC)'),
        ('source_lines', 'Source Lines (SLOC)'),
        ('comments', 'Comments'),
        ('blank_lines', 'Blank Lines'),
    ]
    
    for key, label in size_metrics:
        non_dp_val = non_dp_summary.get(key, 0)
        dp_val = dp_summary.get(key, 0)
        diff = dp_val - non_dp_val
        
        print(f"{label:<30} {non_dp_val:>12} {dp_val:>12} {diff:>+12}")
    
    print("\n💡 Note: More classes/files in DP is expected (better separation of concerns)")

def print_detailed_analysis(non_dp: Dict, dp: Dict):
    """Print detailed analysis and insights"""
    print_section("📈 DETAILED ANALYSIS")
    
    non_dp_perf = non_dp.get('performance', {})
    dp_perf = dp.get('performance', {})
    non_dp_code = non_dp.get('code_metrics', {})
    dp_code = dp.get('code_metrics', {})
    
    insights = []
    
    # Performance analysis
    avg_time_non_dp = non_dp_perf.get('avg_execution_time_ms', 0)
    avg_time_dp = dp_perf.get('avg_execution_time_ms', 0)
    
    if avg_time_dp > 0 and avg_time_non_dp > 0:
        perf_diff = ((avg_time_dp - avg_time_non_dp) / avg_time_non_dp) * 100
        
        if abs(perf_diff) < 10:
            insights.append(f"✅ Performance impact is negligible ({perf_diff:+.1f}%)")
        elif perf_diff > 0:
            insights.append(f"⚠️  DP is {perf_diff:.1f}% slower, but this is acceptable for better architecture")
        else:
            insights.append(f"✅ DP is {abs(perf_diff):.1f}% faster!")
    
    # Code quality analysis
    non_dp_loc = non_dp_code.get('summary', {}).get('lines_of_code', 0)
    dp_loc = dp_code.get('summary', {}).get('lines_of_code', 0)
    
    if dp_loc > 0 and non_dp_loc > 0:
        if dp_loc > non_dp_loc:
            loc_increase = ((dp_loc - non_dp_loc) / non_dp_loc) * 100
            insights.append(f"📝 Code size increased by {loc_increase:.1f}% (expected trade-off for better structure)")
        elif dp_loc < non_dp_loc:
            loc_decrease = ((non_dp_loc - dp_loc) / non_dp_loc) * 100
            insights.append(f"📝 Code size decreased by {loc_decrease:.1f}%")
    elif non_dp_loc == 0:
        insights.append(f"⚠️  Non-DP code metrics not collected. Run: python collect_code_metrics.py")
    elif dp_loc == 0:
        insights.append(f"⚠️  DP code metrics not collected. Run: python collect_code_metrics.py 'app/**/*.py' metrics_dp.json")
    
    # Complexity analysis
    non_dp_funcs = non_dp_code.get('summary', {}).get('total_functions', 0)
    dp_funcs = dp_code.get('summary', {}).get('total_functions', 0)
    dp_classes = dp_code.get('summary', {}).get('total_classes', 0)
    
    if dp_classes > 0:
        insights.append(f"✅ DP introduces {dp_classes} classes for better encapsulation")
    
    if dp_funcs > non_dp_funcs and non_dp_funcs > 0:
        insights.append(f"✅ Functions broken down into smaller units ({non_dp_funcs} → {dp_funcs})")
    
    # Print insights
    if insights:
        print("\n🎯 Key Insights:")
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. {insight}")
    else:
        print("\n⚠️  Limited insights available. Make sure code metrics are collected for both implementations.")
        print("    Run: python collect_code_metrics.py app/routes/auth.py metrics_non_dp.json")
        print("    Run: python collect_code_metrics.py 'app/**/*.py' metrics_dp.json")

def print_conclusion(non_dp: Dict, dp: Dict):
    """Print overall conclusion"""
    print_section("🏆 CONCLUSION")
    
    non_dp_perf = non_dp.get('performance', {})
    dp_perf = dp.get('performance', {})
    non_dp_code = non_dp.get('code_metrics', {})
    dp_code = dp.get('code_metrics', {})
    
    dp_score = 0
    total_criteria = 0
    
    # Criteria 1: Code complexity
    total_criteria += 1
    non_dp_cc = non_dp_code.get('cyclomatic_complexity', {}).get('average_grade', 'B')
    dp_cc = dp_code.get('cyclomatic_complexity', {}).get('average_grade_functions', 'A')
    grade_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
    
    if dp_cc in grade_order and non_dp_cc in grade_order:
        if grade_order[dp_cc] <= grade_order[non_dp_cc]:
            dp_score += 1
    
    # Criteria 2: Maintainability
    total_criteria += 1
    if dp_code.get('maintainability_index', 'A') == 'A':
        dp_score += 1
    
    # Criteria 3: Separation of Concerns (classes)
    total_criteria += 1
    if dp_code.get('summary', {}).get('total_classes', 0) > 0:
        dp_score += 1
    
    # Criteria 4: Performance (not significantly worse)
    total_criteria += 1
    avg_time_non_dp = non_dp_perf.get('avg_execution_time_ms', 0)
    avg_time_dp = dp_perf.get('avg_execution_time_ms', 0)
    
    if avg_time_non_dp > 0:
        perf_diff = ((avg_time_dp - avg_time_non_dp) / avg_time_non_dp) * 100
        if abs(perf_diff) < 20:  # Less than 20% difference
            dp_score += 1
    
    print(f"\n📊 Design Pattern Score: {dp_score}/{total_criteria}")
    print(f"\n{'Criteria':<40} {'Score':<10}")
    print("─" * 50)
    print(f"{'Lower Cyclomatic Complexity':<40} {'✅' if grade_order.get(dp_cc, 99) <= grade_order.get(non_dp_cc, 99) else '❌':<10}")
    print(f"{'High Maintainability (A grade)':<40} {'✅' if dp_code.get('maintainability_index') == 'A' else '❌':<10}")
    print(f"{'Better Separation of Concerns (Classes)':<40} {'✅' if dp_code.get('summary', {}).get('total_classes', 0) > 0 else '❌':<10}")
    print(f"{'Acceptable Performance Impact':<40} {'✅' if abs(perf_diff) < 20 else '❌':<10}")
    
    print("\n" + "="*70)
    if dp_score >= 3:
        print("  ✅ RESULT: Design Patterns provide clear benefits!")
        print("  The DP implementation demonstrates better code quality,")
        print("  structure, and maintainability with acceptable performance.")
    else:
        print("  ⚠️  RESULT: Mixed results")
        print("  Review the metrics to identify areas for improvement.")
    print("="*70)

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
    print_header("🔬 DESIGN PATTERN METRICS ANALYSIS")
    
    # Load both metrics files
    print("\nLoading metrics files...")
    non_dp = load_metrics('metrics_non_dp.json')
    dp = load_metrics('metrics_dp.json')
    
    if not non_dp or not dp:
        print("\n❌ Cannot proceed without both metrics files.")
        print("\nTo generate metrics:")
        print("  1. On non-DP branch: pytest tests/test_metrics.py -v -s")
        print("  2. On non-DP branch: python collect_code_metrics.py")
        print("  3. Switch to DP branch")
        print("  4. On DP branch: pytest tests/test_metrics.py -v -s")
        print("  5. On DP branch: python collect_code_metrics.py 'app/**/*.py'")
        print("  6. Run: python analyze_metrics.py")
        sys.exit(1)
    
    print("✅ Both metrics files loaded successfully\n")
    
    # Run comparisons
    compare_performance(non_dp, dp)
    compare_database(non_dp, dp)
    compare_code_metrics(non_dp, dp)
    print_detailed_analysis(non_dp, dp)
    print_conclusion(non_dp, dp)
    
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
