# Microsoft Forms - Actions

---
type: connector-actions
connector_name: Microsoft Forms
action_count: 2
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [forms, response, form details, get response, microsoft forms, actions]
categories: [read]
---

<action_summary>
**Total Actions**: 2

**By Category**:
- Create Operations: 0 actions
- Read Operations: 2 actions
- Update Operations: 0 actions
- Delete Operations: 0 actions
- Search/Query Operations: 0 actions
- Utility Operations: 0 actions

**Complexity Distribution**:
- Low complexity: 2 actions
- Medium complexity: 0 actions
- High complexity: 0 actions
</action_summary>

<action_categories>
## Categories Overview

### Read Operations
Microsoft Forms connector provides read-only operations to retrieve form metadata and response data. These actions are typically used after a trigger fires to fetch detailed information about form submissions.
</action_categories>

---

## Read Operations

### Get Form Details

<action id="action-001" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetFormDetailsById
</action_header>

<description>
Retrieves metadata and configuration details for a specified form including title, creation date, modification date, status, and creator information. Use this action to get form properties before processing responses or for form management workflows.
</description>

<parameters>
#### Required Parameters

**Form Id** (`string`)
- **Description**: Unique identifier of the form to retrieve
- **Format**: GUID format (e.g., "AbCd1234EfGh5678IjKl9012MnOp3456")
- **Validation**: Must be valid form ID accessible by authenticated user
- **Example**: `v4j5cvGGr0GRqy180BHbRwQ2SyNVw05Iv4aI2PNjYE1UMkhNMlhQ2JOUzkxNU1YOE1GQUIzQy4u`
- **How to get**: Copy from form URL after `/Pages/ResponsePage.aspx?id=` parameter

#### Optional Parameters
None
</parameters>

<returns>
**Return Type**: `Object`

**Structure**:
```json
{
  "id": "v4j5cvGGr0GRqy180BHbRwQ2SyNVw05Iv4aI2PNjYE1UMkhNMlhQ2JOUzkxNU1YOE1GQUIzQy4u",
  "title": "Customer Feedback Survey",
  "created": "2025-01-15T10:30:00Z",
  "modified": "2025-10-25T14:45:00Z",
  "status": "Active",
  "creator": {
    "email": "user@contoso.com",
    "displayName": "John Doe"
  }
}
```

**Key Fields**:
- **`id`** (`string`): Unique form identifier - use for subsequent operations
- **`title`** (`string`): Display name of the form
- **`created`** (`datetime`): ISO 8601 timestamp of form creation
- **`modified`** (`datetime`): ISO 8601 timestamp of last modification
- **`status`** (`string`): Form state - Values: "Active", "Inactive", "Closed"
- **`creator`** (`object`): Information about form owner including email and display name

**Dynamic Content**:
- Use `Get_Form_Details?['title']` to reference form title in subsequent actions
- Access creator email: `Get_Form_Details?['creator']?['email']`
- Check status: `Get_Form_Details?['status']`
</returns>

<limitations>
### Operation-Specific Limits
- **Organizational Account Required**: Only works with organizational Microsoft accounts
  - **Workaround**: Ensure connection uses Azure AD account
- **Form Access Required**: User must have at least read access to form
  - **Workaround**: Verify permissions in Forms portal before flow execution

### Behavioral Notes
- **Group Forms**: Forms created by groups may require manual Form ID entry
- **Deleted Forms**: Returns 404 error if form no longer exists
- **Shared Forms**: Can retrieve details of forms shared with user, not owned

### Dependencies
- Requires: Valid connection to Microsoft Forms
- Conflicts with: None
</limitations>

<use_cases>
1. **Form Metadata Validation**
   - **Scenario**: Verify form title/status before processing responses
   - **Why This Action**: Ensures form is active and correct before data processing
   - **Typical Flow**: Trigger → Get Form Details → Condition (check status) → Process responses

