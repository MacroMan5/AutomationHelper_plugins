# SharePoint - Actions

---
type: connector-actions
connector_name: SharePoint
action_count: 51
deprecated_count: 2
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [sharepoint, list, library, file, item, folder, approval, hub site, syntex, document generation]
categories: [file_operations, folder_operations, list_operations, library_operations, sharing, approval, hub_site, document_generation, utility]
api_limits:
  calls_per_minute: 10
  calls_per_hour: 600
  bandwidth_mb_per_minute: 1000
---

<action_summary>
**Total Actions**: 51 (49 current + 2 deprecated)

**Categories**:
- File Operations: 18 actions (CRUD, check in/out, content, attachments)
- Folder Operations: 8 actions (create, copy, move, list, extract)
- List/Item Operations: 6 actions (CRUD, query, change tracking)
- Library Operations: 5 actions (discovery, document sets)
- Sharing/Permissions: 3 actions (links, access grants)
- Approval Operations: 3 actions (request, status, deprecated)
- Hub Site Operations: 4 actions (join workflows, approval)
- Document Generation: 2 actions (Syntex, Agreements)
- Utility: 2 actions (user resolution, HTTP)

**Most Used**:
1. Get items - Retrieve filtered list data
2. Create item - Add records to lists
3. Update item - Modify list records
4. Create file - Upload documents
5. Get file content - Download files

**API Rate Limit**: 600 calls per 60 seconds per connection
**Bandwidth Limit**: 1000 MB per 60 seconds per connection
</action_summary>

For complete detailed documentation of all 51 SharePoint actions including parameters, outputs, limitations, best practices, and examples, see the comprehensive actions documentation below.

---

## File Operations (18 Actions)

<action id="action-sharepoint-001" operation_id="CreateFile" category="create" complexity="low" throttle_impact="medium">
### Create File

**Description**: Uploads new document to SharePoint library

**Operation ID**: `CreateFile`

**Parameters**:
- **Site Address** (string, required): SharePoint site URL
- **Folder Path** (string, required): Destination path (must begin with existing library)
- **File Name** (string, required): Document label
- **File Content** (binary, required): Document data

**Returns**: `SPBlobMetadataResponse`
```json
{
  "Id": "string",
  "Name": "string",
  "Path": "string",
  "Size": "number",
  "ETag": "string",
  "Created": "datetime",
  "Modified": "datetime"
}
```

**Limitations**:
<limitation id="lim-sp-file-001" severity="high">
Image files up to 90MB in size are supported for upload
</limitation>

**Best Practices**:
- Validate folder path exists before upload
- Use unique file names to avoid conflicts
- Set "If another file is already there" parameter for conflict resolution

**Example Use Case**: Upload processed invoice PDFs to "Documents/Invoices" library

**Throttle Impact**: Medium (counts toward 600 calls/60s limit)
</action>

---

<action id="action-sharepoint-002" operation_id="GetFileContent" category="read" complexity="low" throttle_impact="high">
### Get File Content

**Description**: Retrieves document binary data by identifier

**Operation ID**: `GetFileContent`

**Parameters**:
- **Site Address** (string, required): SharePoint site URL
- **File Identifier** (string, required): Unique file reference
- **Infer Content Type** (boolean, optional): Auto-detect MIME type

**Returns**: Binary file content with inferred content-type header

**Best Practices**:
- Enable "Infer Content Type" for proper MIME handling
- Use file identifiers instead of paths (faster retrieval)
- Consider bandwidth limits for large files (1000 MB/60s)

**Example Use Case**: Download file to send as email attachment

**Throttle Impact**: High (bandwidth consumption + API call)
</action>

---

<action id="action-sharepoint-003" operation_id="GetFileContentByPath" category="read" complexity="low" throttle_impact="high">
### Get File Content Using Path

**Description**: Retrieves document data via file path reference

**Operation ID**: `GetFileContentByPath`

**Parameters**:
- **Site Address** (string, required): SharePoint site URL
- **File Path** (string, required): Location reference
- **Infer Content Type** (boolean, optional): Auto-detect MIME type

**Returns**: Binary file content

**When to Use**: When you have file path but not identifier

**Throttle Impact**: High (bandwidth + API call)
</action>

---

<action id="action-sharepoint-004" operation_id="GetFileMetadata" category="read" complexity="low" throttle_impact="low">
### Get File Metadata

**Description**: Gets file information such as size, etag, created date, etc.

**Operation ID**: `GetFileMetadata`

**Parameters**:
- **Site Address** (string, required): SharePoint site URL
- **File Identifier** (string, required): Unique reference

**Returns**: `SPBlobMetadataResponse`
```json
{
  "Id": "string",
  "Name": "string",
  "Size": "number",
  "ETag": "string",
  "Created": "datetime",
  "Modified": "datetime",
  "Path": "string"
}
```

**Note**: For column values, use "Get File Properties" instead

**Best Practices**:
- Capture ETag before updating files (prevents conflicts)
- Use this for size checks before downloads

**Throttle Impact**: Low (metadata only, no content transfer)
</action>

---

<action id="action-sharepoint-005" operation_id="GetFileMetadataByPath" category="read" complexity="low" throttle_impact="low">
### Get File Metadata Using Path

**Description**: Retrieves file metadata via path reference

**Operation ID**: `GetFileMetadataByPath`

**Parameters**:
- **Site Address** (string, required)
- **File Path** (string, required)

**Returns**: `SPBlobMetadataResponse`

