# Excel Online (Business) - Actions

---
type: connector-actions
connector_name: Excel Online (Business)
action_count: 13
version: 1.0
last_updated: 2025-10-31
fetch_date: 2025-10-31
keywords: [excel, row, table, worksheet, office scripts, add row, update row, list rows, excel online, actions]
categories: [create, read, update, delete, utility]
---

<action_summary>
**Total Actions**: 13 (11 current + 2 deprecated)

**By Category**:
- Create Operations: 4 actions (Add row, Create table, Create worksheet, Add key column)
- Read Operations: 4 actions (Get row, List rows, Get tables, Get worksheets)
- Update Operations: 1 action (Update row)
- Delete Operations: 1 action (Delete row)
- Utility Operations: 2 actions (Run script, Run script from SharePoint)
- Deprecated: 1 action (Add row V1)

**Complexity Distribution**:
- Low complexity: 8 actions
- Medium complexity: 4 actions
- High complexity: 1 action (Office Scripts)
</action_summary>

<action_categories>
## Categories Overview

### Create Operations
Excel Online provides actions to add data and structure to workbooks: adding rows to tables, creating new tables and worksheets, and adding key columns for data identification.

### Read Operations
Read actions retrieve data and metadata from Excel workbooks including individual rows, row lists with filtering/sorting, table lists, and worksheet information.

### Update Operations
Update actions modify existing data in tables using key column identification to locate and patch specific rows with new values.

### Delete Operations
Delete actions remove rows from tables using key column matching to identify target rows for deletion.

### Utility Operations
Office Scripts integration allows running TypeScript-based automation scripts against Excel workbooks with custom logic and complex operations.
</action_categories>

---

## Create Operations

### Add a Row into a Table

<action id="action-001" category="create" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: AddRowV2
</action_header>

<description>
Adds a new row to an Excel table with dynamic column mapping. Automatically detects table schema and provides dynamic fields for each column. Use this action to append data to existing tables from form submissions, database records, or other data sources.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file
- **Values**: OneDrive for Business, SharePoint Site, Teams
- **Example**: "OneDrive for Business"

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file
- **Format**: Dynamic dropdown populated based on location
- **Example**: "Documents"

**File** (`file`, `string`)
- **Description**: Path to Excel workbook
- **Format**: Dynamic file picker showing .xlsx and .xlsb files
- **Example**: "/Shared Documents/Sales Data.xlsx"

**Table** (`table`, `string`)
- **Description**: Name or ID of table to add row to
- **Format**: Dynamic dropdown of tables in workbook
- **Example**: "Table1" or "SalesData"

**Row** (`item`, `dynamic`)
- **Description**: Row data with dynamic fields for each table column
- **Format**: Object with properties matching table columns
- **Example**: `{"CustomerName": "Contoso", "Amount": 1500, "Date": "2025-10-31"}`

#### Optional Parameters

**DateTime Format** (`dateTimeFormat`, `string`)
- **Description**: Format for datetime values
- **Values**: "Local time" or "UTC"
- **Default**: "Local time"
- **Note**: Affects how datetime values are interpreted and stored
</parameters>

<returns>
**Return Type**: `Object` (Dynamic based on table schema)

**Structure**:
Dynamic output matching table structure with all column values for the newly added row.

**Key Fields**:
- Returns all columns defined in the table
- Includes any auto-generated columns or default values
- Timestamps reflect actual storage values after formatting

**Dynamic Content**:
- Access specific columns: `Add_Row?['ColumnName']`
- Use outputs in subsequent actions for confirmation or processing
</returns>

<common_errors>
**403 Forbidden**
- **Cause**: No write access to file or file in read-only mode
- **Solution**: Ensure user has Edit permissions; check file isn't locked

**404 Not Found**
- **Cause**: File, table, or location doesn't exist
- **Solution**: Verify file path and table name are correct

**429 Too Many Requests**
- **Cause**: Exceeded API rate limit (100 calls/60 seconds)
- **Solution**: Add delays between operations; implement exponential backoff

**502 Bad Gateway**
- **Cause**: File locked by another process or spreadsheet in read-only mode
- **Solution**: Wait 6 minutes for file lock to release; check file permissions
</common_errors>

<best_practices>
- **Performance**: Use batch operations when adding multiple rows - consider creating rows first then adding in bulk
- **Concurrency**: Avoid concurrent modifications to same workbook - implement queueing
- **Validation**: Validate data types before adding (string/number/date matching)
- **Key Columns**: Add key column first for future updates/deletes
- **Timing**: Changes may take up to 30 seconds to take effect in Excel Online
</best_practices>

