# OneDrive for Business - Actions

---
type: connector-actions
connector_name: OneDrive for Business
action_count: 22
deprecated_count: 2
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [onedrive, file, folder, metadata, search, archive, conversion, sharing]
categories: [file_content, file_management, metadata, search, archive, conversion, sharing]
api_limits:
  calls_per_minute: 1.67
  calls_per_hour: 100
---

<action_summary>
**Total Actions**: 22 (20 current + 2 deprecated)

**Categories**:
- File Content: 3 actions (get content, get thumbnail)
- File Management: 9 actions (create, copy, move, delete, list, update)
- Metadata: 2 actions (get metadata by ID/path)
- Search: 2 actions (find files by ID/path)
- Archive: 1 action (extract archive)
- Conversion: 2 actions (convert file by ID/path)
- Sharing: 2 actions (create share link by ID/path)

**Most Used**:
1. Create file - Upload new files to OneDrive
2. Get file content - Download file data
3. Get file metadata - Retrieve file properties
4. List files in folder - Enumerate folder contents
5. Copy file - Duplicate files across locations

**Critical Limitations**:
- **Upload from URL**: Always reports success after 20 seconds (verify independently)
- **Archive extraction**: Max 50MB, 100 files limit
- **Copy operations**: May timeout on large files
- **Cross-tenant**: NOT supported
- **Multi-geo**: NOT supported

**API Rate Limit**: 100 calls per 60 seconds per connection
</action_summary>

For complete detailed documentation of all 22 OneDrive for Business actions including parameters, outputs, limitations, best practices, and examples, see the comprehensive actions documentation below.

---

## File Content Actions (3 Actions)

<action id="action-onedrive-001" operation_id="GetFileContent" category="read" complexity="low" throttle_impact="high">
### Get File Content

**Description**: Retrieves binary content of a file by identifier

**Operation ID**: `GetFileContent`

**Parameters**:
- **File** (string, required): File identifier
- **Infer Content Type** (boolean, optional): Auto-detect MIME type for downstream actions

**Returns**: Binary file content with inferred content-type header

**Limitations**:
<limitation id="lim-onedrive-action-001" severity="high">
May timeout on very large files (service load-dependent)
</limitation>

<limitation id="lim-onedrive-action-002" severity="high">
Respects "Prevent file download" organizational policies that may block access
</limitation>

**Best Practices**:
- Enable "Infer Content Type" for proper MIME handling
- Add error handling for policy-blocked scenarios
- Consider file size before retrieval (check metadata first)

**Use Cases**:
- Download files for processing
- Send file as email attachment
- File content analysis

**Example Flow**:
```
Get file metadata → Check size < threshold → Get file content → Process → Send email
```

**Throttle Impact**: High (bandwidth consumption + API call)
</action>

---

<action id="action-onedrive-002" operation_id="GetFileContentByPath" category="read" complexity="low" throttle_impact="high">
### Get File Content Using Path

**Description**: Retrieves binary content using file path reference

**Operation ID**: `GetFileContentByPath`

**Parameters**:
- **File Path** (string, required): Full path to file
- **Infer Content Type** (boolean, optional): MIME type detection

**Returns**: Binary file content

**When to Use**: When file ID unknown but path is available

**Best Practices**:
- Use file ID variant when possible (faster lookup)
- Validate path format before retrieval

**Throttle Impact**: High (bandwidth + API call)
</action>

---

<action id="action-onedrive-003" operation_id="GetFileThumbnail" category="read" complexity="low" throttle_impact="low">
### Get File Thumbnail

**Description**: Retrieves thumbnail image of file

**Operation ID**: `GetFileThumbnail`

**Parameters**:
- **File** (string, required): File identifier
- **Thumbnail Size** (string, required): Desired thumbnail dimensions

**Returns**: Thumbnail object
```json
{
  "url": "string",
  "width": "number",
  "height": "number"
}
```

**Limitations**:
<limitation id="lim-onedrive-action-003" severity="medium">
Thumbnail URLs are only valid for 6 hours
</limitation>

**Best Practices**:
- Cache thumbnail URLs temporarily (max 6 hours)
- Refresh URLs if expired
- Use for preview generation, not permanent storage

**Use Cases**:
- Preview generation in UI
- Image galleries
- Document thumbnails

**Throttle Impact**: Low
</action>

---

## File Management Actions (9 Actions)

<action id="action-onedrive-004" operation_id="CreateFile" category="create" complexity="low" throttle_impact="medium">
### Create File

**Description**: Creates a new file in OneDrive folder

**Operation ID**: `CreateFile`