**When to Use**: When you have path but not identifier

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-006" operation_id="GetFileItem" category="read" complexity="low" throttle_impact="low">
### Get File Properties

**Description**: Gets the properties saved in the columns in the library

**Operation ID**: `GetFileItem`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required): Item identifier
- **Limit Columns by View** (string, optional): Column threshold avoidance

**Returns**: Dynamic (column-dependent schema)

**Note**: When using with On-Premises Data Gateway, library name may need manual entry

**Best Practices**:
- Use "Limit Columns by View" for large libraries
- Test with production data to understand dynamic schema

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-007" operation_id="UpdateFile" category="update" complexity="low" throttle_impact="high">
### Update File

**Description**: Modifies file contents (replaces document data)

**Operation ID**: `UpdateFile`

**Parameters**:
- **Site Address** (string, required)
- **File Identifier** (string, required)
- **File Content** (binary, required): New document data

**Returns**: `BlobMetadataResponse`

**Best Practices**:
- Get file metadata first to capture ETag
- Use "Update File Properties" for metadata-only changes
- Consider version control implications

**Example Use Case**: Replace outdated document with new version

**Throttle Impact**: High (bandwidth consumption)
</action>

---

<action id="action-sharepoint-008" operation_id="PatchFileItem" category="update" complexity="low" throttle_impact="low">
### Update File Properties

**Description**: Modifies library column values for file (metadata only)

**Operation ID**: `PatchFileItem`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required): File item reference
- **Item** (dynamic, required): Properties to change
- **Limit Columns by View** (string, optional)

**Returns**: Dynamic

**Note**: Use "Update File" action for document content changes

**Best Practices**:
- Only update changed properties (avoid full payload)
- Validate column types match expected values

**Throttle Impact**: Low (metadata only)
</action>

---

<action id="action-sharepoint-009" operation_id="PatchFileItemWithPredictedValues" category="update" complexity="high" throttle_impact="low">
### Update File Properties Using AI Builder

**Description**: Sets library columns based on ML model analysis

**Operation ID**: `PatchFileItemWithPredictedValues`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required)
- **ModelId** (string, optional): ML model reference
- **PredictResult** (string, optional): JSON analysis data

**Returns**: Dynamic

**Prerequisites**: Requires AI Builder license and trained model

**Example Use Case**: Auto-classify invoices and set metadata fields

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-010" operation_id="CopyFileAsync" category="utility" complexity="medium" throttle_impact="medium">
### Copy File

**Description**: Duplicates file to new location (current async version)

**Operation ID**: `CopyFileAsync`

**Parameters**:
- **Current Site Address** (string, required)
- **File to Copy** (string, required): File identifier
- **Destination Site Address** (string, required)
- **Destination Folder** (string, required): Target path
- **If another file is already there** (integer, optional): Conflict resolution
  - `0` = Fail
  - `1` = Overwrite
  - `2` = Keep both

**Returns**: `SPBlobMetadataResponse`

**Note**: Works similarly to 'Copy to' command in SharePoint libraries

**Best Practices**:
- Use async version (CopyFileAsync) instead of deprecated CopyFile
- Set conflict resolution strategy explicitly

**Throttle Impact**: Medium
</action>

---

<action id="action-sharepoint-011" operation_id="MoveFileAsync" category="utility" complexity="medium" throttle_impact="medium">
### Move File

**Description**: Relocates file to new location

**Operation ID**: `MoveFileAsync`

**Parameters**:
- **Current Site Address** (string, required)
- **File to Move** (string, required): File identifier
- **Destination Site Address** (string, required)
- **Destination Folder** (string, required): Target path
- **If another file is already there** (integer, optional): Conflict approach

**Returns**: `SPBlobMetadataResponse`

**Best Practices**:
- Verify destination folder exists before moving
- Handle conflicts explicitly

**Throttle Impact**: Medium
</action>

---

<action id="action-sharepoint-012" operation_id="DeleteFile" category="delete" complexity="low" throttle_impact="low">
### Delete File

**Description**: Removes file by identifier (permanent deletion)

**Operation ID**: `DeleteFile`

**Parameters**:
- **Site Address** (string, required)
- **File Identifier** (string, required): Unique reference

**Returns**: None

**Warning**: Permanent deletion - implement confirmation before use

**Best Practices**:
- Consider moving to archive folder instead
- Implement approval workflow for critical deletions

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-013" operation_id="CheckOutFile" category="utility" complexity="low" throttle_impact="low">
### Check Out File

**Description**: Reserves document to prevent concurrent modifications

**Operation ID**: `CheckOutFile`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required): File reference

**Returns**: None

**Effect**: Others cannot see changes until check-in occurs

**Best Practices**:
- Always pair with Check In action
- Implement timeout for abandoned checkouts

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-014" operation_id="CheckInFile" category="utility" complexity="low" throttle_impact="low">
### Check In File

**Description**: Releases checked-out document for collective access

**Operation ID**: `CheckInFile`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required): File reference
- **Comments** (string, required): Version description
- **Check in type** (integer, required): Version classification
  - `0` = Minor version
  - `1` = Major version
  - `2` = Overwrite

**Returns**: None

**Use Case**: Making document edits visible to others

**Best Practices**:
- Provide meaningful comments for version history
- Use major versions for significant changes

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-015" operation_id="DiscardFileCheckOut" category="utility" complexity="low" throttle_impact="low">
### Discard Check Out

**Description**: Cancels file reservation without saving (avoids version proliferation)

