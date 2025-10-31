# Power Automate JSON Format Reference

## Complete Flow Definition Format

When copying an entire flow or creating a flow definition, Power Automate expects this exact structure:

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
      "Trigger_Name": {
        "type": "OpenApiConnectionWebhook",
        "inputs": {
          "host": {
            "connectionName": "shared_sharepointonline",
            "operationId": "GetOnNewItems",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
          },
          "parameters": {
            "dataset": "https://contoso.sharepoint.com/sites/sitename",
            "table": "list-guid"
          }
        },
        "metadata": {
          "operationMetadataId": "guid"
        }
      }
    },
    "actions": {
      "Action_Name": {
        "type": "OpenApiConnection",
        "inputs": {
          "host": {
            "connectionName": "shared_sharepointonline",
            "operationId": "GetItem",
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
          },
          "parameters": {
            "dataset": "https://contoso.sharepoint.com/sites/sitename",
            "table": "list-guid",
            "id": "@triggerOutputs()?['body/ID']"
          }
        },
        "runAfter": {},
        "metadata": {
          "operationMetadataId": "guid"
        }
      },
      "Initialize_variable": {
        "type": "InitializeVariable",
        "inputs": {
          "variables": [
            {
              "name": "varName",
              "type": "string",
              "value": ""
            }
          ]
        },
        "runAfter": {
          "Action_Name": ["Succeeded"]
        },
        "metadata": {
          "operationMetadataId": "guid"
        }
      },
      "Condition": {
        "type": "If",
        "expression": {
          "and": [
            {
              "equals": [
                "@variables('varName')",
                "value"
              ]
            }
          ]
        },
        "actions": {
          "Action_in_yes_branch": {
            "type": "OpenApiConnection",
            "inputs": {},
            "runAfter": {},
            "metadata": {
              "operationMetadataId": "guid"
            }
          }
        },
        "runAfter": {
          "Initialize_variable": ["Succeeded"]
        },
        "else": {
          "actions": {
            "Action_in_no_branch": {
              "type": "OpenApiConnection",
              "inputs": {},
              "runAfter": {},
              "metadata": {
                "operationMetadataId": "guid"
              }
            }
          }
        },
        "metadata": {
          "operationMetadataId": "guid"
        }
      },
      "Apply_to_each": {
        "type": "Foreach",
        "foreach": "@outputs('Action_Name')?['body/value']",
        "actions": {
          "Action_inside_loop": {
            "type": "OpenApiConnection",
            "inputs": {},
            "runAfter": {},
            "metadata": {
              "operationMetadataId": "guid"
            }
          }
        },
        "runAfter": {
          "Condition": ["Succeeded"]
        },
        "runtimeConfiguration": {
          "concurrency": {
            "repetitions": 1
          }
        },
        "metadata": {
          "operationMetadataId": "guid"
        }
      }
    },
    "outputs": {}
  },
  "schemaVersion": "1.0.0.0"
}
```

## Key Components

### 1. Root Structure
- **definition**: Contains the entire flow logic
- **schemaVersion**: Always "1.0.0.0"

### 2. Definition Object
- **$schema**: Azure Logic Apps schema URL (always the same)
- **contentVersion**: Flow version (always "1.0.0.0")
- **parameters**: Connection references (always include $connections)
- **triggers**: Flow trigger(s) - only ONE trigger per flow
- **actions**: All flow actions in key-value pairs
- **outputs**: Flow outputs (usually empty)

### 3. Action Structure

Every action must have:
```json
{
  "Action_Name": {
    "type": "ActionType",
    "inputs": {...},
    "runAfter": {
      "Previous_Action": ["Succeeded"]
    },
    "metadata": {
      "operationMetadataId": "unique-guid"
    }
  }
}
```

**Action Types**:
- `OpenApiConnection` - Connector actions (SharePoint, OneDrive, etc.)
- `InitializeVariable` - Initialize variable
- `SetVariable` - Set variable value
- `IncrementVariable` - Increment variable
- `AppendToArrayVariable` - Add to array variable
- `AppendToStringVariable` - Append to string variable
- `If` - Condition
- `Switch` - Switch
- `Foreach` - Apply to each
- `Until` - Do until
- `Scope` - Scope
- `Compose` - Compose
- `ParseJson` - Parse JSON
- `Select` - Select
- `Filter` - Filter array
- `Join` - Join
- `Terminate` - Terminate

### 4. runAfter Rules

- First action: `"runAfter": {}`
- Subsequent actions: `"runAfter": {"Previous_Action": ["Succeeded"]}`
- Error handling: `"runAfter": {"Action": ["Failed", "TimedOut", "Skipped"]}`
- Always run: `"runAfter": {"Action": ["Succeeded", "Failed", "Skipped", "TimedOut"]}`

### 5. Trigger Types

**Automated Triggers** (Event-based):
```json
{
  "type": "OpenApiConnectionWebhook",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "GetOnNewItems",
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
    },
    "parameters": {...}
  }
}
```

**Scheduled Triggers** (Recurrence):
```json
{
  "type": "Recurrence",
  "recurrence": {
    "frequency": "Day",
    "interval": 1,
    "startTime": "2024-01-01T09:00:00Z",
    "timeZone": "Eastern Standard Time"
  }
}
```

**Manual Triggers** (Instant):
```json
{
  "type": "Request",
  "kind": "Button",
  "inputs": {
    "schema": {
      "type": "object",
      "properties": {...}
    }
  }
}
```

### 6. Common Connector Actions

**SharePoint - Get Item**:
```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_sharepointonline",
      "operationId": "GetItem",
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
    },
    "parameters": {
      "dataset": "https://contoso.sharepoint.com/sites/sitename",
      "table": "list-guid",
      "id": "@triggerOutputs()?['body/ID']"
    }
  }
}
```

**OneDrive - Create File**:
```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_onedrive",
      "operationId": "CreateFile",
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_onedrive"
    },
    "parameters": {
      "path": "/folder/filename.txt",
      "body": "@body('Get_Item')?['FileContent']"
    }
  }
}
```

**HTTP Request**:
```json
{
  "type": "Http",
  "inputs": {
    "method": "POST",
    "uri": "https://api.example.com/endpoint",
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "key": "value"
    }
  }
}
```

**Send Email (Office 365)**:
```json
{
  "type": "OpenApiConnection",
  "inputs": {
    "host": {
      "connectionName": "shared_office365",
      "operationId": "SendEmailV2",
      "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365"
    },
    "parameters": {
      "emailMessage/To": "user@example.com",
      "emailMessage/Subject": "Subject",
      "emailMessage/Body": "<p>Email body</p>"
    }
  }
}
```

### 7. Data Operations

**Compose**:
```json
{
  "type": "Compose",
  "inputs": {
    "property1": "@triggerOutputs()?['body/value']",
    "property2": "static value"
  }
}
```

**Parse JSON**:
```json
{
  "type": "ParseJson",
  "inputs": {
    "content": "@body('Get_Item')",
    "schema": {
      "type": "object",
      "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"}
      }
    }
  }
}
```

**Select**:
```json
{
  "type": "Select",
  "inputs": {
    "from": "@body('List_Items')?['value']",
    "select": {
      "ID": "@item()?['ID']",
      "Title": "@item()?['Title']"
    }
  }
}
```

**Filter Array**:
```json
{
  "type": "Query",
  "inputs": {
    "from": "@body('List_Items')?['value']",
    "where": "@equals(item()?['Status'], 'Active')"
  }
}
```

### 8. Control Actions

**Condition**:
```json
{
  "type": "If",
  "expression": {
    "and": [
      {
        "equals": [
          "@variables('varName')",
          "value"
        ]
      }
    ]
  },
  "actions": {
    "Yes_Branch_Action": {...}
  },
  "else": {
    "actions": {
      "No_Branch_Action": {...}
    }
  }
}
```

**Apply to Each**:
```json
{
  "type": "Foreach",
  "foreach": "@body('Get_Items')?['value']",
  "actions": {
    "Action_For_Each_Item": {...}
  },
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 1
    }
  }
}
```

**Do Until**:
```json
{
  "type": "Until",
  "expression": "@equals(variables('counter'), 10)",
  "limit": {
    "count": 60,
    "timeout": "PT1H"
  },
  "actions": {
    "Action_Inside_Loop": {...}
  }
}
```

**Scope**:
```json
{
  "type": "Scope",
  "actions": {
    "Action_1": {...},
    "Action_2": {...}
  }
}
```

### 9. Error Handling Pattern

```json
{
  "Try_Scope": {
    "type": "Scope",
    "actions": {
      "Action_That_Might_Fail": {...}
    },
    "runAfter": {}
  },
  "Catch_Scope": {
    "type": "Scope",
    "actions": {
      "Handle_Error": {...}
    },
    "runAfter": {
      "Try_Scope": ["Failed", "TimedOut", "Skipped"]
    }
  }
}
```

## Important Notes

1. **Action Names**: Must be unique and use underscores or no spaces
2. **GUIDs**: Each action needs a unique operationMetadataId (use `uuidgen` or similar)
3. **Dynamic Content**: Use expressions like `@triggerOutputs()`, `@body('action')`, `@variables('name')`
4. **Connection Names**: Use standard names:
   - SharePoint: `shared_sharepointonline`
   - OneDrive: `shared_onedrive`
   - Office 365: `shared_office365`
   - Teams: `shared_teams`
5. **API IDs**: Always use `/providers/Microsoft.PowerApps/apis/{connector-name}`

## Copy-Paste Ready

The JSON structure above is ready to copy-paste into Power Automate's "Paste code" feature. The flow will import with placeholder connections that need to be configured.
