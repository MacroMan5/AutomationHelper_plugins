# OneDrive for Business - Triggers

---
type: connector-triggers
connector_name: OneDrive for Business
trigger_count: 5
deprecated_count: 4
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [onedrive, file, folder, polling, instant, properties]
trigger_types: [polling, instant]
---

<trigger_summary>
**Total Triggers**: 5 current (4 deprecated)

**Categories**:
- File Creation: 1 trigger (with content) + 1 trigger (properties only)
- File Modification: 1 trigger (with content) + 1 trigger (properties only)
- Instant Triggers: 1 trigger (manual file selection)

**Most Used**:
1. When a file is created (properties only) - New file monitoring without content
2. When a file is modified (properties only) - Change detection with metadata
3. For a selected file - User-initiated workflows

**Critical Limitation**: Files larger than 50MB are SKIPPED by all polling triggers
**API Rate Limit**: 100 calls per 60 seconds per connection
**Polling Issues**: May have problems when >30 pending changes between polls
</trigger_summary>

For complete detailed documentation of all 5 OneDrive for Business triggers including parameters, outputs, limitations, best practices, and examples, see the comprehensive triggers documentation below.

---

## File Creation Triggers (2 Triggers)

<trigger id="trigger-onedrive-001" operation_id="OnNewFileV2" type="polling" complexity="medium">
### When a File is Created

**Description**: Triggers a flow when a new file is created in a folder (returns file content)

**Operation ID**: `OnNewFileV2`

**Trigger Type**: Polling

**Parameters**:
- **Folder** (`folderId`, string, required): Folder identifier to monitor
- **Include subfolders** (`includeSubfolders`, boolean, optional): Monitor child folders recursively
- **Infer Content Type** (`inferContentType`, boolean, optional): Auto-detect MIME type for downstream actions

**Returns**: Binary file content with inferred content-type header

**Polling Interval**: Configured per flow (typically 1-3 minutes)

**Limitations**:
<limitation id="lim-onedrive-trigger-001" severity="critical">
Files larger than 50 MB will be skipped and not returned by this trigger
</limitation>

<limitation id="lim-onedrive-trigger-002" severity="high">
Files moved within OneDrive are NOT considered "new" and will not trigger this flow
</limitation>

<limitation id="lim-onedrive-trigger-003" severity="high">
May have issues when more than approximately 30 pending changes occur between polls
</limitation>

**Best Practices**:
- Enable "Infer Content Type" for proper file handling downstream
- Use properties-only variant if file content not immediately needed
- Implement file size validation before downstream processing
- Add delay actions if processing triggers multiple rapid saves

**Use Cases**:
- Automated document processing (OCR, conversion)
- File content analysis and classification
- Immediate content-based workflows

**Example Flow**:
```
When file created → Get file content → Parse PDF → Extract data → Save to database
```

**Troubleshooting**:
- **Not firing**: Check folder path, verify file <50MB, confirm API limits not exceeded
- **Missing files**: Likely over 50MB limit; implement alternate detection method
- **Multiple executions**: Normal for rapid saves; add idempotency logic

**Throttle Impact**: High (bandwidth consumption + API call)
</trigger>

---

<trigger id="trigger-onedrive-002" operation_id="OnNewFilesV2" type="polling" complexity="low">
### When a File is Created (Properties Only)

**Description**: Triggers flow for newly created files with metadata only (no content download)

**Operation ID**: `OnNewFilesV2`

**Trigger Type**: Polling

**Parameters**:
- **Folder** (`folderId`, string, required): Folder identifier
- **Include subfolders** (`includeSubfolders`, boolean, optional): Recursive monitoring
- **Max File Count** (`maxFileCount`, integer, optional): 1-100 items per trigger run

**Returns**: Array of `BlobMetadata` objects
```json
[
  {
    "Id": "string",
    "Name": "string",
    "NameNoExt": "string",
    "DisplayName": "string",
    "Path": "string",
    "LastModified": "datetime",
    "Size": "number",
    "MediaType": "string",
    "IsFolder": "boolean",
    "ETag": "string",
    "FileLocator": "string",
    "LastModifiedBy": "object"
  }
]
```

**Polling Interval**: Configured per flow

