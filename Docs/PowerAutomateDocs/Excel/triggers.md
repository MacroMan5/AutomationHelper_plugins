# Excel Online (Business) - Triggers

---
type: connector-triggers
connector_name: Excel Online (Business)
trigger_count: 1
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [excel, trigger, selected row, manual trigger, instant flow]
trigger_types: [instant, manual]
---

<trigger_summary>
**Total Triggers**: 1

**Types**:
- Instant/Manual: 1 trigger
- Automated/Webhook: 0 triggers
- Scheduled: 0 triggers
- Polling: 0 triggers

**Note**: Excel Online (Business) connector provides only instant (manually triggered) flows. There are no automated triggers for Excel file changes. For automated detection of Excel changes, use OneDrive for Business or SharePoint triggers on file modification, then process with Excel actions.

**Recommendation**: For row-level processing workflows, use "For a selected row" trigger. For automated workflows monitoring Excel changes, combine SharePoint/OneDrive "When a file is modified" trigger with Excel Online actions.
</trigger_summary>

---

## Instant Triggers

### For a Selected Row

<trigger id="trigger-001" type="instant" frequency="manual" latency="immediate">

<trigger_header>
**Type**: Instant (Manual)
**Frequency**: User-initiated
**Latency**: Immediate
**Operation ID**: OnRowSelected
**Status**: Current
**Availability**: Power Automate only (not available in Power Apps)
</trigger_header>

<description>
Triggers a cloud flow for a selected row in an Excel table. User manually initiates the flow from Excel Online interface by right-clicking a row and selecting the flow from the Power Automate menu. Provides instant flow execution with row context passed as trigger output.
</description>

<parameters>
#### Configuration Parameters

**operationId** (`string`, required)
- **Description**: Internal operation identifier
- **Value**: "OnRowSelected"
- **Note**: Auto-configured when creating flow

**host** (`object`, required)
- **Description**: Connection host configuration
- **Note**: Auto-configured with connection details

**parameters** (`object`, required)
- **Description**: Trigger parameters including table reference
- **Configuration**:
  - Location: Storage location (OneDrive, SharePoint, Teams)
  - Document Library: Library containing workbook
  - File: Path to Excel workbook
  - Table: Table to enable trigger on

**schema** (`object`, required)
- **Description**: Dynamic schema based on table columns
- **Note**: Auto-generated from table structure

**headersSchema** (`object`, optional)
- **Description**: Optional header schema configuration
</parameters>

<behavior>
**Trigger Mechanism**: User-initiated (Instant)
- User right-clicks row in Excel Online
- Selects flow from Power Automate context menu
- Flow executes immediately with row data

**User Experience**:
1. Open Excel workbook in Excel Online (browser)
2. Navigate to table with configured trigger
3. Right-click any row in table
4. Select "Power Automate" → [Flow Name]
5. Flow executes with selected row context

**Concurrency**: Single execution per trigger
- Each user action triggers one flow run
- Multiple users can trigger flows independently
- Default concurrency: Up to 50 concurrent runs

**Deduplication**: Not applicable
- Each trigger is unique user action
- No automatic deduplication needed

**Batch Size**: Single row per execution
- Trigger provides data for one selected row only
- For multi-row processing, use "Apply to each" with Excel actions
</behavior>

<outputs>
**Trigger Output Structure**:
```json
{
  "rows": [
    {
      "ID": "1234",
      "CustomerName": "Contoso Inc",
      "OrderDate": "2025-10-31T10:30:00Z",
      "Amount": 2500.00,
      "Status": "Pending"
    }
  ],
  "User id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "User email": "john.doe@contoso.com",
  "User name": "John Doe",
  "Timestamp": "2025-10-31T14:45:30Z"
}
```

**Key Fields**:

**rows** (`array`)
- Array containing one row object with all table columns
- Access columns: `triggerBody()?['rows']?[0]?['ColumnName']`
- Dynamic properties based on table schema

**User id** (`guid`)
- Microsoft Entra ID (Azure AD) object ID of user who triggered flow
- Format: GUID
- Example: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

**User email** (`string`)
- Email address of user who triggered flow
- Example: `john.doe@contoso.com`
- Use for notifications or approval routing

**User name** (`string`)
- Display name of user who triggered flow
- Example: "John Doe"
- Use for personalization or logging

**Timestamp** (`string`)
- ISO 8601 timestamp when flow was triggered
- Format: UTC datetime
- Example: `2025-10-31T14:45:30Z`

**Dynamic Content Access**:
- Selected row columns: `triggerBody()?['rows']?[0]?['ColumnName']`
- User who triggered: `triggerBody()?['User email']`
- Trigger time: `triggerBody()?['Timestamp']`
</outputs>

<requirements>
**Prerequisites**:

