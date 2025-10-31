# Complete Debugger Skill Example

This document demonstrates the complete workflow of the power-automate-debugger skill from input to output.

## Example Scenario: SharePoint Throttling Error

### User Input

User provides `erreur_bloc.json`:

```json
{
  "error": {
    "code": "429",
    "message": "Status code: 429, TooManyRequests - The request was throttled. Please retry after some time."
  },
  "failedAction": "Get_items",
  "flowDefinition": {
    "definition": {
      "triggers": {
        "manual": {
          "type": "Request",
          "kind": "Button",
          "inputs": {}
        }
      },
      "actions": {
        "Apply_to_each": {
          "type": "Foreach",
          "foreach": "@range(0, 100)",
          "actions": {
            "Get_items": {
              "type": "ApiConnection",
              "inputs": {
                "host": {
                  "connectionName": "shared_sharepointonline",
                  "operationId": "GetItems",
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
                },
                "parameters": {
                  "dataset": "https://contoso.sharepoint.com/sites/ProjectSite",
                  "table": "d8a0e3c2-4f61-4b89-9012-f3a8c5d6e7b9"
                }
              },
              "runAfter": {}
            }
          },
          "runAfter": {}
        }
      }
    }
  }
}
```

User message: "Debug this erreur_bloc.json - my SharePoint flow keeps failing"

---

## Skill Execution Workflow

### Phase 1: Error Analysis

**Skill identifies**:
- Error Code: 429
- Error Type: Throttling
- Failing Action: "Get_items" (SharePoint Get Items)
- Connector: SharePoint
- Context: Inside Apply to each loop with 100 iterations
- No delay between calls

**Classification**: Throttling error due to exceeding SharePoint API limits

---

### Phase 2: Documentation Research

**Skill launches Task tool with Explore agent**:

```
Task tool call:
subagent_type: "Explore"
thoroughness: "very thorough"
prompt: "Research Power Automate documentation for throttling error in SharePoint connector, specifically the GetItems action.

Search in PowerAutomateDocs/ for:
1. Connector overview (PowerAutomateDocs/SharePoint/overview.md) - find API limits
2. Action documentation (PowerAutomateDocs/SharePoint/actions.md) - find GetItems specifics
3. Control flow docs (PowerAutomateDocs/BuiltIn/control.md) - find Apply to each concurrency

Focus on finding:
- SharePoint API call limits
- Recommended delays between calls
- Concurrency settings for Apply to each
- Throttling mitigation strategies

Return specific file paths, section names, and exact limitations found."
```

**Research Agent Returns**:

```
Found in PowerAutomateDocs/SharePoint/overview.md:

Section: "API and Request Limits"
- SharePoint Online connector: 600 API calls per 60 seconds per connection
- Throttling occurs when limit exceeded
- Recommended: Implement delays and reduce concurrency

Found in PowerAutomateDocs/BuiltIn/control.md:

Section: "Apply to each"
- Default concurrency: 50 parallel iterations
- Can be reduced: "concurrency": { "repetitions": 1 }
- Recommendation: Set to 1 for API-heavy operations

Section: "Delay"
- Use "Wait" action type
- Intervals: seconds, minutes, hours
- Example: 1-2 second delay between API calls
```

---

### Phase 3: Solution Design

**Based on research, skill designs solution**:

**Root Cause**:
- Loop makes 100 rapid SharePoint API calls
- Default concurrency of 50 parallel iterations
- No delays between calls
- Exceeds 600 calls/60 seconds limit

**Solution Strategy**:
1. Reduce concurrency to 1 (sequential processing)
2. Add 1-second delay between iterations
3. Wrap in error handling scope
4. Add retry logic for remaining throttled requests

**Validation**:
- With 1-second delays: Max 60 calls per minute
- Well under 600 calls/60 seconds limit
- Sequential processing prevents burst
- Error handling catches any remaining throttling

---

### Phase 4: Fix Generation

**Skill launches Task tool with flow-builder agent**:

```
Task tool call:
subagent_type: "general-purpose"
prompt: "Generate complete fix_bloc.json for Power Automate flow with the following requirements:

Original Error: SharePoint throttling (429) in Get Items action within Apply to each loop
Root Cause: 100 rapid API calls with 50 concurrent iterations exceeding 600 calls/60 seconds limit
Required Fixes:
1. Reduce Apply to each concurrency to 1 (sequential)
2. Add 1-second delay after each Get Items call
3. Wrap in Scope for error handling
4. Add catch action for any remaining throttling errors

Create a complete, valid Power Automate flow JSON following PowerAutomateDocs/power-automate-json-format.md that:
- Maintains the manual trigger
- Processes 100 iterations sequentially with 1-second delays
- Includes proper GUIDs for all actions
- Has complete error handling structure
- Is ready for copy-paste into Power Automate

Return ONLY the complete JSON with no placeholders."
```

**Flow-Builder Agent Returns**: Complete valid JSON (shown in output below)

---

### Phase 5: Structured Output

**Skill generates final output using template**:

```xml
<debug_report>

<error_analysis>
**Error Type**: Throttling

**Failing Action/Trigger**: Get_items (SharePoint Get Items action)

**Error Message**:
```
Status code: 429, TooManyRequests - The request was throttled. Please retry after some time.
```

**Impact**: Flow fails when processing multiple SharePoint list items due to API rate limit exceeded. The Apply to each loop attempts 100 API calls in rapid succession, exceeding SharePoint's 600 calls per 60 seconds limit.
</error_analysis>

<root_cause>
**Primary Cause**: SharePoint API rate limit exceeded due to high-concurrency loop without throttling mitigation

**Documentation Reference**:
- File: `PowerAutomateDocs/SharePoint/overview.md`
- Section: "API and Request Limits"
- Key Limitation: "SharePoint Online connector enforces 600 API calls per 60 seconds per connection"

**Technical Details**:
- The Apply to each loop has default concurrency of 50 parallel iterations
- 100 Get Items calls attempted simultaneously without delays
- Each Get Items call counts toward the 600/60s limit
- Burst of parallel calls triggers throttling response (429)
- No retry logic to handle transient throttling

**Contributing Factors**:
- File: `PowerAutomateDocs/BuiltIn/control.md`
- Section: "Apply to each - Concurrency Control"
- Default: 50 concurrent iterations (too high for API operations)
- Recommendation: Set to 1 for API-heavy operations
</root_cause>

<solution>
## Recommended Fix

**Approach**: Reduce concurrency to sequential processing with delays between API calls

### Step-by-Step Implementation

1. **Reduce Apply to each Concurrency**
   - Modify: `runtimeConfiguration.concurrency.repetitions`
   - From: `50` (default)
   - To: `1` (sequential)
   - Reason: Prevents burst of parallel API calls that trigger throttling

2. **Add Delay After Each API Call**
   - Add: New "Wait" action after Get_items
   - Duration: 1 second
   - Purpose: Ensures maximum 60 calls per minute (well under 600/60s limit)
   - Documentation: `PowerAutomateDocs/BuiltIn/control.md` - Delay section

3. **Wrap in Error Handling Scope**
   - Add: Scope action wrapping the loop
   - Purpose: Catches any remaining throttling errors
   - Benefit: Graceful failure handling with logging

4. **Add Throttling Error Handler**
   - Add: Action configured to run after Scope fails
   - Purpose: Logs throttling events for monitoring
   - Alternative: Could implement retry logic for complete automation

### Additional Improvements

- **Error Handling**: Scope with "Configure run after" to catch failures
- **Performance**: With 1-second delays, processes 60 items/minute (stable rate)
- **Reliability**: Sequential processing eliminates race conditions
- **Monitoring**: Error handler provides visibility into throttling events

### Validation Checklist

- [x] Concurrency reduced to 1 (sequential processing)
- [x] 1-second delay added between iterations
- [x] API calls rate: ~60/minute (under 600/60s limit)
- [x] Error handling scope implemented
- [x] Throttling catch action added
- [x] All GUIDs valid and unique
- [x] runAfter dependencies correct
- [x] JSON syntax valid
</solution>

<fixed_json>
## Complete Fixed JSON

**Instructions**: Copy the entire JSON block below and paste directly into Power Automate using "Paste code" feature.

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "$connections": {
        "defaultValue": {},
        "type": "Object"
      }
    },
    "triggers": {
      "manual": {
        "type": "Request",
        "kind": "Button",
        "inputs": {
          "schema": {
            "type": "object",
            "properties": {}
          }
        }
      }
    },
    "actions": {
      "Scope_Process_Items": {
        "type": "Scope",
        "actions": {
          "Apply_to_each": {
            "type": "Foreach",
            "foreach": "@range(0, 100)",
            "runtimeConfiguration": {
              "concurrency": {
                "repetitions": 1
              }
            },
            "actions": {
              "Get_items": {
                "type": "ApiConnection",
                "inputs": {
                  "host": {
                    "connectionName": "shared_sharepointonline",
                    "operationId": "GetItems",
                    "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
                  },
                  "parameters": {
                    "dataset": "https://contoso.sharepoint.com/sites/ProjectSite",
                    "table": "d8a0e3c2-4f61-4b89-9012-f3a8c5d6e7b9"
                  }
                },
                "runAfter": {},
                "metadata": {
                  "operationMetadataId": "a1b2c3d4-e5f6-4a8b-9c0d-1e2f3a4b5c6d"
                }
              },
              "Delay_Between_Calls": {
                "type": "Wait",
                "inputs": {
                  "interval": {
                    "count": 1,
                    "unit": "Second"
                  }
                },
                "runAfter": {
                  "Get_items": [
                    "Succeeded"
                  ]
                },
                "metadata": {
                  "operationMetadataId": "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"
                }
              }
            },
            "runAfter": {},
            "metadata": {
              "operationMetadataId": "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f"
            }
          }
        },
        "runAfter": {},
        "metadata": {
          "operationMetadataId": "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a"
        }
      },
      "Handle_Throttling_Error": {
        "type": "Compose",
        "inputs": {
          "status": "Throttling error encountered",
          "message": "Some items may not have been processed due to API limits",
          "recommendation": "Review flow run history for details",
          "timestamp": "@utcNow()"
        },
        "runAfter": {
          "Scope_Process_Items": [
            "Failed",
            "TimedOut"
          ]
        },
        "metadata": {
          "operationMetadataId": "e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b"
        }
      }
    },
    "outputs": {}
  },
  "schemaVersion": "1.0.0.0"
}
```