**Limitations**:
<limitation id="lim-onedrive-trigger-004" severity="critical">
Files larger than 50 MB will be skipped
</limitation>

<limitation id="lim-onedrive-trigger-005" severity="medium">
Split On setting may force individual item processing instead of batching
</limitation>

**Best Practices**:
- Use this variant when file content NOT needed (faster, lower bandwidth)
- Set appropriate Max File Count to balance latency vs batching
- Store file metadata for later retrieval if needed
- Ideal for notification, indexing, and metadata workflows

**Use Cases**:
- File inventory and cataloging
- Notification workflows (email on new upload)
- Metadata-based routing and tagging
- File naming validation

**Example Flow**:
```
When file created (properties) → Check filename pattern → Send notification → Update tracking list
```

**Performance Benefits**:
- No content download (faster execution)
- Lower bandwidth consumption
- Reduced throttling impact

**Throttle Impact**: Low (metadata only, no content transfer)
</trigger>

---

## File Modification Triggers (2 Triggers)

<trigger id="trigger-onedrive-003" operation_id="OnUpdatedFileV2" type="polling" complexity="medium">
### When a File is Modified

**Description**: Triggers a flow when a file is modified in a folder (returns file content)

**Operation ID**: `OnUpdatedFileV2`

**Trigger Type**: Polling

**Parameters**:
- **Folder** (`folderId`, string, required): Folder identifier
- **Include subfolders** (`includeSubfolders`, boolean, optional): Recursive monitoring
- **Infer Content Type** (`inferContentType`, boolean, optional): MIME type detection

**Returns**: Binary file content

**Filtering Behavior**: Makes best effort to filter uninteresting modification events (metadata-only changes like permissions, sharing)

**Limitations**:
<limitation id="lim-onedrive-trigger-006" severity="critical">
Files exceeding 50 MB are skipped
</limitation>

<limitation id="lim-onedrive-trigger-007" severity="high">
May fire multiple times for single edit session (Office auto-save behavior)
</limitation>

<limitation id="lim-onedrive-trigger-008" severity="high">
May have issues when >30 pending changes between polls
</limitation>

**Best Practices**:
- Implement duplicate detection (same file, same timestamp)
- Add delay actions to debounce rapid modifications
- Use approval checkpoints for critical workflows
- Consider file-based unit processing instead of entry-level triggers

**Use Cases**:
- Document version tracking
- Automated backup and sync workflows
- Change detection and audit logging
- Content-based reprocessing

**Example Flow**:
```
When file modified → Get content → Compare with previous version → Log changes → Notify team
```

**Troubleshooting**:
- **Multiple trigger fires**: Normal Office behavior; implement deduplication
- **Triggers on metadata changes**: Some metadata events may leak through filtering
- **Missing modifications**: Check 50MB limit, verify polling frequency

**Throttle Impact**: High (content download)
</trigger>

---

<trigger id="trigger-onedrive-004" operation_id="OnUpdatedFilesV2" type="polling" complexity="low">
### When a File is Modified (Properties Only)

**Description**: Triggers when file properties are modified (metadata only, no content)

**Operation ID**: `OnUpdatedFilesV2`

**Trigger Type**: Polling

**Parameters**:
- **Folder** (`folderId`, string, required)
- **Include subfolders** (`includeSubfolders`, boolean, optional)
- **Max File Count** (`maxFileCount`, integer, optional): 1-100 items per run

**Returns**: Array of `BlobMetadata` objects

**Filtering Behavior**: Filters uninteresting modification events (permissions-only, sharing-only changes)

**Limitations**:
<limitation id="lim-onedrive-trigger-009" severity="critical">
Files larger than 50 MB are skipped
</limitation>

<limitation id="lim-onedrive-trigger-010" severity="medium">
May trigger multiple times for automatic Office application changes
</limitation>

**Best Practices**:
- Lightweight alternative to content-based trigger
- Use for metadata management and tagging workflows
- Implement timestamp checking to avoid duplicates
- Monitor ETag changes for true content modifications

**Use Cases**:
- Metadata synchronization
- File rename detection
- Last modified timestamp tracking
- Tag and category management

**Example Flow**:
```
When file modified (properties) → Check if ETag changed → Update metadata in database
```

