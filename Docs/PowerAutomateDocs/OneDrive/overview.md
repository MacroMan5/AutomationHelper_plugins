# OneDrive for Business - Connector Overview

---
type: connector-overview
connector_name: OneDrive for Business
connector_type: standard
publisher: Microsoft
category: Data
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [onedrive, file, folder, storage, cloud, document, upload, download, metadata, sharing, conversion]
capabilities: [file_management, file_content, metadata_operations, search, archive, conversion, sharing]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
availability:
  power_automate: true
  logic_apps: true
  power_apps: true
  copilot_studio: true
pricing_tier: standard
supported_regions: all_except_china
---

<official_docs>
https://learn.microsoft.com/en-us/connectors/onedriveforbusiness/
</official_docs>

<description>
The OneDrive for Business connector enables cloud-based file management operations including upload, download, modification, and deletion. It provides comprehensive capabilities for file operations, metadata management, search, archive extraction, file conversion, and sharing link generation across Microsoft's business cloud storage platform.
</description>

---

## Capabilities Overview

<capabilities>
**Core Features**:
- **File Management**: Create, copy, move, delete, update files
- **File Content Operations**: Read, write, update binary content
- **Metadata Operations**: Get, manage file properties and metadata
- **Folder Operations**: List, search, organize files in folders
- **Archive Operations**: Extract archive files (.zip) to folders
- **File Conversion**: Convert files to different formats (e.g., Word → PDF)
- **Sharing**: Create sharing links with various scopes and permissions
- **Search**: Find files by name patterns and regex
- **Thumbnail Generation**: Retrieve file thumbnails for preview

**Supported Account Types**:
- Microsoft business accounts (organizational)
- Microsoft school accounts (educational)
- **NOT supported**: Personal Microsoft accounts

**Availability**:
- All Power Automate, Logic Apps, Power Apps, Copilot Studio regions
- **Exception**: China Cloud (21Vianet) and Azure China regions NOT supported
</capabilities>

---

## API Limits and Throttling

<api_limits>
| Limit Type | Value | Scope |
|------------|-------|-------|
| **API Calls** | 100 calls | Per 60 seconds per connection |
| **Renewal Period** | 60 seconds | Per connection |

**Throttling Behavior**:
- Exceeding 100 calls/60s triggers HTTP 429 (Too Many Requests)
- Throttling is per-connection (multiple connections = independent limits)
- Properties-only triggers consume fewer API calls than content triggers

**Throttle Management**:
- Add delays between API calls in loops (minimum 1 second)
- Use properties-only trigger variants when file content not needed
- Implement batch processing to reduce call volume
- Monitor concurrent flow executions
- Distribute load across multiple connections if needed
</api_limits>

---

## Critical Limitations

<critical_limitations>

<limitation id="lim-onedrive-overview-001" severity="critical">
**File Size - Trigger Skip Threshold**: Files exceeding **50 MB** are automatically skipped by all polling triggers ("When a file is created", "When a file is modified").

**Impact**: Large files will NOT trigger flows, causing silent failures.

**Workaround**:
1. Implement scheduled polling via "List files in folder" action
2. Filter for files >50MB created/modified since last run
3. Process large files via manual trigger ("For a selected file")

**Example Workaround**:
```
Schedule: Every 5 minutes
→ List files in folder
→ Filter: Size > 52,428,800 AND Modified > (Now - 5 minutes)
→ Process large files
```
</limitation>

<limitation id="lim-onedrive-overview-002" severity="critical">
**Upload from URL - False Success Reporting**: The "Upload file from URL" action **always reports success after 20 seconds** regardless of actual upload status.

**Impact**: Flows may proceed with subsequent actions before upload completes, causing failures.

**Required Mitigation**:
```
Upload file from URL
→ Delay: 30-60 seconds
→ Get file metadata (verify existence)
→ Condition: File exists AND Size > 0
  → Success: Continue processing
  → Failure: Log error, retry, or alert admin
```

**Never trust immediate success** - always implement independent verification.
</limitation>

<limitation id="lim-onedrive-overview-003" severity="critical">
**Archive Extraction Limits**: Extract archive operation has strict constraints:
- **Maximum archive size**: 50 MB
- **Maximum files inside**: 100 files
- **Character encoding**: Multi-byte characters in filenames NOT supported