**Operation ID**: `DiscardFileCheckOut`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required): File reference

**Returns**: None

**Benefit**: Avoid making new versions when you haven't made changes

**Example Use Case**: Cancel edit when no changes needed

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-016" operation_id="CreateAttachment" category="create" complexity="low" throttle_impact="medium">
### Add Attachment

**Description**: Appends new attachment to specified list item

**Operation ID**: `CreateAttachment`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (integer, required): Item reference
- **File Name** (string, required): Attachment label
- **File Content** (binary, required): Document data

**Returns**: `SPListItemAttachment` object

**Limitations**:
<limitation id="lim-sp-file-002" severity="high">
List item attachments are supported up to 90MB in size
</limitation>

**Throttle Impact**: Medium
</action>

---

<action id="action-sharepoint-017" operation_id="GetItemAttachments" category="read" complexity="low" throttle_impact="low">
### Get Attachments

**Description**: Returns the list of attachments for specified list item

**Operation ID**: `GetItemAttachments`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (string, required): Item reference

**Returns**: Array of `SPListItemAttachment` objects
```json
[
  {
    "Id": "string",
    "Name": "string",
    "Size": "number"
  }
]
```

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-018" operation_id="GetAttachmentContent" category="read" complexity="low" throttle_impact="high">
### Get Attachment Content

**Description**: Downloads specific attachment data from list item

**Operation ID**: `GetAttachmentContent`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (integer, required): Item reference
- **File Identifier** (string, required): Attachment reference

**Returns**: Binary content

**Best Practices**:
- Use Get Attachments first to retrieve file identifier
- Monitor bandwidth limits

**Throttle Impact**: High (bandwidth consumption)
</action>

---

<action id="action-sharepoint-019" operation_id="DeleteAttachment" category="delete" complexity="low" throttle_impact="low">
### Delete Attachment

**Description**: Removes item attachment (permanent deletion)

**Operation ID**: `DeleteAttachment`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (integer, required): Item reference
- **File Identifier** (string, required): Attachment reference

**Returns**: None

**Throttle Impact**: Low
</action>

---

## Folder Operations (8 Actions)

<action id="action-sharepoint-020" operation_id="CreateNewFolder" category="create" complexity="low" throttle_impact="low">
### Create New Folder

**Description**: Establishes new folder or multi-level path

**Operation ID**: `CreateNewFolder`

**Parameters**:
- **Site Address** (string, required)
- **List or Library** (string, required): Container
- **Folder Path** (string, required): Example: "folder1/folder2/folder3"
- **Limit Columns by View** (string, optional)

**Returns**: Dynamic

**Use Case**: Organizing documents hierarchically

**Best Practices**:
- Can create nested folders in single call
- Folder path is relative to library root

**Example**: Create "Projects/2025/Q1" in one action

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-021" operation_id="CopyFolderAsync" category="utility" complexity="medium" throttle_impact="high">
### Copy Folder

**Description**: Duplicates folder structure to new location (recursive)

**Operation ID**: `CopyFolderAsync`

**Parameters**:
- **Current Site Address** (string, required)
- **Folder to Copy** (string, required): Folder identifier
- **Destination Site Address** (string, required)
- **Destination Folder** (string, required): Target path
- **If another folder is already there** (integer, optional): Conflict handling

**Returns**: `SPBlobMetadataResponse`

**Best Practices**:
- Large folder copies consume significant API calls
- Consider async nature for large operations

**Throttle Impact**: High (recursive operation on all contents)
</action>

---

<action id="action-sharepoint-022" operation_id="MoveFolderAsync" category="utility" complexity="medium" throttle_impact="high">
### Move Folder

**Description**: Relocates folder to new location (recursive)

**Operation ID**: `MoveFolderAsync`

**Parameters**:
- **Current Site Address** (string, required)
- **Folder to Move** (string, required): Folder identifier
- **Destination Site Address** (string, required)
- **Destination Folder** (string, required): Target path
- **If another folder is already there** (integer, optional): Conflict approach

**Returns**: `SPBlobMetadataResponse`

**Throttle Impact**: High (recursive operation)
</action>

---

<action id="action-sharepoint-023" operation_id="GetFolderMetadata" category="read" complexity="low" throttle_impact="low">
### Get Folder Metadata

**Description**: Retrieves folder information by identifier

**Operation ID**: `GetFolderMetadata`

**Parameters**:
- **Site Address** (string, required)
- **File Identifier** (string, required): Folder reference

**Returns**: `SPBlobMetadataResponse`

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-024" operation_id="GetFolderMetadataByPath" category="read" complexity="low" throttle_impact="low">
### Get Folder Metadata Using Path

**Description**: Retrieves folder details via path reference

**Operation ID**: `GetFolderMetadataByPath`

**Parameters**:
- **Site Address** (string, required)
- **Folder Path** (string, required)

**Returns**: `SPBlobMetadataResponse`

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-025" operation_id="ListFolder" category="read" complexity="low" throttle_impact="low">
### List Folder

**Description**: Returns files contained in a SharePoint folder

**Operation ID**: `ListFolder`

**Parameters**:
- **Site Address** (string, required)
- **File Identifier** (string, required): Folder reference

**Returns**: Array of `BlobMetadata` objects

**Best Practices**:
- Use for folder-level file enumeration
- Combine with filters to reduce results

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-026" operation_id="ListRootFolder" category="read" complexity="low" throttle_impact="low">
### List Root Folder

