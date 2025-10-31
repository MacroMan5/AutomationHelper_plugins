# Power Automate Error Patterns Reference

Quick reference guide for common Power Automate error patterns and their solutions.

## Authentication Errors (401/403)

### Pattern Recognition
- Status codes: 401, 403
- Error messages containing: "unauthorized", "forbidden", "access denied", "authentication failed"
- Common in: SharePoint, OneDrive, HTTP with authentication

### Research Targets
```
PowerAutomateDocs/{Connector}/overview.md → Authentication section
PowerAutomateDocs/{Connector}/actions.md → Permission requirements
```

### Common Root Causes
1. **Expired or invalid credentials**
   - Connection needs re-authentication
   - Credentials rotated but connection not updated

2. **Insufficient permissions**
   - Service account lacks required permissions
   - SharePoint: Need "Edit" or "Full Control" on list
   - OneDrive: Need appropriate file/folder permissions

3. **Conditional access policies**
   - Azure AD policies blocking service accounts
   - MFA requirements not met
   - Location-based restrictions

### Fix Patterns
```json
{
  "actions": {
    "Scope_Error_Handling": {
      "type": "Scope",
      "actions": {
        "Get_Items": {
          // Original action
        }
      },
      "runAfter": {}
    },
    "Catch_Auth_Error": {
      "type": "Compose",
      "inputs": "Authentication failed - verify connection permissions",
      "runAfter": {
        "Scope_Error_Handling": ["Failed", "TimedOut"]
      }
    }
  }
}
```

## Throttling Errors (429)

### Pattern Recognition
- Status code: 429
- Error messages: "TooManyRequests", "throttled", "rate limit exceeded"
- Common in: SharePoint (600/min), OneDrive (100/min), HTTP APIs

### Research Targets
```
PowerAutomateDocs/{Connector}/overview.md → API Limits section
PowerAutomateDocs/BuiltIn/control.md → Delay actions
```

### Connector-Specific Limits
| Connector | Limit | Per |
|-----------|-------|-----|
| SharePoint | 600 calls | 60 seconds per connection |
| OneDrive | 100 calls | 60 seconds per connection |
| HTTP | 600 calls | 60 seconds (default) |
| Apply to each | 50 iterations | Concurrent (default) |

### Fix Patterns

**1. Add Delays Between Calls**
```json
{
  "actions": {
    "Delay": {
      "type": "Wait",
      "inputs": {
        "interval": {
          "count": 1,
          "unit": "Second"
        }
      },
      "runAfter": {
        "Previous_Action": ["Succeeded"]
      }
    }
  }
}
```