**Impact**: Archives exceeding limits cause extraction failures.

**Workaround**:
1. Validate archive size < 50MB before extraction
2. Use ASCII-only filenames in archives
3. Split large archives into smaller chunks
4. Pre-check file count if possible
</limitation>

<limitation id="lim-onedrive-overview-004" severity="critical">
**Cross-Tenant Access**: Accessing shared files across tenant hostname boundaries is **NOT supported**.

**Example Restriction**:
```
User: user@contoso-my.sharepoint.com
Cannot access: Files in microsoft-my.sharepoint.com
```

**Impact**: Cross-organization file sharing via connector is impossible.

**Workaround**: Implement manual file transfer or use Azure Functions for cross-tenant scenarios.
</limitation>

<limitation id="lim-onedrive-overview-005" severity="critical">
**Multi-Geo Scenarios**: Multi-geo scenarios are **NOT supported**. Both user and file must reside in same geographic region.

**Impact**: Cannot access files stored in different geographic regions (e.g., EU cannot access AU).

**Workaround**: Use region-specific connections or implement cross-region transfer logic.
</limitation>

<limitation id="lim-onedrive-overview-006" severity="critical">
**Cross-Drive Functionality**: Cross-drive functionality is **NOT supported**. Connector operates only on connected account's owned data.

**Impact**: Cannot access or manage files in other users' OneDrive accounts.

**Workaround**: Each user requires separate connection for their OneDrive.
</limitation>

<limitation id="lim-onedrive-overview-007" severity="high">
**Pending Changes Threshold**: Triggers may have issues when **more than approximately 30 pending changes** occur between polling intervals.

**Impact**: Files may be skipped or missed during high-volume periods.

**Solutions**:
1. Reduce polling interval (increase frequency)
2. Distribute monitoring across multiple flows (subfolder-specific)
3. Implement backup detection via scheduled "List files" action
4. Use SharePoint connector for SharePoint-backed OneDrive
</limitation>

<limitation id="lim-onedrive-overview-008" severity="high">
**Organizational Policy Restrictions**: Certain organizational policies block connector access:

**Common Blocking Policies**:
1. **"(Sharing) Prevent file download"** - Blocks Get File Content actions
2. **"Control access from unmanaged devices"** - Prevents unverified device access
3. **"Control access based on network location"** - Restricts network-based access

**Troubleshooting**:
- Verify organizational policies in SharePoint admin center
- Check Conditional Access settings in Azure AD
- Review device compliance requirements
- Contact IT admin for policy exceptions
</limitation>

<limitation id="lim-onedrive-overview-009" severity="medium">
**File Picker Display Limit**: Connector displays **maximum 200 items per folder** in file picker.

**Impact**: Users may have difficulty locating files in folders with 200+ items.

**Best Practice**: Organize files with subfolder hierarchy to keep items per folder under 200.
</limitation>

<limitation id="lim-onedrive-overview-010" severity="medium">
**Thumbnail Expiration**: File thumbnails are only valid for **6 hours** after generation.

**Impact**: Cached thumbnail URLs become invalid and must be regenerated.

**Best Practice**: Generate thumbnails on-demand rather than caching URLs long-term.
</limitation>

<limitation id="lim-onedrive-overview-011" severity="medium">
**Encrypted Files**: Encrypted files saved on OneDrive throw **corrupt file errors** through connector operations.

**Impact**: Files may open manually but fail via connector.

**Solutions**:
1. Decrypt files before processing via connector
2. Handle encryption errors gracefully
3. Log encrypted files for manual processing
</limitation>

<limitation id="lim-onedrive-overview-012" severity="high">
**Conversion Restrictions - Digital Signatures**: Cannot convert digitally signed, password-protected, or IRM-restricted Word documents to PDF for security reasons.

**Impact**: PDF conversion fails for protected documents.

**Workaround**: Remove document restrictions before conversion or handle manually.
</limitation>

<limitation id="lim-onedrive-overview-013" severity="medium">
**Filename Character Replacement**: OneDrive replaces disallowed characters with underscores during file creation.