<requirement id="req-001" type="environment">
**Excel Online**: Workbook must be opened in Excel Online (browser version)
- Desktop Excel app does NOT support flow triggers
- SharePoint embedded Excel viewer does NOT support triggers
- Only full Excel Online interface shows Power Automate menu
</requirement>

<requirement id="req-002" type="permissions">
**User Permissions**: User must have access to both:
- Excel workbook (at least Read permissions)
- Power Automate flow (Run permissions)
</requirement>

<requirement id="req-003" type="table">
**Table Structure**: Target must be Excel table (not range)
- Flow only appears for tables, not cell ranges
- Table must have at least one row
- Hidden tables do NOT show trigger option
</requirement>

<requirement id="req-004" type="licensing">
**Licensing**: User needs Power Automate license
- Microsoft 365 license with Power Automate included, OR
- Standalone Power Automate license
- Premium connectors require Power Automate Premium license
</requirement>
</requirements>

<limitations>
<limitation id="lim-001" severity="high">
**Desktop Excel Not Supported**: Trigger only works in Excel Online (browser)
- Excel Desktop app does not show Power Automate context menu
- Workaround: Open file in browser version of Excel
</limitation>

<limitation id="lim-002" severity="high">
**Embedded Excel Not Supported**: SharePoint-embedded Excel viewers don't support triggers
- Must open in full Excel Online interface
- Workaround: Click "Open in Excel" from SharePoint viewer
</limitation>

<limitation id="lim-003" severity="medium">
**Single Row Only**: Trigger provides only selected row data
- Cannot select multiple rows simultaneously
- Workaround: Use "Apply to each" with List rows action for multi-row operations
</limitation>

<limitation id="lim-004" severity="medium">
**Tables Only**: Trigger not available for cell ranges
- Must convert range to table first
- Workaround: Select range and Insert → Table in Excel
</limitation>

<limitation id="lim-005" severity="low">
**Menu Discovery**: Users must know to right-click for Power Automate menu
- No visual indicator that flow is available
- Recommendation: Provide user training/documentation
</limitation>

<limitation id="lim-006" severity="medium">
**No Automated Detection**: Excel Online has no automated triggers for row/cell changes
- This trigger is manual only
- Workaround: Use SharePoint/OneDrive file modification trigger + Excel List rows action
</limitation>
</limitations>

<common_errors>
**Flow Not Appearing in Menu**
- **Cause**: File opened in Desktop Excel or embedded viewer
- **Solution**: Open file in Excel Online (browser)

**Flow Not Appearing in Menu** (Alternative)
- **Cause**: User lacks Run permissions on flow
- **Solution**: Share flow with user granting Run permissions

**Flow Not Appearing in Menu** (Alternative 2)
- **Cause**: Target is cell range, not table
- **Solution**: Convert range to table (Insert → Table)

**403 Forbidden**
- **Cause**: User lacks access to workbook or flow
- **Solution**: Verify user has Read access to file and Run permissions on flow

**Flow Fails After Trigger**
- **Cause**: Flow connection credentials expired or insufficient permissions
- **Solution**: Re-authenticate connections; ensure Edit permissions for write operations
</common_errors>

<best_practices>
**User Experience**:
1. **Clear Naming**: Name flow descriptively (e.g., "Send Order Email" not "Flow1")
2. **User Training**: Document how users access flows (right-click → Power Automate)
3. **Confirmation**: Show success message or send notification after flow completes
4. **Error Feedback**: Implement error handling with user-friendly notifications

**Flow Design**:
1. **Validation**: Validate row data before processing
2. **User Context**: Use trigger user email for personalization and security
3. **Auditing**: Log trigger user and timestamp for audit trail
4. **Approval Integration**: Use user context for routing approvals to managers

**Performance**:
1. **Minimal Actions**: Keep flow fast for responsive user experience
2. **Async Operations**: For long-running tasks, acknowledge immediately then process async
3. **Error Handling**: Graceful failure with user notification
4. **Concurrency**: Limit if multiple users trigger simultaneously

**Security**:
1. **Row-Level Security**: Validate user permissions for row operations
2. **Data Validation**: Sanitize row data before using in external systems
3. **User Verification**: Verify trigger user has authority for requested action
4. **Sensitive Data**: Avoid including sensitive data in flow outputs/logs
</best_practices>

<use_cases>
**Common Use Cases**:

1. **Send Notification**
   - User selects order row → Flow sends notification email to customer

2. **Create Approval**
   - User selects expense row → Flow creates approval request for manager

3. **Update External System**
   - User selects product row → Flow updates inventory in external database

4. **Generate Document**
   - User selects contract row → Flow generates PDF contract from template

5. **Data Enrichment**
   - User selects customer row → Flow fetches additional data from CRM

