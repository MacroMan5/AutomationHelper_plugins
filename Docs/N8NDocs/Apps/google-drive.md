---
type: node-overview
node_name: Google Drive
node_type: app
category: both
auth_required: true
version: 1.0
last_updated: 2025-10-31
keywords: [google, drive, file, upload, download, folder, storage, cloud, sync, file-management, backup]
related_nodes: [Google Sheets, HTTP Request, Set]
rate_limits:
  service_rate_limit: 500 requests per 100 seconds per user
  n8n_limit: none (N8N doesn't impose limits)
official_docs_url: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/
npm_package: n8n-nodes-base
---

<official_docs>
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/file-operations/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/file-folder-operations/
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/folder-operations/
</official_docs>

<description>
The Google Drive node enables complete file and folder management within Google Drive through N8N workflows. It supports uploading, downloading, copying, deleting, and searching files, as well as managing folders and shared drives. Perfect for automating document management, backup processes, file synchronization, and integration with document storage systems.
</description>

<capabilities>
## Core Capabilities
- **File Upload**: Upload files from URLs, binary data, or workflow data
- **File Download**: Retrieve and pass file content to subsequent nodes
- **File Copy**: Duplicate files with optional renaming
- **File Delete**: Remove files from Google Drive
- **File Search**: Find files by name, type, or metadata
- **Folder Management**: Create and manage folder structures
- **Shared Drive Support**: Work with shared drives and team collaboration
- **File Sharing**: Manage file permissions and sharing settings

## Supported Operations
- **Upload File**: Create new files in Google Drive from various sources
- **Download File**: Retrieve file content for processing
- **Copy File**: Duplicate files with new names
- **Delete File**: Permanently remove files
- **Search**: Find files by query criteria
- **List Files**: Get file listings from folders
- **Create Folder**: Create new directory structures
- **Delete Folder**: Remove empty folders
- **Share File**: Grant access to files/folders
- **Update File**: Modify file metadata

## Integration Features
- **OAuth2 Authentication**: Secure credential-based access
- **Batch File Operations**: Process multiple files
- **Dynamic File Path Resolution**: Use expressions for file names
- **Recursive Folder Operations**: Work with nested folder structures
- **File Type Filtering**: Filter by MIME type or file extension
- **Metadata Preservation**: Maintain file properties across operations
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Throttling**
- **500 requests per 100 seconds** per user per project
- Throttling scope: Per user account
- Retry-After header: Yes
- N8N built-in retry: Yes

**Operation-Specific Limits**
- **Upload File**: Standard rate limit applies; chunked upload for large files
- **Download File**: Standard rate limit applies
- **Search/List**: Standard rate limit applies
- **Copy/Delete**: Standard rate limit applies

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited by server resources and network
- Cloud: Respects Google Drive API quotas

**Throttling Behavior**
- HTTP Status: 429 (Too Many Requests)
- Error message: "Rate limit exceeded"
- N8N automatic retry: Yes (configurable)
- Recommended retry strategy: Exponential backoff with 3-5 retries

## Size Limits

**File Operations**
- Max file upload size: **5TB** per file (Google Drive storage limit)
- Max file download size: **5TB** per file
- Practical N8N limit: **500MB-2GB** (depends on instance resources)
- Max request payload: **10MB** (Google API limit per request)

**Folder Operations**
- Max files per folder: **No hard limit** (performance degradation after ~100K files)
- Max folder nesting depth: **No explicit limit** (typically 100+ levels possible)
- Max folder size: **No explicit limit** (depends on storage quota)

**Shared Drive Operations**
- Max files per shared drive: **Same as regular Drive**
- Max members per shared drive: **600** (soft limit)

## Timeout Limits
- Default timeout: **300 seconds** (N8N default)
- Max timeout: **600 seconds** (configurable)
- Long-running operations: Supported
- Async operations: Yes (for large file uploads/downloads)
- Resumable uploads: Supported for files >5MB
</rate_limits>

<critical_limitations>
## File Upload & Download

<limitation id="lim-001" severity="critical">
**File Size Memory Constraints**: Large file uploads/downloads consume significant memory

- **Impact**: Potential workflow timeout or N8N instance crash with very large files
- **Scope**: Files >1GB on cloud instances, >2GB on self-hosted
- **Workaround**: Use streaming/chunked uploads for large files; implement pagination
- **Affected Operations**: Upload File, Download File

**Example Scenario**: Uploading a 5GB video file may timeout or crash cloud instance
</limitation>

<limitation id="lim-002" severity="high">
**File Type Restrictions**: Certain file types may be blocked by security policies

- **Impact**: Upload/download blocked for executable files or scripts
- **Scope**: Operating system executables, macro-enabled Office docs
- **Workaround**: Compress files or rename with different extension (if allowed)
- **Affected Operations**: Upload File, Download File

**Example Scenario**: Uploading .exe or .bat files fails automatically
</limitation>

## Authentication & Credentials

<limitation id="lim-003" severity="high">
**Service Account Limitations**: Service accounts have different sharing capabilities

- **Impact**: Service account-owned files cannot be directly shared with users
- **Scope**: Service account authentication
- **Workaround**: Create files in shared drive or use OAuth2 with personal account
- **Affected Operations**: Share File, Create/Upload File

**Example Scenario**: Service account uploads file but cannot share it with team
</limitation>

<limitation id="lim-004" severity="medium">
**Cross-Tenant Access**: Cannot access files across Google Workspace organizations

- **Impact**: Multi-organization workflows require separate credentials
- **Scope**: Google Workspace domains
- **Workaround**: Create separate credentials for each domain
- **Affected Operations**: All operations

**Example Scenario**: Workflow cannot copy files from org1.com drive to org2.com drive
</limitation>

## Search & Filtering

<limitation id="lim-005" severity="medium">
**Search Index Lag**: New files may not appear in search results immediately

- **Impact**: Workflows searching for just-created files may not find them
- **Scope**: Search operations
- **Workaround**: Add delay between create and search operations
- **Affected Operations**: Search, List Files

**Example Scenario**: Upload file immediately searches for it, but it's not indexed yet
</limitation>

<limitation id="lim-006" severity="medium">
**Special Character Handling**: Files with certain special characters may cause issues

- **Impact**: File operations fail or behave unexpectedly
- **Scope**: File names with unicode, quotes, or special symbols
- **Workaround**: Sanitize file names before upload
- **Affected Operations**: Upload File, Copy File, Search

**Example Scenario**: File name "test|file<>name.txt" causes parsing errors
</limitation>

## Folder & Organization

<limitation id="lim-007" severity="high">
**Shared Drive Folder Limitations**: Some operations have different restrictions on shared drives

- **Impact**: Folder operations may fail on shared drives vs. personal drive
- **Scope**: Shared drive folder operations
- **Workaround**: Use file-based operations instead of folder operations on shared drives
- **Affected Operations**: Create Folder, Delete Folder

**Example Scenario**: Deleting a folder on shared drive requires specific permissions
</limitation>

<limitation id="lim-008" severity="low">
**Deleted File Recovery**: Deleted files go to Trash but may be permanently deleted

- **Impact**: No direct undelete through API
- **Scope**: Delete File operations
- **Workaround**: Implement backup/versioning before deletion
- **Affected Operations**: Delete File

**Example Scenario**: Accidentally deleted file cannot be recovered through N8N
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### OAuth2 (Recommended)
- Flow type: Authorization Code
- Required credentials: Google account with Drive access
- Token refresh: Automatic (N8N manages refresh tokens)
- Credential storage: N8N encrypted credential store

**Scopes Required**:
- `https://www.googleapis.com/auth/drive` (Full Drive access)
- `https://www.googleapis.com/auth/drive.file` (Application files only)

### Service Account (Alternative)
- Authentication type: Private key
- Use case: Automated, non-interactive access
- Token refresh: Automatic via private key
- Credential storage: N8N encrypted credential store

**Benefits**: No user action required, good for scheduled tasks

## Credential Configuration in N8N

1. Navigate to **Credentials** in N8N
2. Click **Add Credential**
3. Select **Google Drive**
4. Choose authentication method:
   - **OAuth2**: Click "Connect my account" and follow Google OAuth flow
   - **Service Account**: Upload service account JSON key file
5. Grant permissions to access drive files
6. Test connection - N8N verifies access
7. Save credential

## Required Permissions/Scopes

### Google Drive Permissions
- **Drive Full Access** (`drive` scope): Required for all file/folder operations
- **Drive Application Files** (`drive.file` scope): Restricted to files created by app
- **Drive Metadata Read-Only** (`drive.metadata.readonly` scope): Read-only metadata access

## Troubleshooting Authentication
- **"Invalid credentials" or "Unauthorized"**:
  - Check that OAuth token is fresh
  - Re-authenticate the credential
  - Verify Google account has Drive access

- **"Token expiration"**:
  - N8N handles automatically; if persists, update credential
  - Check credential hasn't been revoked in Google account settings

- **"Permission denied" on specific operations**:
  - Verify file/folder is shared with credential account
  - Check credential has required scopes
  - Verify user/service account has folder permissions
</authentication>

<common_use_cases>
## 1. Automated File Backup and Archival

**Description**: Automatically backup files from external systems to Google Drive

**Typical Workflow**:
```
Trigger: Schedule (Daily)
↓
Node 1: List Files - Check which files need backup
↓
Node 2: HTTP Request - Download from source system
↓
Node 3: Google Drive - Upload to backup folder
↓
Node 4: Email - Send confirmation
↓
Result: Automated daily backups in Google Drive
```

**Key Operations**: [Upload File](#), [List Files](#), [Create Folder](#)

**Best For**: Data backup, archive management, compliance

---

## 2. Document Processing Pipeline

**Description**: Download documents, process them, and organize in Drive

**Typical Workflow**:
```
Trigger: Webhook (New document ready)
↓
Node 1: Google Drive - Download document
↓
Node 2: Code - Process/transform document
↓
Node 3: Google Drive - Upload processed version
↓
Node 4: Google Drive - Move to processed folder
↓
Node 5: Notification - Alert processing complete
↓
Result: Documents automatically processed and organized
```

**Key Operations**: [Download File](#), [Upload File](#), [Search](#)

**Best For**: Document management, PDF processing, file organization

---

## 3. File Distribution and Sharing

**Description**: Automatically create and share files with multiple recipients

**Typical Workflow**:
```
Trigger: Form Submission
↓
Node 1: Set - Prepare file content
↓
Node 2: Google Drive - Upload file
↓
Node 3: Google Drive - Share with recipients
↓
Node 4: Email - Send access notification
↓
Result: Files created and shared automatically
```

**Key Operations**: [Upload File](#), [Share File](#)

**Best For**: Report distribution, document sharing, access management

---

## 4. File Synchronization Between Systems

**Description**: Keep files in sync between Drive and external storage

**Typical Workflow**:
```
Trigger: File change webhook
↓
Node 1: Google Drive - Check if file exists
↓
Node 2: IF - Determine action (create/update)
↓
Node 3: Google Drive - Upload/Copy file
↓
Node 4: External API - Update file in other system
↓
Result: Files stay synchronized across systems
```

**Key Operations**: [Search](#), [Upload File](#), [Copy File](#)

**Best For**: Multi-system file sync, cloud migration, data federation

---

## 5. Smart File Organization and Cleanup

**Description**: Automatically organize and manage files in Drive folders

**Typical Workflow**:
```
Trigger: Schedule (Weekly)
↓
Node 1: Google Drive - List all files
↓
Node 2: Split In Batches - Process in chunks
↓
Node 3: Code - Analyze file age/type
↓
Node 4: Google Drive - Move to appropriate folder
↓
Node 5: Google Drive - Delete old files (if archived)
↓
Result: Drive automatically organized and cleaned
```

**Key Operations**: [List Files](#), [Copy/Move File](#), [Delete File](#)

**Best For**: File management, storage optimization, organization automation
</common_use_cases>

<best_practices>
## Performance Optimization

### Execution Efficiency
1. **Use File Metadata Instead of Download**: When only needing file info, use search/list
   - **Why**: Reduces bandwidth and memory usage
   - **How**: Use Search/List operations instead of Download for large files

2. **Batch File Operations**: Process multiple files in single workflow execution
   - **Why**: Reduces overhead and API calls
   - **How**: Use Split In Batches node to handle multiple files

3. **Implement Pagination for Large Folder Listings**: Don't load all files at once
   - **Why**: Prevents timeouts and memory issues with large folders
   - **How**: Use page tokens from API or implement pagination logic

### Throttling Management
1. **Enable Automatic Retry**: Configure in node settings
   - **N8N Setting**: Node settings → Retry settings
   - **Recommended Value**: 3 retries with exponential backoff

2. **Space Out Large Operations**: Add delays between file operations
   - **How**: Use "Wait" node between operations if hitting rate limits
   - **Backoff Strategy**: Exponential: 1s, 2s, 4s, 8s...

### Data Processing
1. **Stream Large Files**: For files >100MB, use streaming if available
   - **Why**: Prevents memory overflow
   - **How**: Configure node for chunked uploads/downloads

2. **Filter at Query Level**: Use search parameters to limit results
   - **Why**: Reduces data transfer
   - **How**: Specify file type, folder, or name filters in search

## Reliability & Error Handling

### Retry Logic
1. **Enable Automatic Retry**: Configure retry settings in node
   - **Max Retries**: 3-5 (for transient failures)
   - **Retry Interval**: 2000ms default (exponential backoff recommended)
   - **Retry On**: [429, 500, 502, 503, 504, "timeout"]

2. **Use Error Workflow**: Create dedicated error handling workflow
   - **Why**: Centralized error management
   - **How**: Set up "Error Workflow" in N8N settings

### Error Recovery
1. **Idempotent File Operations**: Use conditional logic before operations
   - **Why**: Prevents duplicate files or errors on retry
   - **How**: Check if file exists before upload; verify before delete

2. **Implement Verification Steps**: Verify file operations succeed
   - **Why**: Ensure data integrity
   - **How**: Download/list file after upload to confirm

### Idempotency
1. **Check Before Delete**: Always verify before deleting files
   - **Why**: Prevent accidental data loss
   - **How**: Use IF node to confirm file exists and matches criteria

## Security Best Practices

### Credential Management
1. **Use N8N Credential Store**: Never hardcode file IDs or OAuth tokens
   - **Why**: Encrypted storage, centralized management
   - **How**: Always use credential selector in node settings

2. **Rotate Credentials**: Regularly update service account keys
   - **Why**: Limit exposure window if compromised
   - **How**: Regenerate keys in Google Cloud Console periodically

### Data Protection
1. **Encrypt Sensitive Files**: Use encryption before uploading
   - **Why**: Protects data if Drive account compromised
   - **How**: Use Code node to encrypt before upload

2. **Control File Access**: Use minimal permissions for service accounts
   - **Why**: Limits damage if credentials compromised
   - **How**: Share only necessary folders/files with service account

### Access Control
1. **Use Service Accounts for Automation**: Don't use personal account credentials
   - **Why**: Separates user access from automation
   - **How**: Create service account and share only necessary files

2. **Implement Audit Trails**: Log file operations for compliance
   - **Why**: Track who accessed/modified files
   - **How**: Use Set node to log operations or external audit system

## Workflow Design

### Node Placement
1. **Check Existence Before Operations**: Verify files/folders exist
   - **Why**: Prevents 404 errors
   - **How**: Use Search/List operations before Upload/Delete

2. **Handle Errors Gracefully**: Set up error handling for missing files
   - **Why**: Workflows don't fail on missing files
   - **How**: Use Error Trigger or IF node to check before operations

### Connection Management
1. **Reuse Credentials**: Use same credential across nodes
   - **Why**: Easier management, consistent access
   - **How**: Select existing credential from dropdown

2. **Test Credentials**: Always test before production
   - **Why**: Catch permission issues early
   - **How**: Use "Test step" button in N8N

### Data Flow
1. **Organize Files by Purpose**: Use folder structure for organization
   - **Why**: Makes manual review and management easier
   - **How**: Create folders for different file types/projects

2. **Document File Naming**: Use consistent naming conventions
   - **Why**: Easier to find and manage files
   - **How**: Use Set node to format file names consistently
</best_practices>

<troubleshooting>
## Common Errors

### Authentication Errors

<error id="err-401" http_code="401">
- **Symptom**: "Unauthorized" or "Invalid credentials"
- **Cause**: OAuth token expired, credential revoked, or insufficient scopes
- **Immediate Fix**:
  1. Check N8N credential status
  2. Delete and recreate credential
  3. Re-authenticate with Google account
  4. Verify Google account has Drive access
- **Prevention**:
  - Keep credentials up to date
  - Don't revoke credential access in Google settings
  - Use service account for automated workflows
- **N8N Logs**: Check execution logs for "invalid_grant" errors
- **Reference**: [Authentication](#authentication)
</error>

### Rate Limiting Errors

<error id="err-429" http_code="429">
- **Symptom**: "Too Many Requests" or "Rate limit exceeded"
- **Cause**: Exceeded Google Drive API rate limits
- **Immediate Fix**:
  1. Enable automatic retry with exponential backoff
  2. Add "Wait" node between operations (1-2 second delays)
  3. Reduce concurrent workflow executions
  4. Batch file operations together
- **Prevention**:
  - Space out scheduled workflows
  - Use pagination for large listings
  - Monitor API quota in Google Cloud Console
- **N8N Feature**: Built-in retry mechanism with exponential backoff
- **Reference**: [Rate Limits](#rate_limits)
</error>

### File Not Found Errors

<error id="err-404" http_code="404">
- **Symptom**: "File not found" or "Folder not found"
- **Cause**: File ID incorrect, file deleted, or not shared with credential account
- **Immediate Fix**:
  1. Verify file ID is correct
  2. Confirm file still exists in Google Drive
  3. Check file is shared with credential account
  4. Re-copy file ID from Google Drive URL
- **Prevention**:
  - Use search/list operations to get current file IDs
  - Add error handling for missing files
  - Check file access permissions
- **N8N Context**: Use node's file selector when possible instead of ID
</error>

### Permission Errors

<error id="err-403" http_code="403">
- **Symptom**: "Permission denied" or "Forbidden"
- **Cause**: Credential lacks access to file/folder
- **Immediate Fix**:
  1. Verify file/folder is shared with credential account
  2. Check account has edit/delete permissions (if needed)
  3. Re-authenticate credential with proper scopes
  4. Check folder is not team-drive specific without access
- **Prevention**:
  - Share files/folders with service account before workflow
  - Ensure credential has correct scopes
  - Verify permissions immediately after credential creation
- **N8N Context**: Use "Test step" to verify access before deployment
</error>

### File Size Errors

<error id="err-size" http_code="413">
- **Symptom**: "Payload too large" or "File too large"
- **Cause**: File exceeds upload size or memory limits
- **Immediate Fix**:
  1. Compress file before upload
  2. Split large file into chunks
  3. Increase N8N instance timeout settings
  4. Use different approach for large files
- **Prevention**:
  - Check file size before upload
  - Implement chunked uploads for large files
  - Use streaming uploads for files >100MB
- **N8N Context**: Monitor instance memory usage
</error>

## Diagnostic Steps

1. **Check N8N Execution Logs**
   - View execution history
   - Check input/output data
   - Review error messages
   - Inspect node configuration

2. **Test Node Isolation**
   - Run with sample file
   - Verify credential in N8N
   - Check Google Drive API quota
   - Verify file/folder exists in Drive

3. **Verify Configuration**
   - File ID/name is correct
   - Credential is selected
   - Folder path is correct
   - File type filters (if applicable)

4. **Review N8N Environment**
   - N8N version and node version
   - Available memory for file operations
   - Network connectivity to Google APIs
   - Instance resource limits

5. **Check Google Services Status**
   - Google Drive service status
   - Google API quota remaining
   - Recent API changes
   - File sharing and permission settings
</troubleshooting>

<related_docs>
## Documentation Structure

- **Operations**: See [google-drive-operations.md](#) for detailed operation reference
- **Examples**: Check N8N workflow templates for Google Drive patterns

## Related Nodes

- **Google Sheets**: [../google-sheets.md](#) - Spreadsheet integration and data management
- **HTTP Request**: [../Core/http-request.md](#) - For direct Google API calls
- **Set**: [../Core/set.md](#) - Data transformation before upload
- **IF**: [../Core/if.md](#) - Conditional logic for file operations

## External Resources

- **Official N8N Documentation**: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/
- **Google Drive API**: https://developers.google.com/drive/api
- **Google Drive Storage Limits**: https://support.google.com/drive/answer/15474
- **Community Discussions**: https://community.n8n.io/
- **N8N Workflows**: https://n8n.io/workflows/ (search "Google Drive")
- **Service Status**: https://www.google.com/appsstatus
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 85% (Core operations documented, some advanced features pending)
- **Validation Status**: Validated against official N8N documentation
- **Next Review**: 2025-11-30
- **N8N Version Tested**: Latest (self-hosted and cloud)
- **Node Version**: Latest n8n-nodes-base
</metadata_summary>
