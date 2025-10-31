# Microsoft Forms - Triggers

---
type: connector-triggers
connector_name: Microsoft Forms
trigger_count: 2
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [forms, trigger, response submitted, webhook, polling, microsoft forms]
trigger_types: [webhook, polling]
---

<trigger_summary>
**Total Triggers**: 2

**Types**:
- Polling: 1 trigger (deprecated)
- Webhook: 1 trigger (current, recommended)
- Scheduled: 0 triggers

**Recommendation**: Always use the webhook-based trigger (current) for real-time response notifications. The polling trigger is deprecated and checks only once every 24 hours.
</trigger_summary>

---

## When a New Response is Submitted (Current)

<trigger id="trigger-001" type="webhook" frequency="real-time" latency="seconds">

<trigger_header>
**Type**: Webhook (Real-time)
**Frequency**: Instant notification upon submission
**Latency**: 1-5 seconds typical
**Operation ID**: CreateFormWebhook
**Status**: Current (Recommended)
</trigger_header>

<description>
Triggers the flow immediately when a new response is submitted to the specified form. Uses webhook technology to receive real-time notifications from Microsoft Forms service, providing instant response processing with minimal latency. This is the recommended trigger for all new flows.
</description>

<parameters>
#### Required Parameters

**Form Id** (`string`)
- **Description**: Unique identifier of the form to monitor for new responses
- **Format**: GUID format (e.g., "AbCd1234EfGh5678IjKl9012MnOp3456")
- **Validation**: Must be valid form ID accessible by authenticated user
- **Example**: `v4j5cvGGr0GRqy180BHbRwQ2SyNVw05Iv4aI2PNjYE1UMkhNMlhQ2JOUzkxNU1YOE1GQUIzQy4u`
- **How to get**:
  1. Open form in Microsoft Forms portal
  2. Click "..." menu → "Settings"
  3. Look at URL bar: copy everything after `id=` parameter
  4. Alternative: For group forms, copy from address bar when viewing form

#### Optional Parameters
None - This trigger only requires Form ID
</parameters>

<behavior>
**Trigger Mechanism**: Webhook-based (push notification)
- Microsoft Forms service sends HTTP POST to Power Automate when response submitted
- No polling required - instant notification

**Batch Size**: 1 response per trigger execution
- Each response triggers separate flow run
- No batching - responses processed individually

**Deduplication**: Handled by Microsoft Forms service
- Response IDs are unique per submission
- Webhook may occasionally send duplicate notifications (rare)
- Recommended: Implement deduplication logic in flow

**Ordering**: Chronological by submission time
- Responses trigger flows in order of submission
- Concurrent submissions may trigger parallel flow runs
- Use timestamp for definitive ordering if needed

**Concurrency**: Multiple concurrent runs supported
- Default: Up to 50 concurrent flow runs
- Configurable: Limit concurrency in trigger settings
- Recommendation: Limit to 10-20 for stability
</behavior>

<outputs>
**Trigger Output Structure**:
```json
{
  "body": {
    "responder": "user@contoso.com",
    "formId": "v4j5cvGGr0GRqy180BHbRwQ2SyNVw05Iv4aI2PNjYE1UMkhNMlhQ2JOUzkxNU1YOE1GQUIzQy4u",
    "responseId": "678901",
    "submitDate": "2025-10-31T14:30:00Z"
  },
  "headers": {
    "Content-Type": "application/json"
  }
}
```

**Dynamic Content Available**:
- **`responder`** (`string`): Email address of person who submitted form (null for anonymous)
  - Usage: `@triggerOutputs()?['body/responder']`
  - Note: Only available if form collects responder email
- **`formId`** (`string`): Form identifier (same as trigger configuration)
  - Usage: `@triggerOutputs()?['body/formId']`
  - Use case: Multi-form scenarios, validation
- **`responseId`** (`string` or `integer`): Unique response identifier
  - Usage: `@triggerOutputs()?['body/responseId']`
  - **Critical**: Required for Get response details action
- **`submitDate`** (`datetime`): ISO 8601 timestamp of submission
  - Usage: `@triggerOutputs()?['body/submitDate']`
  - Format: `2025-10-31T14:30:00Z`