<example>
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/sales/Shared Documents/Q4 Sales.xlsx",
  "Table": "SalesData",
  "Row": {
    "CustomerName": "Fabrikam Inc",
    "OrderDate": "2025-10-31",
    "Amount": 2500.00,
    "Status": "Pending"
  },
  "DateTimeFormat": "UTC"
}
```

**Use Case**: Adding form submission data to Excel tracking sheet
</example>

</action>

---

### Add a Key Column to a Table

<action id="action-002" category="create" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: CreateIdColumn
</action_header>

<description>
Adds a unique identifier column to an Excel table, appended to the rightmost position. Creates auto-incrementing ID values for existing and new rows. Essential for enabling Get/Update/Delete row operations which require key column identification.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file
- **Values**: OneDrive for Business, SharePoint Site, Teams

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Table** (`table`, `string`)
- **Description**: Table to add key column to

#### Optional Parameters

**Key Column** (`idColumn`, `string`)
- **Description**: Name for the key column
- **Default**: "ID"
- **Note**: Field name is case-sensitive; use exact name in subsequent operations
- **Example**: "OrderID", "CustomerKey", "ID"
</parameters>

<returns>
**Return Type**: `Object`

**Structure**:
```json
{
  "columnName": "ID",
  "columnAdded": true,
  "position": "right"
}
```
</returns>

<common_errors>
**409 Conflict**
- **Cause**: Key column with same name already exists
- **Solution**: Use different column name or delete existing key column first

**403 Forbidden**
- **Cause**: No write access to modify table structure
- **Solution**: Ensure Edit permissions on file
</common_errors>

<best_practices>
- **Naming**: Use descriptive key column names like "OrderID" rather than generic "ID"
- **Timing**: Add key column before building flows that update/delete rows
- **Case Sensitivity**: Remember exact capitalization for use in Get/Update/Delete operations
- **One per Table**: Only one key column needed per table
</best_practices>

<example>
```json
{
  "Location": "OneDrive for Business",
  "DocumentLibrary": "OneDrive",
  "File": "/Data/Inventory.xlsx",
  "Table": "Products",
  "KeyColumn": "ProductID"
}
```

**Use Case**: Preparing table for automated inventory updates using product ID matching
</example>

</action>

---

### Create Table

<action id="action-003" category="create" complexity="medium" throttle_impact="medium">

<action_header>
**Operation Type**: Create
**Complexity**: Medium
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: CreateTable
</action_header>

<description>
Creates a new table in an Excel workbook from a specified range with optional column names. Converts existing data range into a structured table format enabling dynamic operations. Useful for initializing data structures or converting static ranges to manageable tables.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Table Range** (`Range`, `string`)
- **Description**: Cell range for table in A1 notation
- **Format**: "Sheet1!A1:D10" or "A1:D10" (if worksheet specified separately)
- **Example**: "Sheet1!A1:D100"
- **Note**: Range must include header row if using column names

#### Optional Parameters

**Table Name** (`TableName`, `string`)
- **Description**: Name for the new table
- **Default**: Auto-generated (e.g., "Table1", "Table2")
- **Note**: Table names must be unique within workbook
- **Example**: "SalesData", "InventoryTracking"

**Column Names** (`ColumnsNames`, `string`)
- **Description**: Semicolon or comma-separated list of column headers
- **Format**: "Column1;Column2;Column3" or "Name,Email,Phone"
- **Example**: "CustomerName;OrderDate;Amount;Status"
- **Note**: Number of names must match number of columns in range
</parameters>

<returns>
**Return Type**: `TableMetadata`

**Structure**:
```json
{
  "id": "1",
  "name": "SalesData",
  "showHeaders": true,
  "showTotals": false,
  "style": "TableStyleMedium2",
  "highlightFirstColumn": false,
  "highlightLastColumn": false,
  "showBandedColumns": false,
  "showBandedRows": true,
  "showFilterButton": true
}
```

**Key Fields**:
- **`id`** (`string`): Numeric ID of table for reference
- **`name`** (`string`): Table name for use in other actions
- **`showHeaders`** (`boolean`): Whether header row is visible
- **`style`** (`string`): Applied table style name
</returns>

<common_errors>
**400 Bad Request**
- **Cause**: Invalid range format or column name count mismatch
- **Solution**: Verify A1 notation and column name count matches range width

**409 Conflict**
- **Cause**: Table with same name exists or range overlaps existing table
- **Solution**: Use unique table name; ensure range doesn't overlap

**404 Not Found**
- **Cause**: Worksheet in range doesn't exist
- **Solution**: Verify worksheet name in range notation
</common_errors>

<best_practices>
- **Range Selection**: Include one extra empty row below data for expansion
- **Naming**: Use descriptive table names following naming conventions (no spaces, start with letter)
- **Headers**: Always provide column names for clarity and dynamic content access
- **Validation**: Verify data format consistency in range before creating table
</best_practices>

<example>
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/hr/Shared Documents/Employee Data.xlsx",
  "TableName": "Employees",
  "TableRange": "Sheet1!A1:F1000",
  "ColumnNames": "EmployeeID;FirstName;LastName;Department;HireDate;Salary"
}
```

**Use Case**: Converting static employee data range into structured table for automated HR workflows
</example>

</action>

---

### Create Worksheet

<action id="action-004" category="create" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Create
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: CreateWorksheet
</action_header>

<description>
Creates a new blank worksheet in an Excel workbook with optional custom name. Useful for organizing data into separate sheets or dynamically creating worksheets for different categories, time periods, or departments.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

#### Optional Parameters

**Name** (`name`, `string`)
- **Description**: Name for the new worksheet
- **Default**: Auto-generated (e.g., "Sheet1", "Sheet2")
- **Constraints**: Max 31 characters; cannot contain: \ / ? * [ ]
- **Example**: "Q4 Sales", "2025 Data", "Summary"
</parameters>

<returns>
**Return Type**: `WorksheetMetadata`

