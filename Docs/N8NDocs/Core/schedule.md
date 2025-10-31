# Schedule Trigger Node Overview

---
type: node-overview
node_name: Schedule Trigger
node_type: core
category: trigger
auth_required: false
version: 1.0
last_updated: 2025-10-31
keywords: [schedule, trigger, cron, timer, automation, recurring, interval, periodic]
related_nodes: [Wait, Execute Workflow, HTTP Request]
rate_limits:
  service_rate_limit: none
  n8n_limit: Based on cron expression frequency
official_docs_url: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
npm_package: n/a (built-in)
---

<official_docs>
https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
https://docs.n8n.io/workflows/components/
</official_docs>

<description>
The Schedule Trigger node enables time-based workflow automation by triggering workflows at specified intervals, times, or according to cron expressions. It supports flexible scheduling options including simple intervals (every X minutes/hours/days), specific times, and advanced cron patterns for complex scheduling requirements like "every weekday at 9 AM" or "first Monday of each month."
</description>

<capabilities>
## Core Capabilities
- Trigger workflows at specified intervals
- Execute workflows at specific times daily/weekly/monthly
- Support for cron expressions (advanced scheduling)
- Timezone-aware scheduling
- Skip executions if previous run still active
- Multiple trigger modes (Days, Hours, Minutes, Cron, Seconds)

## Supported Operations
- **Interval Scheduling**: Every X seconds/minutes/hours/days
- **Time-Based Scheduling**: Specific time daily (e.g., 9:00 AM every day)
- **Weekday Scheduling**: Specific days of week at specific times
- **Cron Scheduling**: Advanced patterns (first Monday, last Friday, etc.)
- **Custom Patterns**: Complex schedules via cron expressions

## Integration Features
- **Timezone Support**: Execute in any timezone
- **Overlap Prevention**: Skip if previous execution still running
- **Manual Testing**: Test trigger without waiting for schedule
- **Flexible Intervals**: From seconds to months
- **Multiple Schedules**: Use multiple Schedule nodes for different patterns
</capabilities>

<rate_limits>
## Execution Limits

**N8N Platform Limits**
- **Minimum Interval**: 1 second (not recommended for production)
- **Recommended Minimum**: 1 minute for stability
- **Max Executions**: Limited by N8N plan (cloud) or resources (self-hosted)
- **Concurrent Executions**: One at a time (by default with overlap prevention)

**Scheduling Frequency**
- **Seconds Mode**: Every 1-60 seconds
- **Minutes Mode**: Every 1-60 minutes
- **Hours Mode**: Every 1-24 hours
- **Days Mode**: Every 1-365 days
- **Cron Mode**: Custom frequency via cron expression

**Resource Considerations**
- High-frequency schedules (every second) can overload server
- Consider workflow execution time vs schedule frequency
- Use overlap prevention to avoid concurrent executions

## Execution Behavior

**Overlap Handling**
- **Default**: Skip execution if previous run still active
- **Configurable**: Can allow concurrent executions
- **Best Practice**: Keep overlap prevention enabled

**Missed Executions**
- If N8N is down during scheduled time, execution is skipped (not queued)
- When N8N restarts, next scheduled time is calculated
- No automatic catch-up for missed schedules
</rate_limits>

<critical_limitations>
## Scheduling Precision

<limitation id="lim-001" severity="medium">
**No Sub-Second Precision**: Cannot schedule more frequently than once per second

- **Impact**: Cannot trigger multiple times per second
- **Scope**: All scheduling modes
- **Workaround**: Use external service for sub-second triggers via webhook
- **Affected Operations**: All schedules

**Example Scenario**: Need to trigger every 500ms for high-frequency monitoring
</limitation>

<limitation id="lim-002" severity="high">
**Missed Executions Not Recovered**: If N8N is down, scheduled executions are lost

- **Impact**: Critical scheduled tasks may be skipped
- **Scope**: All schedules during downtime
- **Workaround**: Implement catch-up logic in workflow, use external monitoring
- **Affected Operations**: All scheduled workflows

