import json
import subprocess
import re
import sys
import os
import glob

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
    functions = []
    classes = []
    lines = output.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('F '):
            match = re.match(r'F\s+(\d+):(\d+)\s+(\w+)\s+-\s+([A-F])', line)
            if match:
                functions.append({
                    'line': int(match.group(1)),
                    'name': match.group(3),
                    'complexity_grade': match.group(4)
                })
        elif line.startswith('C '):
            match = re.match(r'C\s+(\d+):(\d+)\s+(\w+)\s+-\s+([A-F])', line)
            if match:
                classes.append({
                    'line': int(match.group(1)),
                    'name': match.group(3),
                    'complexity_grade': match.group(4)
                })
        elif line.startswith('M '):
            match = re.match(r'M\s+(\d+):(\d+)\s+(\w+)\.(\w+)\s+-\s+([A-F])', line)
            if match:
                functions.append({
                    'line': int(match.group(1)),
                    'class': match.group(3),
                    'name': match.group(4),
                    'complexity_grade': match.group(5)
                })
    
    return functions, classes

def parse_maintainability(output):
    """Parse maintainability index output"""
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
                
                try:
                    value = int(value)
                except ValueError:
                    pass
                
                metrics[key] = value
    
    return metrics

def calculate_average_complexity(items):
    """Calculate average complexity from grades"""
    grade_to_score = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6
    }
    
    if not items:
        return 'N/A'
    
    scores = [grade_to_score.get(item['complexity_grade'], 0) for item in items]
    avg_score = sum(scores) / len(scores)
    
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

def collect_code_metrics_for_pattern(pattern, metrics_json_path):
    """Collect code metrics for files matching pattern"""
    print(f"\nCollecting code metrics for pattern: {pattern}")
    print("="*60)
    
    # Find all matching files
    files = glob.glob(pattern, recursive=True)
    
    if not files:
        print(f"No files found matching pattern: {pattern}")
        return None
    
    all_functions = []
    all_classes = []
    total_loc = 0
    total_lloc = 0
    total_sloc = 0
    total_comments = 0
    total_blank = 0
    file_metrics = []
    
    for file_path in files:
        print(f"\nAnalyzing: {file_path}")
        
        cc_output = run_radon_command(f"radon cc {file_path} -a")
        mi_output = run_radon_command(f"radon mi {file_path}")
        raw_output = run_radon_command(f"radon raw {file_path}")
        
        functions, classes = parse_complexity(cc_output)
        maintainability = parse_maintainability(mi_output)
        raw_metrics = parse_raw_metrics(raw_output)
        
        all_functions.extend(functions)
        all_classes.extend(classes)
        
        loc = raw_metrics.get('LOC', 0)
        total_loc += loc
        total_lloc += raw_metrics.get('LLOC', 0)
        total_sloc += raw_metrics.get('SLOC', 0)
        total_comments += raw_metrics.get('Comments', 0)
        total_blank += raw_metrics.get('Blank', 0)
        
        file_metrics.append({
            'file': file_path,
            'loc': loc,
            'maintainability': maintainability,
            'functions': len(functions),
            'classes': len(classes)
        })
    
    avg_complexity_funcs = calculate_average_complexity(all_functions)
    avg_complexity_classes = calculate_average_complexity(all_classes)
    
    code_metrics = {
        'pattern': pattern,
        'total_files': len(files),
        'files_analyzed': file_metrics,
        'cyclomatic_complexity': {
            'average_grade_functions': avg_complexity_funcs,
            'average_grade_classes': avg_complexity_classes,
            'total_functions': len(all_functions),
            'total_classes': len(all_classes),
            'functions': all_functions,
            'classes': all_classes
        },
        'raw_metrics': {
            'LOC': total_loc,
            'LLOC': total_lloc,
            'SLOC': total_sloc,
            'Comments': total_comments,
            'Blank': total_blank
        },
        'summary': {
            'total_files': len(files),
            'total_classes': len(all_classes),
            'total_functions': len(all_functions),
            'lines_of_code': total_loc,
            'logical_lines': total_lloc,
            'source_lines': total_sloc,
            'comments': total_comments,
            'blank_lines': total_blank
        }
    }
    
    # Load existing metrics
    try:
        with open(metrics_json_path, 'r') as f:
            metrics = json.load(f)
    except FileNotFoundError:
        print(f"\nWarning: {metrics_json_path} not found. Creating new file.")
        metrics = {
            'implementation': 'dp',
            'timestamp': 0,
            'performance': {},
            'database': {},
            'detailed_metrics': []
        }
    
    metrics['code_metrics'] = code_metrics
    
    with open(metrics_json_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("\n" + "="*60)
    print(f"Code metrics saved to {metrics_json_path}")
    print("="*60)
    
    print("\nCode Metrics Summary:")
    print(f"  Files analyzed: {len(files)}")
    print(f"  Total Classes: {len(all_classes)}")
    print(f"  Total Functions/Methods: {len(all_functions)}")
    print(f"  Average Complexity (Functions): {avg_complexity_funcs}")
    print(f"  Average Complexity (Classes): {avg_complexity_classes}")
    print(f"  Total Lines of Code: {total_loc}")
    print(f"  Logical Lines: {total_lloc}")
    print(f"  Comments: {total_comments}")
    
    return code_metrics

if __name__ == '__main__':
    # For DP implementation, analyze all auth-related files
    pattern = 'app/routes/auth.py'  # Default for non-DP
    metrics_json = 'metrics_dp.json'
    
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    if len(sys.argv) > 2:
        metrics_json = sys.argv[2]
    
    collect_code_metrics_for_pattern(pattern, metrics_json)
    
    print("\nDone! Run 'python analyze_metrics.py' to compare implementations.")