2. **Multi-Form Management**
   - **Scenario**: Managing multiple forms with centralized tracking
   - **Combined With**: [Get response details](#action-002), SharePoint Create item
   - **Why**: Track form metadata in centralized repository
   - **Typical Flow**: Scheduled trigger → Get Form Details (multiple) → Update SharePoint list

3. **Form Lifecycle Monitoring**
   - **Scenario**: Monitor form modifications and alert owners
   - **Why This Action**: Provides modification timestamp for change detection
   - **Alternative**: Consider manual check in Forms portal if real-time not needed
   - **Typical Flow**: Scheduled trigger → Get Form Details → Compare modified date → Send alert if changed
</use_cases>

<best_practices>
### Performance
1. **Cache Form Details**: Store form metadata in variables to avoid repeated API calls
   - **Impact**: Reduces API calls from multiple retrievals to single call
   - **Implementation**: Call once at flow start, store in Compose or variable, reuse throughout flow

2. **Use Only When Needed**: Skip this action if form metadata not required for flow logic
   - **Impact**: Saves API calls toward 300/60s limit
   - **Implementation**: Only call when form title, status, or creator info is used in flow

### Reliability
1. **Handle 404 Errors**: Wrap in Scope with error handling for deleted forms
   - **Why**: Form may be deleted after flow deployment
   - **How**: Use Scope + Configure run after to catch and handle 404 gracefully

2. **Validate Form ID**: Check Form ID format before calling action
   - **Why**: Prevents unnecessary API calls with invalid IDs
   - **How**: Use Condition to verify Form ID is not null/empty and matches GUID pattern

### Data Integrity
1. **Store Form ID Separately**: Don't rely solely on form title for identification
   - **Why**: Form titles can change, IDs are permanent
   - **How**: Store Form ID in configuration list or environment variables

2. **Log Form Metadata**: Record form details when processing begins
   - **Why**: Audit trail for troubleshooting and compliance
   - **How**: Write form title, creator, and timestamp to SharePoint or logging system

### Error Handling
1. **Check Status Before Processing**: Verify form status is "Active"
   - **Why**: Closed forms may have different behavior
   - **How**: Add Condition after Get Form Details to check status field

2. **Retry on Transient Failures**: Configure retry policy for network errors
   - **Why**: Temporary network issues should not break flow
   - **How**: Enable automatic retry in flow settings or use Scope with Configure run after
</best_practices>

<example>
### Example 1: Validate Form Before Processing Responses

**Objective**: Verify form is active before processing new responses

**Configuration**:
```json
{
  "action": "GetFormDetailsById",
  "parameters": {
    "form_id": "@triggerOutputs()?['body/formId']"
  }
}
```

**Power Automate Expression**:
```
@triggerOutputs()?['body/formId']
```

**Expected Result**:
```json
{
  "id": "AbCd1234EfGh5678",
  "title": "Event Registration Form",
  "status": "Active",
  "created": "2025-10-01T08:00:00Z",
  "modified": "2025-10-15T12:30:00Z"
}
```

**What Happens**:
1. Flow triggered by new form response
2. Get Form Details retrieves form metadata
3. Condition checks if status equals "Active"
4. If active, proceed with response processing
5. If inactive, terminate flow with custom message

---

### Example 2: Multi-Form Monitoring Dashboard

**Objective**: Create dashboard showing status of all managed forms

**Configuration**:
```json
{
  "action": "GetFormDetailsById",
  "parameters": {
    "form_id": "@items('Apply_to_each_form')?['FormID']"
  }
}
```

**Use Case**: Scheduled flow runs daily, retrieves details for list of forms, updates SharePoint dashboard

**Typical Flow**:
1. Scheduled trigger (daily at 6 AM)
2. Get items from SharePoint (form registry list)
3. Apply to each form in list
4. Get Form Details for current item
5. Update SharePoint item with latest metadata
6. Send summary email with forms modified in last 24 hours

</example>

<common_errors>
### Error: Form not found (404)

<error ref="err-action-001-404">
- **Full Message**: "Resource not found" or "The requested form does not exist"
- **Cause**: Form ID invalid, form deleted, or user lacks access
- **Fix**:
  1. Verify Form ID is correct (copy from form URL)
  2. Check form exists in Forms portal
  3. Verify user connection has access to form
- **Prevention**: Validate Form ID before calling action, implement error handling
- **Related**: See [limitation lim-001](./overview.md#lim-001) for account requirements
</error>

### Error: Unauthorized (401)

<error ref="err-action-001-401">
- **Full Message**: "Unauthorized" or "Authentication token is invalid"
- **Cause**: Connection expired, personal account used, or token invalid
- **Fix**:
  1. Re-authenticate connection in Power Automate
  2. Verify organizational account is used (not personal)
  3. Check if user still has access to Forms service
- **Prevention**: Use service account with stable permissions, monitor connection health
- **Related**: See [authentication section](./overview.md#authentication)
</error>

### Error: Forbidden (403)

<error ref="err-action-001-403">
- **Full Message**: "Forbidden" or "You don't have permission to access this form"
- **Cause**: User doesn't have read access to form
- **Fix**:
  1. Form owner must share form with user
  2. Verify user email in form sharing settings
  3. Check organizational permissions
- **Prevention**: Document form access requirements, use admin account for monitoring flows
</error>

### Validation Errors
- **"Form ID is required"**: Ensure Form ID parameter is provided and not null
- **"Invalid Form ID format"**: Verify Form ID matches expected GUID pattern from URL
</common_errors>

<related_actions>
### Commonly Used Together
- **[Get response details](#action-002)**: After getting form details, retrieve specific response data
- **Compose (Data Operation)**: Format form metadata for display or storage

### Alternatives
- **Manual form management**: If form details rarely change, document manually instead of API calls

### Sequential Operations
Typical sequence:
1. **Trigger: When a new response is submitted** - Initiates flow
2. **This Action: Get Form Details** - Validates form before processing
3. **[Get response details](#action-002)** - Retrieves actual response data
4. **Condition** - Checks form status or other metadata
5. **Process response data** - Continue with business logic

### See Also
- Overview: [API Limits](./overview.md#api_limits)
- Related Trigger: [When a new response is submitted](./triggers.md#trigger-001)
</related_actions>

<troubleshooting>
### Performance Issues
**Problem**: Action takes too long (>10 seconds)
- **Check**: Network latency, Forms service health
- **Solution**: Implement timeout handling, check service status dashboard

### Unexpected Results
**Problem**: Form details show outdated information
- **Check**: Form modification timestamp, caching behavior
- **Solution**: Forms service has minimal caching, issue likely with flow logic

### Intermittent Failures
**Problem**: Action sometimes returns 404 for valid form
- **Check**: Connection health, service availability, permissions
- **Solution**: Implement retry logic with exponential backoff, verify form not temporarily inaccessible
</troubleshooting>

</action>

---

### Get Response Details

<action id="action-002" category="read" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Medium (called for every response)
**Premium**: No
**Operation ID**: GetFormResponseById
</action_header>

<description>
Retrieves detailed response data for a specific form submission including all question answers and responder metadata. This action provides dynamic output schema based on the form structure, making response fields available as dynamic content in subsequent actions. Essential for processing form submissions in automated workflows.
</description>

<parameters>
#### Required Parameters

**Form Id** (`string`)
- **Description**: Unique identifier of the form containing the response
- **Format**: GUID format (e.g., "AbCd1234EfGh5678IjKl9012MnOp3456")
- **Validation**: Must be valid form ID accessible by authenticated user
- **Example**: `v4j5cvGGr0GRqy180BHbRwQ2SyNVw05Iv4aI2PNjYE1UMkhNMlhQ2JOUzkxNU1YOE1GQUIzQy4u`
- **Source**: Usually from trigger output: `@triggerOutputs()?['body/formId']`

**Response Id** (`integer`)
- **Description**: Unique numeric identifier of the specific response to retrieve
- **Format**: Integer (e.g., 12345)
- **Validation**: Must be valid response ID for the specified form
- **Example**: `678901`
- **Source**: From trigger output: `@triggerOutputs()?['body/responseId']`

#### Optional Parameters
None
</parameters>

<returns>
**Return Type**: `Object` (dynamic schema based on form structure)

**Structure** (example for event registration form):
```json
{
  "responder": "user@contoso.com",
  "submitDate": "2025-10-31T14:30:00Z",
  "r1": "John Doe",
  "r2": "john.doe@contoso.com",
  "r3": "Yes, I will attend",
  "r4": ["Workshop A", "Workshop B"],
  "r5": "Looking forward to the event!"
}
```

**Key Fields**:
- **`responder`** (`string`): Email of person who submitted response (if collected)
- **`submitDate`** (`datetime`): ISO 8601 timestamp of submission
- **`r1`, `r2`, `r3`, etc.** (`string` | `array`): Response values for each question (field names are auto-generated)
- **Dynamic Fields**: Field names and types depend on form structure

**Dynamic Content**:
- Use `Get_response_details?['r1']` to reference first question answer
- Access responder email: `Get_response_details?['responder']`
- Get submission time: `Get_response_details?['submitDate']`
- Multi-select answers returned as arrays: `Get_response_details?['r4']`

**Important**: Field names (r1, r2, etc.) are assigned in order of form questions. To identify which field maps to which question, test with sample response or use form preview.
</returns>

<limitations>
### Operation-Specific Limits
- **Dynamic Schema**: Output schema changes if form questions are modified
  - **Workaround**: Use Parse JSON with regenerated schema when form changes
- **Response Deletion**: Returns 404 if response deleted by form owner
  - **Workaround**: Implement error handling to catch 404 gracefully
- **Anonymous Responses**: `responder` field may be null if form allows anonymous submissions
  - **Workaround**: Check if responder field is null before using

### Behavioral Notes
- **Field Naming**: Fields named sequentially (r1, r2, r3, etc.) based on question order
- **Multi-Select Questions**: Return array of strings, not single string
- **Date Questions**: Return ISO 8601 formatted datetime strings
- **File Uploads**: Forms connector doesn't support file upload questions - use OneDrive/SharePoint attachments instead

### Dependencies
- Requires: Valid Form ID and Response ID (typically from trigger)
- Conflicts with: None
</limitations>

<use_cases>
1. **Event Registration Processing**
   - **Scenario**: Process event registrations and send confirmations
   - **Why This Action**: Extract attendee details from form submission
   - **Typical Flow**: Trigger → Get response details → Parse responses → Send confirmation email

2. **Survey Data Aggregation**
   - **Scenario**: Collect survey responses in Excel for analysis
   - **Combined With**: Excel Online Add row action
   - **Why**: Transform form responses into structured data for reporting
   - **Typical Flow**: Trigger → Get response details → Map to Excel columns → Add row to table

3. **Conditional Workflow Routing**
   - **Scenario**: Route requests based on form responses
   - **Why This Action**: Retrieve answer data to evaluate conditions
   - **Typical Flow**: Trigger → Get response details → Switch (based on response) → Route to appropriate team

4. **Approval Initiation**
   - **Scenario**: Start approval workflows based on form submissions
   - **Combined With**: Start and wait for approval action
   - **Why**: Extract request details to populate approval form
   - **Typical Flow**: Trigger → Get response details → Compose approval details → Start approval

5. **Customer Feedback Notification**
   - **Scenario**: Notify teams of customer feedback
   - **Why This Action**: Retrieve feedback text and customer information
   - **Typical Flow**: Trigger → Get response details → Post to Teams channel → Create support ticket if needed
</use_cases>

<best_practices>
### Performance
1. **Call Immediately After Trigger**: Minimize delay between trigger and response retrieval
   - **Impact**: Ensures response still exists and is fresh
   - **Implementation**: Make Get response details first action after trigger

2. **Parse Responses Into Variables**: Extract frequently-used response fields into variables
   - **Impact**: Simplifies expressions later in flow, improves readability
   - **Implementation**: Use Initialize Variable or Compose to store name, email, etc.

### Reliability
1. **Handle 404 Errors**: Wrap in Scope with error handling for deleted responses
   - **Why**: Form owners can delete responses after trigger fires
   - **How**: Use Scope + Configure run after for Failed/Timed Out status

2. **Validate Response ID**: Check Response ID exists before calling action
   - **Why**: Trigger may provide null Response ID in rare cases
   - **How**: Add Condition to verify Response ID is greater than 0

### Data Integrity
1. **Store Response ID**: Record Response ID for deduplication and tracking
   - **Why**: Prevents duplicate processing if flow reruns
   - **How**: Write Response ID to SharePoint list or database before processing

2. **Validate Required Fields**: Check that critical response fields are not null
   - **Why**: Responders may skip optional questions
   - **How**: Use Condition to verify required fields have values before proceeding

### Error Handling
1. **Implement Retry Logic**: Retry on transient failures (503, 504, 429)
   - **Why**: Temporary service issues should not break flow
   - **How**: Enable automatic retry or use Scope with Configure run after

2. **Log Failed Retrievals**: Record Response IDs that fail to retrieve
   - **Why**: Enables manual review and troubleshooting
   - **How**: Send failed Response IDs to SharePoint list or email admin

3. **Handle Anonymous Responses**: Check if responder field is null
   - **Why**: Anonymous forms don't provide responder email
   - **How**: Use Condition to branch logic based on responder field

4. **Graceful Form Changes**: Update Parse JSON schema when form questions change
   - **Why**: Form modifications change response schema
   - **How**: Re-run action with sample response, regenerate schema, update Parse JSON

</best_practices>

<example>
### Example 1: Event Registration with Confirmation Email

**Objective**: Process event registration and send personalized confirmation

**Configuration**:
```json
{
  "action": "GetFormResponseById",
  "parameters": {
    "form_id": "@triggerOutputs()?['body/formId']",
    "response_id": "@triggerOutputs()?['body/responseId']"
  }
}
```

**Power Automate Expression** (mapping response fields):
```
Name: @{body('Get_response_details')?['r1']}
Email: @{body('Get_response_details')?['r2']}
Attendance: @{body('Get_response_details')?['r3']}
Workshops: @{join(body('Get_response_details')?['r4'], ', ')}
```

**Expected Result**:
```json
{
  "responder": "john.doe@contoso.com",
  "submitDate": "2025-10-31T14:30:00Z",
  "r1": "John Doe",
  "r2": "john.doe@contoso.com",
  "r3": "Yes",
  "r4": ["Workshop A", "Workshop B"],
  "r5": "Looking forward to it!"
}
```

**What Happens**:
1. Trigger fires with Response ID 678901
2. Get response details retrieves full response data
3. Parse JSON (optional) structures response for easier access
4. Compose action formats confirmation message with name, workshops
5. Send email action sends confirmation to r2 (email address)

---

### Example 2: Survey Data to Excel

**Objective**: Aggregate survey responses in Excel table for analysis

**Configuration**:
```json
{
  "action": "GetFormResponseById",
  "parameters": {
    "form_id": "@triggerOutputs()?['body/formId']",
    "response_id": "@triggerOutputs()?['body/responseId']"
  }
}
```

**Excel Mapping** (Add row to table):
```
Timestamp: @{body('Get_response_details')?['submitDate']}
Responder: @{body('Get_response_details')?['responder']}
Question1: @{body('Get_response_details')?['r1']}
Question2: @{body('Get_response_details')?['r2']}
Question3: @{body('Get_response_details')?['r3']}
```

**Use Case**: Real-time survey response aggregation without manual data entry

---

### Example 3: Conditional Routing Based on Response

**Objective**: Route support requests to appropriate team based on issue type

**Configuration**:
```json
{
  "action": "GetFormResponseById",
  "parameters": {
    "form_id": "@triggerOutputs()?['body/formId']",
    "response_id": "@triggerOutputs()?['body/responseId']"
  }
}
```

**Switch Expression**:
```
@body('Get_response_details')?['r3']
```

**Switch Cases**:
- Case "Technical Issue": Post to IT Support Teams channel
- Case "Billing Question": Create Dynamics 365 case for Finance team
- Case "Feature Request": Add item to Product Backlog SharePoint list
- Default: Send email to general support queue

</example>

<common_errors>
### Error: Response not found (404)

<error ref="err-action-002-404">
- **Full Message**: "The requested response does not exist"
- **Cause**: Response ID invalid, response deleted, or user lacks access to form
- **Fix**:
  1. Verify Response ID from trigger output is valid
  2. Check if response still exists in Forms portal
  3. Implement error handling to catch 404 gracefully
- **Prevention**:
  - Process responses immediately after trigger
  - Wrap action in Scope with Configure run after
  - Log failed Response IDs for investigation
- **Related**: See [troubleshooting section](./overview.md#troubleshooting)
</error>

### Error: Rate limit exceeded (429)

<error ref="err-action-002-429">
- **Full Message**: "Too Many Requests" or "Rate limit exceeded"
- **Cause**: Exceeded 300 API calls per 60 seconds limit
- **Fix**:
  1. Add delay between calls if processing multiple responses
  2. Enable concurrency control on trigger (limit to 10-20 concurrent runs)
  3. Implement exponential backoff in retry logic
- **Prevention**:
  - Monitor flow run frequency
  - Limit concurrent executions
  - Batch response processing if possible
- **Related**: See [API limits](./overview.md#api_limits)
</error>

### Error: Invalid Response ID

<error ref="err-action-002-validation">
- **Full Message**: "Response ID must be a positive integer"
- **Cause**: Response ID is null, negative, or non-integer
- **Fix**:
  1. Verify trigger is providing Response ID correctly
  2. Check Response ID expression syntax
  3. Add Condition to validate Response ID before calling action
- **Prevention**:
  - Always source Response ID from trigger output
  - Validate Response ID is greater than 0
</error>

### Validation Errors
- **"Form ID is required"**: Ensure Form ID parameter provided and not null
- **"Response ID is required"**: Verify Response ID from trigger is being passed correctly
- **"Schema validation failed"**: Form questions may have changed - regenerate Parse JSON schema
</common_errors>

<related_actions>
### Commonly Used Together
- **Parse JSON (Data Operation)**: Structure response data with known schema for easier access
- **Compose (Data Operation)**: Format response values for display or storage
- **Condition (Control)**: Branch logic based on response values
- **Apply to each (Control)**: Process multi-select answers (arrays)
- **Excel Online - Add row**: Store responses in Excel table
- **SharePoint - Create item**: Save responses to SharePoint list
- **Office 365 Outlook - Send email**: Send notifications or confirmations
- **Teams - Post message**: Notify teams of new responses

### Alternatives
- **Microsoft Forms - Get responses**: Retrieves all responses for a form (not available, would require custom connector)
- **Manual export**: Download responses from Forms portal if automation not needed

### Sequential Operations
Typical sequence:
1. **Trigger: When a new response is submitted** - Provides Response ID
2. **This Action: Get response details** - Retrieves full response data
3. **Parse JSON** - Structures response (optional but recommended)
4. **Compose / Initialize Variable** - Extract key fields (name, email, etc.)
5. **Condition / Switch** - Route based on response values
6. **Actions based on response** - Send emails, create items, etc.

### See Also
- Overview: [Common Use Cases](./overview.md#common_use_cases)
- Trigger: [When a new response is submitted](./triggers.md#trigger-001)
- Best Practices: [Error Handling](./overview.md#best_practices)
</related_actions>

<troubleshooting>
### Performance Issues
**Problem**: Action takes longer than expected (>5 seconds)
- **Check**: Response complexity (many questions), network latency, Forms service health
- **Solution**: Monitor service health, implement timeout handling, consider caching if retrieving same response multiple times

### Unexpected Results
**Problem**: Response fields are null or missing
- **Check**: Responder may have skipped optional questions, form allows anonymous responses
- **Solution**: Add null checks before using response fields, validate required fields after retrieval

**Problem**: Multi-select answers not parsing correctly
- **Check**: Multi-select fields return arrays, not strings
- **Solution**: Use Apply to each to process array values, or join() function to combine into string

**Problem**: Date fields in unexpected format
- **Check**: Date responses are ISO 8601 strings, not date objects
- **Solution**: Use formatDateTime() function to convert to desired format

### Intermittent Failures
**Problem**: Action randomly fails with 404 for valid Response ID
- **Check**: Response may have been deleted between trigger and retrieval
- **Solution**: Process responses immediately, implement error handling with Scope, log failures for investigation

**Problem**: Action times out occasionally
- **Check**: Forms service latency, network issues, response complexity
- **Solution**: Implement retry logic, increase timeout if possible, check Microsoft 365 service health
</troubleshooting>

</action>

---

<action_index>
## Quick Reference Index

### Alphabetical
- [Get Form Details](#action-001)
- [Get Response Details](#action-002)

### By Complexity
**Low Complexity**:
- [Get Form Details](#action-001) - Retrieve form metadata
- [Get Response Details](#action-002) - Retrieve response data

### By Use Case
**Response Processing**:
- [Get Response Details](#action-002) - Primary action for processing submissions
- [Get Form Details](#action-001) - Optional validation before processing

**Form Management**:
- [Get Form Details](#action-001) - Monitor form status and metadata
</action_index>

<related_docs>
- **Overview**: [overview.md](./overview.md) - Connector limitations and capabilities
- **Triggers**: [triggers.md](./triggers.md) - Available triggers for this connector
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/microsoftforms/
</related_docs>