**Example Scenario**: Server restart during scheduled 3 AM backup means backup is skipped that day
</limitation>

## Timezone Limitations

<limitation id="lim-003" severity="medium">
**Daylight Saving Time Complexity**: DST transitions may affect exact execution times

- **Impact**: Schedules may execute at unexpected times during DST changes
- **Scope**: Timezone-aware schedules
- **Workaround**: Use UTC timezone, add logic to handle DST in workflow
- **Affected Operations**: Non-UTC timezone schedules

**Example Scenario**: "9 AM daily" schedule shifts to 8 AM or 10 AM during DST transition
</limitation>

## Execution Control

<limitation id="lim-004" severity="low">
**No Dynamic Schedule Modification**: Cannot change schedule during execution

- **Impact**: Schedule changes require workflow edit and reactivation
- **Scope**: Runtime schedule modification
- **Workaround**: Use multiple workflows with different schedules, activate/deactivate as needed
- **Affected Operations**: All schedules

**Example Scenario**: Cannot temporarily increase frequency during business hours automatically
</limitation>

<limitation id="lim-005" severity="medium">
**Single Schedule Per Node**: Each Schedule node supports only one pattern

- **Impact**: Complex schedules require multiple nodes or cron expressions
- **Scope**: Multi-pattern scheduling
- **Workaround**: Use multiple Schedule nodes or complex cron expressions
- **Affected Operations**: Multi-pattern schedules

**Example Scenario**: "Weekdays at 9 AM and weekends at 11 AM" requires two Schedule nodes
</limitation>

## Cron Expression Limitations

<limitation id="lim-006" severity="low">
**Non-Standard Cron Syntax**: Uses specific cron format (may differ from Linux cron)

- **Impact**: Linux cron expressions may need adjustment
- **Scope**: Cron mode
- **Workaround**: Test cron expressions in N8N, use cron validation tools
- **Affected Operations**: Cron-based schedules

**Example Scenario**: Some advanced cron features from Linux cron may not work
</limitation>
</critical_limitations>

<authentication>
## Authentication

**N8N Schedule Trigger node does not require authentication.**

The Schedule node is a built-in trigger that operates entirely within N8N. It does not connect to external services and requires no credentials.

## Configuration Only

Schedule configuration includes:
- **Trigger Interval**: When to run (seconds/minutes/hours/days/cron)
- **Timezone**: What timezone to use for scheduling
- **Trigger Times**: Specific times for daily/weekly schedules

## Access Control

Access to Schedule triggers is controlled by:
- N8N user permissions (who can edit workflows)
- Workflow activation status (only active workflows trigger)
- Server availability (N8N must be running)
</authentication>

<common_use_cases>
## 1. Daily Reports and Summaries

**Description**: Generate and send daily reports at specific times

**Typical Workflow**:
```
Schedule (Daily 8:00 AM) → Database Query → Code (aggregate data) → Send Email
```

**Configuration**:
- **Mode**: Days of Month
- **Hour**: 8
- **Minute**: 0
- **Timezone**: America/New_York

**Use Case**: Daily sales report sent to management every morning

**Best For**: Daily/weekly/monthly reports, summaries, digests

---

## 2. Periodic Data Synchronization

**Description**: Sync data between systems at regular intervals

**Typical Workflow**:
```
Schedule (Every 15 minutes) → HTTP Request (fetch data) → Database → Update records
```

**Configuration**:
- **Mode**: Minutes
- **Value**: 15
- **Overlap**: Skip if previous execution running

**Use Case**: Sync inventory from e-commerce platform to internal database

**Best For**: Real-time-ish data syncing, API polling, database synchronization

---

## 3. Automated Backups

**Description**: Create backups of databases or files on schedule

**Typical Workflow**:
```
Schedule (Daily 3:00 AM) → Database Backup → Compress → Upload to S3 → Notification
```