**2. Implement Exponential Backoff**
```json
{
  "actions": {
    "Do_Until_Success": {
      "type": "Until",
      "expression": "@equals(variables('Success'), true)",
      "limit": {
        "count": 5,
        "timeout": "PT1H"
      },
      "actions": {
        "Try_Action": {
          "type": "ApiConnection",
          "inputs": { /* action config */ }
        },
        "Check_Status": {
          "type": "If",
          "expression": {
            "and": [
              {
                "equals": [
                  "@outputs('Try_Action')['statusCode']",
                  429
                ]
              }
            ]
          },
          "actions": {
            "Wait_Exponential": {
              "type": "Wait",
              "inputs": {
                "interval": {
                  "count": "@mul(2, variables('RetryCount'))",
                  "unit": "Second"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**3. Reduce Concurrent Iterations**
```json
{
  "Apply_to_each": {
    "type": "Foreach",
    "foreach": "@body('Get_Items')",
    "runtimeConfiguration": {
      "concurrency": {
        "repetitions": 1
      }
    },
    "actions": { /* ... */ }
  }
}
```

## Data Format Errors

### Pattern Recognition
- Error messages: "InvalidTemplate", "Unable to process template", "cannot be evaluated", "property doesn't exist"
- Common in: Parse JSON, Compose, expressions with dynamic content

### Research Targets
```
PowerAutomateDocs/BuiltIn/data-operation.md → Parse JSON section
PowerAutomateDocs/BuiltIn/data-operation.md → Compose section
```

### Common Root Causes

1. **Missing Parse JSON Schema**
   - Dynamic content not available without schema
   - Schema doesn't match actual data structure

2. **Incorrect Expression Syntax**
   - Invalid Power Automate expression functions
   - Wrong property paths in JSON
   - Type mismatches (string vs number vs array)

3. **Null/Undefined Values**
   - Expressions trying to access null properties
   - Missing optional fields

### Fix Patterns

**1. Add Parse JSON with Proper Schema**
```json
{
  "Parse_JSON": {
    "type": "ParseJson",
    "inputs": {
      "content": "@body('HTTP')",
      "schema": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "items": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "value": {
                  "type": "string"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**2. Add Null Checks in Expressions**
```json
{
  "Compose_Safe": {
    "type": "Compose",
    "inputs": "@if(not(empty(body('Parse_JSON')?['property'])), body('Parse_JSON')['property'], 'default_value')"
  }
}
```

**3. Use Proper Type Conversions**
```json
{
  "Convert_To_String": {
    "type": "Compose",
    "inputs": "@string(variables('NumberValue'))"
  },
  "Convert_To_Int": {
    "type": "Compose",
    "inputs": "@int(variables('StringValue'))"
  }
}
```

## Timeout Errors

### Pattern Recognition
- Error messages: "timeout", "timed out", "operation took too long"
- Common in: Large file operations, long-running HTTP calls, Do until loops

### Research Targets
```
PowerAutomateDocs/{Connector}/overview.md → Known Limitations
PowerAutomateDocs/BuiltIn/control.md → Do until limits
```

### Connector-Specific Limits
| Operation | Timeout |
|-----------|---------|
| OneDrive file triggers | 50MB max file size |
| SharePoint attachments | 90MB max size |
| HTTP actions | 2 minutes default |
| Do until loops | No default (must set) |

### Fix Patterns

**1. Add Timeout Configuration**
```json
{
  "Do_Until": {
    "type": "Until",
    "expression": "@equals(variables('Complete'), true)",
    "limit": {
      "count": 60,
      "timeout": "PT1H"
    },
    "actions": { /* ... */ }
  }
}
```

**2. Implement Chunking for Large Operations**
```json
{
  "Apply_to_each_Batch": {
    "type": "Foreach",
    "foreach": "@chunk(body('Get_Items'), 100)",
    "actions": {
      "Process_Batch": {
        "type": "Scope",
        "actions": { /* Process smaller batch */ }
      }
    }
  }
}
```

**3. Add File Size Check**
```json
{
  "Check_File_Size": {
    "type": "If",
    "expression": {
      "and": [
        {
          "lessOrEquals": [
            "@triggerBody()?['Size']",
            52428800
          ]
        }
      ]
    },
    "actions": {
      "Process_File": { /* ... */ }
    },
    "else": {
      "actions": {
        "Handle_Large_File": { /* Alternative approach */ }
      }
    }
  }
}
```

## Not Found Errors (404)

### Pattern Recognition
- Status code: 404
- Error messages: "not found", "does not exist", "cannot find"
- Common in: SharePoint Get Item, OneDrive Get File Content, HTTP calls

### Research Targets
```
PowerAutomateDocs/{Connector}/actions.md → Specific action requirements
PowerAutomateDocs/{Connector}/overview.md → Naming conventions
```

### Common Root Causes

1. **Incorrect Resource Paths/IDs**
   - Hardcoded IDs that don't exist
   - Wrong site URLs
   - Invalid file paths

2. **Permissions**
   - User lacks read access to resource
   - Resource moved or deleted

3. **SharePoint-Specific Issues**
   - List names with periods (.) cause errors
   - Special characters in file names
   - Spaces in URLs not encoded

### Fix Patterns

**1. Add Existence Check**
```json
{
  "Try_Get_Item": {
    "type": "Scope",
    "actions": {
      "Get_Item": {
        "type": "ApiConnection",
        "inputs": { /* ... */ }
      }
    }
  },
  "Check_If_Failed": {
    "type": "If",
    "expression": {
      "and": [
        {
          "equals": [
            "@result('Try_Get_Item')[0]['status']",
            "Failed"
          ]
        }
      ]
    },
    "runAfter": {
      "Try_Get_Item": ["Failed", "Succeeded"]
    },
    "actions": {
      "Handle_Not_Found": {
        "type": "Compose",
        "inputs": "Item not found - creating new one"
      }
    }
  }
}
```

**2. Use Dynamic IDs from Previous Actions**
```json
{
  "Get_Items": {
    "type": "ApiConnection",
    "inputs": { /* Get items first */ }
  },
  "Apply_to_each": {
    "type": "Foreach",
    "foreach": "@outputs('Get_Items')?['body/value']",
    "actions": {
      "Get_Item_Detail": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connectionName": "shared_sharepointonline"
          },
          "method": "get",
          "path": "/datasets/@{encodeURIComponent(variables('SiteURL'))}/tables/@{encodeURIComponent(variables('ListID'))}/items/@{items('Apply_to_each')?['ID']}"
        }
      }
    }
  }
}
```

## Permission Errors (403)

### Pattern Recognition
- Status code: 403
- Error messages: "forbidden", "access denied", "insufficient permissions"
- Different from 401 (authentication vs authorization)

### Research Targets
```
PowerAutomateDocs/{Connector}/actions.md → Required permissions
PowerAutomateDocs/{Connector}/overview.md → Permission scopes
```

### Common Root Causes

1. **SharePoint Permissions**
   - Need "Edit" for Create/Update/Delete
   - Need "Read" for Get operations
   - Site-level vs list-level permissions

2. **OneDrive Permissions**
   - Need write access for file operations
   - Shared folders require special handling

3. **Delegated vs Application Permissions**
   - Service accounts need proper permission grants
   - Azure AD application permissions

### Fix Patterns

**1. Verify and Document Required Permissions**
```json
{
  "actions": {
    "Comment_Permissions": {
      "type": "Compose",
      "inputs": "This flow requires: SharePoint site collection admin or list owner permissions"
    },
    "Try_Action_With_Permission": {
      "type": "Scope",
      "actions": { /* Action requiring permissions */ }
    },
    "Handle_Permission_Error": {
      "type": "If",
      "expression": {
        "and": [
          {
            "equals": [
              "@result('Try_Action_With_Permission')[0]['code']",
              "Forbidden"
            ]
          }
        ]
      },
      "runAfter": {
        "Try_Action_With_Permission": ["Failed", "Succeeded"]
      },
      "actions": {
        "Send_Permission_Request": {
          "type": "ApiConnection",
          "inputs": { /* Send email to admin */ }
        }
      }
    }
  }
}
```

## Invalid JSON/Syntax Errors

### Pattern Recognition
- Error messages: "Invalid JSON", "syntax error", "unexpected token"
- Common in: HTTP response parsing, JSON composition, dynamic expression building

### Research Targets
```
PowerAutomateDocs/BuiltIn/data-operation.md → JSON handling
PowerAutomateDocs/power-automate-json-format.md → Valid structure
```

### Fix Patterns

**1. Escape Special Characters**
```json
{
  "Compose_JSON_String": {
    "type": "Compose",
    "inputs": "@{replace(variables('TextWithQuotes'), '\"', '\\\"')}"
  }
}
```

**2. Validate JSON Before Parsing**
```json
{
  "Try_Parse": {
    "type": "Scope",
    "actions": {
      "Parse_JSON": {
        "type": "ParseJson",
        "inputs": {
          "content": "@body('HTTP')"
        }
      }
    }
  },
  "Handle_Invalid_JSON": {
    "type": "If",
    "expression": {
      "and": [
        {
          "equals": [
            "@result('Try_Parse')[0]['status']",
            "Failed"
          ]
        }
      ]
    },
    "runAfter": {
      "Try_Parse": ["Failed", "Succeeded"]
    },
    "actions": {
      "Log_Invalid_Response": {
        "type": "Compose",
        "inputs": "Invalid JSON received from API"
      }
    }
  }
}
```

## Cross-Reference Matrix

| Error Code | Error Type | Primary Research Location | Common Connectors |
|------------|------------|--------------------------|-------------------|
| 401 | Authentication | {Connector}/overview.md | SharePoint, OneDrive, HTTP |
| 403 | Permission | {Connector}/actions.md | SharePoint, OneDrive |
| 404 | Not Found | {Connector}/actions.md | SharePoint, OneDrive, HTTP |
| 429 | Throttling | {Connector}/overview.md | SharePoint, OneDrive, HTTP |
| 500 | Server Error | {Connector}/overview.md | HTTP, SharePoint |
| N/A | Data Format | BuiltIn/data-operation.md | Parse JSON, Compose |
| N/A | Timeout | BuiltIn/control.md | Do Until, HTTP |
| N/A | Expression Error | BuiltIn/data-operation.md | All actions |

## Usage in Debugger Skill

This reference should be consulted during Phase 1 (Error Analysis) to:
1. Quickly classify the error type
2. Identify relevant research targets
3. Understand common root causes
4. Reference appropriate fix patterns

The patterns here are templates - always customize based on:
- Specific connector documentation from PowerAutomateDocs/
- Actual error details from erreur.json
- User's flow requirements and constraints