**Disallowed Characters**: `\ / : * ? " < > |`

**Example**:
```
Requested: "Report:2025.docx"
Created:   "Report_2025.docx"
```

**Best Practice**: Pre-validate and sanitize filenames before creation.
</limitation>

<limitation id="lim-onedrive-overview-014" severity="critical">
**Account Type Requirement**: Connector requires **Microsoft business or school accounts**. Personal Microsoft accounts are NOT supported.

**Impact**: Connection fails with personal accounts.

**Verification**: Ensure organizational credentials used for connection.
</limitation>

<limitation id="lim-onedrive-overview-015" severity="medium">
**Trigger False Positives**: Modification triggers may fire without noticeable changes due to metadata or permission updates.

**Impact**: Unnecessary flow executions and duplicate processing.

**Solutions**:
1. Implement ETag comparison to verify content changes
2. Use file-based unit processing logic
3. Add deduplication logic (track processed file IDs)
4. Consider using approval checkpoints
</limitation>

</critical_limitations>

---

## Authentication & Connection

<authentication>
**Required Account Type**:
- **Business accounts**: Microsoft organizational accounts
- **School accounts**: Microsoft educational accounts
- **NOT supported**: Personal Microsoft accounts (outlook.com, hotmail.com, etc.)

**Authentication Method**:
- OAuth 2.0 authorization
- User consent required for file access

**Connection Model**: User-specific connections
- Each user must create their own connection
- No shared service account model available
- Cannot access other users' OneDrive files

**Required Permissions**:
- **Read operations**: OneDrive file read access
- **Write operations**: OneDrive file write/modify access
- **Delete operations**: OneDrive file delete permissions
- **Sharing operations**: Sharing link creation permissions (may be restricted by admin)
</authentication>

---

## Common Use Cases

<common_use_cases>

**1. Automated Document Conversion**
```
Trigger: When file created (filter: .docx files)
→ Delay: 10 seconds (allow file to settle)
→ Convert file to PDF
→ Error handling: Retry on 502 Bad Gateway
→ Save PDF to "Converted" folder
→ Delete original Word file (optional)
→ Send email with PDF link
```
**Benefits**: Automated format standardization, consistent delivery

---

**2. File Synchronization & Backup**
```
Trigger: When file created or modified (properties only)
→ Get file metadata (validate size < threshold)
→ Condition: File size < 100MB
  → Copy file to backup location
  → Update tracking list with timestamp
  → Log sync success
→ Else: Log "File too large for backup"
```
**Benefits**: Automated backup, disaster recovery

---

**3. Verified URL Upload**
```
Upload file from URL
→ Delay: 30 seconds
→ Get file metadata
→ Condition: File exists AND Size > 0
  → Success: Continue processing
  → Failure:
    → Log error "Upload verification failed"
    → Retry OR send admin alert
```
**Benefits**: Compensates for 20-second false success issue

---

**4. Archive Processing**
```
Trigger: When file created (filter: .zip files)
→ Get file metadata
→ Condition: Size < 52,428,800 (50MB)
  → Extract archive to folder
  → List destination folder (verify extraction)
  → Process extracted files
  → Delete archive (cleanup)
→ Else: Log "Archive exceeds 50MB limit"
```
**Benefits**: Automated archive unpacking, bulk file processing

---

**5. Metadata-Driven File Organization**
```
Trigger: When file created (properties only)
→ Extract metadata from filename (date, category, etc.)
→ Create organized folder structure (Year/Month/Category)
→ Move file to appropriate folder
→ Update file properties with metadata
→ Send notification to stakeholders
```
**Benefits**: Automated file organization, metadata enrichment

---

**6. Large File Workaround (>50MB)**
```
Schedule: Every 10 minutes
→ List files in folder
→ Filter: Size > 52,428,800 AND Modified > (Now - 10 minutes)
→ Apply to each large file:
  → Get file content
  → Process file
  → Move to "Processed" folder
  → Log processing
```
**Benefits**: Handles files skipped by standard triggers

---