**Configuration**:
- **Mode**: Days of Month
- **Hour**: 3
- **Minute**: 0
- **Timezone**: UTC
- **Overlap**: Must skip (critical for backups)

**Use Case**: Daily database backup at low-traffic time

**Best For**: Backups, maintenance tasks, cleanup operations

---

## 4. Monitoring and Health Checks

**Description**: Regularly check system health and alert on issues

**Typical Workflow**:
```
Schedule (Every 5 minutes) → HTTP Request (health check) → IF (check status) → Alert if down
```

**Configuration**:
- **Mode**: Minutes
- **Value**: 5
- **Overlap**: Skip if checking

**Use Case**: Monitor website uptime, alert if down

**Best For**: Uptime monitoring, health checks, status polling

---

## 5. Scheduled Social Media Posts

**Description**: Post content to social media at optimal times

**Typical Workflow**:
```
Schedule (Weekdays 10 AM & 2 PM) → Database (get queued posts) → Twitter API → Mark posted
```

**Configuration**:
- **Mode**: Cron
- **Expression**: `0 10,14 * * 1-5` (10 AM and 2 PM weekdays)
- **Timezone**: America/Los_Angeles

**Use Case**: Automated social media posting at peak engagement times

**Best For**: Content scheduling, social media automation, marketing campaigns

---

## 6. Cleanup and Maintenance Tasks

**Description**: Delete old data, clear caches, perform maintenance

**Typical Workflow**:
```
Schedule (Weekly Sunday 2 AM) → Database → Delete old records → Vacuum/Optimize → Log
```

**Configuration**:
- **Mode**: Cron
- **Expression**: `0 2 * * 0` (Sunday at 2 AM)
- **Timezone**: UTC

**Use Case**: Weekly database cleanup and optimization

**Best For**: Data retention policies, cache clearing, log rotation

</common_use_cases>

<best_practices>
## Scheduling Strategy

### Frequency Selection
1. **Choose Appropriate Interval**: Match business needs, not technical capability
   - **Why**: Avoid unnecessary executions, reduce server load
   - **How**: "Near real-time" usually means 5-15 minutes, not seconds

2. **Consider Execution Time**: Schedule frequency > execution duration
   - **Why**: Prevent overlapping executions
   - **How**: If workflow takes 10 minutes, schedule at least 15 minutes apart
   - **Example**: 30-minute data sync for 20-minute average execution

3. **Use Cron for Complex Patterns**: Business hours, specific days, etc.
   - **Why**: More flexible than simple intervals
   - **Example**: `0 9-17 * * 1-5` (every hour 9 AM-5 PM weekdays)

### Timezone Management
1. **Use UTC for Consistency**: Avoid DST complications
   - **Why**: UTC never changes, predictable behavior
   - **When**: Server operations, international teams, time-sensitive tasks

2. **Use Local Timezone for User-Facing**: Match user expectations
   - **Why**: Reports/notifications arrive at expected local time
   - **When**: Email reports, notifications, user-facing automations

3. **Document Timezone Choice**: Add note in workflow
   - **Why**: Clear for team members, future debugging
   - **How**: Use Sticky Note node to document

### Overlap Prevention
1. **Always Enable Overlap Prevention**: Except for very fast workflows
   - **Why**: Prevents resource exhaustion, ensures sequential execution
   - **How**: Keep "Skip if workflow is busy" enabled (default)

2. **Monitor for Skipped Executions**: Track when schedules are skipped
   - **Why**: Indicates workflow is too slow for schedule frequency
   - **How**: Add logging, check execution history regularly

## Performance Optimization

### Resource Management
1. **Batch Operations**: Process multiple items per execution
   - **Why**: More efficient than per-item schedules
   - **Example**: Process all pending orders vs. one order per minute

2. **Off-Peak Scheduling**: Run heavy tasks during low-traffic periods
   - **Why**: Doesn't impact user-facing services
   - **When**: Backups, reports, bulk operations
   - **Time**: Early morning (2-5 AM) in target timezone