**Description**: Returns files in the root SharePoint folder

**Operation ID**: `ListRootFolder`

**Parameters**:
- **Site Address** (string, required)

**Returns**: Array of `BlobMetadata` objects

**When to Use**: Quick access to library root contents

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-027" operation_id="ExtractFolderV2" category="utility" complexity="medium" throttle_impact="medium">
### Extract Folder

**Description**: Extracts archive file (e.g., .zip) into SharePoint folder

**Operation ID**: `ExtractFolderV2`

**Parameters**:
- **Site Address** (string, required)
- **Source File Path** (string, required): Archive location
- **Destination Folder Path** (string, required): Extraction target
- **Overwrite Flag** (boolean, optional): Collision handling

**Returns**: Array of `BlobMetadata` objects (extracted files)

**Limitations**:
<limitation id="lim-sp-folder-001" severity="medium">
Extract Folder action may cause character distortion during extraction when special characters are involved
</limitation>

**Workaround**: Use modern zip archive tool or library that adheres to standard zip specification (UTF-8, language encoding headers)

**Throttle Impact**: Medium
</action>

---

## List/Item Operations (6 Actions)

<action id="action-sharepoint-028" operation_id="PostItem" category="create" complexity="low" throttle_impact="low">
### Create Item

**Description**: Creates a new item in a SharePoint list

**Operation ID**: `PostItem`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Item** (dynamic, required): Data values
- **Limit Columns by View** (string, optional): Threshold avoidance

**Returns**: Dynamic (list schema-dependent)

**Use Case**: Adding records to lists

**Best Practices**:
- Validate required columns before submission
- Use "Limit Columns by View" for large lists (>5000 items)

**Example**: Create new employee record in "Employees" list

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-029" operation_id="GetItem" category="read" complexity="low" throttle_impact="low">
### Get Item

**Description**: Gets a single item by its id from a SharePoint list

**Operation ID**: `GetItem`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (integer, required): Record reference
- **Limit Columns by View** (string, optional)

**Returns**: Dynamic (all item properties)

**Best Practices**:
- Use for single record retrieval
- Cache list schema to parse dynamic results

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-030" operation_id="GetItems" category="read" complexity="medium" throttle_impact="medium">
### Get Items

**Description**: Gets items from a SharePoint list with filtering/sorting

**Operation ID**: `GetItems`

**Parameters** (all optional):
- **Site Address** (string, required)
- **List Name** (string, required)
- **Filter Query** (string): ODATA filtering
  - Example: `"stringColumn eq 'value' OR numberColumn lt 123"`
- **Order By** (string): ODATA sorting
  - Example: `"Created desc"`
- **Top Count** (integer): Result limit (max 5000)
- **Limit Entries to Folder** (string): Path restriction
- **Include Nested Items** (string): Subfolder inclusion (default: true)
- **Limit Columns by View** (string)

**Returns**: Dynamic array

**Best Practices**:
1. **Server-Side Filtering**: Use Filter Query for ODATA filtering
   - Delegable: `And`, `Or`, `eq`, `ne`, `lt`, `gt`
   - NOT delegable: `Not`, complex expressions
2. **ID Field**: Only supports equal ('=') operation for delegation
3. **Nested Items**: Set to false if folder-scoped only

**Example Filter Queries**:
```
Status eq 'Active' AND Priority lt 3
Title eq 'Invoice' OR Category eq 'Finance'
Created gt '2025-01-01T00:00:00Z'
```

**Limitations**:
<limitation id="lim-sp-list-001" severity="high">
Delegation limits apply to lists with >5000 items. Use indexed columns and ODATA filters.
</limitation>

**Throttle Impact**: Medium (increases with result count)
</action>

---

<action id="action-sharepoint-031" operation_id="PatchItem" category="update" complexity="low" throttle_impact="low">
### Update Item

**Description**: Updates an item in a SharePoint list

**Operation ID**: `PatchItem`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (integer, required): Record reference
- **Item** (dynamic, required): Modified values
- **Limit Columns by View** (string, optional)

**Returns**: Dynamic

**Best Practices**:
- Only include changed fields in Item payload
- Verify item exists before update (or handle 404)

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-032" operation_id="DeleteItem" category="delete" complexity="low" throttle_impact="low">
### Delete Item

**Description**: Deletes an item from a SharePoint list (permanent)

**Operation ID**: `DeleteItem`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)
- **Id** (integer, required): Record reference

**Returns**: None

**Warning**: Permanent deletion - implement confirmation workflows

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-033" operation_id="GetItemChanges" category="read" complexity="high" throttle_impact="low">
### Get Changes for Item or File

**Description**: Returns information about columns that changed within given time window

**Operation ID**: `GetItemChanges`

**Parameters**:
- **Site Address** (string, required)
- **List or Library Name** (string, required)
- **Id** (integer, required): Record/file reference
- **Since** (string, required): Start point (version label, ISO 8601 date, or token)
- **Until** (string, optional): End point (defaults to latest)
- **Include Minor Versions** (boolean, optional): Draft inclusion
- **Limit Columns by View** (string, optional)

**Returns**: Dynamic (changed columns with values)

**Prerequisites**:
<limitation id="lim-sp-list-002" severity="critical">
The list must have Versioning turned on
</limitation>

**Use Case**: Audit trail, change notifications

**Example Since Values**:
- Version label: `"1.0"`, `"2.3"`
- ISO 8601 date: `"2025-01-15T10:30:00Z"`
- Token: From previous call

