# Schedule Connector

## Overview
**Triggers**: 1
**Actions**: 2

The Schedule connector provides time-based triggers and delay actions for flow timing control.

## Trigger

### Recurrence
**Description**: Triggers flow on specified schedule
**Parameters**:
- Interval (required) - Numeric value
- Frequency (required) - Second, Minute, Hour, Day, Week, Month
- Time zone (optional)
- Start time (optional)
- At these hours (optional) - For Day/Week/Month
- At these minutes (optional) - For Day/Week/Month
- On these days (optional) - For Week/Month

**Frequency Options**:
- **Second**: 1-59 seconds (not recommended for production)
- **Minute**: 1-59 minutes
- **Hour**: 1-23 hours
- **Day**: 1-365 days
- **Week**: 1-52 weeks
- **Month**: 1-12 months

**Use Cases**:
- Batch processing
- Scheduled reports
- Regular data sync
- Cleanup tasks
- Monitoring checks

**Examples**:

**Every 5 minutes**:
```
Interval: 5
Frequency: Minute
```

**Daily at 9 AM EST**:
```
Interval: 1
Frequency: Day
Time zone: Eastern Standard Time
At these hours: 9
At these minutes: 0
```

**Every Monday at 8 AM**:
```
Interval: 1
Frequency: Week
On these days: Monday
At these hours: 8
At these minutes: 0
```

**Monthly on 1st at midnight**:
```
Interval: 1
Frequency: Month
At these hours: 0
At these minutes: 0
```

**Best Practices**:
- Use appropriate frequency (avoid seconds)
- Set time zone explicitly
- Consider business hours
- Plan for timezone changes (DST)
- Monitor for failures
- Implement idempotency

**Important Notes**:
- Minimum frequency varies by plan
- Flows timeout after 30 days by default
- Daylight Saving Time affects scheduling
- First run may not be immediate

---

## Actions

### Delay
**Description**: Pauses flow for specified duration
**Parameters**:
- Count (required) - Numeric value
- Unit (required) - Second, Minute, Hour, Day

**Maximum**: 30 days

**Use Cases**:
- Rate limiting compliance
- Polling intervals
- Processing delays
- Debouncing actions
- Batch timing

**Examples**:

**Wait 30 seconds**:
```
Count: 30
Unit: Second
```

**Wait 5 minutes**:
```
Count: 5
Unit: Minute
```

**Wait 1 hour**:
```
Count: 1
Unit: Hour
```

**Best Practices**:
- Use shortest necessary delay
- Consider timeout limits
- Document why delay is needed
- Avoid delays in loops (causes long runs)
- Use Delay until for specific times

**Warning**: Long delays count toward flow execution time

---

### Delay until
**Description**: Pauses until specific date/time
**Parameters**:
- Timestamp (required) - ISO 8601 format

**Format**: YYYY-MM-DDTHH:mm:ssZ

**Use Cases**:
- Schedule for specific time
- Business hours enforcement
- Embargo periods
- Timed releases
- SLA enforcement

**Examples**:

**Wait until specific date/time**:
```
Timestamp: 2025-12-31T23:59:59Z
```

**Wait until tomorrow 9 AM**:
```
Timestamp: @{addDays(utcNow(), 1, 'yyyy-MM-ddT09:00:00Z')}
```

**Wait until next business day**:
```
Use expression to calculate next weekday at 9 AM
```

**Best Practices**:
- Use UTC or specify timezone
- Validate timestamp is in future
- Consider timezone conversions
- Handle past timestamps (flow continues immediately)
- Document expected wait duration

---

## Schedule Patterns

### Pattern 1: Regular Polling
```
Recurrence (every 5 min) → Check for new items → Process → Complete
```

### Pattern 2: Business Hours Only
```
Recurrence (every hour) → Condition (is business hours?) → If yes: Process
```

### Pattern 3: Batch with Delay
```
Trigger → Apply to each → Action → Delay (rate limiting) → Next item
```

### Pattern 4: Scheduled Report
```
Recurrence (daily 8 AM) → Get data → Format report → Send email
```

### Pattern 5: Retry with Delay
```
Do until (success OR max retries)
  → Action
  → If failed: Delay (30 seconds)
  → Retry
```

### Pattern 6: Time-based Release
```
Trigger → Create content → Delay until (publish time) → Publish
```

## Time Zone Reference

**Common Time Zones**:
- UTC - Coordinated Universal Time
- Eastern Standard Time - EST (UTC-5)
- Central Standard Time - CST (UTC-6)
- Mountain Standard Time - MST (UTC-7)
- Pacific Standard Time - PST (UTC-8)
- GMT Standard Time - GMT (UTC+0)
- Central Europe Standard Time - CET (UTC+1)

**Important**: Daylight Saving Time automatically adjusts for most zones

## Date/Time Expressions

### Get Current Time
```
utcNow() → 2025-10-31T15:30:00.0000000Z
```

### Add Time
```
addDays(utcNow(), 1) → Tomorrow same time
addHours(utcNow(), 2) → 2 hours from now
addMinutes(utcNow(), 30) → 30 minutes from now
```

### Subtract Time
```
addDays(utcNow(), -1) → Yesterday
addHours(utcNow(), -5) → 5 hours ago
```

### Convert Time Zone
```
convertTimeZone(utcNow(), 'UTC', 'Eastern Standard Time')
```

### Format Time
```
formatDateTime(utcNow(), 'yyyy-MM-dd HH:mm:ss')
```

### Get Day of Week
```
dayOfWeek(utcNow()) → Integer (0=Sunday, 6=Saturday)
```

## Best Practices

### Scheduling
1. Use appropriate frequency for task
2. Avoid second-level frequencies in production
3. Set explicit time zones
4. Consider business hours
5. Plan for holidays/weekends
6. Monitor for skipped runs

### Delays
1. Use shortest necessary delay
2. Document delay purpose
3. Avoid long delays in loops
4. Consider flow timeout limits
5. Use Delay until for specific times
6. Plan for timezone differences

### Reliability
1. Implement error handling
2. Make flows idempotent
3. Log execution times
4. Monitor for failures
5. Handle daylight saving changes
6. Test across time zones

### Performance
1. Batch operations when possible
2. Avoid excessive polling
3. Use webhooks over polling when available
4. Consider concurrency for parallel work
5. Optimize delay durations

## Common Pitfalls

1. **Too frequent recurrence** - Causes throttling
2. **No timezone specified** - Unexpected timing
3. **Long delays in loops** - Flow timeouts
4. **No error handling** - Silent failures
5. **Not idempotent** - Duplicate processing
6. **Ignoring DST** - Timing issues twice per year
7. **Past timestamps in Delay until** - Continues immediately
8. **No logging** - Hard to debug timing issues

## Debugging

### Check Execution History
- Verify trigger fire times
- Check delay durations
- Review timezone conversions
- Identify skipped runs

### Test Scheduling
1. Create test flow with short interval
2. Verify timezone handling
3. Check business hours logic
4. Test delay calculations
5. Monitor for consistency

### Common Issues
- **Flow not triggering**: Check recurrence settings, verify enabled
- **Wrong timing**: Verify timezone, check DST
- **Skipped runs**: Check for errors, verify plan limits
- **Delays not working**: Verify timestamp format, check calculations
