# Example Usage - Fetching and Formatting Documentation

This guide demonstrates how to use the output-style templates to fetch and format Power Automate connector documentation.

## Scenario 1: Adding a New Connector (Excel Online)

### Step 1: Fetch Overview Documentation

**Use WebFetch with overview prompt:**

```markdown
Extract comprehensive Excel Online connector overview information including:

<required_sections>
1. Official documentation URL (Microsoft Learn)
2. Brief description (2-3 sentences) of connector purpose and what it connects to
3. Main capabilities (5-7 items in bullet list format)
4. API limits and throttling constraints (specific numbers: calls per time period, size limits)
5. Critical limitations grouped by category
6. Known issues and constraints that cause errors
7. Common use cases (top 5 scenarios)
</required_sections>

<formatting_requirements>
- Use clear markdown headers (## for main sections)
- Use bullet lists for capabilities and limitations
- Include specific numbers for all limits
- Use **bold** for limitation names
- Group related limitations under category headers
- Keep descriptions concise (1-2 sentences)
</formatting_requirements>

<focus>
Focus on actionable information needed for debugging flows and understanding constraints.
</focus>
```

### Step 2: Format Using Template

Open `template-overview.md` and fill in with fetched data:

```markdown
# Excel Online Connector Overview

## Official Documentation
https://learn.microsoft.com/en-us/connectors/excelonline/

## Description
Excel Online connector allows you to work with Excel files stored in OneDrive for Business and SharePoint Online. You can read, create, update tables, rows, and worksheets programmatically.

## Capabilities
- Read and write data to Excel tables
- Create and manage worksheets
- Add and update table rows
- List tables and worksheets
- Execute Excel calculations
- Work with named ranges

## API Limits
- **100 calls per 60 seconds** per connection
- **Maximum file size**: 100 MB
- **Maximum rows per operation**: 5000 rows

[... continue filling template ...]
```

### Step 3: Save Documentation

Save to: `PowerAutomateDocs/ExcelOnline/overview.md`

---

## Scenario 2: Debugging a Throttling Error

### Step 1: Check Existing Documentation

Look up the connector in `PowerAutomateDocs/{ConnectorName}/overview.md` for API limits.

**Example: SharePoint throttling**

From `PowerAutomateDocs/SharePoint/overview.md`:
```
## API Limits
- **600 calls per 60 seconds** per connection
```

### Step 2: Fetch Specific Error Documentation

If more detail needed, use error resolution prompt:

```xml
<task>
Extract troubleshooting information for 429 throttling errors in SharePoint connector.

<required_information>
1. Common scenarios that cause this error
2. Error message patterns to recognize
3. Root causes
4. Step-by-step resolution procedures
5. Prevention strategies
6. Alternative approaches if error persists
</required_information>
</task>
```

### Step 3: Apply Solution from Documentation

Based on `PowerAutomateDocs/SharePoint/actions.md` best practices:
- Implement delay between calls
- Use batch operations
- Enable concurrency with caution
- Filter at source to reduce calls

---

## Scenario 3: Understanding an Action

### Goal
Understand how to use SharePoint "Create file" action

### Step 1: Locate Action Documentation

Open: `PowerAutomateDocs/SharePoint/actions.md`

Search for: "### Create file"

### Step 2: Review Structure

```markdown
### Create file
**Description**: Creates a new file in SharePoint

**Parameters**:
- Site Address (required)
- Folder Path (required)
- File Name (required)
- File Content (required)

**Returns**: File properties including ID, path, metadata

**Use Cases**:
- Document generation workflows
- Backup automation
- Report creation

**Best Practices**:
- Use unique naming to avoid overwrites
- Validate folder path exists
- Handle large files appropriately
```

### Step 3: Implement in Flow

Use the information to configure the action correctly in flow.json

---

## Scenario 4: Creating Documentation for Missing Actions

### Situation
You need documentation for a specific action not yet documented.

### Step 1: Use Actions WebFetch Prompt

```xml
Extract detailed documentation for SharePoint "Generate document using Syntex" action including:
- Action name and description
- All parameters (required/optional)
- Return values
- Limitations and constraints
- Use cases
- Configuration examples
- Best practices
```

### Step 2: Format Using Template

Use `template-actions.md` structure:

```markdown
### Generate document using Syntex
**Description**: Creates a document using Microsoft Syntex template

**Parameters**:
- Site Address (required) - SharePoint site URL
- Template Id (required) - Syntex template identifier
- Output Location (required) - Where to save generated document
- Document Name (required) - Name for generated file

**Returns**: Generated document metadata including ID and path

**Important Notes**:
- Requires Microsoft Syntex license
- Template must be trained and published
- Limited to supported document types

**Use Cases**:
- Automated contract generation
- Report templating
- Document standardization

**Examples**:
```
Site Address: https://contoso.sharepoint.com/sites/Docs
Template Id: template-12345
Output Location: /Shared Documents/Generated
Document Name: Contract-2025-001.docx
```

**Best Practices**:
- Verify template is published before using
- Use consistent naming conventions
- Handle generation failures gracefully
- Test with sample data first
```

### Step 3: Add to Actions Document

Insert into appropriate category in `PowerAutomateDocs/SharePoint/actions.md`

---

## Scenario 5: Comparing Two Connectors

### Goal
Decide between OneDrive and SharePoint for file storage in flow

### Step 1: Use Comparison Prompt

```xml
Compare OneDrive and SharePoint connectors for file storage and management workflows.

<comparison_points>
- Capabilities overlap and differences
- API limits and throttling
- File size constraints
- Performance characteristics
- Use case suitability
</comparison_points>
```

### Step 2: Review Existing Documentation

**From OneDrive overview**:
- 100 calls per 60 seconds
- Files over 50MB skipped by triggers
- Personal and business storage

**From SharePoint overview**:
- 600 calls per 60 seconds
- 90MB attachment limit
- Collaborative document management
- Does not support custom list templates

### Step 3: Make Decision

Based on comparison:
- **Use OneDrive** for: Personal file storage, simple file operations
- **Use SharePoint** for: Collaborative documents, team sites, complex metadata

---

## Scenario 6: Building a Complete Flow Documentation

### Goal
Document a complete flow pattern: "OneDrive file sync to SharePoint"

### Step 1: Identify Components

- Trigger: OneDrive "When a file is created"
- Actions:
  - OneDrive "Get file content"
  - SharePoint "Create file"
  - Data Operation "Compose" for metadata

### Step 2: Reference Documentation

Check each in respective docs:
- `PowerAutomateDocs/OneDrive/triggers.md` - When file created
- `PowerAutomateDocs/OneDrive/actions.md` - Get file content
- `PowerAutomateDocs/SharePoint/actions.md` - Create file
- `PowerAutomateDocs/BuiltIn/data-operation.md` - Compose

### Step 3: Document Pattern

Add to connector's documentation:

```markdown
## Common Patterns

### Pattern: OneDrive to SharePoint Sync
```
When file created (OneDrive) → Get file content → Compose metadata → Create file (SharePoint)
```

**Use Case**: Automatically sync files from personal OneDrive to team SharePoint site

**Implementation**:
1. Configure OneDrive trigger on specific folder
2. Get file content immediately
3. Compose SharePoint metadata (site, library, folder)
4. Create file in SharePoint with content
5. Add error handling for file size limits

**Considerations**:
- OneDrive trigger skips files > 50MB
- SharePoint has 90MB attachment limit
- Add retry logic for throttling
- Use unique file naming to avoid conflicts
```

---

## Best Practices for Using Templates

### 1. Always Start with WebFetch Prompt
Use standardized prompts from `webfetch-prompts.md` for consistency

### 2. Follow Template Structure
Don't skip sections - they ensure completeness

### 3. Be Specific with Numbers
Never use "several", "many", "large" - use actual limits

### 4. Include Examples
Concrete examples are more valuable than abstract descriptions

### 5. Update Regularly
When you find new information, update the docs

### 6. Cross-Reference
Link related actions, triggers, and patterns

### 7. Test Documentation
Verify links work and examples are accurate

### 8. Keep It Concise
Follow Anthropic's guidance: clarity over verbosity

---

## Quick Checklist

When creating new documentation:
- [ ] Used appropriate WebFetch prompt template
- [ ] Followed correct template structure
- [ ] Included all required sections
- [ ] Used specific numbers for limits
- [ ] Added concrete examples
- [ ] Included best practices
- [ ] Added troubleshooting guidance
- [ ] Formatted with proper markdown
- [ ] Saved to correct directory
- [ ] Updated main README if needed