**Throttle Impact**: Low
</action>

---

## Library Operations (5 Actions)

<action id="action-sharepoint-034" operation_id="GetTables" category="read" complexity="low" throttle_impact="low">
### Get Lists

**Description**: Gets SharePoint lists from a site

**Operation ID**: `GetTables`

**Parameters**:
- **Site Address** (string, required)

**Returns**: `TablesList` object
```json
{
  "value": [
    {"Name": "Documents", "DisplayName": "Documents", "Id": "guid"}
  ]
}
```

**Best Practices**:
- Cache results to avoid repeated calls
- Use for dynamic list discovery

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-035" operation_id="GetAllTables" category="read" complexity="low" throttle_impact="low">
### Get All Lists and Libraries

**Description**: Get all lists and libraries from site

**Operation ID**: `GetAllTables`

**Parameters**:
- **Site Address** (string, required)

**Returns**: `TablesList` object (includes document libraries)

**When to Use**: Complete site inventory

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-036" operation_id="GetTableViews" category="read" complexity="low" throttle_impact="low">
### Get List Views

**Description**: Gets views from a SharePoint list

**Operation ID**: `GetTableViews`

**Parameters**:
- **Site Address** (string, required)
- **List Name** (string, required)

**Returns**: Array of `Table` objects
```json
[
  {"Name": "All Items", "DisplayName": "All Items"}
]
```

**Use Case**: Dynamic view selection, column filtering

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-037" operation_id="GetFileItems" category="read" complexity="medium" throttle_impact="medium">
### Get Files (Properties Only)

**Description**: Gets properties saved in columns in library for all folders and files

**Operation ID**: `GetFileItems`

**Parameters** (all optional):
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Filter Query** (string): ODATA filtering
- **Order By** (string): ODATA sorting
- **Top Count** (integer): Result limit
- **Limit Entries to Folder** (string)
- **Include Nested Items** (string): Subfolder inclusion
- **Limit Columns by View** (string)

**Returns**: Dynamic array

**Note**: "An 'Apply to each' section is usually used to work with the output"

**Best Practices**:
- Use for bulk file metadata retrieval
- Apply ODATA filters to reduce payload

**Throttle Impact**: Medium
</action>

---

<action id="action-sharepoint-038" operation_id="CreateNewDocumentSet" category="create" complexity="high" throttle_impact="low">
### Create New Document Set

**Description**: Creates a new document set list item

**Operation ID**: `CreateNewDocumentSet`

**Parameters**:
- **Site Address** (string, required)
- **Library** (string, required): Container
- **Document Set Path** (string, required): Example: "folder1/folder2/dsName"
- **Content Type Id** (string, required): Example: "0x0120D520"
- **DynamicProperties** (object)

**Returns**: Dynamic

**Prerequisites**: Library must support document sets content type

**Example Use Case**: Create project document set with predefined structure

**Throttle Impact**: Low
</action>

---

## Sharing & Permissions (3 Actions)

<action id="action-sharepoint-039" operation_id="CreateSharingLink" category="utility" complexity="medium" throttle_impact="low">
### Create Sharing Link

**Description**: Create sharing link for a file or folder

**Operation ID**: `CreateSharingLink`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Item Id** (integer, required): File/folder reference
- **Link Type** (string, required): Sharing link classification
  - `View` - Read-only access
  - `Edit` - Modify permissions
- **Link Scope** (string, required): Access boundary
  - `Anyone` - Public link (requires admin enablement)
  - `Organization` - Internal users only
  - `Specific People` - Named recipients
- **Link Expiration** (datetime, optional): Format: yyyy-MM-dd

**Returns**: `SharingLinkPermission` object
```json
{
  "Link": "https://...",
  "Scope": "Organization"
}
```

**Best Practices**:
- Verify "Anyone" links are enabled by admin before use
- Set expiration dates for temporary access
- Use "Specific People" for sensitive content

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-040" operation_id="GrantAccess" category="utility" complexity="medium" throttle_impact="low">
### Grant Access to an Item or Folder

**Description**: Grant access to specific people with defined roles

**Operation ID**: `GrantAccess`

**Parameters**:
- **Site Address** (string, required)
- **List or Library Name** (string, required)
- **Id** (integer, required): Item/folder reference
- **Recipients** (email, required): Recipient collection (comma-separated)
- **Roles** (string, required): Permission level
  - `View` - Read-only
  - `Edit` - Modify permissions
- **Message** (string, optional): Invitation text
- **Notify Recipients** (boolean, optional): Email notification control

**Returns**: None

**Best Practices**:
- Use Notify Recipients to control email volume
- Validate email addresses before granting

**Example Use Case**: Grant contractor access to specific project folder

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-041" operation_id="UnshareItem" category="utility" complexity="medium" throttle_impact="low">
### Stop Sharing an Item or File

**Description**: Delete all links giving access and remove all people with direct access except owners

**Operation ID**: `UnshareItem`

**Parameters**:
- **Site Address** (string, required)
- **List or Library Name** (string, required)
- **Id** (integer, required): Item/file reference

**Returns**: None

**Warning**: Revokes ALL access immediately except for owners

**Use Case**: Expire access after project completion

**Throttle Impact**: Low
</action>

---

## Approval Operations (3 Actions)

<action id="action-sharepoint-042" operation_id="CreateApprovalRequest" category="utility" complexity="high" throttle_impact="low">
### Create Approval Request

**Description**: Creates an approval request for an item or file