**Parameters**:
- **Folder Path** (string, required): Destination folder
- **File Name** (string, required): Name for new file
- **File Content** (binary, required): Binary file data

**Returns**: `BlobMetadata` object
```json
{
  "Id": "string",
  "Name": "string",
  "DisplayName": "string",
  "Path": "string",
  "LastModified": "datetime",
  "Size": "number",
  "MediaType": "string",
  "IsFolder": "boolean",
  "ETag": "string",
  "FileLocator": "string"
}
```

**Behavior**:
<limitation id="lim-onedrive-action-004" severity="medium">
Certain characters are disallowed by OneDrive and will be replaced by underscores
</limitation>

**Disallowed Characters**: `\ / : * ? " < > |`

**Best Practices**:
- Validate filename before creation (remove disallowed chars)
- Overwrites existing file with same name by default
- Use unique naming or check existence first

**Example Use Case**: Upload processed document to "Processed" folder

**Throttle Impact**: Medium
</action>

---

<action id="action-onedrive-005" operation_id="CopyDriveFile" category="utility" complexity="medium" throttle_impact="medium">
### Copy File

**Description**: Copies a file to another location within OneDrive

**Operation ID**: `CopyDriveFile`

**Parameters**:
- **File** (string, required): Source file identifier
- **Destination Path** (string, required): Destination path including filename
- **Overwrite** (boolean, optional): Overwrite if file exists at destination

**Returns**: `BlobMetadata`

**Limitations**:
<limitation id="lim-onedrive-action-005" severity="high">
Larger files may fail with timeout error (due to needing to take longer to copy larger files). Threshold varies based on service load.
</limitation>

**Best Practices**:
- Check destination folder exists before copy
- Set "Overwrite" parameter explicitly
- Verify completion with Get File Metadata for large files
- Implement retry logic for timeout errors

**Use Cases**:
- File backup workflows
- Duplicate files for processing
- Archive operations

**Example Flow**:
```
Copy file → Wait 5 seconds → Get file metadata from destination → Verify success
```

**Throttle Impact**: Medium (increases with file size)
</action>

---

<action id="action-onedrive-006" operation_id="CopyDriveFileByPath" category="utility" complexity="medium" throttle_impact="medium">
### Copy File Using Path

**Description**: Copies file using path reference instead of ID

**Operation ID**: `CopyDriveFileByPath`

**Parameters**:
- **File Path** (string, required): Source file path
- **Destination Path** (string, required): Destination path including filename
- **Overwrite** (boolean, optional)

**Returns**: `BlobMetadata`

**When to Use**: When source file ID unavailable but path is known

**Limitations**: Same as Copy File action (timeout on large files)

**Throttle Impact**: Medium
</action>

---

<action id="action-onedrive-007" operation_id="MoveFile" category="utility" complexity="low" throttle_impact="low">
### Move or Rename a File

**Description**: Moves file to new location or renames it

**Operation ID**: `MoveFile`

**Parameters**:
- **File** (string, required): File identifier
- **Destination Path** (string, required): New location/name
- **Overwrite** (boolean, optional): Overwrite if target exists

**Returns**: `BlobMetadata`

**Behavior**:
- Provide either new path, new name, or both
- Maintains file ID after operation (ID unchanged)
- Faster than copy+delete pattern

