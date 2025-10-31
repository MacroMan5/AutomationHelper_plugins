# N8N Workflow Automation Documentation

## Overview

This documentation provides comprehensive information about N8N nodes, their capabilities, limitations, and best practices. It follows an agent-optimized format for efficient search and retrieval.

## Documentation Structure

```
N8NDocs/
├── README.md                    # This file - overview and navigation
├── DOCUMENTATION_STATUS.md      # Current status of all documentation
├── Templates/                   # Documentation templates
│   ├── README.md               # Template usage guide
│   ├── template-node-overview.md    # Node overview template
│   ├── template-node-operations.md  # Node operations template
│   └── agent-optimized-format.md    # Format specifications
├── Core/                        # Built-in core nodes
│   ├── overview.md             # Core nodes overview
│   ├── http-request.md         # HTTP Request node
│   ├── webhook.md              # Webhook node
│   ├── code.md                 # Code/Function node
│   ├── schedule.md             # Schedule trigger
│   ├── set.md                  # Set/Transform node
│   ├── if.md                   # IF conditional node
│   └── merge.md                # Merge node
├── AI/                         # AI integration nodes
│   ├── overview.md             # AI nodes overview
│   ├── openai.md               # OpenAI node
│   ├── anthropic.md            # Anthropic Claude node
│   ├── langchain.md            # LangChain integration
│   └── ai-agent.md             # AI Agent node
├── Apps/                       # Third-party app integrations
│   ├── overview.md             # App nodes overview
│   ├── google-sheets.md        # Google Sheets node
│   ├── slack.md                # Slack node
│   ├── gmail.md                # Gmail node
│   ├── notion.md               # Notion node
│   └── github.md               # GitHub node
├── Database/                   # Database nodes
│   ├── overview.md             # Database nodes overview
│   ├── postgresql.md           # PostgreSQL node
│   ├── mysql.md                # MySQL node
│   └── mongodb.md              # MongoDB node
└── Community/                  # Popular community nodes
    ├── overview.md             # Community nodes overview
    ├── firecrawl.md            # Firecrawl Scraper
    ├── apify.md                # Apify node
    └── tesseract.md            # Tesseract OCR node
```

## Node Categories

### Core Nodes (Built-in)
Essential nodes that come pre-installed with N8N:
- **HTTP Request**: Make API calls to any service
- **Webhook**: Receive data from external sources
- **Code**: Execute custom JavaScript/Python
- **Schedule**: Trigger workflows on a schedule
- **Set**: Transform and manipulate data
- **IF**: Conditional logic branching
- **Merge**: Combine data from multiple sources

### AI Nodes
Nodes for AI and machine learning integrations:
- **OpenAI**: GPT-4, DALL-E, Whisper integration
- **Anthropic**: Claude AI integration
- **LangChain**: 70+ nodes for building AI applications
- **AI Agent**: Build autonomous AI agents
- **Vector Store**: Store and query embeddings

### App Nodes
Third-party service integrations:
- **Google Workspace**: Sheets, Gmail, Drive, Calendar
- **Microsoft 365**: Excel, SharePoint, Outlook, Teams
- **Communication**: Slack, Discord, Telegram
- **Productivity**: Notion, Airtable, Asana
- **Development**: GitHub, GitLab, Jira

### Database Nodes
Database integrations for data storage and retrieval:
- **SQL Databases**: PostgreSQL, MySQL, SQL Server
- **NoSQL Databases**: MongoDB, Redis, Firestore
- **Cloud Databases**: Supabase, AWS RDS, Azure SQL

### Community Nodes
Popular community-contributed nodes:
- **Web Scraping**: Firecrawl, Apify
- **OCR**: Tesseract, Google Vision
- **Utilities**: Logger, Custom Auth

## Documentation Format (v2)

All N8N node documentation uses the **agent-optimized format v2**:

### Key Features
- **YAML Frontmatter**: Metadata for filtering (keywords, categories, rate limits)
- **XML Tags**: Structured sections (`<limitation>`, `<operation>`, `<error>`)
- **Unique IDs**: Easy reference (lim-001, op-http-get, err-429)
- **Semantic Attributes**: Advanced filtering (severity, complexity, throttle_impact)

### Benefits
- **Fast Agent Search**: Find specific information quickly
- **Direct Navigation**: Jump to sections by ID
- **Precise Extraction**: XML tags enable targeted queries
- **Smart Filtering**: Filter by severity, category, complexity

## Quick Search Examples

### Find API Rate Limits
```bash
grep -r "rate_limit:" Docs/N8NDocs/*/overview.md
grep "requests_per_minute:" Docs/N8NDocs/AI/openai.md
```

### Find Critical Limitations
```bash
grep -r '<limitation.*severity="critical"' Docs/N8NDocs/
grep '<limitation' Docs/N8NDocs/Core/http-request.md
```

### Find Operations by Type
```bash
grep -r 'category="read"' Docs/N8NDocs/*/*.md
grep 'complexity="low"' Docs/N8NDocs/Core/*.md
```

### Search by Keywords
```bash
grep -r "keywords:.*api" Docs/N8NDocs/*/overview.md
grep -r "keywords:.*database" Docs/N8NDocs/Database/*.md
```

## Common Use Cases

### 1. API Integration
Use HTTP Request node to integrate with any REST API

### 2. Data Processing Pipelines
Chain nodes to transform and route data

### 3. AI-Powered Workflows
Use AI nodes for intelligent automation

### 4. Scheduled Tasks
Run workflows on a schedule for periodic tasks

### 5. Event-Driven Automation
Use webhooks to trigger workflows from external events

## Best Practices

### Workflow Design
1. Start with simple workflows and iterate
2. Use error handling nodes (Error Trigger)
3. Add logging for debugging
4. Test with sample data first

### Performance
1. Use pagination for large datasets
2. Implement rate limit handling
3. Cache frequently accessed data
4. Use batch operations when available

### Security
1. Store credentials securely in N8N
2. Use environment variables
3. Validate input data
4. Implement authentication properly

## Official Resources

- **N8N Documentation**: https://docs.n8n.io/
- **Node Reference**: https://docs.n8n.io/integrations/builtin/
- **Community Nodes**: https://www.npmjs.com/search?q=n8n-nodes-*
- **Community Forum**: https://community.n8n.io/
- **GitHub Repository**: https://github.com/n8n-io/n8n

## Related Documentation

- **PowerAutomate Docs**: [../PowerAutomateDocs/](../PowerAutomateDocs/) - Similar automation platform
- **Templates**: [./Templates/](./Templates/) - Documentation templates
- **Status**: [DOCUMENTATION_STATUS.md](./DOCUMENTATION_STATUS.md) - Documentation completeness

## Contributing

To add or update documentation:
1. Use templates from `Templates/` directory
2. Follow agent-optimized format v2
3. Include YAML frontmatter with keywords
4. Use XML tags for structured sections
5. Assign unique IDs to all elements
6. Update DOCUMENTATION_STATUS.md

## Documentation Status

See [DOCUMENTATION_STATUS.md](./DOCUMENTATION_STATUS.md) for current progress.

---

**Last Updated**: 2025-10-31
**Version**: 1.0
**Format**: Agent-Optimized v2