**Operation ID**: `CreateApprovalRequest`

**Parameters**:
- **Site Address** (string, required)
- **List or Library** (string, required)
- **Id** (integer, required): Item reference
- **Approval Type** (integer, required): Request classification
  - `0` = Approve/Reject - First to respond
  - `1` = Approve/Reject - Everyone must approve
  - `2` = Custom responses
- **Approval Schema** (dynamic, required): Type-specific parameters
  - Title, Assigned To, Details, Item Link

**Returns**: `ApprovalData` object
```json
{
  "ApprovalId": "string",
  "Outcome": "Approve/Reject",
  "Responses": []
}
```

**Best Practices**:
- Consult approval schema documentation for each type
- Implement timeout handling for approvals

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-043" operation_id="SetApprovalStatus" category="utility" complexity="medium" throttle_impact="low">
### Set Content Approval Status

**Description**: Sets content approval status for item in list/library with content approval enabled

**Operation ID**: `SetApprovalStatus`

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Id** (integer, required): Item reference
- **Action** (string, required): Approval decision
  - `Approve`
  - `Reject`
  - `Pending`
- **Comments** (string, optional): Approver notes
- **ETag** (string, optional): Required for pages/files (from Get File Metadata)

**Returns**: `SetApprovalStatusOutput`

**Availability**: SharePoint Online and 2019 only

**Prerequisites**:
<limitation id="lim-sp-approval-001" severity="high">
Library must have content approval enabled. ETag mandatory for pages and files.
</limitation>

**Best Practices**:
- Get File Metadata first to capture ETag
- Provide meaningful comments for audit trail

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-044" operation_id="CheckIfFileIsPublished" category="utility" complexity="medium" throttle_impact="low" status="deprecated">
### Check If Scheduled Version Published (DEPRECATED)

**Description**: Returns result in output variable IsFilePublished

**Operation ID**: `CheckIfFileIsPublished`

**Status**: DEPRECATED - No longer actively maintained

**Parameters**:
- **Site Address** (string, required)
- **Library Name** (string, required)
- **Item ID** (integer, required)
- **Scheduled Version** (string, required)

**Returns**: `PublishedResult`

**Replacement**: Use "Set Content Approval Status" and monitor via approval status

**Throttle Impact**: Low
</action>

---

## Hub Site Operations (4 Actions)

<action id="action-sharepoint-045" operation_id="JoinHubSite" category="utility" complexity="high" throttle_impact="low">
### Join Hub Site

**Description**: Join the requested site to the hub site

**Operation ID**: `JoinHubSite`

**Parameters**:
- **Requesting Site Address** (string, required)
- **Hub Site Id** (string, required): Target hub reference
- **Approval Token** (string, optional): Required if approval needed
- **Approval Correlation Id** (string, optional): Request tracking

**Returns**: None

**Prerequisites**: May require approval token from hub admin

**Best Practices**:
- Check if approval required before joining
- Use correlation ID for tracking multi-step approval

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-046" operation_id="ApproveHubSiteJoin" category="utility" complexity="medium" throttle_impact="low">
### Approve Hub Site Join Request

**Description**: Authorizes hub affiliation request

**Operation ID**: `ApproveHubSiteJoin`

**Parameters**:
- **Hub Site Address** (string, required)
- **Requesting Site Id** (string, required): Applicant site reference

**Returns**: `ApproveHubSiteJoinResponse`
```json
{
  "ApprovalToken": "string"
}
```

**Use Case**: Hub governance workflows

**Best Practices**:
- Provide approval token to requesting site
- Implement approval workflow with notifications

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-047" operation_id="NotifyHubSiteJoinApprovalStarted" category="utility" complexity="medium" throttle_impact="low">
### Set Hub Site Join Status to Pending

**Description**: Set requested site's hub join request status to pending

**Operation ID**: `NotifyHubSiteJoinApprovalStarted`

**Parameters**:
- **Requesting Site Address** (string, required)
- **Approval Correlation Id** (string, optional): Request identifier

**Returns**: None

**Note**: Requesting site can only have one pending request at a time

**Use Case**: Multi-stage approval initialization

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-048" operation_id="CancelHubSiteJoinApproval" category="utility" complexity="medium" throttle_impact="low">
### Cancel Hub Site Join Request

**Description**: Cancel hub join request

**Operation ID**: `CancelHubSiteJoinApproval`

**Parameters** (optional):
- **Requesting Site Address** (string)
- **Approval Correlation Id** (string): Request tracking identifier

**Returns**: None

**Use Case**: Withdraw pending hub join requests

**Throttle Impact**: Low
</action>

---

## Document Generation (2 Actions)

<action id="action-sharepoint-049" operation_id="CreateContentAssemblyDocument" category="utility" complexity="high" throttle_impact="medium">
### Generate Document Using Microsoft Syntex

**Description**: Create documents based on modern templates from Microsoft Syntex

**Operation ID**: `CreateContentAssemblyDocument`

**Parameters**:
- **Site Address** (string, required)
- **Document Library Name** (string, required)
- **Document Template** (string, required): Template reference
- **Placeholders** (dynamic, required): Template variables
- **Folder Path** (string, optional): Destination
- **File Name** (string, optional): Document label

**Returns**: `SPBlobMetadataResponse`

**Prerequisites**:
<limitation id="lim-sp-syntex-001" severity="critical">
This preview requires a Syntex license. Pricing is subject to change.
</limitation>

**Use Case**: Auto-generate contracts, reports from templates