**Changes Applied**:
1. **Concurrency Reduced**: Added `runtimeConfiguration.concurrency.repetitions: 1` to Apply_to_each
2. **Delay Added**: New "Delay_Between_Calls" action with 1-second wait after each Get_items
3. **Error Scope**: Wrapped loop in "Scope_Process_Items" for structured error handling
4. **Throttling Handler**: Added "Handle_Throttling_Error" Compose action with helpful error message
5. **Metadata GUIDs**: All actions have unique operationMetadataId values
6. **runAfter Dependencies**: Proper sequential execution configured

**Configuration Notes**:
- After pasting, verify SharePoint connection is configured
- Confirm site URL and list ID match your environment
- Test with smaller range (e.g., `range(0, 10)`) before full run
- Monitor first execution to confirm throttling resolved
- Can reduce delay to 0.5 seconds if processing speed needed (still safe under limits)
</fixed_json>

<alternative_approaches>
## Alternative Solutions

### Alternative 1: Batch Processing
**When to use**: Need faster processing while respecting limits
**Pros**:
- Processes items faster (groups of 10 with delays)
- Still respects API limits
**Cons**:
- More complex to implement
- Requires additional scope for batch logic
**Implementation**:
1. Use nested Apply to each
2. Outer loop chunks items into batches of 10
3. Inner loop processes batch with concurrency 10
4. Add 10-second delay between batches