**Structure**:
```json
{
  "id": "{00000000-0001-0000-0000-000000000000}",
  "name": "Q4 Sales",
  "position": 2,
  "visibility": "Visible"
}
```

**Key Fields**:
- **`id`** (`string`): Unique GUID identifier for worksheet
- **`name`** (`string`): Worksheet name for reference in other actions
- **`position`** (`integer`): Zero-based position in workbook tab order
- **`visibility`** (`string`): "Visible", "Hidden", or "VeryHidden"
</returns>

<common_errors>
**409 Conflict**
- **Cause**: Worksheet with same name already exists
- **Solution**: Use unique worksheet name or delete existing worksheet

**400 Bad Request**
- **Cause**: Invalid characters in worksheet name
- **Solution**: Remove prohibited characters: \ / ? * [ ]
</common_errors>

<best_practices>
- **Naming**: Use descriptive names indicating content or purpose
- **Organization**: Create worksheets before adding tables or data to them
- **Limits**: Excel supports maximum 255 worksheets per workbook
- **References**: Use worksheet name in table ranges for clarity
</best_practices>

<example>
```json
{
  "Location": "OneDrive for Business",
  "DocumentLibrary": "OneDrive",
  "File": "/Reports/Monthly Sales.xlsx",
  "Name": "October 2025"
}
```

**Use Case**: Creating monthly worksheet for automated sales report generation
</example>

</action>

---

## Read Operations

### Get a Row

<action id="action-005" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetItem
</action_header>

<description>
Retrieves a single row from an Excel table using key column matching. Returns all column values for the first row where key column matches the specified value. Requires table to have a key column (added via "Add a key column" action).
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Table** (`table`, `string`)
- **Description**: Table to retrieve row from

**Key Column** (`idColumn`, `string`)
- **Description**: Name of key column to match
- **Format**: Exact column name (case-sensitive)
- **Example**: "ID", "OrderID", "CustomerKey"
- **Note**: Must match key column name exactly as created

**Key Value** (`id`, `string`)
- **Description**: Value to search for in key column
- **Format**: String representation of key value
- **Example**: "1234", "ORD-2025-001"

#### Optional Parameters

**DateTime Format** (`dateTimeFormat`, `string`)
- **Description**: Format for datetime values in response
- **Values**: "Local time" or "UTC"
- **Default**: "Local time"

**Extract Sensitivity Label** (`extractSensitivityLabel`, `boolean`)
- **Description**: Whether to extract sensitivity label metadata
- **Default**: false

**Sensitivity Label Metadata** (`fetchSensitivityLabelMetadata`, `boolean`)
- **Description**: Whether to fetch detailed sensitivity label info
- **Default**: false
</parameters>

<returns>
**Return Type**: `Object` (Dynamic based on table schema)

**Structure**:
Dynamic output with all column values for matched row.

**Example**:
```json
{
  "ID": "1234",
  "CustomerName": "Contoso",
  "OrderDate": "2025-10-31T10:30:00Z",
  "Amount": 2500.00,
  "Status": "Shipped"
}
```

**Dynamic Content**:
- Access columns: `Get_Row?['ColumnName']`
- All table columns available as dynamic outputs
</returns>

<common_errors>
**404 Not Found**
- **Cause**: No row with matching key value found
- **Solution**: Verify key value exists; check key column name is correct

**400 Bad Request**
- **Cause**: Table doesn't have key column or key column name incorrect
- **Solution**: Add key column first; verify exact column name (case-sensitive)

**Multiple Matches**
- **Behavior**: Only first matching row returned
- **Recommendation**: Ensure key column has unique values
</common_errors>

<best_practices>
- **Key Column**: Always use unique identifier column for reliable results
- **Case Sensitivity**: Key column name must match exactly (case-sensitive)
- **Error Handling**: Add condition to check if row was found before using outputs
- **Performance**: Get Row is faster than List Rows with filter for single record retrieval
</best_practices>