**Example Placeholders**:
```json
{
  "CustomerName": "Acme Corp",
  "ContractDate": "2025-01-15",
  "Amount": "$10,000"
}
```

**Throttle Impact**: Medium
</action>

---

<action id="action-sharepoint-050" operation_id="CreateAgreementsSolutionDocument" category="utility" complexity="high" throttle_impact="medium">
### Agreements Solution - Generate Document

**Description**: Create documents based on modern templates in Agreements Solution workspace

**Operation ID**: `CreateAgreementsSolutionDocument`

**Parameters**:
- **Agreements Solution Workspace** (string, required): Site reference
- **Agreements Solution Template** (string, required): Template reference
- **Fields** (dynamic, required): Placeholder values
- **File Name** (string, optional): Document label

**Returns**: `SPBlobMetadataResponse`

**Status**: "This is behind a payment wall currently in planning"

**Prerequisites**: Requires Agreements Solution license

**Throttle Impact**: Medium
</action>

---

## Utility Actions (2 Actions)

<action id="action-sharepoint-051" operation_id="SearchForUser" category="utility" complexity="medium" throttle_impact="low">
### Resolve Person

**Description**: Returns single matching user value for assignment to person column

**Operation ID**: `SearchForUser`

**Parameters**:
- **Site Address** (string, required)
- **List or Library** (string, required): Column container
- **Column** (string, required): Target field reference
- **Email or name** (string, required): Search criteria

**Returns**: `SPListExpandedUser`
```json
{
  "Claims": "string",
  "DisplayName": "string",
  "Email": "string",
  "Department": "string",
  "JobTitle": "string"
}
```

**Behavior**: Errors if no matches or multiple matches found

**Limitations**:
<limitation id="lim-sp-user-001" severity="medium">
Guest user accounts can't view or retrieve drop-down list information
</limitation>

**Best Practices**:
- Use email for exact matching
- Implement error handling for no/multiple matches

**Throttle Impact**: Low
</action>

---

<action id="action-sharepoint-052" operation_id="HttpRequest" category="utility" complexity="high" throttle_impact="varies">
### Send an HTTP Request to SharePoint

**Description**: Construct a SharePoint REST API to invoke any operation

**Operation ID**: `HttpRequest`