### Alternative 2: Scheduled Batch Flow
**When to use**: Not time-sensitive, large volume of items
**Pros**:
- Eliminates throttling entirely
- Processes all items reliably
**Cons**:
- Not real-time
- Requires separate tracking of processed items
**Implementation**:
1. Change to scheduled trigger (every 15 minutes)
2. Get only unprocessed items (filtered query)
3. Process up to 600 items per run
4. Mark items as processed

### Alternative 3: Multiple Connections
**When to use**: Extremely high volume requirements
**Pros**:
- Multiplies rate limit (600 per connection)
- Faster processing
**Cons**:
- Requires multiple SharePoint connections
- More complex configuration
- Higher licensing considerations
**Implementation**:
1. Create multiple SharePoint connections
2. Distribute items across connections (modulo operation)
3. Process each subset with separate Apply to each
4. Merge results
</alternative_approaches>

<prevention>
## Preventing Similar Errors

**Best Practices**:
1. **Always set concurrency** for API-heavy Apply to each loops
   - Default 50 concurrent is too high for most API operations
   - Use 1 for critical operations, 5-10 for less strict APIs

2. **Add delays proactively** when making repeated API calls
   - 1-second delay for SharePoint (600/min limit)
   - 3-second delay for OneDrive (100/min limit)
   - Check connector documentation for specific limits

3. **Implement error handling** for all API interactions
   - Use Scope actions with "Configure run after"
   - Log throttling events for monitoring
   - Consider retry logic for transient failures

**Monitoring**:
- Watch for: 429 status codes in flow run history
- Metrics to track:
  - Number of API calls per flow run
  - Average flow duration (sudden increases indicate throttling)
  - Failure rate over time
- Regular checks:
  - Review flow analytics weekly
  - Adjust delays if approaching limits
  - Optimize queries to reduce API calls

**Design Guidelines**:
- **Filter at source**: Use $filter in Get Items to reduce results
- **Properties-only**: Use "Get Items (properties only)" when content not needed
- **Batch operations**: Group operations when connector supports it
- **Cache data**: Store frequently accessed data in variables
- **Parallel flows**: Distribute load across multiple flows if appropriate

</prevention>

</debug_report>
```

---

## Key Success Factors

### Documentation Research
- Research agent found exact API limit (600/60s)
- Identified specific sections in PowerAutomateDocs/
- Referenced control flow documentation for concurrency

### Solution Quality
- Addresses root cause (high concurrency)
- Implements proven pattern (sequential + delays)
- Adds comprehensive error handling
- Provides monitoring capability

### JSON Completeness
- Flow-builder agent generated valid JSON
- All GUIDs unique and properly formatted
- runAfter dependencies correct
- Ready for immediate paste into Power Automate
- No placeholders or TODOs

### User Experience
- Clear explanation of problem
- Step-by-step fix instructions
- Multiple alternative approaches
- Prevention guidance for future
- Complete working solution

---

## Verification

After user pastes the JSON:

1. **Immediate checks**:
   - [ ] JSON accepted by Power Automate (no syntax errors)
   - [ ] All connections show properly
   - [ ] Actions display correctly in designer

2. **Configuration**:
   - [ ] SharePoint connection authenticated
   - [ ] Site URL and List ID correct for environment
   - [ ] Test with small range first (range(0, 5))

3. **Test run**:
   - [ ] Flow completes without 429 errors
   - [ ] Items processed sequentially (check run history)
   - [ ] Delays visible in action history (~1 second between calls)
   - [ ] Total run time reasonable (~100 seconds for 100 items)

4. **Production readiness**:
   - [ ] Scale up to full range if test successful
   - [ ] Monitor first few runs
   - [ ] Confirm no throttling in analytics
   - [ ] Document configuration for team

---

This example demonstrates the complete capability of the power-automate-debugger skill to transform an error report into a production-ready solution.