**7. Sharing Link Generation**
```
Trigger: When item created in "Share Requests" SharePoint list
→ Get file from OneDrive (using path from list)
→ Create share link (scope: organization)
→ Update SharePoint item with link
→ Send email to requester with link
→ Log sharing activity
```
**Benefits**: Controlled file sharing, audit trail

</common_use_cases>

---

## Best Practices

<best_practices>

### Performance Optimization

1. **Use Properties-Only Triggers**
   - Faster execution (no content download)
   - Lower bandwidth consumption
   - Reduced API throttling impact
   ```
   "When file created (properties only)" instead of "When file created"
   ```

2. **Folder Scoping**
   - Monitor specific subfolders instead of root
   - Reduces polling overhead
   - Improves trigger performance

3. **Max File Count Parameter**
   - Set appropriate batch size (1-100)
   - Balance latency vs throughput
   - Avoid processing too many files at once

4. **Enable Content Type Inference**
   - Improves downstream action compatibility
   - Proper MIME type handling
   - Better integration with other connectors

### Reliability Patterns

1. **50MB File Handling**
   - Implement scheduled workaround for large files
   - Add file size validation before operations
   - Use SharePoint connector if files in SharePoint-backed OneDrive
   - Create manual trigger flows for large file scenarios

2. **Upload from URL Verification**
   - **NEVER trust immediate success**
   - Add 30-60 second delay before verification
   - Get file metadata to confirm existence
   - Check file size matches expected
   - Implement maximum wait timeout

3. **Duplicate Detection**
   - Track processed file IDs with timestamps
   - Check ETag for content change verification
   - Implement delay actions (30-60s) to debounce rapid changes
   - Use approval gates for critical operations

4. **Error Handling with Scopes**
   ```
   Scope: Main Operations
   → Actions inside scope

   Scope: Error Handling (Configure run after: has failed)
   → Log error to tracking list
   → Send admin notification
   → Implement retry logic
   ```

### Archive Operations

1. **Pre-Validation**
   - Check archive size < 50MB
   - Verify file count < 100 (if possible)
   - Use ASCII-only filenames

2. **Extraction Verification**
   - Add extraction failure handling
   - List destination folder to confirm
   - Verify expected file count

3. **Character Encoding**
   - Create archives with UTF-8 encoding
   - Test with ASCII-only filenames if issues arise

### Conversion Operations

1. **PDF Conversion Best Practices**
   - Add 5-10 second delay after file creation
   - Catch 502 Bad Gateway errors
   - Implement retry logic with exponential backoff
   - Verify source format compatibility

2. **Security Restrictions**
   - Cannot convert digitally signed documents
   - Cannot convert password-protected files
   - Cannot convert IRM-restricted documents
   - Check document security before conversion

### Metadata Management

1. **Use Metadata First**
   - Check file size before content retrieval
   - Verify existence before operations
   - Cache metadata to reduce API calls
   - Use ETag for change detection

2. **ID vs Path**
   - Prefer ID-based actions (faster lookup)
   - Use path variants when ID unavailable
   - IDs remain constant after move/rename

### Sharing Operations

1. **Link Scope Selection**
   - Verify organizational policies before anonymous links
   - Use "organization" scope for internal sharing
   - Test with policies applied before production

2. **Link Expiration**
   - Set expiration dates on anonymous links
   - Document link lifecycle
   - Implement link revocation workflows

### API Throttling Management

1. **Rate Monitoring**
   - Track API calls per flow (100/60s limit)
   - Add delays in loops (minimum 1 second)
   - Monitor concurrent flow executions

2. **Call Reduction**
   - Use properties-only variants when possible
   - Cache metadata instead of repeated queries
   - Batch operations to reduce overhead

3. **Error Handling**
   - Implement retry logic for 429 errors
   - Use exponential backoff strategy
   - Distribute load if throttling common

</best_practices>

---

## Troubleshooting Guide

<troubleshooting>

<error id="err-onedrive-overview-001" severity="critical">
**Error**: Files >50MB not triggering flows

**Cause**: Trigger skip threshold for files exceeding 50MB.

**Solutions**:
1. Implement scheduled polling workaround (see limitation lim-onedrive-overview-001)
2. Use manual trigger "For a selected file"
3. Move files to SharePoint and use SharePoint connector
4. Split large files before upload if possible
</error>