6. **Status Update**
   - User selects task row → Flow updates status in project management system

7. **Multi-System Sync**
   - User selects record row → Flow syncs to multiple connected systems
</use_cases>

<example>
**Scenario**: Send order confirmation email when user selects order row

**Trigger Configuration**:
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/sales/Shared Documents/Orders.xlsx",
  "Table": "OrdersTable"
}
```

**Flow Logic**:
1. Trigger: For a selected row (OrdersTable)
2. Get row data from trigger output:
   - Order ID: `triggerBody()?['rows']?[0]?['OrderID']`
   - Customer Email: `triggerBody()?['rows']?[0]?['CustomerEmail']`
   - Order Amount: `triggerBody()?['rows']?[0]?['Amount']`
3. Compose email with order details
4. Send email (Office 365 Outlook):
   - To: `triggerBody()?['rows']?[0]?['CustomerEmail']`
   - Subject: "Order Confirmation - [OrderID]"
   - Body: Order details with amount and delivery info
5. Update row Status to "Confirmed":
   - Use Update row action with OrderID as key

**User Experience**:
1. User opens Orders.xlsx in Excel Online
2. Right-clicks order row that needs confirmation
3. Selects "Power Automate" → "Send Order Confirmation"
4. Flow runs immediately
5. Customer receives email
6. Order status updates to "Confirmed"
7. User sees success notification (optional)

**Benefits**:
- One-click order processing
- Consistent email format
- Automatic status tracking
- Audit trail with trigger user and timestamp
</example>

---

## Alternative Approaches for Automated Triggers

Since Excel Online (Business) does not provide automated triggers for data changes, consider these alternatives:

### Option 1: SharePoint "When a file is modified" Trigger
**Use Case**: Detect when Excel file changes, then process data

**Flow Pattern**:
1. **Trigger**: SharePoint "When a file is modified"
   - Monitors Excel file for any changes
   - Fires when file saved
2. **Action**: Excel "List rows present in a table"
   - Retrieves updated data
   - Apply filters to find new/changed rows
3. **Action**: Process rows with "Apply to each"

**Limitations**:
- Triggers on ANY file change, not specific row changes
- Must implement logic to detect which rows changed
- May trigger multiple times for single user session
- 5-minute minimum polling interval

### Option 2: Scheduled Flow with Change Detection
**Use Case**: Periodic check for new/updated rows

**Flow Pattern**:
1. **Trigger**: Recurrence (every hour, daily, etc.)
2. **Action**: Excel "List rows present in a table"
   - Filter for rows added/modified since last check
   - Use date column: `LastModified gt '[last-check-time]'`
3. **Action**: Process new/updated rows
4. **Action**: Update last-check timestamp in variable or storage

**Benefits**:
- Reliable scheduled execution
- Predictable resource usage
- Batch processing efficiency

**Limitations**:
- Latency equal to schedule interval
- Requires LastModified column in table
- Manual change tracking logic needed

### Option 3: OneDrive for Business Triggers
**Use Case**: Excel files stored in OneDrive

**Available Triggers**:
- "When a file is created in a folder"
- "When a file is modified in a folder"

**Same pattern as SharePoint approach**

### Option 4: Microsoft Forms + Excel
**Use Case**: Form submissions automatically saved to Excel

**Flow Pattern**:
1. **Trigger**: Microsoft Forms "When a new response is submitted"
2. **Action**: Forms "Get response details"
3. **Action**: Excel "Add a row into a table"
4. **Action**: Additional processing on new row

**Benefits**:
- Real-time webhook trigger
- Automatic row creation
- Built-in form validation

---

## Comparison: Excel Triggers vs Other Connectors

| Feature | Excel Online | SharePoint | OneDrive | Microsoft Forms |
|---------|-------------|------------|----------|----------------|
| **Automated Row Changes** | ❌ No | ⚠️ File-level only | ⚠️ File-level only | ✅ Yes (Form submission) |
| **Real-time Webhook** | ❌ No | ⚠️ File-level | ⚠️ File-level | ✅ Yes |
| **Manual/Instant Trigger** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Row-level Context** | ✅ Yes (manual) | ❌ No | ❌ No | ✅ Yes |
| **Polling Interval** | N/A | 5 min | 5 min | Instant |
| **Desktop App Support** | ❌ No | N/A | N/A | N/A |

**Recommendation**:
- For manual user-initiated workflows: Use "For a selected row" trigger
- For automated data collection: Use Microsoft Forms with Excel actions
- For file change detection: Use SharePoint/OneDrive triggers with Excel List rows
- For scheduled processing: Use Recurrence trigger with change detection logic

---

**Last Updated**: 2025-10-31
**Documentation Version**: 1.0
**Connector Version**: Current (as of 2025-10-31)
**Official Reference**: https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/