3. **Stagger Multiple Schedules**: Don't run all workflows at same time
   - **Why**: Prevents server overload
   - **How**: 9:00, 9:15, 9:30 instead of all at 9:00

### Error Handling
1. **Add Error Handling**: Wrap workflow in try-catch pattern
   - **Why**: Scheduled workflows run unattended
   - **How**: Use Scope with "Continue On Fail", send error notifications

2. **Implement Logging**: Track all scheduled executions
   - **Why**: Audit trail, debugging, monitoring
   - **How**: Log start time, end time, status, item count

3. **Alert on Failures**: Send notifications for critical failures
   - **Why**: Immediate awareness of issues
   - **How**: Email/Slack on error, include error details

## Reliability

### Idempotency
1. **Design Idempotent Workflows**: Safe to run multiple times
   - **Why**: Handles duplicate triggers gracefully
   - **Example**: Check if already processed before inserting

2. **Use Unique Identifiers**: Prevent duplicate processing
   - **How**: Check database for existing records by ID before creating

### Missed Execution Handling
1. **Implement Catch-Up Logic**: Detect and handle missed runs
   - **Why**: N8N doesn't replay missed schedules
   - **How**: Check last execution time, process backlog if gap found
   - **Example**:
```javascript
// In Code node
const lastRun = await getLastExecutionTime();
const now = new Date();
const hoursSinceLastRun = (now - lastRun) / (1000 * 60 * 60);

if (hoursSinceLastRun > 25) { // Expected every 24 hours
  // Catch-up logic here
  console.log('Missed execution detected, processing backlog');
}
```

2. **External Monitoring**: Use uptime monitoring for critical schedules
   - **Why**: Alert if N8N is down or schedules aren't running
   - **How**: Services like UptimeRobot, Pingdom, external health check

### Testing
1. **Test Before Activating**: Use "Execute Workflow" button
   - **Why**: Verify workflow works before schedule kicks in
   - **How**: Click "Execute Workflow" in N8N editor

2. **Start with Longer Intervals**: Test with hourly before going to per-minute
   - **Why**: Easier to monitor, less impact if bugs exist
   - **How**: Start with 1 hour, reduce to 15 min, then 5 min if needed

## Cron Expression Best Practices

### Cron Syntax Guide
```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-7, 0 and 7 are Sunday)
│ │ │ │ │
* * * * *
```

### Common Patterns
```
0 9 * * 1-5          Every weekday at 9 AM
0 */2 * * *          Every 2 hours
0 0 1 * *            First day of every month at midnight
0 9 * * 1            Every Monday at 9 AM
*/15 * * * *         Every 15 minutes
0 9,12,15,18 * * *   At 9 AM, 12 PM, 3 PM, 6 PM daily
0 2 * * 0            Every Sunday at 2 AM
```

### Validation
1. **Use Cron Validation Tools**: Test expressions before deploying
   - **Tools**: crontab.guru, cron expression validator
   - **Why**: Avoid syntax errors and unexpected behavior

2. **Document Complex Patterns**: Add comment explaining cron
   - **Example**: "0 9 15 * * - Runs 15th of every month at 9 AM"
</best_practices>

<troubleshooting>
## Common Issues

### Schedule Not Triggering

<error id="err-001" http_code="N/A">
- **Symptom**: Workflow never executes on schedule
- **Cause**: Workflow not activated, N8N not running, invalid cron expression
- **Immediate Fix**:
  1. Verify workflow is activated (toggle in top-right)
  2. Check N8N service is running
  3. Validate cron expression with online tool
  4. Check N8N logs for errors
- **Prevention**:
  - Always activate after editing
  - Monitor N8N service health
  - Test cron expressions before deploying
- **N8N Check**: Look for active indicator (green dot) on workflow
</error>

### Executions Being Skipped

