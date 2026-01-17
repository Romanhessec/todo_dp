import json
import subprocess
import re
import sys

def run_radon_command(command):
    """Run a radon command and return the output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        return ""

def parse_complexity(output):
    """Parse cyclomatic complexity output"""
    # Example: F 9:0 register - B
    functions = []
    lines = output.strip().split('\n')
    
    for line in lines:
        if line.strip().startswith('F '):
            # Extract function info
            match = re.match(r'F\s+(\d+):(\d+)\s+(\w+)\s+-\s+([A-F])', line.strip())
            if match:
                functions.append({
                    'line': int(match.group(1)),
                    'name': match.group(3),
                    'complexity_grade': match.group(4)
                })
    
    return functions

def parse_maintainability(output):
    """Parse maintainability index output"""
    # Example: app/routes/auth.py - A
    lines = output.strip().split('\n')
    for line in lines:
        if ' - ' in line:
            parts = line.split(' - ')
            if len(parts) == 2:
                return parts[1].strip()
    return "Unknown"

def parse_raw_metrics(output):
    """Parse raw code metrics"""
    metrics = {}
    lines = output.strip().split('\n')
    
    for line in lines:
        if ':' in line:
            parts = line.strip().split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                
                # Try to convert to int
                try:
                    value = int(value)
                except ValueError:
                    # Keep as string if not a number
                    pass
                
                metrics[key] = value
    
    return metrics

def calculate_average_complexity(functions):
    """Calculate average complexity from function grades"""
    grade_to_score = {
        'A': 1,  # 1-5 (low risk)
        'B': 2,  # 6-10 (low risk)
        'C': 3,  # 11-20 (moderate risk)
        'D': 4,  # 21-30 (moderate risk)
        'E': 5,  # 31-40 (high risk)
        'F': 6   # 41+ (very high risk)
    }
    
    if not functions:
        return 'N/A'
    
    scores = [grade_to_score.get(f['complexity_grade'], 0) for f in functions]
    avg_score = sum(scores) / len(scores)
    
    # Convert back to grade
    if avg_score <= 1.5:
        return 'A'
    elif avg_score <= 2.5:
        return 'B'
    elif avg_score <= 3.5:
        return 'C'
    elif avg_score <= 4.5:
        return 'D'
    elif avg_score <= 5.5:
        return 'E'
    else:
        return 'F'

def collect_code_metrics(file_path, metrics_json_path):
    """Collect all code metrics using radon"""
    print(f"\nCollecting code metrics for {file_path}...")
    print("="*60)
    
    # Run radon commands
    cc_output = run_radon_command(f"radon cc {file_path} -a")
    mi_output = run_radon_command(f"radon mi {file_path}")
    raw_output = run_radon_command(f"radon raw {file_path}")
    
    # Parse outputs
    functions = parse_complexity(cc_output)
    maintainability = parse_maintainability(mi_output)
    raw_metrics = parse_raw_metrics(raw_output)
    avg_complexity = calculate_average_complexity(functions)
    
    # Display results
    print("\n1. Cyclomatic Complexity:")
    print(cc_output)
    print(f"\n2. Maintainability Index:")
    print(mi_output)
    print(f"\n3. Raw Metrics:")
    print(raw_output)
    
    # Prepare code metrics structure
    code_metrics = {
        'file': file_path,
        'cyclomatic_complexity': {
            'average_grade': avg_complexity,
            'functions': functions
        },
        'maintainability_index': maintainability,
        'raw_metrics': raw_metrics,
        'summary': {
            'total_functions': len(functions),
            'lines_of_code': raw_metrics.get('LOC', 0),
            'logical_lines': raw_metrics.get('LLOC', 0),
            'source_lines': raw_metrics.get('SLOC', 0),
            'comments': raw_metrics.get('Comments', 0),
            'blank_lines': raw_metrics.get('Blank', 0)
        }
    }
    
    # Load existing metrics
    try:
        with open(metrics_json_path, 'r') as f:
            metrics = json.load(f)
    except FileNotFoundError:
        print(f"\nWarning: {metrics_json_path} not found. Creating new file.")
        metrics = {
            'implementation': 'non-dp',
            'timestamp': 0,
            'performance': {},
            'database': {},
            'detailed_metrics': []
        }
    
    # Update code metrics
    metrics['code_metrics'] = code_metrics
    
    # Save updated metrics
    with open(metrics_json_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("\n" + "="*60)
    print(f"Code metrics saved to {metrics_json_path}")
    print("="*60)
    
    # Print summary
    print("\nCode Metrics Summary:")
    print(f"  File: {file_path}")
    print(f"  Total Functions: {len(functions)}")
    print(f"  Average Complexity: {avg_complexity}")
    print(f"  Maintainability: {maintainability}")
    print(f"  Lines of Code: {raw_metrics.get('LOC', 0)}")
    print(f"  Logical Lines: {raw_metrics.get('LLOC', 0)}")
    print(f"  Comments: {raw_metrics.get('Comments', 0)}")
    
    return code_metrics

if __name__ == '__main__':
    # Default values
    file_path = 'app/routes/auth.py'
    metrics_json = 'metrics_non_dp.json'
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    if len(sys.argv) > 2:
        metrics_json = sys.argv[2]
    
    # Collect and save metrics
    collect_code_metrics(file_path, metrics_json)