**Performance Benefits**:
- No content download
- Faster execution
- Lower API throttling impact

**Throttle Impact**: Low (metadata only)
</trigger>

---

## Instant Triggers (1 Trigger)

<trigger id="trigger-onedrive-005" operation_id="OnFileSelected" type="instant" complexity="low">
### For a Selected File

**Description**: Manual trigger for user-initiated workflows (Power Automate only)

**Operation ID**: `OnFileSelected`

**Trigger Type**: Instant (user-initiated from OneDrive context menu)

**Parameters**: None (user selects file via UI)

**Returns**:
```json
{
  "filePath": "string",
  "fileURL": "string",
  "user": {
    "id": "string",
    "email": "string",
    "displayName": "string"
  },
  "timestamp": "datetime"
}
```

**Availability**: Power Automate only (not available in Logic Apps)

**User Experience**: Right-click file in OneDrive → "Automate" → Select flow

**Limitations**:
<limitation id="lim-onedrive-trigger-011" severity="medium">
Flow must be in default environment to appear in OneDrive context menu
</limitation>

**Best Practices**:
- Provide clear flow naming for user recognition
- Add input validation for user-provided data
- Include confirmation or approval steps for destructive actions
- Use for ad-hoc processing workflows

**Use Cases**:
- Manual file processing (convert, compress, analyze)
- User-initiated file sharing or distribution
- On-demand report generation
- Ad-hoc file operations (move, copy, tag)

**Example Flow**:
```
For selected file → Get file properties → Convert to PDF → Save to SharePoint → Send email
```

**Throttle Impact**: Low (single user-initiated execution)
</trigger>

---

## Deprecated Triggers

<deprecated_triggers>
| Trigger Name | Operation ID | Status | Replacement |
|---|---|---|---|
| When a file is created | OnNewFile | Deprecated | OnNewFileV2 |
| When a file is created (properties only) | OnNewFiles | Deprecated | OnNewFilesV2 |
| When a file is modified | OnUpdatedFile | Deprecated | OnUpdatedFileV2 |
| When a file is modified (properties only) | OnUpdatedFiles | Deprecated | OnUpdatedFilesV2 |
</deprecated_triggers>

**Deprecation Note**: Triggers marked as 'deprecated' are no longer actively maintained. Strongly recommended to migrate to V2 versions for new applications.

**Migration Path**: V2 triggers offer same functionality with improved reliability and performance.

---

## Common Error Codes and Troubleshooting

<error id="err-onedrive-trigger-001" severity="critical">
**Error**: Files not triggering (>50MB)

**Cause**: File size exceeds 50MB skip threshold

**Solutions**:
1. Implement alternate detection method (scheduled polling via Get Files action)
2. Use SharePoint connector if files stored in SharePoint-backed OneDrive
3. Split large files before upload
4. Create manual trigger flow for large file processing

**Workaround Example**:
```
Schedule: Every 5 minutes
→ List files in folder (Get Files action)
→ Filter: Size > 50MB AND Created > LastRunTime
→ Process large files
```
</error>

<error id="err-onedrive-trigger-002" severity="high">
**Error**: Trigger firing multiple times for same file

**Causes**:
- Office applications auto-saving (Word, Excel)
- Rapid successive modifications
- Metadata changes triggering modification events

**Solutions**:
1. Implement deduplication logic (track processed file IDs with timestamps)
2. Add Delay action (30-60 seconds) before processing
3. Use approval checkpoints to prevent duplicate actions
4. Check ETag to verify actual content changes

**Deduplication Pattern**:
```
Trigger → Initialize variable (processedFiles array)
→ Condition: File ID not in processedFiles
→ Process file
→ Append File ID to processedFiles
```
</error>

<error id="err-onedrive-trigger-003" severity="high">
**Error**: ">30 pending changes" causing missed files

**Cause**: Polling frequency too low for high-volume folder

**Solutions**:
1. Reduce polling interval (increase frequency)
2. Distribute monitoring across multiple flows (subfolder-specific)
3. Implement backup detection via scheduled Get Files action
4. Use SharePoint connector for high-volume scenarios

**Recommendation**: "Flows do not rely solely on OneDrive connector's file changed detection" for critical workflows
</error>