**Parameters**:
- **Site Address** (string, required)
- **Method** (string, required): HTTP verb
  - `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Uri** (string, required): REST API endpoint
  - Example: `"_api/web/lists/getbytitle('Documents')"`
- **Headers** (object, optional): Request headers as JSON
  - Example: `{"Accept": "application/json", "Content-Type": "application/json"}`
- **Body** (string, optional): Request payload (JSON format)

**Returns**: Dynamic (API-dependent)

**Warning**: "This action may execute any SharePoint REST API you have access to. Please proceed with caution"

**Use Cases**:
- Custom operations not covered by standard actions
- Advanced batch operations
- Site administration tasks

**Example URI Patterns**:
```
_api/web/lists/getbytitle('Documents')/items
_api/web/siteusers
_api/search/query?querytext='keyword'
_api/web/lists/getbytitle('Tasks')/items($batch)
```

**Best Practices**:
- Reference SharePoint REST API documentation
- Test with GET before using POST/PATCH/DELETE
- Handle errors gracefully (400, 403, 404, 429)

**Throttle Impact**: Varies by operation (can be very high for batch)
</action>

---

## Common Error Codes

<error id="err-sp-001" http_code="400" severity="high">
**Error**: Bad Request - List or library name contains period

**Cause**: Periods in list/library names cause parsing errors when used as dynamic values

**Solution**:
- Select list from dropdown menu instead of dynamic value
- Use list's GUID instead of name
- Reference: /home/therouxe/debug_powerAutomate/Docs/PowerAutomateDocs/SharePoint/overview.md:lim-007
</error>

<error id="err-sp-002" http_code="401" severity="critical">
**Error**: Unauthorized - Authentication failure

**Causes**:
- Invalid credentials or expired token
- Conditional Access policies blocking access (MFA, device compliance)

**Solutions**:
- Verify connection credentials
- Review Microsoft Entra ID Conditional Access documentation
- Check service principal permissions (if applicable)
</error>

<error id="err-sp-003" http_code="403" severity="high">
**Error**: Forbidden - Insufficient permissions

**Causes**:
- Missing required SharePoint permissions
- Site collection admin required (deletion triggers)
- Guest user accessing restricted data

**Solutions**:
- Verify user has required permission level
- Use site collection admin account for deletions
- Check guest user limitations
</error>

<error id="err-sp-004" http_code="404" severity="medium">
**Error**: Not Found - Resource doesn't exist

**Causes**:
- File/item/list deleted or moved
- Incorrect identifier or path
- Typo in library/list name

**Solutions**:
- Verify resource existence before operation
- Use identifiers instead of paths (more reliable)
- Implement error handling for "not found" scenarios
</error>

<error id="err-sp-429" http_code="429" severity="critical">
**Error**: Too Many Requests - Throttling limit exceeded

**Cause**: Exceeded 600 API calls per 60 seconds per connection

**Solutions**:
1. Add delays between operations (Delay action)
2. Implement batch operations where possible
3. Use server-side filtering to reduce calls
4. Distribute load across multiple connections
5. Reference: /home/therouxe/debug_powerAutomate/Docs/PowerAutomateDocs/SharePoint/overview.md:lim-002

**Throttle Formula**:
```
Max concurrent flows = 600 calls / (calls per flow * flows per minute)
```
</error>

<error id="err-sp-005" http_code="500" severity="high">
**Error**: Internal Server Error - SharePoint service issue

**Causes**:
- Transient SharePoint service errors
- Complex formula timeouts
- Large file processing failures

**Solutions**:
- Implement retry logic with exponential backoff
- Break large operations into smaller chunks
- Check Microsoft 365 Service Health Dashboard
</error>

<error id="err-sp-006" severity="high">
**Error**: CannotDisableTriggerConcurrency

**Cause**: Concurrency control cannot be disabled after enabling

**Solution**:
- Export flow JSON
- Edit to remove 'concurrency control' section
- Re-import flow
</error>

<error id="err-sp-007" severity="medium">
**Error**: Character distortion in Extract Folder

**Cause**: Special characters in zip file with non-standard encoding

**Solution**:
- Use modern zip tools supporting UTF-8
- Ensure language encoding headers in archive
- Reference: /home/therouxe/debug_powerAutomate/Docs/PowerAutomateDocs/SharePoint/actions.md:action-sharepoint-027
</error>

<error id="err-sp-008" severity="medium">
**Error**: Term set label changes not reflected

**Cause**: Term set labels cached in flow/app

**Solution**:
- Directly edit affected list item from SharePoint list to force refresh
- Re-save flow after term set updates
</error>

---

## Best Practices Summary

### File Operations
1. **Content Type Inference**: Enable "Infer Content Type" when retrieving binary content
2. **ETag Usage**: Always capture ETag from Get File Metadata before updates (prevents conflicts)
3. **Check-In/Check-Out**: Pair checkout → edit → check-in; use Discard for unwanted changes
4. **Large Files**: Monitor 90MB attachment limit; consider chunking for large uploads
5. **Identifiers vs. Paths**: Use file identifiers when available (faster, more reliable)

### List/Item Operations
1. **Server-Side Filtering**: Use ODATA Filter Query instead of client-side processing
   - Delegable: `And`, `Or`, `eq`, `ne`, `lt`, `gt`, `le`, `ge`
   - NOT delegable: `Not`, `in`, `startsWith`, complex expressions
2. **Column Threshold**: Use "Limit Columns by View" for lists >5000 items
3. **Nested Items**: Explicitly set "Include Nested Items" parameter
4. **Indexed Columns**: Use indexed columns in Filter Query for large lists
5. **Batch Operations**: Group multiple operations to reduce API calls

### Library Operations
1. **Dynamic Schema**: Test with production data to understand return schema
2. **View Filtering**: Pre-define views for column subset optimization
3. **Document Sets**: Must specify Content Type ID (format: "0x0120D520")

### Sharing & Permissions
1. **Link Expiration**: Format dates as yyyy-MM-dd for anonymous links
2. **"Anyone" Links**: Verify admin enablement before creating public shares
3. **Notification Control**: Use "Notify Recipients" flag to manage email volume
4. **Access Audit**: Implement logging for Grant/Revoke access operations

### API Throttling Management
1. **Rate Monitoring**: Track API calls per flow (600/60s limit)
2. **Delay Actions**: Add delays in loops (minimum 1-2 seconds)
3. **Concurrent Flows**: Calculate max concurrent: `600 / (calls_per_flow * flows_per_minute)`
4. **Error Handling**: Implement retry logic with exponential backoff for 429 errors
5. **Batch Operations**: Use Get Items with filters instead of multiple Get Item calls

### Performance Optimization
1. **Minimize Columns**: Return only needed columns via "Limit Columns by View"
2. **Server-Side Processing**: Apply filters/sorting at source
3. **Caching**: Store metadata (library IDs, list IDs) to avoid repeated lookups
4. **Async Operations**: Use CopyFileAsync/MoveFileAsync over synchronous variants
5. **Folder Scoping**: Scope triggers to specific folders to reduce notifications

### Error Handling Patterns
1. **Scope + Configure Run After**: Wrap operations in Scope for error isolation
2. **Retry Logic**: Implement exponential backoff for transient errors (429, 500)
3. **Validation**: Check resource existence before operations (avoid 404)
4. **Graceful Degradation**: Provide fallback actions for common failures
5. **Logging**: Record critical operations for debugging

### Data Gateway (On-Premises)
1. **Manual Entry**: Enter library name manually when dropdown fails
2. **Trigger Limitations**: Only default environment flows listed for selected item/file triggers
3. **Connection Testing**: Verify gateway connectivity before production use

---

## Deprecated Actions

<deprecated_actions>
| Action | Operation ID | Status | Replacement |
|--------|-------------|--------|-------------|
| Copy file (deprecated) | CopyFile | Deprecated | CopyFileAsync |
| Check if scheduled version published | CheckIfFileIsPublished | Deprecated | Set Content Approval Status |
</deprecated_actions>

**Deprecation Note**: Actions marked as 'deprecated' are no longer actively maintained. While still present in connector, strongly recommended to NOT use in new applications or solutions.

---

## Official Documentation

<official_docs>
https://learn.microsoft.com/en-us/connectors/sharepointonline/
</official_docs>

**Related Documentation**:
- SharePoint REST API: https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service
- ODATA Query Reference: https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/use-odata-query-operations-in-sharepoint-rest-requests
- Conditional Access: https://learn.microsoft.com/en-us/entra/identity/conditional-access/

---

**Last Updated**: 2025-10-31
**Fetch Date**: 2025-10-31
**Version**: 1.0
