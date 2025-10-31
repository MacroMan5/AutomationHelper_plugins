# 🎣 Claude Code Hooks - Auto JSON Validation

## What This Does

This hook **automatically validates JSON files** every time you create or edit them with Claude Code. It runs the deployment readiness checklist without you having to ask!

## ✅ What Gets Checked

Every time you write or edit a `.json` file, the hook automatically validates:

1. **✓ JSON syntax valid** - Catches syntax errors immediately
2. **✓ Power Automate block format correct** - Verifies proper structure
3. **✓ All required fields present** - Ensures no missing data
4. **✓ runAfter chains valid** - No orphaned actions, no circular dependencies
5. **✓ Expressions correct (no duplicates)** - Catches duplicate expression bugs
6. **✓ No security vulnerabilities** - Scans for hardcoded credentials
7. **✓ Within API limits** - Action count and structure checks
8. **✓ No blocking issues** - Overall deployment readiness

## 🚀 How It Works

### Configuration (Already Set Up!)

The hook is configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$FILE_PATH\" == *.json ]] && ...; then python3 .claude/hooks/validate_json.py \"$FILE_PATH\"; fi",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### What Happens

1. **You write/edit a JSON file** → Claude uses Write or Edit tool
2. **Hook triggers automatically** → PostToolUse event fires
3. **Validation script runs** → Python script analyzes the file
4. **Results displayed** → Color-coded output shows status

### Example Output

When you create a flow JSON:

```
🔍 Auto-Validating JSON File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: fix_bloc.json

✓ JSON Syntax: Valid
✓ Power Automate Format: Detected
✓ Structure: Valid
✓ Expressions: Valid
✓ runAfter Chains: Valid
✓ Security: No issues detected
ℹ Total Actions: 20

📋 Deployment Readiness Checklist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ JSON syntax valid
✓ Power Automate block format correct
✓ All required fields present
✓ runAfter chains valid
✓ Expressions correct (no duplicates)
✓ No security vulnerabilities
✓ Actions defined

✅ READY TO DEPLOY
This JSON can be pasted into Power Automate!
```

## 📁 Files

```
.claude/
├── hooks/
│   ├── validate_json.py      # Python validation script
│   └── README.md              # This file
└── settings.local.json        # Hook configuration
```

## 🎛️ Customization

### Disable the Hook Temporarily

Edit `.claude/settings.local.json` and remove the `"hooks"` section, or use:

```json
{
  "disableAllHooks": true
}
```

### Change What Gets Validated

Edit `.claude/hooks/validate_json.py`:

- **Line 165-167**: Skip files (add to `skip_files` list)
- **Line 170**: File extension filter
- **Line 240-280**: Add/remove validation checks

### Adjust Timeout

In `.claude/settings.local.json`:

```json
{
  "timeout": 5  // Increase if validation takes longer
}
```

### Change Validation Strictness

The script exits with code 0 (non-blocking) by default, so issues are shown but don't prevent operations. To make it blocking:

```python
# In validate_json.py, line 350
sys.exit(1)  # Change from 0 to 1 to block on errors
```

## 🧪 Testing

### Test Manually

```bash
python3 .claude/hooks/validate_json.py your_flow.json
```

### Test with Good JSON

```bash
echo '{"test": "valid"}' > test.json
# Write or Edit the file with Claude
# Should see: ✓ General JSON validation: PASSED
```

### Test with Bad Power Automate JSON

```bash
# Create a file with duplicate expressions (like error_bloc.json had)
# Hook will automatically detect and show:
# ✗ Expressions correct (no duplicates)
```

## 🔧 Troubleshooting

### Hook Not Running

1. **Check configuration**: `cat .claude/settings.local.json | jq .hooks`
2. **Check script permissions**: `ls -la .claude/hooks/validate_json.py`
3. **Test manually**: `python3 .claude/hooks/validate_json.py test.json`

### Python Not Found

Install Python 3:
```bash
# Ubuntu/Debian
sudo apt install python3

# macOS
brew install python3
```

### Script Errors

Check Python version (needs 3.6+):
```bash
python3 --version
```

Run with debug output:
```bash
python3 -v .claude/hooks/validate_json.py test.json
```

## 🎨 Customizing Validation Rules

### Add New Check

Edit `validate_json.py` and add a function:

```python
def check_my_custom_rule(data):
    """Your custom validation"""
    issues = []
    # Your logic here
    return issues
```

Then call it in `main()`:

```python
custom_issues = check_my_custom_rule(data)
if custom_issues:
    print(f"{RED}✗ Custom Check:{RESET}")
    for issue in custom_issues:
        print(f"  • {issue}")
```

### Add to Checklist

Update the checklist in `main()`:

```python
checklist = [
    # ... existing checks ...
    (len(custom_issues) == 0, "My custom rule passes"),
]
```

## 💡 Tips

1. **Fast Feedback**: You get validation results immediately after creating/editing files
2. **Catch Bugs Early**: No need to paste into Power Automate to find syntax errors
3. **Team Consistency**: Everyone using the repo gets the same validation
4. **CI/CD Ready**: Use the script in pipelines:
   ```bash
   python3 .claude/hooks/validate_json.py flow.json || exit 1
   ```

## 🌟 Advanced: Hook Types

Claude Code supports multiple hook types:

- **PostToolUse** ← We use this
- **PreToolUse** - Run before tool execution
- **UserPromptSubmit** - Run when user sends a message
- **SessionStart** - Run at session start
- **Notification** - Custom notifications

### Example: Pre-validation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if the file about to be written contains any TODOs or placeholders. If yes, warn the user. Input: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

## 📚 References

- [Claude Code Hooks Documentation](https://docs.claude.com/claude-code/hooks)
- [Power Automate JSON Format](../../../Docs/PowerAutomateDocs/)
- [Validation Script Source](./ validate_json.py)

---

**Created**: 2025-10-31
**Last Updated**: 2025-10-31
**Tested With**: Claude Code v1.x, Python 3.8+