<error id="err-onedrive-overview-002" severity="high">
**Error**: Upload from URL false success

**Cause**: 20-second timeout before actual upload completion.

**Required Solution**:
```
Upload from URL
→ Delay: 30 seconds minimum
→ Get file metadata
→ Condition: File exists AND Size > 0
  → Verified success
  → Failure: Retry or alert
```

**Never proceed without verification**.
</error>

<error id="err-onedrive-overview-003" severity="high">
**Error**: Archive extraction failure

**Causes**:
- Archive exceeds 50MB
- Archive contains >100 files
- Multi-byte characters in filenames
- Corrupted archive

**Solutions**:
1. Pre-validate: Get archive metadata, check Size < 52,428,800
2. Use ASCII-only filenames
3. Re-create archive with standard tools
4. Split into smaller archives if needed
</error>

<error id="err-onedrive-overview-004" http_code="403" severity="high">
**Error**: Access Denied - Policy blocking

**Causes**:
- "Prevent file download" organizational policy
- Unmanaged device access controls
- Network location restrictions
- Conditional Access policies

**Solutions**:
1. Verify organizational policies in SharePoint admin center
2. Check Conditional Access in Azure AD
3. Review device compliance requirements
4. Test with properties-only triggers (may bypass download restrictions)
5. Contact IT admin for policy exceptions
</error>

<error id="err-onedrive-overview-005" http_code="502" severity="medium">
**Error**: Bad Gateway - Conversion failure

**Specific To**: Convert file actions (especially HTML → PDF)

**Cause**: Service delay; file not ready for conversion.

**Solutions**:
1. Add 5-10 second delay between file creation and conversion
2. Implement retry logic (exponential backoff)
3. Catch 502 errors gracefully
4. Verify format supports conversion
</error>

<error id="err-onedrive-overview-006" http_code="429" severity="critical">
**Error**: Too Many Requests - Throttling

**Cause**: Exceeded 100 API calls per 60 seconds per connection.

**Solutions**:
1. Add Delay actions in loops (minimum 1 second)
2. Reduce polling frequency
3. Use properties-only triggers to reduce calls
4. Distribute load across multiple connections
5. Implement batch processing

**Formula**:
```
Max operations per minute = 100 / (API calls per operation)
Example: Get File Content uses 2 calls
Max = 100 / 2 = 50 file retrievals per minute
```
</error>

<error id="err-onedrive-overview-007" severity="medium">
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
</error>

<error id="err-onedrive-overview-008" severity="medium">
**Error**: Connection failure with personal account

**Cause**: Personal Microsoft accounts not supported (only business/school accounts).

**Solution**: Use organizational credentials (user@company.com format).
</error>

<error id="err-onedrive-overview-009" severity="high">
**Error**: Cross-tenant access failure

**Cause**: User in one tenant cannot access files in different tenant.

**Example**:
```
User: user@contoso-my.sharepoint.com
Attempting: Access to microsoft-my.sharepoint.com
Result: FAILED
```

**Solutions**:
1. Implement manual file transfer
2. Use Azure Functions for cross-tenant operations
3. Request file sharing via standard SharePoint sharing
4. Use SharePoint connector if applicable
</error>

<error id="err-onedrive-overview-010" severity="medium">
**Error**: Encrypted file corrupt error

**Cause**: Encrypted files saved on OneDrive throw corrupt errors via connector.

**Solutions**:
1. Decrypt files before OneDrive upload
2. Handle encryption errors gracefully in flows
3. Verify file opens manually before automation
4. Log encrypted files for manual processing
</error>

</troubleshooting>

---

## Connector Metadata

<connector_metadata>
| Property | Value |
|----------|-------|
| **Publisher** | Microsoft |
| **Service Class** | Standard |
| **Category** | Data |
| **Pricing Tier** | Standard (included in Microsoft 365) |
| **Website** | https://products.office.com/onedrive/onedrive-for-business |
| **Privacy Policy** | https://privacy.microsoft.com/ |
| **Contact Email** | spo_bapi_connector@service.microsoft.com |
| **Available In** | Power Automate, Logic Apps, Power Apps, Copilot Studio |
| **Supported Regions** | All except China Cloud (21Vianet) and Azure China |
| **Account Requirement** | Business or school accounts only (no personal accounts) |
</connector_metadata>

