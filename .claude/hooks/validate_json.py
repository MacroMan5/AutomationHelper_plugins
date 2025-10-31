#!/usr/bin/env python3
"""
Auto-validator for Power Automate JSON files
Triggered by post_tool_use hook on Write/Edit operations
"""

import json
import sys
import re
from pathlib import Path

# ANSI color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def validate_json_syntax(file_path):
    """Validate JSON syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def check_power_automate_structure(data):
    """Check if JSON is Power Automate block format"""
    issues = []
    warnings = []

    # Check if it's a Power Automate block (nodeId + serializedValue)
    is_pa_block = 'nodeId' in data and 'serializedValue' in data

    if is_pa_block:
        # Validate block structure
        if 'type' not in data.get('serializedValue', {}):
            issues.append("Missing 'type' in serializedValue")

        if 'actions' not in data.get('serializedValue', {}):
            issues.append("Missing 'actions' in serializedValue")

        # Check for proper connection data
        if 'allConnectionData' not in data:
            warnings.append("Missing 'allConnectionData' - connections may need reconfiguration")

        return True, issues, warnings

    # Check if it's a full Power Automate flow definition
    if 'definition' in data:
        definition = data['definition']

        if 'triggers' not in definition:
            issues.append("Missing 'triggers' in definition")

        if 'actions' not in definition:
            issues.append("Missing 'actions' in definition")

        return True, issues, warnings

    # Not a Power Automate format
    return False, [], []

def validate_expressions(data, path=""):
    """Recursively validate Power Automate expressions"""
    issues = []

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            # Check for duplicate expressions in 'inputs' field
            if key == 'inputs' and isinstance(value, str):
                # Look for duplicate function calls
                if value.count('@int(') > 1 or value.count('@substring(') > 1:
                    issues.append(f"Possible duplicate expression in {current_path}")

                # Check for missing @ prefix
                function_pattern = r'\b(int|substring|contains|formatDateTime|outputs|variables|body|items|first|last|split|length|equals|and|or|if)\s*\('
                matches = re.finditer(function_pattern, value)
                for match in matches:
                    start = match.start()
                    if start > 0 and value[start-1] != '@':
                        issues.append(f"Expression missing @ prefix in {current_path}: {match.group()}")

            # Recurse into nested structures
            issues.extend(validate_expressions(value, current_path))

    elif isinstance(data, list):
        for i, item in enumerate(data):
            issues.extend(validate_expressions(item, f"{path}[{i}]"))

    return issues

def validate_runafter_chains(data):
    """Validate runAfter chains in Power Automate actions"""
    issues = []

    # Extract actions
    actions = None
    if 'serializedValue' in data and 'actions' in data['serializedValue']:
        actions = data['serializedValue']['actions']
    elif 'definition' in data and 'actions' in data['definition']:
        actions = data['definition']['actions']

    if not actions:
        return []

    action_names = set(actions.keys())

    for action_name, action_data in actions.items():
        if 'runAfter' in action_data:
            run_after = action_data['runAfter']

            # Check if referenced actions exist
            for ref_action in run_after.keys():
                if ref_action not in action_names:
                    issues.append(f"Action '{action_name}' references non-existent action '{ref_action}' in runAfter")

            # Check for valid status values
            for ref_action, statuses in run_after.items():
                valid_statuses = ['Succeeded', 'Failed', 'Skipped', 'TimedOut', 'SUCCEEDED', 'FAILED', 'SKIPPED', 'TIMEDOUT']
                for status in statuses:
                    if status not in valid_statuses:
                        issues.append(f"Invalid runAfter status '{status}' in action '{action_name}'")

    return issues

def check_security(data):
    """Check for security issues"""
    issues = []
    data_str = json.dumps(data)

    # Check for hardcoded credentials patterns
    patterns = [
        (r'"password"\s*:\s*"[^@]', "Possible hardcoded password"),
        (r'"apiKey"\s*:\s*"[^@]', "Possible hardcoded API key"),
        (r'"secret"\s*:\s*"[^@]', "Possible hardcoded secret"),
        (r'"connectionString"\s*:\s*"[^@]', "Possible hardcoded connection string"),
    ]

    for pattern, message in patterns:
        if re.search(pattern, data_str, re.IGNORECASE):
            issues.append(message)

    return issues

def count_actions(data):
    """Count total actions in flow"""
    def count_recursive(obj):
        if isinstance(obj, dict):
            count = 0
            if 'type' in obj and obj['type'] in ['Compose', 'If', 'Foreach', 'Scope', 'SetVariable', 'Query', 'Select', 'OpenApiConnection', 'Terminate']:
                count = 1
            for value in obj.values():
                count += count_recursive(value)
            return count
        elif isinstance(obj, list):
            return sum(count_recursive(item) for item in obj)
        return 0

    return count_recursive(data)

def main():
    if len(sys.argv) < 2:
        print(f"{RED}Error: No file path provided{RESET}")
        sys.exit(1)

    file_path = sys.argv[1]

    # Only validate .json files
    if not file_path.endswith('.json'):
        sys.exit(0)  # Silent exit for non-JSON files

    # Skip validation for certain files
    skip_files = ['package.json', 'tsconfig.json', 'settings.json', 'launch.json']
    if any(skip in file_path for skip in skip_files):
        sys.exit(0)

    print(f"\n{BLUE}{BOLD}🔍 Auto-Validating JSON File{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
    print(f"File: {file_path}\n")

    # 1. Validate JSON syntax
    is_valid, error = validate_json_syntax(file_path)
    if not is_valid:
        print(f"{RED}✗ JSON Syntax: INVALID{RESET}")
        print(f"  {error}\n")
        sys.exit(1)

    print(f"{GREEN}✓ JSON Syntax: Valid{RESET}")

    # Load JSON data
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Check if Power Automate format
    is_pa, structure_issues, structure_warnings = check_power_automate_structure(data)

    if not is_pa:
        print(f"{YELLOW}ℹ Not a Power Automate flow file{RESET}")
        print(f"{GREEN}✓ General JSON validation: PASSED{RESET}\n")
        sys.exit(0)

    print(f"{GREEN}✓ Power Automate Format: Detected{RESET}")

    # 3. Validate structure
    if structure_issues:
        print(f"{RED}✗ Structure Issues:{RESET}")
        for issue in structure_issues:
            print(f"  • {issue}")
        print()
    else:
        print(f"{GREEN}✓ Structure: Valid{RESET}")

    if structure_warnings:
        print(f"{YELLOW}⚠ Structure Warnings:{RESET}")
        for warning in structure_warnings:
            print(f"  • {warning}")
        print()

    # 4. Validate expressions
    expression_issues = validate_expressions(data)
    if expression_issues:
        print(f"{RED}✗ Expression Issues:{RESET}")
        for issue in expression_issues[:5]:  # Show first 5
            print(f"  • {issue}")
        if len(expression_issues) > 5:
            print(f"  ... and {len(expression_issues) - 5} more")
        print()
    else:
        print(f"{GREEN}✓ Expressions: Valid{RESET}")

    # 5. Validate runAfter chains
    runafter_issues = validate_runafter_chains(data)
    if runafter_issues:
        print(f"{RED}✗ runAfter Chain Issues:{RESET}")
        for issue in runafter_issues:
            print(f"  • {issue}")
        print()
    else:
        print(f"{GREEN}✓ runAfter Chains: Valid{RESET}")

    # 6. Security check
    security_issues = check_security(data)
    if security_issues:
        print(f"{RED}✗ Security Issues:{RESET}")
        for issue in security_issues:
            print(f"  • {issue}")
        print()
    else:
        print(f"{GREEN}✓ Security: No issues detected{RESET}")

    # Count actions
    action_count = count_actions(data)
    print(f"{BLUE}ℹ Total Actions: {action_count}{RESET}")

    # Summary
    print(f"\n{BLUE}{BOLD}📋 Deployment Readiness Checklist{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")

    checklist = [
        (is_valid, "JSON syntax valid"),
        (is_pa, "Power Automate block format correct"),
        (len(structure_issues) == 0, "All required fields present"),
        (len(runafter_issues) == 0, "runAfter chains valid"),
        (len(expression_issues) == 0, "Expressions correct (no duplicates)"),
        (len(security_issues) == 0, "No security vulnerabilities"),
        (action_count > 0, "Actions defined"),
    ]

    all_passed = all(passed for passed, _ in checklist)

    for passed, item in checklist:
        symbol = "✓" if passed else "✗"
        color = GREEN if passed else RED
        print(f"{color}{symbol}{RESET} {item}")

    print()

    if all_passed:
        print(f"{GREEN}{BOLD}✅ READY TO DEPLOY{RESET}")
        print(f"{GREEN}This JSON can be pasted into Power Automate!{RESET}\n")
        sys.exit(0)
    else:
        total_issues = len(structure_issues) + len(expression_issues) + len(runafter_issues) + len(security_issues)
        print(f"{YELLOW}{BOLD}⚠️  NEEDS ATTENTION{RESET}")
        print(f"{YELLOW}Found {total_issues} issue(s) that should be reviewed.{RESET}\n")
        sys.exit(0)  # Exit 0 to not block the operation

if __name__ == "__main__":
    main()