<error id="err-002" http_code="N/A">
- **Symptom**: Schedule triggers less frequently than configured
- **Cause**: Previous execution still running (overlap prevention active)
- **Immediate Fix**:
  1. Check execution history for long-running executions
  2. Optimize workflow to complete faster
  3. Increase schedule interval
  4. Disable overlap prevention (not recommended)
- **Prevention**:
  - Schedule frequency > execution duration
  - Optimize slow workflows
  - Use batching for efficiency
- **N8N Logs**: Shows "Skipped execution" in logs
</error>

### Wrong Execution Time

<error id="err-003" http_code="N/A">
- **Symptom**: Workflow executes at unexpected time
- **Cause**: Timezone mismatch, DST transition, incorrect cron expression
- **Immediate Fix**:
  1. Verify timezone setting in Schedule node
  2. Check if DST just occurred
  3. Validate cron expression matches intent
  4. Test with UTC timezone
- **Prevention**:
  - Use UTC to avoid DST issues
  - Document expected execution times
  - Test schedule in target timezone
- **N8N Setting**: Check "Timezone" parameter in node
</error>

### Cron Expression Error

<error id="err-004" http_code="N/A">
- **Symptom**: "Invalid cron expression" error
- **Cause**: Syntax error in cron pattern
- **Immediate Fix**:
  1. Validate expression on crontab.guru
  2. Check for typos (spaces, special characters)
  3. Verify field order (minute hour day month weekday)
  4. Use known-good pattern as template
- **Prevention**:
  - Test cron expressions before deploying
  - Use online validators
  - Reference common patterns
- **Example**: `0 9 * * *` (valid) vs `9 0 * * *` (wrong order)
</error>

### Missed Executions After Restart

<error id="err-005" http_code="N/A">
- **Symptom**: Schedule didn't execute while N8N was down
- **Cause**: N8N doesn't queue missed executions
- **Immediate Fix**:
  1. Accept that missed executions are lost
  2. Manually trigger workflow if needed
  3. Implement catch-up logic for critical workflows
- **Prevention**:
  - Ensure N8N high availability
  - Implement catch-up logic in workflow
  - Use external monitoring and alerts
- **N8N Behavior**: Expected behavior, not a bug
</error>

## Diagnostic Steps

1. **Check Workflow Active Status**
   - Look for green dot/active indicator
   - Verify in workflow list
   - Check activation toggle

2. **View Execution History**
   - Check "Executions" tab
   - Look for scheduled executions
   - Review execution times and statuses

3. **Validate Schedule Configuration**
   - Review trigger interval/cron expression
   - Confirm timezone setting
   - Test cron with validator tool

4. **Check N8N Logs**
   - View N8N server logs
   - Look for schedule-related errors
   - Check for skipped execution messages

5. **Test Manually**
   - Use "Execute Workflow" button
   - Verify workflow logic works
   - Check execution completes successfully

6. **Monitor Over Time**
   - Watch for first scheduled execution
   - Verify timing matches expectation
   - Check multiple executions for consistency
</troubleshooting>

<related_docs>
## Documentation Structure

- **Cron Syntax**: Reference external cron documentation for advanced patterns
- **Workflow Design**: Best practices for scheduled workflows

## Related Nodes

- **Wait** - Add delays within workflows (not a trigger)
- **Execute Workflow** - Trigger other workflows (can be used with Schedule)
- **[HTTP Request](./http-request.md)** - Common in scheduled data fetching
- **[Code](./code.md)** - Implement catch-up logic, complex scheduling decisions

## External Resources

- **Official N8N Schedule Docs**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
- **Cron Expression Validator**: https://crontab.guru/
- **N8N Community**: https://community.n8n.io/
- **Workflow Examples**: https://n8n.io/workflows?search=schedule
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 95% (Core functionality, cron patterns, best practices documented)
- **Validation Status**: Validated against N8N scheduling patterns
- **Next Review**: 2025-11-30
- **N8N Version**: Compatible with all recent versions
</metadata_summary>