<error id="err-onedrive-trigger-004" http_code="403" severity="high">
**Error**: Access denied / Policy blocking

**Causes**:
- Organizational policies blocking file downloads
- Device access controls restricting flow execution
- Network-based restrictions
- Conditional Access policies

**Solutions**:
1. Verify organizational policies allow connector access
2. Check Conditional Access settings in Azure AD
3. Review device compliance requirements
4. Test with properties-only triggers (may bypass download restrictions)
5. Contact IT admin for policy exceptions
</error>

<error id="err-onedrive-trigger-005" severity="medium">
**Error**: Trigger not appearing in OneDrive context menu

**Cause**: Flow not in default environment (Power Automate limitation)

**Solutions**:
1. Create flow in default environment
2. Export and import flow to default environment
3. Verify flow is published and enabled
4. Refresh OneDrive page after flow creation

**Note**: "For Flows that use the 'For a selected file' trigger, only those that are part of the default environment are listed"
</error>

<error id="err-onedrive-trigger-006" http_code="429" severity="critical">
**Error**: Too Many Requests - Throttling

**Cause**: Exceeded 100 API calls per 60 seconds per connection

**Solutions**:
1. Add Delay actions in loops (minimum 1 second)
2. Reduce polling frequency for triggers
3. Distribute load across multiple connections
4. Implement batch processing instead of item-by-item
5. Use properties-only triggers to reduce API call volume

**Throttle Calculation**:
```
Max flows per minute = 100 calls / (calls per flow execution)
Example: If flow makes 5 calls, max = 20 flow runs per minute
```
</error>

<error id="err-onedrive-trigger-007" severity="medium">
**Error**: Files moved within OneDrive triggering "created"

**Expected Behavior**: Files moved within OneDrive are NOT considered new

**Cause**: Misconception about trigger behavior

**Solution**: Implement separate logic for move detection if needed (compare file paths, check creation date vs modified date)
</error>

---

## Best Practices Summary

### Trigger Selection Strategy

**Use "Properties Only" When**:
- File content NOT immediately needed
- Metadata-based routing or notification workflows
- High-volume monitoring (reduce bandwidth)
- File size validation before content retrieval

**Use "With Content" When**:
- Immediate content processing required (OCR, parsing)
- No additional Get File Content action desired
- Low-volume, content-critical workflows

### Performance Optimization

1. **Minimize Content Downloads**: Use properties-only triggers when possible (faster, lower throttling)
2. **Folder Scoping**: Monitor specific subfolders instead of root (reduces polling overhead)
3. **Max File Count**: Set appropriate batch size (balance latency vs throughput)
4. **Polling Frequency**: Match business needs (faster polling = more API calls)
5. **Enable Content Type Inference**: Improves downstream action compatibility

### Reliability Patterns

1. **50MB Handling**:
   - Implement backup detection for large files
   - Add file size validation before processing
   - Use SharePoint connector for SharePoint-backed OneDrive
   - Create manual trigger flows for large file scenarios

2. **Duplicate Detection**:
   - Track processed file IDs with timestamps
   - Check ETag for content change verification
   - Implement delay actions (30-60s) to debounce rapid changes
   - Use approval gates for critical operations

3. **High-Volume Monitoring**:
   - Distribute monitoring across multiple flows (subfolder-specific)
   - Reduce polling frequency if >30 pending changes common
   - Implement scheduled Get Files action as backup
   - Consider SharePoint triggers for libraries with heavy traffic

4. **Error Handling**:
   - Add Scope actions with "Configure run after" for error isolation
   - Implement retry logic for transient failures (429, 500)
   - Log errors to tracking list or database
   - Send admin notifications for critical failures

### Multi-Tenant and Cross-Geo Constraints

<limitation id="lim-onedrive-trigger-012" severity="critical">
Cross-tenant and multi-geo access UNSUPPORTED. Both user and file must reside in same tenant and geographic region.
</limitation>

**Workaround**: Implement manual file transfer or use Azure Functions for cross-tenant scenarios

### Policy Awareness

<limitation id="lim-onedrive-trigger-013" severity="high">
Organizational policies may block file downloads, device access, or network-based restrictions affecting trigger functionality.
</limitation>

**Best Practice**: Test triggers with organizational policies applied before production deployment

