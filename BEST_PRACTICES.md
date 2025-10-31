# Best Practices - How to Use This Plugin Effectively

⚠️ **This plugin has limitations.** Follow these practices to get the best results.

## The #1 Rule: Section Your Workflows

### ❌ What NOT to Do

**Don't paste huge workflows:**
```
You: "Fix this workflow [pastes 3000 lines of JSON]"

Result:
- Context overflow
- AI gets confused
- Misses important details
- Poor quality output
```

**Don't expect miracles:**
```
You: "Debug my entire complex workflow and fix everything"

Result:
- Too broad, unfocused
- Can't understand the full context
- May fix one thing, break another
```

### ✅ What TO Do

**Section your workflow into logical parts:**

```
You: "I have a SharePoint flow with 3 sections:
     1. Get items and filter (lines 50-150)
     2. Loop and process (lines 151-300) ← THIS IS FAILING
     3. Send notifications (lines 301-400)

     I'm getting 429 errors in section 2. Here's that section:
     [paste 150 lines of the loop section]

     It should filter CNESST items and extract dates."

Result:
✅ Focused analysis
✅ Better understanding
✅ Accurate fix
```

## Size Limits - Keep It Manageable

### Recommended Sizes

| What You're Debugging | Max Lines | Why |
|----------------------|-----------|-----|
| Single action error | 50-100 | Simple, focused |
| Loop/condition section | 150-200 | One logical unit |
| Multiple related actions | 200-300 | Connected operations |
| Full workflow | ❌ Don't | Too much context |

### How to Section a Large Flow

**Example: 1000-line workflow**

Instead of pasting everything, break it down:

```
Your workflow structure:
├── Trigger (lines 1-50)
├── Initialize variables (lines 51-100)
├── Get SharePoint items (lines 101-200)
├── Filter and loop ← ERROR HERE (lines 201-500)
├── Process each item (lines 501-800)
└── Send notifications (lines 801-1000)
```

**Debugging approach:**

1. **First request:** "I have an error in the filter/loop section (lines 201-500). Here's that part: [paste lines 201-500]"

2. **If needed:** "Now the loop works, but processing fails. Here's the process section: [paste lines 501-800]"

3. **Finally:** "Validate the whole flow structure" - now paste the full JSON

## Provide Context, Not Just JSON

### ❌ Bad Request

```
You: [pastes 200 lines of JSON]
```

**Why it's bad:**
- No context about what it should do
- No info about the error
- AI has to guess your intent

### ✅ Good Request

```
You: "I have a Power Automate flow that monitors SharePoint for new files.
     When a file is added, it should:
     1. Check if filename contains 'CNESST'
     2. Extract the date from filename
     3. Store in a variable

     It's failing at step 2 with this error:
     'Cannot access property Nom on primitive value'

     Here's the relevant section (the filter and loop):
     [paste 150 lines]

     The variable ListeDesDossier contains filenames like:
     ['CNESST 2025-01-15', 'INVALIDITÉ 2025-02-20']"

Result:
✅ AI understands the goal
✅ Knows the data structure
✅ Has the error context
✅ Can provide accurate fix
```

## Be Specific About What You Need

### ❌ Vague Requests

```
❌ "Optimize this"
❌ "Fix errors"
❌ "Make it better"
❌ "Debug this workflow"
```

### ✅ Specific Requests

```
✅ "Reduce API calls in this loop section"
✅ "Fix the 429 throttling error in SharePoint calls"
✅ "Add error handling to this HTTP action"
✅ "Debug why items('Loop')?['Nom'] returns null"
```

## One Problem at a Time

### ❌ Multiple Issues at Once

```
You: "This flow has:
     - 429 throttling errors
     - Wrong date format
     - Missing error handling
     - Performance issues
     - Validation problems

     Fix all of these [pastes 1000 lines]"

Result: Overwhelmed, poor results
```

### ✅ Sequential Problem Solving

```
Session 1:
You: "Fix the 429 throttling error in this loop [paste 100 lines]"
✅ Gets fixed

Session 2:
You: "Now fix the date format in this section [paste 80 lines]"
✅ Gets fixed

Session 3:
You: "Add error handling to these actions [paste 150 lines]"
✅ Gets fixed
```

## Understand the Documentation Limits

### What's Well Documented

✅ **Power Automate:**
- Forms (100%)
- Excel (100%)
- Outlook (100%)
- Teams (100%)
- Built-in actions (100%)

✅ **n8n:**
- Core nodes (basic)
- AI nodes (basic)

### What's NOT Well Documented

⚠️ **Power Automate:**
- SharePoint (20% - basic only)
- OneDrive (20% - basic only)

❌ **Not documented:**
- Make/Integromat
- Zapier
- Advanced n8n nodes

**What this means:**
- For well-documented connectors → Good results
- For poorly documented → Limited help
- For undocumented → Won't work well

## Realistic Expectations

### What This Plugin CAN Do

✅ Debug common errors (401, 403, 429)
✅ Suggest fixes based on documentation
✅ Generate basic workflow JSON
✅ Refactor simple sections for performance
✅ Validate syntax and basic best practices