**Important Notes**:
- Trigger output contains only metadata, not actual response data
- Use "Get response details" action to retrieve question answers
- Response ID is the key to fetching full response content
</outputs>

<limitations>
### Trigger-Specific Limits

<limitation id="lim-trigger-001" severity="low">
**No Response Data in Trigger**: Trigger output doesn't include form answers
- **Impact**: Must call Get response details action to retrieve answers
- **Workaround**: None - this is by design for performance
- **Pattern**: Trigger → Get response details → Process answers
</limitation>

<limitation id="lim-trigger-002" severity="medium">
**Anonymous Forms**: Responder field is null if form allows anonymous submissions
- **Impact**: Cannot identify who submitted response
- **Workaround**: Include "Email" question in form to collect identity
- **Affected Scenarios**: Flows that route/notify based on responder
</limitation>

<limitation id="lim-trigger-003" severity="low">
**Group Forms Not Listed**: Forms created by Microsoft 365 Groups don't appear in dropdown
- **Impact**: Cannot select from UI dropdown
- **Workaround**: Manually enter Form ID from URL
- **Related**: See [overview limitation lim-002](./overview.md#lim-002)
</limitation>

<limitation id="lim-trigger-004" severity="medium">
**Concurrency Cannot Be Disabled**: Once enabled, concurrency control cannot be fully disabled
- **Impact**: "CannotDisableTriggerConcurrency" error if attempting to disable
- **Workaround**: Export flow JSON, modify settings, re-import
- **Related**: See [overview limitation lim-004](./overview.md#lim-004)
</limitation>

<limitation id="lim-trigger-005" severity="low">
**Organizational Accounts Only**: Trigger requires organizational Microsoft account
- **Impact**: Personal Microsoft accounts not supported
- **Workaround**: None - use organizational account
- **Related**: See [overview limitation lim-001](./overview.md#lim-001)
</limitation>
</limitations>

<filtering>
**Filtering Options**:
- **Server-side**: None available at trigger level
  - All form submissions trigger the flow
  - Cannot filter by response content at trigger

- **Client-side**: Use Condition action after Get response details
  - Filter by responder email
  - Filter by response values (after retrieving with Get response details)
  - Filter by submission date/time

**Recommendation**:
1. Let all responses trigger the flow
2. Add Condition action early in flow to filter by criteria
3. Use Terminate action to exit flow for unwanted responses
4. This approach ensures no responses are missed

**Example Filter Pattern**:
```
Trigger: When a new response is submitted
↓
Get response details
↓
Condition: Check if response meets criteria
  - Yes branch: Process response
  - No branch: Terminate flow
```
</filtering>

<use_cases>
1. **Real-Time Event Registration**
   - **Scenario**: Process event registrations instantly and send confirmation emails
   - **Why This Trigger**: Real-time processing ensures immediate confirmation
   - **Pattern**: Trigger → Get response → Send confirmation
   - **Typical Flow**:
     1. Trigger fires with Response ID
     2. Get response details retrieves registration info
     3. Create SharePoint list item for tracking
     4. Send confirmation email to attendee
     5. Optional: Send summary to event organizer

2. **Customer Feedback Routing**
   - **Scenario**: Route customer feedback to appropriate teams based on feedback type
   - **Why This Trigger**: Instant notification enables quick response to customers
   - **Pattern**: Trigger → Get response → Route to team
   - **Typical Flow**:
     1. Trigger fires when customer submits feedback
     2. Get response details retrieves feedback content
     3. Switch action routes based on feedback category
     4. Post message to appropriate Teams channel
     5. Create support ticket if needed

3. **Survey Response Aggregation**
   - **Scenario**: Collect survey responses in Excel in real-time for live dashboard
   - **Why This Trigger**: Real-time data collection for live reporting
   - **Pattern**: Trigger → Get response → Add to Excel
   - **Typical Flow**:
     1. Trigger fires when survey submitted
     2. Get response details retrieves answers
     3. Map responses to Excel columns
     4. Add row to Excel table
     5. Optional: Update Power BI dataset

4. **Quiz Auto-Grading**
   - **Scenario**: Automatically grade quiz submissions and notify students
   - **Why This Trigger**: Immediate feedback improves learning experience
   - **Pattern**: Trigger → Get response → Calculate score → Notify
   - **Typical Flow**:
     1. Trigger fires when quiz submitted
     2. Get response details retrieves answers
     3. Compose action calculates score
     4. Condition checks if passing
     5. Send email with results to student

5. **Approval Workflow Initiation**
   - **Scenario**: Start approval workflows based on form submissions
   - **Why This Trigger**: Immediate approval request upon submission
   - **Pattern**: Trigger → Get response → Start approval
   - **Typical Flow**:
     1. Trigger fires when request form submitted
     2. Get response details retrieves request data
     3. Compose approval message with details
     4. Start and wait for approval
     5. Notify requester of decision
</use_cases>

<best_practices>
## Trigger Configuration

1. **Always Use Current Webhook Trigger**: Select trigger labeled "(current)", not deprecated version
   - **Why**: Real-time vs 24-hour polling delay
   - **How**: When adding trigger, choose "When a new response is submitted" without "(DEPRECATED)" label

2. **Manually Enter Group Form IDs**: For group-created forms, enter Form ID manually
   - **Why**: Group forms don't appear in dropdown
   - **How**: Copy Form ID from URL, paste directly in Form Id field

3. **Configure Concurrency Control**: Limit concurrent runs to prevent throttling
   - **Why**: Too many concurrent runs can exceed API limits
   - **How**: Trigger settings → Concurrency Control → Set to 10-20
   - **Warning**: Cannot disable once enabled without JSON export/import

## Flow Design

1. **Get Response Details Immediately**: Make it first action after trigger
   - **Why**: Trigger only provides Response ID, not actual data
   - **How**: Add "Get response details" as first action, pass Form ID and Response ID from trigger

2. **Implement Deduplication**: Check for duplicate response processing
   - **Why**: Webhooks may occasionally send duplicate notifications
   - **How**: Store Response IDs in SharePoint list, check if exists before processing

3. **Add Error Handling Early**: Wrap Get response details in Scope with error handling
   - **Why**: Response may be deleted between trigger and retrieval
   - **How**: Use Scope + Configure run after for Failed/TimedOut

4. **Validate Response ID**: Check Response ID is valid before processing
   - **Why**: Trigger may provide null Response ID in edge cases
   - **How**: Add Condition to verify Response ID is greater than 0

## Performance Optimization

1. **Enable Concurrency with Limits**: Allow parallel processing but set reasonable limit
   - **Why**: Improves throughput while preventing throttling
   - **How**: Set concurrency to 10-20 runs
   - **Balance**: Higher = faster processing but more API calls

2. **Cache Form Details**: Store form metadata in variables if needed in flow
   - **Why**: Avoids repeated Get form details calls
   - **How**: Call Get form details once, store in Compose/variable, reuse

3. **Minimize API Calls**: Design flow to minimize actions per response
   - **Why**: Each response triggers flow, multiple flows can hit rate limits
   - **How**: Combine operations where possible, cache reusable data

## Reliability

1. **Monitor Flow Runs**: Regularly check run history for failures
   - **Why**: Detect issues early before they impact many responses
   - **How**: Set up alert for flow failure rate > threshold

2. **Log Successful Processing**: Record processed Response IDs
   - **Why**: Audit trail and troubleshooting
   - **How**: Write Response ID + timestamp to SharePoint list

3. **Handle Anonymous Responses**: Check if responder field is null
   - **Why**: Anonymous forms don't provide responder email
   - **How**: Use Condition to branch logic based on responder presence

## Security

1. **Use Service Account**: Don't use personal account for production flows
   - **Why**: Flow breaks when user leaves organization
   - **How**: Create dedicated service account with Forms permissions

2. **Validate Form ID**: Verify Form ID matches expected form
   - **Why**: Prevents processing responses from wrong form
   - **How**: Add Condition to check Form ID equals expected value

3. **Sanitize User Input**: Validate/sanitize response data before using
   - **Why**: Prevent injection attacks in downstream systems
   - **How**: Use Compose to validate/clean data before SharePoint/SQL operations
</best_practices>

<example>
### Example 1: Basic Event Registration Flow

**Scenario**: Process event registrations with immediate confirmation

**Trigger Configuration**:
```json
{
  "trigger": "CreateFormWebhook",
  "parameters": {
    "form_id": "v4j5cvGGr0GRqy180BHbRwQ2SyNVw05Iv4aI2PNjYE1UMkhNMlhQ2JOUzkxNU1YOE1GQUIzQy4u"
  }
}
```

**Trigger Outputs Used**:
```
Response ID: @{triggerOutputs()?['body/responseId']}
Form ID: @{triggerOutputs()?['body/formId']}
Responder: @{triggerOutputs()?['body/responder']}
Submit Date: @{triggerOutputs()?['body/submitDate']}
```

**Flow Structure**:
1. Trigger: When a new response is submitted
2. Get response details (Form ID: trigger output, Response ID: trigger output)
3. Create SharePoint item (Registration list)
4. Send email (Office 365 Outlook)
   - To: `@{body('Get_response_details')?['r2']}` (email from form)
   - Subject: "Registration Confirmed"
   - Body: "Hi `@{body('Get_response_details')?['r1']}`, your registration is confirmed..."

**Expected Behavior**:
- User submits form at 2:30 PM
- Trigger fires within 1-5 seconds
- Response details retrieved
- SharePoint item created
- Confirmation email sent by 2:31 PM

---

### Example 2: Survey with Response Count Threshold

**Scenario**: Aggregate survey responses, send summary when 100 responses reached

**Trigger Configuration**:
```json
{
  "trigger": "CreateFormWebhook",
  "parameters": {
    "form_id": "SurveyFormIdHere"
  },
  "concurrency": {
    "runs": 20
  }
}
```

**Flow Structure**:
1. Trigger: When a new response is submitted
2. Get response details
3. Add row to Excel table (Survey Responses)
4. Get rows from Excel table (count total)
5. Condition: If row count >= 100
   - Yes: Send summary email to team
   - No: Do nothing (flow ends)

**Key Expressions**:
- Count rows: `@length(body('List_rows_from_table')?['value'])`
- Check threshold: `@greaterOrEquals(length(body('List_rows_from_table')?['value']), 100)`

---

### Example 3: Conditional Routing with Deduplication

**Scenario**: Route support requests to teams, prevent duplicate processing

**Trigger Configuration**:
```json
{
  "trigger": "CreateFormWebhook",
  "parameters": {
    "form_id": "SupportFormIdHere"
  },
  "concurrency": {
    "runs": 10
  }
}
```

**Flow Structure**:
1. Trigger: When a new response is submitted
2. Compose: Store Response ID
3. Get items from SharePoint (Processed Responses list, filter by Response ID)
4. Condition: If Response ID already exists
   - Yes: Terminate (duplicate)
   - No: Continue processing
5. Create SharePoint item (mark as processing)
6. Get response details
7. Switch: Route based on issue type (r3 field)
   - Technical: Post to IT Support Teams channel
   - Billing: Post to Finance Teams channel
   - General: Post to Customer Service Teams channel
8. Update SharePoint item (mark as complete)

**Deduplication Expression**:
```
@empty(body('Get_items_from_SharePoint')?['value'])
```

</example>

<performance_impact>
- **Throttling**: Each response triggers flow, counts toward 300 API calls per 60 seconds
  - Mitigation: Enable concurrency control with reasonable limit (10-20)
  - Monitoring: Track flow run frequency, implement delays if approaching limit

- **Resource Usage**: Minimal - webhook-based, no polling overhead
  - CPU: Negligible - trigger is push-based
  - Memory: Minimal - only stores Response ID and metadata

- **Scaling**: Handles high-volume forms well with proper concurrency limits
  - Up to 50 concurrent runs by default
  - Recommend limiting to 10-20 for stability
  - Monitor run queue depth in flow analytics
</performance_impact>

<related_triggers>
### Alternative Triggers
- **[When a new response is submitted (DEPRECATED)](#trigger-002)**: Old polling-based trigger - DO NOT USE for new flows
  - Use when: Never - always use current webhook trigger
  - Difference: Polling once per 24 hours vs real-time webhook

### Often Paired With Actions
- **Get response details**: Primary action after trigger (retrieves actual response data)
- **Condition**: Filter responses based on criteria
- **Parse JSON**: Structure response data with schema
- **Compose**: Extract and format response fields
- **Office 365 Outlook - Send email**: Send notifications/confirmations
- **SharePoint - Create item**: Store responses for tracking
- **Excel Online - Add row**: Aggregate responses in Excel
- **Teams - Post message**: Notify teams of new responses

### Sequential Pattern
Recommended pattern:
1. **This Trigger**: When a new response is submitted (current)
2. **Deduplication Check** (optional): Verify Response ID not already processed
3. **Get response details**: Retrieve full response data
4. **Parse JSON** (optional): Structure data with schema
5. **Validation**: Check required fields present
6. **Business Logic**: Process response (conditions, approvals, etc.)
7. **Output Actions**: Send emails, create items, post messages
8. **Logging**: Record processing completion

### See Also
- Actions: [Get response details](./actions.md#action-002), [Get form details](./actions.md#action-001)
- Overview: [Common Use Cases](./overview.md#common_use_cases)
- Best Practices: [Flow Design](./overview.md#best_practices)
</related_triggers>

<troubleshooting>
## Common Issues

### Trigger Not Firing

**Problem**: Flow not triggered when form submitted
- **Check**:
  1. Verify trigger is turned on (check flow status)
  2. Confirm Form ID is correct
  3. Check connection is valid (re-authenticate if needed)
  4. Verify form is not in draft mode
- **Solution**:
  1. Test with sample form submission
  2. Check flow run history for errors
  3. Re-save trigger configuration
  4. Create new flow if issue persists

### Delayed Trigger

**Problem**: Flow triggers several minutes after submission
- **Check**: Service health, webhook delivery status
- **Solution**:
  1. Check Microsoft 365 Service Health dashboard
  2. Verify not using deprecated polling trigger
  3. Monitor for pattern (consistent delay vs intermittent)
  4. Contact Microsoft support if persistent

### Multiple Triggers for Same Response

**Problem**: Flow triggers multiple times for single response
- **Check**: Webhook may send duplicate notifications (rare)
- **Solution**: Implement deduplication logic (check Response ID in SharePoint before processing)

### Missing Responder Email

**Problem**: Responder field is null even though form should collect email
- **Check**:
  1. Form settings - verify "Record name" is enabled
  2. Check if anonymous submissions allowed
  3. Verify responder was signed in when submitting
- **Solution**:
  1. Disable anonymous responses in form settings
  2. Add email question to form as backup
  3. Add error handling for null responder

### Concurrency Issues

**Problem**: "CannotDisableTriggerConcurrency" error
- **Check**: Concurrency control was previously enabled
- **Solution**:
  1. Export flow as package
  2. Edit flow definition JSON
  3. Modify concurrency settings
  4. Re-import flow
- **Prevention**: Carefully plan concurrency before enabling

### Group Form Not Listed

**Problem**: Form doesn't appear in Form ID dropdown
- **Check**: Form created by Microsoft 365 Group
- **Solution**:
  1. Open form in browser
  2. Copy Form ID from URL (after `id=` parameter)
  3. Paste directly in Form Id field (don't use dropdown)
</troubleshooting>

</trigger>

---

## When a New Response is Submitted [DEPRECATED]

<trigger id="trigger-002" type="polling" frequency="daily" latency="24-hours">

<trigger_header>
**Type**: Polling (Check at interval)
**Frequency**: Once every 86,400 seconds (24 hours)
**Latency**: Up to 24 hours
**Operation ID**: GetFormResponses
**Status**: DEPRECATED (Do Not Use)
</trigger_header>

<description>
**⚠️ DEPRECATED - DO NOT USE FOR NEW FLOWS**

Legacy polling-based trigger that checks for new form responses once every 24 hours. This trigger has been superseded by the webhook-based trigger (CreateFormWebhook) which provides real-time notifications. The 24-hour polling delay makes this trigger unsuitable for most automation scenarios.
</description>

<parameters>
#### Required Parameters

**Form Id** (`string`)
- Same as current trigger
- Form identifier for monitoring

**Note**: Parameter structure identical to current trigger, but polling behavior is vastly different.
</parameters>

<behavior>
**Trigger Mechanism**: Polling (pull at interval)
- Power Automate checks Microsoft Forms service every 86,400 seconds (24 hours)
- Significant delay between submission and flow execution

**Batch Size**: All responses since last poll
- Can trigger with multiple responses if several submitted since last check
- Unpredictable batch sizes

**Polling Interval**: 86,400 seconds (24 hours)
- Fixed, cannot be adjusted
- Extremely long delay for most use cases

**Why Deprecated**:
- 24-hour delay unacceptable for most automation scenarios
- Webhook trigger provides instant notifications
- Polling consumes unnecessary resources
- No advantages over webhook-based trigger
</behavior>

<outputs>
Same structure as current trigger, but timing and batching differ significantly.
</outputs>

<limitations>
<limitation id="lim-trigger-deprecated-001" severity="critical">
**24-Hour Polling Delay**: Flow only triggers once per day
- **Impact**: Responses processed up to 24 hours after submission
- **Workaround**: Use current webhook-based trigger instead
- **Affected Scenarios**: Any scenario requiring timely response processing
</limitation>

<limitation id="lim-trigger-deprecated-002" severity="high">
**Deprecated Status**: May be removed in future Power Automate updates
- **Impact**: Flows using this trigger may break without warning
- **Workaround**: Migrate to current trigger immediately
- **Migration**: Create new trigger, test, delete old trigger
</limitation>
</limitations>

<filtering>
Not applicable - trigger should not be used.
</filtering>

<use_cases>
**None Recommended** - Use current webhook trigger for all scenarios.

Historical use cases (before webhook trigger availability):
- Batch processing of daily responses
- Low-priority feedback collection
- Non-time-sensitive surveys

**Migration Path**: Replace with current webhook trigger for all existing flows.
</use_cases>

<best_practices>
## Migration Best Practice

1. **Immediate Migration**: Replace deprecated trigger with current webhook trigger
   - **Why**: Avoid potential breakage when trigger removed
   - **How**:
     1. Note current flow logic
     2. Create new flow with current trigger
     3. Copy actions from old flow
     4. Test new flow thoroughly
     5. Disable old flow
     6. Delete old flow after successful migration

2. **Do Not Use**: Never create new flows with deprecated trigger
   - **Why**: Unsupported and will be removed
   - **How**: Always select trigger labeled "When a new response is submitted" (current)
</best_practices>

<example>
**No examples provided** - Do not use this trigger.

For migration example, see current trigger documentation.
</example>

<performance_impact>
Significant negative impact:
- Polling every 24 hours wastes resources
- Delays response processing unacceptably
- No performance benefits vs webhook trigger
</performance_impact>

<related_triggers>
### Replacement Trigger
- **[When a new response is submitted (CURRENT)](#trigger-001)**: Use this instead
  - Migration: Copy flow logic to new flow with current trigger
  - Benefits: Real-time vs 24-hour delay, webhook vs polling

### Migration Instructions
1. Open flow using deprecated trigger
2. Create new flow with current webhook trigger
3. Copy all actions from old flow to new flow
4. Update any action parameters referencing trigger output
5. Test new flow with sample form submission
6. Verify behavior matches expectations
7. Turn off old flow
8. Monitor new flow for 1 week
9. Delete old flow after successful validation
</related_triggers>

<troubleshooting>
**Primary Issue**: Using deprecated trigger

**Solution**: Migrate to current webhook trigger immediately

**If experiencing issues**:
1. Do not attempt to fix - trigger is deprecated
2. Create new flow with current trigger
3. Migrate flow logic
4. Delete old flow
</troubleshooting>

</trigger>

---

<related_docs>
- **Overview**: [overview.md](./overview.md) - Connector limitations and capabilities
- **Actions**: [actions.md](./actions.md) - Available actions for this connector
- **Official Docs**: https://learn.microsoft.com/en-us/connectors/microsoftforms/
- **Troubleshooting**: https://learn.microsoft.com/en-us/power-automate/forms/troubleshoot-issues
</related_docs>