---

## Common Workflow Patterns

### Pattern 1: New Document Processing
```
Trigger: When file created (properties only)
→ Condition: File extension = .pdf AND Size < 50MB
→ Get file content
→ Parse PDF (AI Builder or custom)
→ Extract data
→ Create item in SharePoint list
→ Move file to "Processed" folder
→ Send notification email
```

**Why Properties-Only**: Validate file before downloading content (avoid 50MB skip)

---

### Pattern 2: Metadata Synchronization
```
Trigger: When file modified (properties only)
→ Initialize variable: lastETag
→ Condition: ETag ≠ lastETag (avoid metadata-only triggers)
→ Get file properties
→ Update database record
→ Set lastETag = current ETag
```

**Deduplication**: ETag comparison ensures only real content changes trigger sync

---

### Pattern 3: Large File Backup (>50MB Workaround)
```
Schedule: Every 10 minutes
→ List files in folder (Get Files action)
→ Filter: Size > 50MB AND Modified > (Now - 10 minutes)
→ Apply to each large file:
   → Copy file to backup location
   → Log to tracking list
```

**Compensates**: 50MB trigger limitation with scheduled polling

---

### Pattern 4: User-Initiated Conversion
```
Trigger: For a selected file
→ Get file content
→ Condition: File extension = .docx
→ Convert to PDF (Word Online connector)
→ Create file in "Converted" folder
→ Send success notification to user
→ Handle errors: Send failure notification
```

**User Experience**: Right-click in OneDrive → Select flow → Receive converted PDF

---

### Pattern 5: High-Volume Change Detection
```
Trigger: When file created (properties only)
→ Add to Azure Storage Queue
→ [Separate Flow] Queue trigger
   → Process file from queue
   → Batch operations to reduce API calls
```

**Decoupling**: Queue-based processing handles >30 pending changes gracefully

---

## Trigger Comparison Matrix

| Feature | Created (Content) | Created (Properties) | Modified (Content) | Modified (Properties) | For Selected File |
|---------|-------------------|---------------------|-------------------|----------------------|-------------------|
| Returns Content | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ❌ No (path only) |
| 50MB Limitation | ✅ Skips | ✅ Skips | ✅ Skips | ✅ Skips | ❌ No limit |
| Throttle Impact | High | Low | High | Low | Low |
| Subfolder Support | ✅ Optional | ✅ Optional | ✅ Optional | ✅ Optional | ❌ N/A |
| Polling Type | Automatic | Automatic | Automatic | Automatic | Instant (manual) |
| Best For | Content processing | Notifications | Version tracking | Metadata sync | Ad-hoc tasks |
| Duplicate Risk | Medium | Low | High | Medium | None |

**Decision Tree**:
1. **Need immediate content?** → Use content variant
2. **Metadata workflow only?** → Use properties-only variant
3. **User-initiated?** → Use "For a selected file"
4. **File >50MB?** → Implement scheduled workaround

---

## API Rate Limits and Throttling

**Global Limit**: 100 API calls per connection per 60 seconds

**Trigger Impact**:
- Properties-only: ~1 call per trigger execution
- With content: ~2 calls per trigger execution (metadata + content)
- High-volume folders: Multiple triggers per polling interval

**Throttle Management**:
1. **Monitor Usage**: Track flow runs per minute
2. **Delay Actions**: Add 1-2 second delays in loops
3. **Batch Processing**: Use Max File Count to control throughput
4. **Multiple Connections**: Distribute load across connections
5. **Reduce Frequency**: Increase polling interval if throttling common

**Formula**:
```
Max concurrent flows = 100 / (API calls per flow * flows per minute)
Example: 100 / (2 calls * 10 flows/min) = 5 concurrent flows max
```

---

## Official Documentation

<official_docs>
https://learn.microsoft.com/en-us/connectors/onedriveforbusiness/
</official_docs>

**Related Documentation**:
- OneDrive for Business API: https://learn.microsoft.com/en-us/onedrive/developer/rest-api/
- Microsoft Graph Files API: https://learn.microsoft.com/en-us/graph/api/resources/onedrive

---

**Last Updated**: 2025-10-31
**Fetch Date**: 2025-10-31
**Version**: 1.0