### What This Plugin CANNOT Do

❌ Understand your entire business logic
❌ Fix complex multi-step workflows in one go
❌ Work miracles with 3000-line JSONs
❌ Debug undocumented connectors perfectly
❌ Read your mind about what data structure you're using

## Example: Good Workflow

### Scenario: Complex SharePoint Flow with Multiple Issues

**❌ Bad Approach:**
```
1. Paste entire 2000-line workflow
2. Say "fix everything"
3. Get confused output
4. Nothing works
```

**✅ Good Approach:**

**Request 1 - Throttling:**
```
You: "I'm getting 429 errors in this SharePoint loop.
     Here's the loop section (lines 200-350):
     [paste loop section]

     It processes about 500 items."

Result: Adds concurrency limits and delays
```

**Request 2 - Data Structure:**
```
You: "Now I'm getting 'Cannot access property' error.
     Here's the filter and loop (lines 200-450):
     [paste section]

     The filter shows: contains(item(), 'CNESST')
     But loop tries: items('Loop')?['Nom']

     Variable is array of strings like:
     ['CNESST 2025-01', 'INVALIDITÉ 2025-02']"

Result: Fixes property access on string primitives
```

**Request 3 - Error Handling:**
```
You: "Add error handling to this HTTP section:
     [paste 150 lines]

     If HTTP fails, I want to log and continue."

Result: Adds Scope with error handler
```

**Request 4 - Validation:**
```
You: "Validate the complete flow structure now"
     [paste full workflow - now it's context-aware from previous fixes]

Result: Final validation and polish
```

## Tips for Better Results

### 1. Use Clear Action Names

❌ `Compose`, `Compose_2`, `Compose_3`
✅ `Extract_Date_From_Filename`, `Validate_CNESST_Format`

**Why:** Clear names help AI understand your intent

### 2. Explain Your Data

❌ "This variable contains items"
✅ "Variable contains array of strings: ['CNESST 2025-01-15', 'INVALIDITÉ 2025-02-20']"

**Why:** AI needs to know data types to suggest correct fixes

### 3. Include the Error Message

❌ "It's not working"
✅ "Error: 'Cannot access property Nom on primitive value of type String'"

**Why:** Exact error messages are crucial for accurate diagnosis

### 4. Mention What Works

❌ "Everything is broken"
✅ "The filter works and returns correct items, but the loop assignment fails"

**Why:** Helps isolate the actual problem

### 5. Test Incrementally

After each fix:
1. Test it
2. Confirm it works
3. Move to next issue

Don't pile all fixes without testing.

## Common Mistakes

### Mistake 1: Kitchen Sink Approach
```
❌ Sending entire workflow + all errors + "fix everything"
✅ One section + one specific error + clear context
```

### Mistake 2: No Data Structure Info
```
❌ "items('Loop')?['Nom'] returns null, fix it"
✅ "items('Loop')?['Nom'] returns null.
    Loop iterates array from this filter: contains(item(), 'CNESST')
    So it's array of strings, not objects"
```

### Mistake 3: Expecting Perfection
```
❌ "Generate a perfect enterprise workflow for [complex requirements]"
✅ "Generate basic structure for SharePoint->Email workflow,
    I'll refine it"
```

### Mistake 4: Not Reading Limitations
```
❌ "Debug my Zapier workflow"
✅ Reads README, sees Zapier not supported, uses for PA/n8n instead
```

## When to Use Which Skill

### automation-debugger
**Use for:** Specific errors with error messages
**Size:** 100-300 lines of the failing section
**Provide:** Error message, data structure, what it should do

### automation-refactor
**Use for:** Optimizing a working section
**Size:** 150-300 lines of one logical section
**Provide:** Current behavior, what you want to improve

### automation-quick-fix
**Use for:** Common errors (401, 429)
**Size:** 50-150 lines around the error
**Provide:** Error code and connector name

### automation-validator
**Use for:** Final check before deployment
**Size:** Can handle larger workflows (but still not 3000 lines)
**Provide:** Full section or workflow to validate

### automation-build-flow
**Use for:** Generating new workflows
**Provide:** Clear requirements, step-by-step logic, examples

## Summary

### The Golden Rules

1. **Section your workflows** - max 200-300 lines per request
2. **Provide context** - explain what it should do
3. **Include data structure** - what types are your variables?
4. **One problem at a time** - don't pile issues
5. **Be specific** - "fix 429 error" not "fix everything"
6. **Test incrementally** - verify each fix before moving on
7. **Read the docs** - know what's supported
8. **Realistic expectations** - it's alpha, it has limits

### Remember

🎯 **This is an AI assistant, not a magic wand**

It works best when:
- You give it manageable chunks
- You provide clear context
- You have realistic expectations
- You test and iterate

It works poorly when:
- You dump 3000 lines of JSON
- You expect it to understand everything
- You don't provide context
- You're using unsupported platforms

---

**Follow these practices and you'll get much better results!** 🚀

Still have issues? Open a [Discussion](https://github.com/therouxe/automation-helper/discussions) with:
- What you tried
- What didn't work
- A focused example (not 3000 lines!)
