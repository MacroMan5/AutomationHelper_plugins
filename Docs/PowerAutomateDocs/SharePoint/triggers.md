# SharePoint - Triggers

---
type: connector-triggers
connector_name: SharePoint
trigger_count: 13
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [sharepoint, list, library, file, item, trigger, webhook, syntex]
trigger_types: [instant, webhook, polling]
---

<trigger_summary>
**Total Triggers**: 13 (11 automated + 2 instant)

**Categories**:
- File Triggers: 5 (created, modified, deleted, classified, properties only)
- Item Triggers: 4 (created, modified, deleted, changed)
- Hub Site Triggers: 1 (join approval)
- Instant Triggers: 2 (selected file/item)

**Most Used**:
1. When a file is created or modified (properties only) - General file monitoring
2. When an item is created or modified - General list monitoring
3. When a file is created (properties only) - New file tracking
4. For a selected file/item - User-initiated workflows

**API Rate Limit**: 600 calls per 60 seconds per connection
**Permissions**: Site collection admin required for deletion triggers
</trigger_summary>

For complete detailed documentation of all 13 SharePoint triggers including parameters, outputs, limitations, best practices, and examples, see the comprehensive triggers documentation.

## Quick Reference

### File Monitoring
- **When a file is created (properties only)** - New files only
- **When a file is created or modified (properties only)** - New and changed files (most common)
- **When a file is deleted** - File deletions (admin only)
- **When classified by Syntex** - AI classification events

### List Monitoring
- **When an item is created** - New items only
- **When an item is created or modified** - New and changed items (most common)
- **When an item is deleted** - Item deletions (admin only)
- **When an item or file is modified** - Modifications only (excludes creates)

### Manual Triggers
- **For a selected file** - User right-click on file
- **For a selected item** - User right-click on item

### Governance
- **When site requests hub join** - Hub site governance

## Key Limitations

<limitation id="lim-summary-001" severity="critical">
**Deletion Triggers**: Only site collection administrators can use deletion triggers
</limitation>

<limitation id="lim-summary-002" severity="high">
**API Rate Limit**: 600 API calls per 60 seconds per connection across all operations
</limitation>

<limitation id="lim-summary-003" severity="high">
**Large Lists**: Delegation limits apply to lists with >5000 items
</limitation>

<limitation id="lim-summary-004" severity="medium">
**Custom Templates**: Announcements, Contacts, Events, Tasks list templates unsupported in flows
</limitation>

## Best Practices Summary

1. **Use Properties-Only Triggers**: Unless file content specifically needed
2. **Folder Filtering**: Scope triggers to specific folders for performance
3. **Column Limiting**: Use "Limit Columns by View" to reduce payload
4. **Monitor Rate Limits**: Add delays in high-volume scenarios
5. **Indexed Columns**: Use indexed columns for large list filtering