<example>
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/sales/Orders.xlsx",
  "Table": "OrdersTable",
  "KeyColumn": "OrderID",
  "KeyValue": "ORD-2025-12345",
  "DateTimeFormat": "UTC"
}
```

**Use Case**: Retrieving order details for email notification after status update trigger
</example>

</action>

---

### List Rows Present in a Table

<action id="action-006" category="read" complexity="medium" throttle_impact="high">

<action_header>
**Operation Type**: Read
**Complexity**: Medium
**Throttling Impact**: High
**Premium**: No
**Operation ID**: GetItems
</action_header>

<description>
Retrieves multiple rows from an Excel table with advanced filtering, sorting, and pagination capabilities. Supports OData query syntax for complex data retrieval. Returns dynamic array of row objects with all column values.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Table** (`table`, `string`)
- **Description**: Table to list rows from

#### Optional Parameters

**Filter Query** (`$filter`, `string`)
- **Description**: OData filter expression for row selection
- **Format**: OData v4 syntax
- **Operators**: `eq` (equals), `ne` (not equals), `contains`, `startswith`, `endswith`
- **Examples**:
  - `Status eq 'Active'`
  - `Amount gt 1000`
  - `contains(CustomerName, 'Contoso')`
  - `startswith(OrderID, 'ORD-2025')`
- **Limitations**: Only one filter function per column; no complex AND/OR combinations

**Order By** (`$orderby`, `string`)
- **Description**: Column to sort results by
- **Format**: "ColumnName asc" or "ColumnName desc"
- **Example**: "OrderDate desc", "CustomerName asc"
- **Limitation**: Only one column can be sorted

**Top Count** (`$top`, `integer`)
- **Description**: Maximum number of rows to return
- **Default**: Returns all rows (up to 256 default limit)
- **Example**: 100, 500
- **Note**: Use with Skip for pagination

**Skip Count** (`$skip`, `integer`)
- **Description**: Number of rows to skip from beginning
- **Default**: 0
- **Example**: 100, 500
- **Note**: Use with Top for pagination

**Select Query** (`$select`, `string`)
- **Description**: Comma-separated list of columns to return
- **Format**: "Column1,Column2,Column3"
- **Example**: "OrderID,CustomerName,Amount"
- **Benefit**: Reduces payload size and improves performance

**DateTime Format** (`dateTimeFormat`, `string`)
- **Description**: Format for datetime values
- **Values**: "Local time" or "UTC"

**Extract Sensitivity Label** (`extractSensitivityLabel`, `boolean`)
- **Description**: Whether to extract sensitivity labels

**Sensitivity Label Metadata** (`fetchSensitivityLabelMetadata`, `boolean`)
- **Description**: Whether to fetch label metadata
</parameters>

<returns>
**Return Type**: `Array` of `Object`

**Structure**:
```json
{
  "value": [
    {
      "ID": "1",
      "CustomerName": "Contoso",
      "Amount": 2500.00,
      "Status": "Active"
    },
    {
      "ID": "2",
      "CustomerName": "Fabrikam",
      "Amount": 1800.00,
      "Status": "Pending"
    }
  ]
}
```

**Dynamic Content**:
- Loop through results: Apply to each on `List_Rows?['value']`
- Access row columns in loop: `item()?['ColumnName']`
</returns>

<common_errors>
**400 Bad Request**
- **Cause**: Invalid OData filter syntax or column name doesn't exist
- **Solution**: Verify filter syntax; check column names match exactly

**429 Too Many Requests**
- **Cause**: Too many List Rows calls in short period
- **Solution**: Reduce frequency; implement caching; use filters to reduce calls

**Pagination Issues**
- **Limitation**: Returns maximum 256 rows by default
- **Solution**: Use Top and Skip parameters for pagination
</common_errors>

<best_practices>
- **Performance**: Use $select to return only needed columns
- **Filtering**: Filter at source rather than retrieving all rows and filtering in flow
- **Pagination**: For large datasets, implement pagination with Top/Skip
- **Sorting**: Sort at source using $orderby for better performance
- **Limits**: Be aware of 256 default row limit - use pagination for larger datasets
- **Throttling**: Add delays between List Rows calls in loops
</best_practices>

<example>
**Example 1: Basic filtering and sorting**
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/sales/Orders.xlsx",
  "Table": "Orders",
  "FilterQuery": "Status eq 'Active'",
  "OrderBy": "OrderDate desc",
  "TopCount": 50,
  "Select": "OrderID,CustomerName,Amount,OrderDate"
}
```

**Example 2: Pagination (second page of 100 results)**
```json
{
  "Location": "OneDrive for Business",
  "DocumentLibrary": "OneDrive",
  "File": "/Data/Products.xlsx",
  "Table": "ProductCatalog",
  "TopCount": 100,
  "SkipCount": 100
}
```

**Use Case**: Retrieving active orders for daily summary email report
</example>

</action>

---

### Get Tables

<action id="action-007" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetTables
</action_header>

<description>
Retrieves a list of all tables in an Excel workbook with metadata including table names, IDs, and formatting options. Useful for dynamic table selection or validation before performing operations.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

#### Optional Parameters

**Extract Sensitivity Label** (`extractSensitivityLabel`, `boolean`)
- **Description**: Whether to extract sensitivity labels
- **Default**: false

**Sensitivity Label Metadata** (`fetchSensitivityLabelMetadata`, `boolean`)
- **Description**: Whether to fetch label metadata
- **Default**: false
</parameters>

<returns>
**Return Type**: `Array` of table objects

**Structure**:
```json
{
  "value": [
    {
      "id": "1",
      "name": "SalesData",
      "showHeaders": true,
      "showTotals": false,
      "style": "TableStyleMedium2",
      "showBandedRows": true,
      "showBandedColumns": false,
      "showFilterButton": true,
      "highlightFirstColumn": false,
      "highlightLastColumn": false
    }
  ]
}
```

**Key Fields**:
- **`id`**: Numeric table identifier
- **`name`**: Table name for use in other actions
- **`showHeaders`**: Whether header row visible
- **`style`**: Applied table style
</returns>

<common_errors>
**404 Not Found**
- **Cause**: File doesn't exist or no access
- **Solution**: Verify file path; check permissions

**Empty Result**
- **Behavior**: Returns empty array if no tables in workbook
- **Note**: Not an error condition
</common_errors>

<best_practices>
- **Dynamic Selection**: Use Get Tables to populate dynamic dropdowns for user selection
- **Validation**: Check if specific table exists before attempting operations
- **Caching**: Cache table list if running multiple operations on same workbook
</best_practices>