**Best Practices**:
- Use for rename operations (more efficient than copy/delete)
- File ID remains constant (references don't break)

**Use Cases**:
- File organization workflows
- Rename based on content analysis
- Move to archive folder after processing

**Throttle Impact**: Low
</action>

---

<action id="action-onedrive-008" operation_id="MoveFileByPath" category="utility" complexity="low" throttle_impact="low">
### Move or Rename a File Using Path

**Description**: Moves/renames file using path reference

**Operation ID**: `MoveFileByPath`

**Parameters**:
- **File Path** (string, required): Source file path
- **Destination Path** (string, required): New path/name
- **Overwrite** (boolean, optional)

**Returns**: `BlobMetadata`

**When to Use**: Path-based move when ID unavailable

**Throttle Impact**: Low
</action>

---

<action id="action-onedrive-009" operation_id="UpdateFile" category="update" complexity="low" throttle_impact="high">
### Update File

**Description**: Updates content of existing file (replaces content)

**Operation ID**: `UpdateFile`

**Parameters**:
- **File** (string, required): File identifier
- **File Content** (binary, required): New binary content

**Returns**: `BlobMetadata` (updated metadata)

**Behavior**:
- Creates new version if versioning enabled
- Locks file briefly during update
- File ID remains unchanged

**Best Practices**:
- Get file metadata first to verify file exists
- Consider version control implications
- Add error handling for file locks

**Use Cases**:
- Update processed document
- Replace file content after modification
- Automated content updates

**Throttle Impact**: High (bandwidth consumption)
</action>

---

<action id="action-onedrive-010" operation_id="DeleteFile" category="delete" complexity="low" throttle_impact="low">
### Delete File

**Description**: Permanently deletes a file from OneDrive

**Operation ID**: `DeleteFile`

**Parameters**:
- **File** (string, required): File identifier

**Returns**: No data

**Warning**:
<limitation id="lim-onedrive-action-006" severity="critical">
Cannot be undone through connector. No recycle bin recovery via API.
</limitation>

**Best Practices**:
- Implement confirmation workflows before deletion
- Consider moving to archive folder instead
- Log deletions for audit trail

**Use Cases**:
- Cleanup workflows
- Remove temporary files
- Delete after processing complete

**Throttle Impact**: Low
</action>

---

<action id="action-onedrive-011" operation_id="ListFolderV2" category="read" complexity="low" throttle_impact="low">
### List Files in Folder

**Description**: Lists all files in specified folder

**Operation ID**: `ListFolderV2`

**Parameters**:
- **Folder** (string, required): Folder identifier
- **Include Subfolders** (boolean, optional): Recursive listing

**Returns**: `BlobMetadataPage` object (array of file metadata)

**Limitations**:
<limitation id="lim-onedrive-action-007" severity="medium">
Connector will only display up to 200 items per folder in the file picker. Users may struggle locating items in folders exceeding this threshold.
</limitation>

**Best Practices**:
- Not recursive by default (set Include Subfolders if needed)
- Use for batch processing workflows
- Combine with filtering for targeted operations

**Use Cases**:
- Enumerate files for processing
- File inventory workflows
- Batch operations

**Example Flow**:
```
List files in folder → Apply to each file → Check criteria → Process matching files
```

**Throttle Impact**: Low (metadata only)
</action>

---

<action id="action-onedrive-012" operation_id="ListRootFolder" category="read" complexity="low" throttle_impact="low">
### List Root Folder

**Description**: Lists files in OneDrive root directory

**Operation ID**: `ListRootFolder`

**Parameters**: None

**Returns**: `BlobMetadataPage` object (files in root only)

**Note**: Excludes subfolders' contents

**When to Use**: Quick access to root-level files

**Throttle Impact**: Low
</action>

---

<action id="action-onedrive-013" operation_id="CopyFile" category="utility" complexity="medium" throttle_impact="high">
### Upload File from URL

**Description**: Downloads file from URL and uploads to OneDrive

**Operation ID**: `CopyFile` (same as copy operation)

**Parameters**:
- **File URL** (string, required): Source URL
- **Destination Path** (string, required): OneDrive destination including filename
- **Overwrite** (boolean, optional): Overwrite existing file

**Returns**: `BlobMetadata`

**CRITICAL LIMITATION**:
<limitation id="lim-onedrive-action-008" severity="critical">
Will ALWAYS report success after 20 seconds regardless of the actual result. Actual upload time may exceed 20 seconds depending on file size and download rate.
</limitation>

**REQUIRED WORKAROUND**:
<limitation id="lim-onedrive-action-009" severity="critical">
You should ALWAYS create logic in the flow to check for the existence of the file and/or a timeout before operating on the uploaded file data
</limitation>

**Best Practices**:
1. **Never trust immediate success**: Implement verification
2. **Add delay**: Wait 30-60 seconds before verification
3. **Verify existence**: Get file metadata after delay
4. **Check size**: Compare expected vs actual file size
5. **Implement timeout**: Set maximum wait time

**Verified Upload Pattern**:
```
Upload file from URL
→ Wait 30 seconds (Delay action)
→ Get file metadata from destination
→ Condition: File exists AND Size > 0
  → Success: Continue processing
  → Failure: Log error, retry or alert
```

**Use Cases**:
- Import files from external sources
- Download and archive web content
- Automated file imports

**Throttle Impact**: High (download + upload bandwidth)
</action>

---

## Metadata Actions (2 Actions)

<action id="action-onedrive-014" operation_id="GetFileMetadata" category="read" complexity="low" throttle_impact="low">
### Get File Metadata

**Description**: Retrieves comprehensive file properties and metadata

**Operation ID**: `GetFileMetadata`

**Parameters**:
- **File** (string, required): File identifier

**Returns**: `BlobMetadata` object
```json
{
  "Id": "string",
  "Name": "string",
  "DisplayName": "string",
  "Path": "string",
  "LastModified": "datetime",
  "LastModifiedBy": {
    "DisplayName": "string",
    "Email": "string"
  },
  "Size": "number",
  "MediaType": "string",
  "IsFolder": "boolean",
  "ETag": "string",
  "FileLocator": "string",
  "Created": "datetime",
  "CreatedBy": {
    "DisplayName": "string"
  },
  "SharingStatus": "string",
  "WebUrl": "string"
}
```

**Best Practices**:
- Use to verify file size before content retrieval
- Check ETag for content change detection
- Cache metadata to reduce API calls

**Use Cases**:
- File existence verification
- Size validation before processing
- Metadata-based routing
- Change detection (ETag comparison)

**Throttle Impact**: Low (metadata only, no content)
</action>

---

<action id="action-onedrive-015" operation_id="GetFileMetadataByPath" category="read" complexity="low" throttle_impact="low">
### Get File Metadata Using Path

**Description**: Retrieves metadata using file path reference

**Operation ID**: `GetFileMetadataByPath`

**Parameters**:
- **File Path** (string, required): Full path to file

**Returns**: `BlobMetadata` object (same as Get File Metadata)

**When to Use**: Path-based metadata retrieval when ID unavailable

**Best Practices**:
- Prefer ID-based variant when possible (faster)
- Validate path format before call

**Throttle Impact**: Low
</action>

---

## Search Actions (2 Actions)

<action id="action-onedrive-016" operation_id="FindFiles" category="read" complexity="medium" throttle_impact="medium">
### Find Files in Folder

**Description**: Searches for files matching criteria in specified folder

**Operation ID**: `FindFiles`

**Parameters**:
- **Folder** (string, required): Folder identifier to search
- **Search Query** (string, required): Filename pattern or regex
- **Search Mode** (string, required): "Search" or "Regular Expression Pattern Match"
- **Max Results** (integer, optional): 1-100 files to return

**Returns**: Array of `BlobMetadata` objects (matching files)

**Search Modes**:
1. **Search**: Uses search engine similar to standard OneDrive search
2. **Regular Expression Pattern Match**: Treats query as regex pattern

**Best Practices**:
- Use regex mode for complex pattern matching
- Set Max Results appropriately (balance performance vs completeness)
- Combine with filtering for targeted results

**Use Cases**:
- Find files by naming pattern
- Conditional file processing
- File discovery workflows

**Example Patterns**:
```
Search Mode: ".*invoice.*\\.pdf$"  → Find all PDF invoices
Search Mode: "report_\\d{4}_\\d{2}"  → Find reports with YYYY_MM pattern
```

**Throttle Impact**: Medium (increases with result count)
</action>

---

<action id="action-onedrive-017" operation_id="FindFilesByPath" category="read" complexity="medium" throttle_impact="medium">
### Find Files in Folder By Path

**Description**: Searches for files using folder path reference

**Operation ID**: `FindFilesByPath`

**Parameters**:
- **Folder Path** (string, required): Folder path to search
- **Search Query** (string, required): Pattern
- **Search Mode** (string, required): Search method
- **Max Results** (integer, optional): 1-100

**Returns**: Array of `BlobMetadata`

**When to Use**: Path-based search when folder ID unavailable

**Throttle Impact**: Medium
</action>

---

## Archive Actions (1 Action)

<action id="action-onedrive-018" operation_id="ExtractFolderV2" category="utility" complexity="medium" throttle_impact="medium">
### Extract Archive to Folder

**Description**: Extracts archive file (.zip, etc.) to OneDrive folder

**Operation ID**: `ExtractFolderV2`

**Parameters**:
- **Source Archive Path** (string, required): Path to archive file
- **Destination Folder Path** (string, required): Extraction target
- **Overwrite** (boolean, optional): Overwrite existing files

**Returns**: Array of `BlobMetadata` (extracted files)

**CRITICAL LIMITATIONS**:
<limitation id="lim-onedrive-action-010" severity="critical">
Maximum archive size is 50 MB and 100 files inside. Exceeding limits causes operation failure.
</limitation>

<limitation id="lim-onedrive-action-011" severity="high">
Does not support multi-byte characters in the file name (encoding issues)
</limitation>

**Best Practices**:
1. **Pre-validate archive**:
   - Check archive size < 50MB
   - Verify file count < 100 (if possible)
2. **Add error handling**: Catch extraction failures
3. **Verify extraction**: List destination folder after extraction

**Validation Pattern**:
```
Get archive metadata
→ Condition: Size < 52,428,800 bytes (50MB)
  → True: Extract archive → List destination folder → Process files
  → False: Log error "Archive too large" → Send alert
```

**Use Cases**:
- Automated archive unpacking
- Bulk file imports
- Compressed file processing

**Throttle Impact**: Medium
</action>

---

## Conversion Actions (2 Actions)

<action id="action-onedrive-019" operation_id="ConvertFile" category="utility" complexity="high" throttle_impact="high">
### Convert File

**Description**: Converts file to another format (e.g., to PDF)

**Operation ID**: `ConvertFile`

**Parameters**:
- **File** (string, required): File identifier
- **Target Type** (string, optional): Destination format (e.g., "pdf")

**Returns**: Binary file content (converted format)

**Supported Conversions**: See https://aka.ms/onedriveconversions

**Known Issues**:
<limitation id="lim-onedrive-action-012" severity="high">
HTML-to-PDF conversions may fail with "Bad gateway" errors. Recommend adding delays between file creation and conversion.
</limitation>

<limitation id="lim-onedrive-action-013" severity="high">
Cannot convert digitally signed, password-protected, or IRM-restricted Word documents to PDF for security reasons
</limitation>

**Best Practices**:
1. **Add delay**: Wait 5-10 seconds after file creation before conversion
2. **Error handling**: Catch "Bad gateway" (502) errors
3. **Retry logic**: Implement exponential backoff
4. **Verify format**: Check source file supports conversion

**Conversion Pattern**:
```
Create file (Word doc)
→ Wait 10 seconds (Delay action)
→ Convert file to PDF
→ Error handling: If 502, wait and retry
→ Save converted PDF
```

**Use Cases**:
- Document format standardization (Word → PDF)
- Export workflows
- Format conversion pipelines

**Throttle Impact**: High (content processing + bandwidth)
</action>

---

<action id="action-onedrive-020" operation_id="ConvertFileByPath" category="utility" complexity="high" throttle_impact="high">
### Convert File Using Path

**Description**: Converts file using path reference

**Operation ID**: `ConvertFileByPath`

**Parameters**:
- **File Path** (string, required): Source file path
- **Target Type** (string, optional): Destination format

**Returns**: Binary converted content

**Limitations**: Same as Convert File action (delays, security restrictions)

**When to Use**: Path-based conversion when ID unavailable

**Throttle Impact**: High
</action>

---

## Sharing Actions (2 Actions)

<action id="action-onedrive-021" operation_id="CreateShareLinkV2" category="utility" complexity="medium" throttle_impact="low">
### Create Share Link

**Description**: Creates a sharing link for file or folder

**Operation ID**: `CreateShareLinkV2`

**Parameters**:
- **File/Folder** (string, required): Item identifier
- **Link Type** (string, required): Sharing link type
  - `view` - Read-only access
  - `edit` - Modify permissions
  - `embed` - Embeddable link
- **Link Scope** (string, optional): Access boundary
  - `anonymous` - Public link (anyone with link)
  - `organization` - Internal users only

**Returns**: `SharingLink` object
```json
{
  "webUrl": "string"
}
```

**Limitations**:
<limitation id="lim-onedrive-action-014" severity="high">
May be blocked by organizational sharing policies (e.g., prevent external sharing)
</limitation>

**Best Practices**:
- Verify link scope matches security requirements
- Test with organizational policies applied
- Handle policy-blocked errors gracefully

**Use Cases**:
- Generate file sharing links
- Temporary access provisioning
- External collaboration workflows

**Policy Warning**: Anonymous links may be disabled by IT admins

**Throttle Impact**: Low
</action>

---

<action id="action-onedrive-022" operation_id="CreateShareLinkByPathV2" category="utility" complexity="medium" throttle_impact="low">
### Create Share Link By Path

**Description**: Creates sharing link using path reference

**Operation ID**: `CreateShareLinkByPathV2`

**Parameters**:
- **File/Folder Path** (string, required): Item path
- **Link Type** (string, required): Type of link
- **Link Scope** (string, optional): Access scope

**Returns**: `SharingLink` object

**When to Use**: Path-based sharing when ID unavailable

**Limitations**: Same policy restrictions as Create Share Link

**Throttle Impact**: Low
</action>

---

## Deprecated Actions

<deprecated_actions>
| Action | Operation ID | Status | Replacement |
|--------|-------------|--------|-------------|
| Create share link | CreateShareLink | Deprecated | CreateShareLinkV2 |
| Create share link by path | CreateShareLinkByPath | Deprecated | CreateShareLinkByPathV2 |
</deprecated_actions>

**Deprecation Note**: Use V2 versions for new implementations. Deprecated actions no longer actively maintained.

---

## Common Error Codes

<error id="err-onedrive-action-001" http_code="403" severity="high">
**Error**: Access Denied - File locked or policy blocking

**Causes**:
- File locked by Excel or other application
- "Prevent file download" organizational policy
- "Control access from unmanaged devices" policy
- Network location-based restrictions

**Solutions**:
1. Verify no active Excel sessions on file
2. Check organizational policies in SharePoint admin center
3. Review device compliance requirements
4. Test with managed device
5. Contact IT admin for policy exceptions

**Example Policy**: "Control access to SharePoint and OneDrive data based on network location"
</error>

<error id="err-onedrive-action-002" http_code="408" severity="high">
**Error**: Timeout - Operation exceeded time limit

**Causes**:
- Large file copy operation
- Service load high
- Network latency issues

**Solutions**:
1. Break large operations into smaller chunks
2. Implement retry logic with exponential backoff
3. Monitor service health status
4. Increase timeout thresholds if possible
5. Use properties-only variants when content not needed

**Note**: Timeout thresholds vary based on service load
</error>

<error id="err-onedrive-action-003" http_code="502" severity="medium">
**Error**: Bad Gateway - Conversion service failure

**Specific To**: Convert File actions (especially HTML → PDF)

**Cause**: Service delay; file not ready for conversion

**Solutions**:
1. Add 5-10 second delay between file creation and conversion
2. Implement retry logic (exponential backoff)
3. Catch 502 errors gracefully
4. Verify file format supports conversion

**Pattern**:
```
Create file → Wait 10 seconds → Try convert → On 502: Wait 5s → Retry
```
</error>

<error id="err-onedrive-action-004" http_code="404" severity="medium">
**Error**: Not Found - File or folder doesn't exist

**Causes**:
- Incorrect file path or ID
- File deleted before operation
- Typo in path reference
- File in recycle bin

**Solutions**:
1. Verify file path format (case-sensitive)
2. Check file ID is current (IDs change on move)
3. Confirm file not in recycle bin
4. Use Get File Metadata to verify existence before operations
</error>

<error id="err-onedrive-action-005" http_code="429" severity="critical">
**Error**: Too Many Requests - API throttling

**Cause**: Exceeded 100 API calls per 60 seconds per connection

**Solutions**:
1. Add Delay actions in loops (minimum 1 second)
2. Reduce operation frequency
3. Distribute load across multiple connections
4. Implement batch processing
5. Use properties-only variants to reduce call volume

**Throttle Formula**:
```
Max operations per minute = 100 / (calls per operation)
Example: If operation uses 2 calls, max = 50 operations/minute
```
</error>

<error id="err-onedrive-action-006" severity="high">
**Error**: Upload from URL false success

**Specific To**: Upload file from URL action

**Cause**: 20-second timeout before actual upload completes

**Solutions**:
1. **Always verify**: Don't trust immediate success
2. Add 30-60 second delay before verification
3. Get file metadata to confirm existence
4. Check file size matches expected
5. Implement maximum wait timeout

**Required Verification**:
```
Upload from URL
→ Wait 30 seconds
→ Get file metadata
→ Condition: File exists AND Size > 0
```
</error>

<error id="err-onedrive-action-007" severity="high">
**Error**: Archive extraction failure

**Specific To**: Extract Archive action

**Causes**:
- Archive exceeds 50MB limit
- Archive contains more than 100 files
- Multi-byte characters in filenames
- Corrupted archive

**Solutions**:
1. Validate archive size < 50MB before extraction
2. Use ASCII-only filenames in archives
3. Pre-check file count if possible
4. Add error handling for extraction failures

**Validation**:
```
Get archive metadata
→ Condition: Size < 52,428,800
  → Extract
  → Log "Archive too large"
```
</error>

<error id="err-onedrive-action-008" severity="medium">
**Error**: Encrypted file corrupt error

**Cause**: Encrypted files saved on OneDrive throw corrupt file errors through connector

**Solutions**:
1. Decrypt files before processing
2. Handle encryption errors gracefully
3. Verify file opens manually before automation
4. Log encrypted files for manual processing
</error>

<error id="err-onedrive-action-009" severity="medium">
**Error**: Filename characters modified

**Cause**: OneDrive replaces disallowed characters with underscores

**Disallowed**: `\ / : * ? " < > |`

**Solutions**:
1. Pre-validate filenames before creation
2. Remove/replace disallowed characters proactively
3. Log original vs modified names for tracking

**Example**:
```
Original: "Report:2025.docx"
Created:  "Report_2025.docx"
```
</error>

---

## Best Practices Summary

### File Operations

1. **Upload from URL Verification**:
   - Never trust immediate success
   - Add 30-60 second delay
   - Verify with Get File Metadata
   - Check file size matches expected

2. **Large File Handling**:
   - Check size before copy operations
   - Implement timeout error handling
   - Use retry logic with exponential backoff
   - Monitor service health for load issues

3. **File Naming**:
   - Remove disallowed characters: `\ / : * ? " < > |`
   - Use underscores instead of special chars
   - Validate names before creation

4. **Delete Operations**:
   - Implement confirmation workflows
   - Consider move-to-archive instead
   - Log deletions for audit trail
   - No recycle bin recovery via API

### Conversion Operations

1. **PDF Conversion**:
   - Add 5-10 second delay after file creation
   - Catch 502 Bad Gateway errors
   - Implement retry logic
   - Verify source format compatibility

2. **Security Restrictions**:
   - Cannot convert digitally signed docs
   - Cannot convert password-protected files
   - Cannot convert IRM-restricted documents

### Archive Operations

1. **Pre-Validation**:
   - Check archive size < 50MB
   - Verify file count < 100 (if possible)
   - Use ASCII-only filenames

2. **Error Handling**:
   - Add extraction failure handling
   - Verify extraction completion
   - List destination folder to confirm

### Metadata Management

1. **Use Metadata First**:
   - Check file size before content retrieval
   - Verify existence before operations
   - Cache metadata to reduce API calls
   - Use ETag for change detection

2. **ID vs Path**:
   - Prefer ID-based actions (faster lookup)
   - Use path variants when ID unavailable
   - IDs remain constant after move/rename

### Search Operations

1. **Query Optimization**:
   - Use regex mode for complex patterns
   - Set appropriate Max Results (1-100)
   - Combine with filtering for precision

2. **Performance**:
   - Account for 200-item folder picker limit
   - Use targeted searches instead of list-all

### Sharing Operations

1. **Link Scope Selection**:
   - Verify organizational policies before anonymous links
   - Use "organization" scope for internal sharing
   - Test with policies applied before production

2. **Policy Awareness**:
   - Handle policy-blocked errors gracefully
   - Anonymous sharing may be disabled by admins
   - Document sharing requirements

### API Throttling Management

1. **Rate Monitoring**:
   - Track API calls per flow (100/60s limit)
   - Add delays in loops (minimum 1 second)
   - Monitor concurrent flow executions

2. **Call Reduction**:
   - Use properties-only variants when possible
   - Cache metadata instead of repeated queries
   - Batch operations to reduce overhead

3. **Error Handling**:
   - Implement retry logic for 429 errors
   - Use exponential backoff strategy
   - Distribute load if throttling common

### Cross-Tenant and Multi-Geo Constraints

<limitation id="lim-onedrive-action-015" severity="critical">
Cross-tenant access UNSUPPORTED. User in "contoso-my.sharepoint.com" cannot access files in "microsoft-my.sharepoint.com"
</limitation>

<limitation id="lim-onedrive-action-016" severity="critical">
Multi-geo scenarios are NOT supported. Both user and file must reside in same geographic region.
</limitation>

<limitation id="lim-onedrive-action-017" severity="critical">
Cross-drive functionality is NOT supported. Connector operates only on connected account's owned data.
</limitation>

**Workaround**: Implement manual file transfer or Azure Functions for cross-tenant scenarios

### Account Requirements

<limitation id="lim-onedrive-action-018" severity="high">
Use Microsoft business or school accounts instead of Microsoft personal accounts
</limitation>

**Authentication**: Requires authorization for page access

---

## Common Workflow Patterns

### Pattern 1: Verified URL Upload
```
Upload file from URL
→ Delay: 30 seconds
→ Get file metadata
→ Condition: File exists AND Size > 0
  → Success:
    → Process file
    → Log success
  → Failure:
    → Log error "Upload verification failed"
    → Send admin alert
    → Retry OR mark for manual review
```

**Why**: Compensates for 20-second false success issue

---

### Pattern 2: Safe Large File Copy
```
Get source file metadata
→ Condition: Size < 100MB threshold
  → True:
    → Copy file
    → Wait 5 seconds
    → Get destination metadata
    → Verify success
  → False:
    → Log "File too large for copy"
    → Use alternate method (manual or chunked)
```

**Why**: Prevents timeout errors on large files

---

### Pattern 3: Archive Extraction with Validation
```
Get archive metadata
→ Condition: Size < 52,428,800 (50MB)
  → True:
    → Extract archive to folder
    → Error handling: Catch extraction failures
    → List destination folder
    → Condition: File count > 0
      → Process extracted files
      → Delete archive (optional)
    → Failure: Log "Extraction failed"
  → False:
    → Log "Archive exceeds 50MB limit"
    → Send alert to admin
```

**Why**: Pre-validates against 50MB limit, verifies extraction

---

### Pattern 4: PDF Conversion with Retry
```
Create file (Word document)
→ Delay: 10 seconds
→ Convert file to PDF
→ Error handling:
  → On 502 Bad Gateway:
    → Delay: 5 seconds
    → Retry conversion (max 3 attempts)
  → On other error:
    → Log error
    → Send alert
→ Success:
  → Save PDF to destination
  → Delete source file (optional)
```

**Why**: Handles conversion timing issues and service delays

---

### Pattern 5: File Search and Process
```
Find files in folder (regex: ".*invoice.*\\.pdf$")
→ Apply to each found file:
  → Get file content
  → Parse PDF (AI Builder)
  → Extract invoice data
  → Create item in database
  → Move file to "Processed" folder
  → Log processing
```

**Why**: Targeted processing of specific file types

---

## Action Comparison Matrix

| Feature | By ID | By Path | Performance Impact |
|---------|-------|---------|-------------------|
| Get File Content | ✅ | ✅ | High (bandwidth) |
| Get File Metadata | ✅ | ✅ | Low |
| Copy File | ✅ | ✅ | Medium-High (size-dependent) |
| Move File | ✅ | ✅ | Low |
| Convert File | ✅ | ✅ | High (processing) |
| Create Share Link | ✅ | ✅ | Low |
| Find Files | ✅ | ✅ | Medium (result count) |

**Decision Tree**:
1. **Have file ID?** → Use ID variant (faster)
2. **Only have path?** → Use path variant
3. **Need to enumerate?** → Use List or Find actions
4. **Large files?** → Add error handling for timeouts

---

## API Rate Limits and Throttling

**Global Limit**: 100 API calls per connection per 60 seconds

**Action Impact**:
- Get File Content: ~2 calls (metadata + content)
- Get File Metadata: ~1 call
- Create File: ~1 call
- Copy File: ~2 calls
- List Files: ~1-2 calls (depends on result count)
- Upload from URL: ~2-3 calls

**Throttle Management**:
1. **Monitor Usage**: Track flow runs and API calls
2. **Add Delays**: 1-2 seconds between operations in loops
3. **Batch Processing**: Group operations to reduce overhead
4. **Multiple Connections**: Distribute load if needed
5. **Properties-Only**: Use metadata variants when content not needed

**Formula**:
```
Max operations per minute = 100 / (API calls per operation)
Example: Get File Content uses 2 calls
Max = 100 / 2 = 50 file retrievals per minute
```

---

## Cross-Tenant and Multi-Geo Limitations

**NOT Supported**:
- ❌ Cross-tenant file access
- ❌ Multi-geo scenarios
- ❌ Cross-drive functionality
- ❌ Shared files across tenant boundaries

**Example Restriction**:
```
User: user@contoso-my.sharepoint.com
Cannot access: Files in microsoft-my.sharepoint.com
```

**Workarounds**:
- Manual file transfer
- Azure Functions for cross-tenant operations
- Use SharePoint connector if files in SharePoint-backed OneDrive
- Implement custom API integration

---

## Organizational Policy Impact

Three common policies affecting connector operations:

1. **"(Sharing) Prevent file download"**
   - **Impact**: Blocks Get File Content actions
   - **Workaround**: Use properties-only, request policy exception

2. **"Control access from unmanaged devices"**
   - **Impact**: Prevents unverified device access
   - **Workaround**: Ensure device compliance, use managed devices

3. **"Control access based on network location"**
   - **Impact**: Restricts network-based access
   - **Workaround**: Verify network allowlist, use approved networks

**Best Practice**: Test all flows with organizational policies applied before production deployment

---

## Official Documentation

<official_docs>
https://learn.microsoft.com/en-us/connectors/onedriveforbusiness/
</official_docs>

**Related Documentation**:
- OneDrive API: https://learn.microsoft.com/en-us/onedrive/developer/rest-api/
- Supported Conversions: https://aka.ms/onedriveconversions
- Microsoft Graph Files API: https://learn.microsoft.com/en-us/graph/api/resources/onedrive

---

**Last Updated**: 2025-10-31
**Fetch Date**: 2025-10-31
**Version**: 1.0