---

## Related Connectors

<related_connectors>
- **SharePoint**: Document library operations (OneDrive backed by SharePoint)
- **Microsoft 365 Users**: User profile lookups
- **Excel Online (Business)**: Excel files stored in OneDrive
- **Word Online (Business)**: Word documents in OneDrive
- **Microsoft Teams**: OneDrive as file storage for Teams
- **Approvals**: File validation and approval workflows
- **Azure Blob Storage**: Alternative cloud file storage
</related_connectors>

---

## Integration Patterns

<integration_patterns>

**Pattern 1: Verified URL Upload with Retry**
```
Upload file from URL
→ Delay: 30 seconds
→ Get file metadata
→ Condition: File exists
  → Success: Continue
  → Failure (1st attempt):
    → Delay: 60 seconds
    → Get file metadata again
    → Condition: File exists
      → Success: Continue
      → Failure (2nd attempt): Alert admin, log error
```

**Pattern 2: Large File Backup (>50MB Workaround)**
```
Schedule: Every 10 minutes
→ List files in folder
→ Filter: Size > 52,428,800 AND Modified > (Now - 10 minutes)
→ Apply to each:
  → Copy file to backup location
  → Log to tracking list
  → Update last backup timestamp
```

**Pattern 3: PDF Conversion with Error Handling**
```
Create Word file
→ Delay: 10 seconds
→ Try Convert to PDF:
  → On 502 Bad Gateway:
    → Delay: 5 seconds
    → Retry (max 3 attempts)
  → On success:
    → Save PDF
    → Delete Word file
  → On final failure:
    → Log error
    → Send alert
```

**Pattern 4: Deduplication Pattern**
```
Trigger: When file modified (properties only)
→ Initialize variable: processedFiles (array)
→ Condition: File ID not in processedFiles
  → True:
    → Process file
    → Append File ID to processedFiles
    → Update timestamp
  → False: Skip (already processed)
```

**Pattern 5: Archive Validation & Extraction**
```
Trigger: When file created (filter: .zip)
→ Get file metadata
→ Condition: Size < 52,428,800
  → True:
    → Extract archive
    → List destination folder
    → Condition: File count > 0
      → Process extracted files
      → Delete archive
    → Else: Log "Extraction failed"
  → False: Log "Archive too large (>50MB)"
```

</integration_patterns>

---

## Known Issues & Workarounds

<known_issues>

| Issue | Impact | Workaround |
|-------|--------|------------|
| **Files >50MB skipped by triggers** | Silent failures | Scheduled polling workaround (List files action) |
| **Upload from URL false success** | Processing failures | Mandatory verification delay + Get metadata |
| **Archive 50MB/100 file limits** | Extraction failures | Pre-validate size, split archives |
| **Cross-tenant access blocked** | Cannot share across orgs | Manual transfer or Azure Functions |
| **Multi-geo unsupported** | Regional access blocked | Use region-specific connections |
| **>30 pending changes issues** | Files skipped | Reduce polling frequency, distribute flows |
| **Thumbnail 6-hour expiration** | Stale cached URLs | Regenerate on-demand |
| **File picker 200-item limit** | Difficult file location | Organize with subfolders |
| **Encrypted file errors** | Corrupt file errors | Decrypt before upload |
| **Conversion restrictions** | PDF conversion fails | Remove digital signatures/IRM |
| **Filename character replacement** | Unexpected names | Pre-sanitize filenames |
| **Personal account unsupported** | Connection failures | Use business/school accounts |
| **Modification trigger false positives** | Unnecessary executions | ETag comparison, deduplication |

</known_issues>

---

## Version History

**Version 1.0** (2025-10-31):
- Initial comprehensive overview documentation
- Format v2 with YAML frontmatter and XML tags
- 15 critical limitations documented
- 22 actions and 5 triggers covered
- Troubleshooting guide with 10 common errors
- 7 workflow patterns and integration examples

---

**Last Updated**: 2025-10-31
**Fetch Date**: 2025-10-31
**Documentation Format**: Agent-Optimized v2