<example>
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/finance/Reports/Budget.xlsx"
}
```

**Use Case**: Listing available tables for user selection in approval flow
</example>

</action>

---

### Get Worksheets

<action id="action-008" category="read" complexity="low" throttle_impact="low">

<action_header>
**Operation Type**: Read
**Complexity**: Low
**Throttling Impact**: Low
**Premium**: No
**Operation ID**: GetAllWorksheets
</action_header>

<description>
Retrieves a list of all worksheets in an Excel workbook with metadata including names, IDs, positions, and visibility settings. Useful for worksheet validation or dynamic selection workflows.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

#### Optional Parameters

**Extract Sensitivity Label** (`extractSensitivityLabel`, `boolean`)
- **Description**: Whether to extract sensitivity labels
- **Default**: false

**Sensitivity Label Metadata** (`fetchSensitivityLabelMetadata`, `boolean`)
- **Description**: Whether to fetch label metadata
- **Default**: false
</parameters>

<returns>
**Return Type**: `Array` of WorksheetMetadata objects

**Structure**:
```json
{
  "value": [
    {
      "id": "{00000000-0001-0000-0000-000000000000}",
      "name": "Sales Data",
      "position": 0,
      "visibility": "Visible"
    },
    {
      "id": "{00000000-0002-0000-0000-000000000000}",
      "name": "Archive",
      "position": 1,
      "visibility": "Hidden"
    }
  ]
}
```

**Key Fields**:
- **`id`**: Unique GUID identifier
- **`name`**: Worksheet name
- **`position`**: Zero-based tab order
- **`visibility`**: "Visible", "Hidden", or "VeryHidden"
</returns>

<common_errors>
**404 Not Found**
- **Cause**: File doesn't exist or no access
- **Solution**: Verify file path and permissions
</common_errors>

<best_practices>
- **Dynamic Operations**: Use Get Worksheets to validate worksheet exists before operations
- **Filtering**: Filter for visible worksheets only in user-facing workflows
- **Naming**: Use worksheet names in table range specifications
</best_practices>

<example>
```json
{
  "Location": "OneDrive for Business",
  "DocumentLibrary": "OneDrive",
  "File": "/Financial Reports/2025 Budget.xlsx"
}
```

**Use Case**: Listing available worksheets for report generation selection
</example>

</action>

---

## Update Operations

### Update a Row

<action id="action-009" category="update" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Update
**Complexity**: Low
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: PatchItem
</action_header>

<description>
Updates an existing row in an Excel table using key column matching. Overwrites specified columns while leaving blank columns unchanged. Only updates first matching row if multiple rows have same key value. Requires table to have key column.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Table** (`table`, `string`)
- **Description**: Table containing row to update

**Key Column** (`idColumn`, `string`)
- **Description**: Name of key column to match
- **Format**: Exact column name (case-sensitive)
- **Example**: "ID", "OrderID"

**Key Value** (`id`, `string`)
- **Description**: Value to search for in key column
- **Example**: "1234", "ORD-2025-001"

**Provide the item properties** (`item`, `dynamic`)
- **Description**: Object with column names and new values
- **Format**: Dynamic fields for each column
- **Example**: `{"Status": "Completed", "Amount": 3000}`
- **Note**: Only include columns to update; blank columns remain unchanged

#### Optional Parameters

**DateTime Format** (`dateTimeFormat`, `string`)
- **Description**: Format for datetime values
- **Values**: "Local time" or "UTC"
</parameters>

<returns>
**Return Type**: `Object` (Dynamic based on table schema)

**Structure**:
Returns all column values for the updated row.

**Example**:
```json
{
  "ID": "1234",
  "CustomerName": "Contoso",
  "Status": "Completed",
  "Amount": 3000,
  "UpdatedDate": "2025-10-31T15:45:00Z"
}
```
</returns>

<common_errors>
**404 Not Found**
- **Cause**: No row with matching key value found
- **Solution**: Verify key value exists; check key column name

**400 Bad Request**
- **Cause**: Table doesn't have key column or column name incorrect
- **Solution**: Add key column first; verify exact name (case-sensitive)

**Multiple Matches**
- **Behavior**: Only first matching row updated
- **Recommendation**: Ensure key column values are unique

**403 Forbidden**
- **Cause**: No write access to file
- **Solution**: Ensure Edit permissions

**429 Too Many Requests**
- **Cause**: Too many update operations
- **Solution**: Add delays between updates
</common_errors>

<best_practices>
- **Partial Updates**: Only include columns that need updating; omitted columns retain values
- **Unique Keys**: Ensure key column has unique values to avoid updating wrong row
- **Timing**: Changes may take up to 30 seconds to appear in Excel Online
- **Validation**: Verify row exists with Get Row before updating
- **Concurrency**: Avoid concurrent updates to same row from multiple flows
</best_practices>

<example>
```json
{
  "Location": "SharePoint Site",
  "DocumentLibrary": "Documents",
  "File": "/sites/sales/Orders.xlsx",
  "Table": "Orders",
  "KeyColumn": "OrderID",
  "KeyValue": "ORD-2025-12345",
  "ProvidedItemProperties": {
    "Status": "Shipped",
    "ShipDate": "2025-10-31",
    "TrackingNumber": "1Z999AA10123456784"
  }
}
```

**Use Case**: Updating order status and tracking info after shipping integration trigger
</example>

</action>

---

## Delete Operations

### Delete a Row

<action id="action-010" category="delete" complexity="low" throttle_impact="medium">

<action_header>
**Operation Type**: Delete
**Complexity**: Low
**Throttling Impact**: Medium
**Premium**: No
**Operation ID**: DeleteItem
</action_header>

<description>
Deletes a row from an Excel table using key column matching. Removes first row where key column matches specified value. Requires table to have key column. Action is irreversible - deleted data cannot be recovered through Power Automate.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Table** (`table`, `string`)
- **Description**: Table containing row to delete

**Key Column** (`idColumn`, `string`)
- **Description**: Name of key column to match
- **Format**: Exact column name (case-sensitive)

**Key Value** (`id`, `string`)
- **Description**: Value to search for in key column
- **Example**: "1234", "ORD-2025-001"
</parameters>

<returns>
**Return Type**: None (204 No Content on success)

**Behavior**: Returns empty response on successful deletion
</returns>

<common_errors>
**404 Not Found**
- **Cause**: No row with matching key value found
- **Solution**: Verify key value exists; action succeeds even if row not found

**400 Bad Request**
- **Cause**: Table doesn't have key column or column name incorrect
- **Solution**: Verify key column exists; check exact name (case-sensitive)

**Multiple Matches**
- **Behavior**: Only first matching row deleted
- **Recommendation**: Ensure key column values are unique

**403 Forbidden**
- **Cause**: No write/delete access to file
- **Solution**: Ensure Edit permissions
</common_errors>

<best_practices>
- **Confirmation**: Implement approval or confirmation before deleting important data
- **Validation**: Use Get Row first to verify correct row before deletion
- **Logging**: Log deleted row data before deletion for audit trail
- **Unique Keys**: Ensure key column has unique values to delete correct row
- **Error Handling**: Configure "Run After" to handle 404 if row might not exist
- **Backup**: Consider moving row to archive table instead of deleting
</best_practices>

<example>
```json
{
  "Location": "OneDrive for Business",
  "DocumentLibrary": "OneDrive",
  "File": "/Data/Temporary Orders.xlsx",
  "Table": "TempOrders",
  "KeyColumn": "OrderID",
  "KeyValue": "TEMP-12345"
}
```

**Use Case**: Removing temporary order after permanent order created in main system
</example>

</action>

---

## Utility Operations

### Run Script

<action id="action-011" category="utility" complexity="high" throttle_impact="high">

<action_header>
**Operation Type**: Utility
**Complexity**: High
**Throttling Impact**: High
**Premium**: Yes (requires Office Scripts license)
**Operation ID**: RunScriptProd
</action_header>

<description>
Executes an Office Script (TypeScript) against an Excel workbook. Enables complex operations beyond standard connector actions including custom calculations, conditional formatting, advanced data transformations, and multi-table operations. Scripts must be stored in default OneDrive location.
</description>

<parameters>
#### Required Parameters

**Location** (`source`, `string`)
- **Description**: Storage location of the Excel file

**Document Library** (`drive`, `string`)
- **Description**: Document library or drive containing the file

**File** (`file`, `string`)
- **Description**: Path to Excel workbook

**Script** (`scriptId`, `string`)
- **Description**: ID of Office Script to execute
- **Format**: GUID or script reference
- **Location**: Scripts must be in default OneDrive Script storage
- **Note**: Script must be pre-created in Excel Online Script editor

**Script Parameters** (`ScriptParameters`, `dynamic`)
- **Description**: Input parameters for script
- **Format**: Object matching script's parameter signature
- **Example**: `{"sheetName": "Sales", "threshold": 1000}`
- **Note**: Parameters must match script function signature exactly
</parameters>

<returns>
**Return Type**: Dynamic (based on script return value)

**Structure**: Determined by Office Script's return statement

**Example**:
```json
{
  "totalSales": 125000,
  "averageOrder": 2500,
  "topCustomer": "Contoso Inc"
}
```

**Dynamic Content**: Access returned properties based on script output structure
</returns>

<limitations>
**Critical Limitations**:

<limitation id="lim-script-001" severity="critical">
**Throttling**: Maximum 3 calls per 10 seconds per user
</limitation>

<limitation id="lim-script-002" severity="critical">
**Daily Limit**: Maximum 1,600 calls per day per user
</limitation>

<limitation id="lim-script-003" severity="high">
**Availability**: NOT available in sovereign clouds (GCC, GCC High, DoD)
</limitation>

<limitation id="lim-script-004" severity="medium">
**File Format**: Supports .xlsm format in addition to .xlsx
</limitation>

<limitation id="lim-script-005" severity="medium">
**Timeout**: Scripts timeout after 120 seconds of execution
</limitation>

<limitation id="lim-script-006" severity="high">
**License**: Requires Office Scripts feature (Microsoft 365 E3/E5 or specific add-on)
</limitation>
</limitations>

<common_errors>
**429 Too Many Requests**
- **Cause**: Exceeded 3 calls per 10 seconds or 1,600 daily limit
- **Solution**: Add 5-second delays between calls; implement queueing for bulk operations

**400 Bad Request**
- **Cause**: Script parameters don't match function signature
- **Solution**: Verify parameter names and types match script definition

**500 Internal Server Error**
- **Cause**: Script error during execution or timeout
- **Solution**: Review script logic; optimize for performance; reduce data processing scope

**404 Not Found**
- **Cause**: Script ID invalid or not accessible
- **Solution**: Verify script exists in default location; check script sharing permissions
</common_errors>

<best_practices>
- **Throttling**: Implement 5-second delays between script calls
- **Daily Quota**: Monitor usage; implement rotation across multiple users if needed
- **Error Handling**: Wrap script calls in try-scope with proper error handling
- **Performance**: Optimize scripts for minimal execution time (under 30 seconds ideal)
- **Testing**: Test scripts in Excel Online before using in flows
- **Parameters**: Validate parameters before calling script
- **Alternatives**: Use standard actions when possible; reserve scripts for complex operations
</best_practices>

<example>
**Script**: Calculate sales metrics and apply conditional formatting
```typescript
// Office Script (saved in Excel Online)
function main(workbook: ExcelScript.Workbook, sheetName: string, threshold: number) {
  const sheet = workbook.getWorksheet(sheetName);
  const range = sheet.getUsedRange();
  const values = range.getValues();

  let total = 0;
  let count = 0;

  for (let i = 1; i < values.length; i++) {
    const amount = values[i][2] as number;
    total += amount;
    count++;

    // Apply formatting for values above threshold
    if (amount > threshold) {
      const cell = range.getCell(i, 2);
      cell.getFormat().getFont().setColor("Green");
      cell.getFormat().getFont().setBold(true);
    }
  }

  return {
    totalSales: total,
    averageOrder: total / count,
    processedRows: count
  };
}
```

**Flow Action**:
```json
{
  "Location": "OneDrive for Business",
  "DocumentLibrary": "OneDrive",
  "File": "/Reports/Q4 Sales.xlsx",
  "Script": "Script123456789",
  "ScriptParameters": {
    "sheetName": "October",
    "threshold": 5000
  }
}
```

**Use Case**: Running complex sales analysis with custom formatting beyond standard actions
</example>

</action>

---

### Run Script from SharePoint Library

<action id="action-012" category="utility" complexity="high" throttle_impact="high">

<action_header>
**Operation Type**: Utility
**Complexity**: High
**Throttling Impact**: High
**Premium**: Yes (requires Office Scripts license)
**Operation ID**: RunScriptProdV2
</action_header>

<description>
Executes an Office Script stored in a SharePoint document library (instead of default OneDrive location). Enables centralized script management and team collaboration on script development. Functionality identical to "Run script" but with flexible storage location.
</description>

<parameters>
#### Required Parameters

**Workbook Location** (`source`, `string`)
- **Description**: Storage location of the Excel file to process

**Workbook Library** (`drive`, `string`)
- **Description**: Document library containing the workbook

**Workbook** (`file`, `string`)
- **Description**: Path to Excel workbook to process

**Script Location** (`scriptSource`, `string`)
- **Description**: Storage location of the Office Script
- **Values**: SharePoint Site, OneDrive, Teams

**Script Library** (`scriptDrive`, `string`)
- **Description**: Document library containing the script file

**Script** (`scriptId`, `string`)
- **Description**: Path or ID of Office Script file (.osts)

**Script Parameters** (`ScriptParameters`, `dynamic`)
- **Description**: Input parameters matching script function signature
</parameters>

<returns>
**Return Type**: Dynamic (based on script return value)

Same return behavior as "Run script" action.
</returns>

<limitations>
**Same limitations as "Run script" action**:
- Maximum 3 calls per 10 seconds
- Maximum 1,600 calls per day per user
- NOT available in sovereign clouds
- 120-second timeout
- Requires Office Scripts license
</limitations>

<common_errors>
Same error scenarios as "Run script" action plus:

**403 Forbidden**
- **Cause**: No access to script file in SharePoint library
- **Solution**: Ensure script file permissions allow execution by flow identity
</common_errors>

<best_practices>
- **Centralization**: Store commonly used scripts in SharePoint for team access
- **Version Control**: Use SharePoint versioning for script change tracking
- **Access Control**: Set appropriate permissions on script library
- **Documentation**: Maintain script documentation in same library
- **All other best practices from "Run script" action apply**
</best_practices>

<example>
```json
{
  "WorkbookLocation": "SharePoint Site",
  "WorkbookLibrary": "Documents",
  "Workbook": "/sites/finance/Shared Documents/Budget 2025.xlsx",
  "ScriptLocation": "SharePoint Site",
  "ScriptLibrary": "Scripts",
  "Script": "/sites/finance/Scripts/BudgetAnalysis.osts",
  "ScriptParameters": {
    "department": "Sales",
    "quarter": "Q4"
  }
}
```

**Use Case**: Running centrally managed budget analysis script across department workbooks
</example>

</action>

---

## Deprecated Actions

### Add a Row into a Table (V1) [DEPRECATED]

<action id="action-013-deprecated" category="create" complexity="low">

<action_header>
**Status**: DEPRECATED - Use AddRowV2 instead
**Operation ID**: AddRow
</action_header>

<description>
Original version of "Add a row" action without DateTime Format parameter. Deprecated in favor of AddRowV2 which provides better datetime handling. Existing flows using this action will continue to work but should be migrated.
</description>

<recommendation>
**Migration**: Replace with "Add a row into a table (V2)" action and specify DateTime Format parameter for consistent datetime behavior.
</recommendation>

</action>

---

## Common Error Codes (All Actions)

<error id="err-403" http_code="403">
**Error**: 403 Forbidden
**Causes**:
- No write access to file
- File in read-only mode
- File checked out by another user
- Insufficient SharePoint permissions

**Solutions**:
- Verify Edit permissions on file
- Ensure file not locked by another process
- Wait 6 minutes for file lock to release
- Check SharePoint/OneDrive permissions
</error>

<error id="err-404" http_code="404">
**Error**: 404 Not Found
**Causes**:
- File path invalid or file moved/deleted
- Table or worksheet doesn't exist
- Location or library incorrect

**Solutions**:
- Verify file path is current
- Check table/worksheet names are correct
- Validate location and library selections
- Use dynamic content to avoid hardcoded paths
</error>

<error id="err-429" http_code="429">
**Error**: 429 Too Many Requests
**Causes**:
- Exceeded 100 API calls per 60 seconds per connection
- Too many concurrent operations

**Solutions**:
- Add delays between operations (5+ seconds recommended)
- Implement exponential backoff retry logic
- Reduce frequency of operations
- Use multiple connections to distribute load
- Enable concurrency control on triggers
</error>

<error id="err-502" http_code="502">
**Error**: 502 Bad Gateway
**Causes**:
- File locked by another process
- Workbook in read-only mode
- Excel service timeout

**Solutions**:
- Wait 6 minutes for file lock to release
- Check file permissions (read-only attribute)
- Reduce complexity of operation
- Retry operation after delay
</error>

<error id="err-400" http_code="400">
**Error**: 400 Bad Request
**Causes**:
- Invalid parameter format
- Missing required parameter
- Invalid OData query syntax
- Column name mismatch

**Solutions**:
- Validate parameter formats (A1 notation, column names, etc.)
- Verify all required parameters provided
- Check OData syntax in filter queries
- Ensure column names match exactly (case-sensitive)
</error>

---

## General Limitations

<limitation id="lim-general-001" severity="critical">
**File Size**: Maximum 25 MB per workbook
- Larger files may cause timeouts or failures
- Recommendation: Split large datasets across multiple workbooks
</limitation>

<limitation id="lim-general-002" severity="high">
**API Rate Limit**: 100 calls per 60 seconds per connection
- Shared across all actions using same connection
- Recommendation: Add delays between operations; use multiple connections
</limitation>

<limitation id="lim-general-003" severity="high">
**File Lock**: Files remain locked for up to 6 minutes after connector use
- Prevents concurrent modifications
- Affects manual editing and other automation
- Recommendation: Wait 6 minutes between flow runs on same file
</limitation>

<limitation id="lim-general-004" severity="high">
**Write Access Required**: All actions require write access, even read operations
- Graph API limitation
- Recommendation: Grant Edit permissions even for read-only flows
</limitation>

<limitation id="lim-general-005" severity="medium">
**Concurrent Modifications**: Unsupported
- Multiple flows modifying same file simultaneously cause conflicts
- Recommendation: Implement queueing or locking mechanism
</limitation>

<limitation id="lim-general-006" severity="medium">
**Complex Formulas**: May cause timeout errors
- Heavy calculations in worksheets slow operations
- Recommendation: Minimize formula complexity; pre-calculate values
</limitation>

<limitation id="lim-general-007" severity="medium">
**Delay in Changes**: Changes may take up to 30 seconds to reflect in Excel Online
- Affects immediately subsequent reads after writes
- Recommendation: Add 30-second delay before reading recently modified data
</limitation>

<limitation id="lim-general-008" severity="low">
**Request Size**: Maximum 5 MB per connector request
- Affects large row operations and file uploads
- Recommendation: Batch large operations into smaller chunks
</limitation>

---

## Performance Optimization Best Practices

### Throttling Management
1. **Add Delays**: Insert 5+ second delays between operations
2. **Batch Operations**: Group multiple row additions into single operation when possible
3. **Concurrent Limit**: Limit trigger concurrency to 10-20 parallel runs
4. **Multiple Connections**: Use separate connections for high-volume flows

### Query Optimization
1. **Filter at Source**: Use $filter instead of retrieving all rows
2. **Select Columns**: Use $select to return only needed columns
3. **Pagination**: Use Top/Skip for large datasets instead of retrieving all rows
4. **Sort at Source**: Use $orderby instead of sorting in flow

### File Management
1. **Keep Files Small**: Target under 10 MB for optimal performance
2. **Minimize Formulas**: Reduce complex calculations in worksheets
3. **Archive Old Data**: Move historical data to separate workbooks
4. **Avoid Concurrent Access**: Queue operations to prevent conflicts

### Error Handling
1. **Configure Run After**: Handle failures gracefully
2. **Retry Logic**: Implement exponential backoff for transient failures
3. **Validation**: Check for existence before operations
4. **Logging**: Log operations for debugging and audit

---

**Last Updated**: 2025-10-31
**Documentation Version**: 1.0
**Connector Version**: Current (as of 2025-10-31)
**Official Reference**: https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/
