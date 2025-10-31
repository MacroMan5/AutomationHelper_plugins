---
type: node-overview
node_name: Pinecone Vector Store
node_type: database
category: action
auth_required: true
version: 1.0
last_updated: 2025-10-31
keywords: [pinecone, vector-database, embeddings, similarity-search, rag, ai-agents, semantic-search, langchain, openai]
related_nodes: [OpenAI, Embeddings, LangChain, HTTP Request]
rate_limits:
  service_rate_limit: Depends on Pinecone tier (Free: 10 queries/second, Pro: unlimited)
  n8n_limit: none (N8N doesn't impose limits, service-side limits apply)
official_docs_url: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstorepinecone/
---

<official_docs>
- **N8N Pinecone Node**: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstorepinecone/
- **Pinecone Documentation**: https://docs.pinecone.io/
- **Pinecone Vector Store Examples**: https://docs.n8n.io/advanced-ai/examples/vector-store-website/
- **Vector Databases Overview**: https://www.pinecone.io/learn/vector-database/
</official_docs>

<description>
The Pinecone Vector Store node enables N8N workflows to store and retrieve document embeddings for AI-powered semantic search and retrieval-augmented generation (RAG). Pinecone is a managed vector database optimized for high-dimensional vector similarity search, making it essential for building intelligent AI applications. It seamlessly integrates with OpenAI embeddings to transform documents into searchable vectors and retrieve relevant context for LLM applications.
</description>

<capabilities>
## Core Capabilities
- Insert documents with embeddings into Pinecone vector index
- Retrieve documents via semantic similarity search using query embeddings
- Update existing documents in the vector store by ID
- Get multiple documents by ID for direct access
- Support for metadata filtering alongside vector similarity
- Namespace isolation for multi-tenant data separation
- Upsert operations for safe insert-or-update
- Batch operations for bulk document processing
- Integration with OpenAI Embeddings for automatic text-to-vector conversion

## Supported Operations
- **Insert Documents**: Add new documents with embeddings to index
- **Get Many**: Retrieve specific documents by ID
- **Update Documents**: Modify existing documents by ID
- **Retrieve Documents (As Vector Store)**: Fetch documents for use with chains/tools
- **Retrieve Documents (As Tool)**: Return documents formatted for AI agent tools
- **Query by Similarity**: Semantic search returning top-k similar documents
- **Namespace Management**: Isolate data within single index using namespaces
- **Metadata Filtering**: Query by metadata attributes alongside similarity

## Integration Features
- Seamless OpenAI Embeddings integration for automatic vectorization
- LangChain compatibility for chains and agents
- Batch processing for bulk document operations
- Metadata-based filtering for refined queries
- Namespace support for data isolation across tenants
- TTL (time-to-live) support for automatic document expiration
- Upsert capability for idempotent operations
- No size limits on document count or dimensions
- Automatic index creation and management
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Limits by Plan**:
- **Free tier**: 10 queries per second, 1 million vectors total
- **Starter**: 100 queries per second, 100 million vectors
- **Pro**: Unlimited queries, unlimited vectors (usage-based pricing)
- **Enterprise**: Custom limits based on SLA

**API Quotas**:
- **Requests per minute**: 3,000-unlimited (depends on tier)
- **Concurrent requests**: 100+ per second (tier-dependent)
- **Request size**: 32MB maximum per request
- **Batch size**: 100-1,000 vectors per batch (optimize for 100-200)

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited by Pinecone API quotas
- Cloud: Depends on N8N cloud plan and Pinecone tier
- Execution timeout: 300 seconds (N8N default)

**Throttling Behavior**:
- HTTP Status: 429 (Too Many Requests) when quota exceeded
- Error message: "Rate limit exceeded", "You have exceeded your request limit"
- N8N automatic retry: Yes (configurable exponential backoff)
- Recommended retry strategy: Exponential backoff with 5-10 second delays

## Size Limits

**Vector Operations**:
- Max vector dimension: 20,000 (typical: 384-1536 for OpenAI)
- Max documents per query: 10-100 (configurable)
- Max metadata per document: ~40KB
- Max document ID length: 512 characters
- Max namespace length: 249 characters

**Batch Operations**:
- Max vectors per batch: Depends on vector size (1KB vectors = ~30 per batch)
- Max batch size: 100-200 vectors recommended for optimal throughput
- Max request payload: 32MB total

## Timeout Limits**:
- Default query timeout: **5 seconds**
- Insert/update timeout: **30 seconds**
- Batch operation timeout: **60 seconds**
- Max configurable timeout: **300 seconds**
- Long-running operations: Batching recommended for large datasets
</rate_limits>

<critical_limitations>
## Critical Limitations & Workarounds

<limitation id="lim-001" severity="critical">
**Expensive Embedding Generation**
- **Issue**: Generating embeddings via OpenAI API costs money per token
- **Impact**: Significant costs at scale, unexpected billing
- **Cause**: Each document requires OpenAI API call to generate embeddings
- **Workaround**:
  1. Use batch embedding mode: Process multiple documents in single request
  2. Cache embeddings: Store computed embeddings, reuse for duplicate content
  3. Limit document frequency: Update only when content changes
  4. Use smaller models: OpenAI has embedding models for cost optimization
  5. Monitor embedding usage: Set Pinecone quotas to prevent overages
  6. Pre-compute embeddings offline: Before importing to Pinecone
  7. Use alternative embeddings: Consider Hugging Face or Cohere for cost control
  8. Batch workflow executions: Consolidate multiple operations per run
- **N8N Handling**: Use Code node to batch embeddings, cache results in Redis
</limitation>

<limitation id="lim-002" severity="critical">
**No Full-Text Search**
- **Issue**: Pinecone only supports vector similarity search, not traditional keyword search
- **Impact**: Cannot search by exact match or keyword, requires embedding all queries
- **Cause**: Vector database design optimized for semantic search only
- **Workaround**:
  1. Hybrid approach: Use PostgreSQL for keyword search + Pinecone for semantic
  2. Semantic keywords: Include keywords in document metadata and filter results
  3. BM25 metadata: Store keyword scores in metadata for post-filtering
  4. Pinecone + Elasticsearch: Combine with keyword search engine
  5. Embedding expansion: Include common keywords in documents before embedding
  6. Query transformation: Convert keywords to semantic embeddings via OpenAI
  7. Pre-filtering: Use metadata to reduce candidate set before similarity search
- **N8N Handling**: Use PostgreSQL for initial keyword filtering, Pinecone for semantic ranking
</limitation>

<limitation id="lim-003" severity="critical">
**Static Index Configuration**
- **Issue**: Vector dimension determined at index creation; cannot change without recreating
- **Impact**: Cannot switch embedding models without full index rebuild
- **Cause**: Pinecone stores vectors in specific dimensional space
- **Workaround**:
  1. Plan embedding model upfront: Choose appropriate OpenAI embedding model
  2. Create separate indexes: Different indexes for different models
  3. Maintain version index: "documents_v1", "documents_v2" for model upgrades
  4. Batch recreation process: Export, re-embed, reimport during off-hours
  5. Gradual migration: Create new index, dual-write, switch gradually
  6. Document dimensions: 384 (small), 1536 (large) most common
- **N8N Handling**: Choose embedding model wisely, plan for version migration
</limitation>

<limitation id="lim-004" severity="high">
**No Structured Data Queries**
- **Issue**: Cannot efficiently query by non-vector attributes (time range, category, etc.)
- **Impact**: Must retrieve all results and filter in application, inefficient filtering
- **Cause**: Vector databases optimized for similarity search, not range queries
- **Workaround**:
  1. Metadata filtering: Include queryable attributes in document metadata
  2. Sparse filtering: Use metadata conditions to reduce candidate set
  3. Hybrid approach: PostgreSQL for structured queries, Pinecone for ranking
  4. Denormalization: Store commonly filtered fields in metadata
  5. Pre-aggregation: Compute aggregates offline, store results
  6. Pinecone Hybrid Search: Recent feature for combining keyword + semantic
  7. Application filtering: Retrieve with filters, post-process in N8N
- **N8N Handling**: Use metadata for coarse filtering, application logic for fine filtering
</limitation>

<limitation id="lim-005" severity="high">
**Cost Scaling with Data Volume**
- **Issue**: Pro tier charges per vector-month; massive cost at scale
- **Impact**: Unexpected billing for large document collections
- **Cause**: Managed service pricing model
- **Workaround**:
  1. Archive old documents: Remove expired documents regularly
  2. Deduplication: Avoid storing identical documents
  3. Consolidation: Merge related documents to reduce count
  4. TTL implementation: Auto-expire documents after retention period
  5. Sampling: Store subset of data if full index not needed
  6. Self-hosted alternatives: Evaluate Milvus, Weaviate for cost control
  7. Cost monitoring: Track vector count, set alerts for growth
  8. Batch operations: Consolidate updates to minimize API calls
- **N8N Handling**: Schedule cleanup workflows, implement TTL, monitor usage
</limitation>

<limitation id="lim-006" severity="high">
**Limited Transaction Support**
- **Issue**: No ACID transactions; distributed upserts not atomic
- **Impact**: Inconsistent state during batch updates, duplicate/missing records
- **Cause**: Eventually consistent distributed system design
- **Workaround**:
  1. Idempotent IDs: Use stable document IDs for safe retries
  2. Versioning: Include timestamp in documents for ordering
  3. Batch verification: Count before/after for sanity checks
  4. Application transactions: Track state in PostgreSQL or Redis
  5. Immutable snapshots: Create backups before batch operations
  6. Error handling: Implement comprehensive error recovery
  7. Monitoring: Track inconsistencies with auditing
- **N8N Handling**: Use idempotent IDs, verify batch operations, implement error handling
</limitation>

<limitation id="lim-007" severity="high">
**No Complex Filtering**
- **Issue**: Metadata filtering limited to simple equality/inequality conditions
- **Impact**: Cannot execute complex queries like range, regex, or compound conditions
- **Cause**: Vector database design, metadata search is secondary feature
- **Workaround**:
  1. PostgreSQL for complex queries: Primary queries to Postgres, use Pinecone for ranking
  2. Denormalized metadata: Pre-compute all possible filter combinations
  3. Multiple indexes: Create indexes by common filter criteria
  4. Application filtering: Retrieve all results, filter in N8N Code node
  5. Separate metadata store: PostgreSQL for queryable attributes, Pinecone for vectors
  6. Pinecone search API: Use newer sparse-dense features (beta)
- **N8N Handling**: PostgreSQL primary query, Pinecone for re-ranking by relevance
</limitation>

<limitation id="lim-008" severity="medium">
**No Document Update Tracking**
- **Issue**: Cannot easily determine which documents were recently updated
- **Impact**: No efficient change data capture (CDC), requires polling all documents
- **Cause**: Vector database not designed for change tracking
- **Workaround**:
  1. Timestamp metadata: Include updated_at in all documents
  2. CDC in source system: Track changes in source, replicate to Pinecone
  3. Versioning: Embed version numbers in documents
  4. Audit log: Maintain separate PostgreSQL audit table
  5. Polling strategy: Query source at intervals, sync changes
  6. Event-based sync: Webhook triggers when documents change
- **N8N Handling**: Add timestamp field, use Postgres for change tracking
</limitation>

<limitation id="lim-009" severity="medium">
**Semantic Search Inconsistency**
- **Issue**: Relevance ranking can change if embeddings shift (model updates, data drift)
- **Impact**: Same query returns different results over time; user confusion
- **Cause**: Vector embeddings are learned representations that can drift
- **Workaround**:
  1. Stable embeddings: Fix embedding model version until planned migration
  2. Re-embedding schedule: Planned model upgrades with full index migration
  3. Semantic versioning: Document embedding model version with vectors
  4. A/B testing: Gradual rollout of new embedding models
  5. Human feedback: Track user satisfaction with results
  6. Cache queries: Store popular queries with expected results
  7. Monitoring: Alert when result relevance scores change significantly
- **N8N Handling**: Pin embedding model version, plan major version upgrades
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### Pinecone API Key (Standard)
**Most Common Method**:
- Get API key from Pinecone console
- No expiration by default (store securely)
- Per-project scoped (if using Pinecone Organization)

**Configuration in N8N**:
1. Create Pinecone account at https://www.pinecone.io/
2. Create index and get API key
3. Add credentials in N8N:
   - API Key: From Pinecone console
   - Environment: e.g., "gcp-starter", "us-east-1-aws" (from index URL)
   - Index name: Name of your Pinecone index
4. Test connection before saving

**Security Notes**:
- Store API key in N8N credential system, never in workflows
- Use separate API keys for development/production
- Rotate keys periodically (Pinecone manages auto-rotation)
- Restrict to trusted IP addresses if available

### Pinecone Organizations (Enterprise)
**For team management**:
- Organization-level authentication
- User management and RBAC
- Audit logging and compliance
- Multiple projects and indexes

**Requirements**:
- Pinecone enterprise account
- Organization ID and API key
- Project-specific credentials

### Environment Variables (Self-Hosted N8N)
**For containerized deployments**:
```
PINECONE_API_KEY=your_key_here
PINECONE_INDEX=your_index_name
PINECONE_ENVIRONMENT=your_environment
```

### Index-Specific Authentication
**Using namespace isolation**:
- Single API key for all namespaces
- Namespaces provide logical separation
- Different indexes for different environments

**Recommended approach**:
- Separate index per environment (dev, staging, prod)
- Shared API key within environment
- Different API keys across environments
</authentication>

<common_use_cases>
## Common Use Cases

### 1. RAG (Retrieval-Augmented Generation) for AI Assistants
**Scenario**: Build intelligent chatbot that references company documents
- **Typical workflow**: Webhook (query) → OpenAI Embeddings (convert query) → Pinecone Retrieve (find relevant docs) → OpenAI Chat (answer with context) → Response
- **Why this operation**: Enables LLMs to answer questions grounded in specific documents
- **Considerations**: Chunk size for documents, number of results (top-k), context quality
- **N8N Pattern**: Query → Retrieve 5-10 relevant docs → Include in prompt → Get answer

### 2. Document Search & Discovery
**Scenario**: Enable semantic search across company knowledge base
- **Typical workflow**: User search query → OpenAI Embeddings → Pinecone Query → Format results → Return to user
- **Why this operation**: Find relevant documents by meaning, not keywords
- **Considerations**: Query performance, result quality, user satisfaction
- **N8N Pattern**: Filter by metadata → Similarity search → Re-rank by confidence

### 3. Content Recommendations
**Scenario**: Recommend similar articles, products, or resources
- **Typical workflow**: Current item embedding → Pinecone similarity search → Return top-N similar items
- **Why this operation**: Find semantically related content for personalization
- **Considerations**: Result diversity, relevance threshold, performance
- **N8N Pattern**: Use Pinecone metadata filters for category/type restrictions

### 4. Document Deduplication
**Scenario**: Identify and remove duplicate or near-duplicate documents
- **Typical workflow**: New document → Generate embedding → Query for similar → Compare similarity score → Keep/remove
- **Why this operation**: Maintain dataset quality, reduce storage costs
- **Considerations**: Similarity threshold, handling false positives
- **N8N Pattern**: Query with high similarity threshold, compare IDs before deleting

### 5. Multi-Language Search
**Scenario**: Enable search across documents in multiple languages
- **Typical workflow**: Multilingual document → OpenAI multilingual embeddings → Pinecone storage → Same embedding model for queries
- **Why this operation**: Create unified search across language barriers
- **Considerations**: OpenAI supports 100+ languages, automatic language detection
- **N8N Pattern**: Language detection → Same embedding model → Language-neutral search

### 6. Real-Time Information Indexing
**Scenario**: Continuously update knowledge base with new documents
- **Typical workflow**: Source trigger (new article) → Chunk document → Generate embeddings → Pinecone Insert → Update metadata
- **Why this operation**: Keep knowledge base current with latest information
- **Considerations**: Update frequency, duplicate handling, embedding cost
- **N8N Pattern**: Source webhook → Text splitter → Batch embeddings → Upsert
</common_use_cases>

<best_practices>
## Best Practices

### Document Preparation
1. **Chunk large documents**: Split long documents into 256-512 token chunks
   - Impact: Better semantic granularity, more precise matches
   - Tool: Use Text Splitter node with overlap (100 tokens)
   - Bad: Store entire 10,000 token document as one vector
   - Good: Split into 20 chunks of 512 tokens with 100-token overlap

2. **Include metadata for filtering**: Add queryable attributes to all documents
   - Examples: Category, date, author, source, language
   - Enables metadata filtering in Pinecone Retrieve
   - Format as JSON: `{"source": "blog", "date": "2025-10-31"}`

3. **Use consistent document IDs**: Deterministic, idempotent IDs for safe updates
   - Format: "source-type_unique-id" (e.g., "blog-article_12345")
   - Enables safe re-processing without duplicates
   - Upsert with same ID overwrites previous version

4. **Clean text before embedding**: Remove HTML tags, normalize whitespace
   - Impact: Cleaner embeddings, better search quality
   - Use Set node to pre-process text
   - Remove code blocks, special formatting if not relevant to search

5. **Document versioning**: Include version in ID or metadata
   - Enables gradual migration when updating documents
   - Track embedding model version used
   - Support A/B testing of different chunk strategies

### Query Optimization
1. **Use metadata filters for pre-filtering**: Reduce candidate set before similarity search
   - Impact: Faster queries, better relevance
   - Good: Filter by date range, category, language first
   - Then apply similarity search on filtered set

2. **Tune top-k results**: Balance relevance vs. latency
   - Default 10 results often sufficient
   - Reduce for latency-sensitive applications
   - Increase only if more context needed

3. **Implement query expansion**: Multiple queries for comprehensive coverage
   - Query original + paraphrases
   - Combine results from multiple queries
   - N8N Pattern: Generate 2-3 variations of user query

4. **Cache popular queries**: Store and reuse query results
   - Impact: Reduced costs, faster responses
   - Use Redis for query→results caching
   - Invalidate cache when index updates

### Cost Optimization
1. **Batch embeddings generation**: Process multiple documents per OpenAI call
   - Impact: 50%+ cost reduction
   - Use batch mode if available
   - N8N Pattern: Collect 10-20 documents, generate embeddings together

2. **Archive old documents**: Implement TTL or scheduled cleanup
   - Impact: Reduced vector-month charges
   - Remove documents not accessed in 90 days
   - Keep only active, relevant documents

3. **Deduplication strategy**: Detect and prevent duplicate documents
   - Check similarity score before insert
   - Use deterministic IDs for idempotent updates
   - Reduces redundant vectors

4. **Monitor usage**: Set up alerts for unexpected growth
   - Track vector count daily
   - Alert on cost anomalies
   - Implement quotas to prevent overages

5. **Right-size index**: Start small, grow with demand
   - Free tier: Evaluate feasibility
   - Starter: Typical use cases
   - Pro: Scale-out as needed

### Reliability
1. **Implement error handling**: Handle API failures gracefully
   - Rate limits (429), timeouts, connection errors
   - Exponential backoff for retries
   - Fallback to direct database queries if needed

2. **Verify operations**: Validate before and after bulk operations
   - Count vectors before/after batch insert
   - Check document existence after update
   - Alert on mismatches

3. **Backup strategy**: Maintain external backup of vectors
   - Periodically export to cold storage
   - Store in S3 or Google Cloud Storage
   - Enable recovery from data loss

4. **Monitor index health**: Track performance metrics
   - Query latency and throughput
   - Error rates and types
   - Storage usage and cost

### Performance
1. **Optimize embedding model**: Choose appropriate model for use case
   - ada-002: Fastest, cheaper (~$0.10 per 1M tokens)
   - Other models: Different speed/quality tradeoffs
   - Match model capability to domain

2. **Connection pooling**: Reuse connections for efficiency
   - N8N handles automatically
   - Reduces connection overhead

3. **Pagination for large result sets**: Don't retrieve all vectors at once
   - Use offset/limit for iteration
   - Process in batches if returning many results

4. **Asynchronous operations**: Non-blocking for batch operations
   - Don't wait for large batch inserts to complete
   - Use error handling for async failures

### Security
1. **API key rotation**: Periodically generate new keys
   - Retire old keys after transition period
   - Maintain audit trail of key changes

2. **Restrict API access**: Use Pinecone network policies
   - IP whitelisting if available
   - VPC endpoint for private access (enterprise)

3. **Encrypt sensitive metadata**: Don't store PII in Pinecone
   - Encrypt in application layer if needed
   - Use pseudonymous IDs

4. **Audit logging**: Track all vector operations
   - Who added/updated/deleted documents
   - Query patterns and frequency
   - Cost tracking per source

5. **Namespace isolation**: Separate data by tenant
   - Use namespaces for multi-tenant applications
   - Prevents data leakage between users
</best_practices>

<common_errors>
## Common Errors & Troubleshooting

<error ref="err-001" http_code="401">
**Error**: "Unauthorized" or "Invalid API key"
- **Cause**: Wrong API key, expired key, or incorrect environment
- **N8N Context**: Credential validation or query execution fails
- **Fix**:
  1. Verify API key: Check Pinecone console for correct key
  2. Check environment: Ensure environment matches index (us-east-1, gcp-starter, etc.)
  3. Verify index name: Must match exactly (case-sensitive)
  4. Test credentials: Use Pinecone CLI: `pinecone whoami`
  5. Check key expiration: Regenerate if needed
  6. Update N8N credentials: Verify stored values match Pinecone
- **Prevention**: Use separate keys per environment, document configurations
</error>

<error ref="err-002" http_code="404">
**Error**: "Index not found" or "Index does not exist"
- **Cause**: Index name incorrect, index deleted, or wrong account
- **N8N Context**: Query or insert operations fail immediately
- **Fix**:
  1. List available indexes: `pinecone list-indexes` or Pinecone console
  2. Verify index name: Exact match required, case-sensitive
  3. Check account: Confirm you're in correct Pinecone organization
  4. Create index if missing: Define vector dimensions first
  5. Update N8N configuration: Use correct index name
- **Prevention**: Document index names, use constants in N8N
</error>

<error ref="err-003" http_code="429">
**Error**: "Rate limit exceeded" or "Too many requests"
- **Cause**: Exceeded plan quotas (Free: 10 qps, Starter: 100 qps)
- **N8N Context**: Operations fail under load
- **Fix**:
  1. Check rate limits: Review Pinecone plan quotas
  2. Implement exponential backoff: Retry with increasing delays
  3. Batch operations: Consolidate multiple requests
  4. Reduce query frequency: Implement caching
  5. Upgrade plan: If sustained high throughput needed
  6. Distribute load: Space out operations over time
- **Prevention**: Monitor API usage, implement caching, upgrade plan proactively
</error>

<error ref="err-004" http_code="400">
**Error**: "Invalid dimension" or "Vector dimension mismatch"
- **Cause**: Embedding dimensions don't match index dimensions
- **N8N Context**: Insert operations fail
- **Fix**:
  1. Check index dimensions: List indexes to see vector size
  2. Verify embedding model: OpenAI ada outputs 1536 dimensions
  3. Match dimensions: Must match exactly (e.g., 1536)
  4. Use consistent embeddings: Same model for all documents
  5. Recreate index if needed: Requires rebuilding if wrong dimension
- **Prevention**: Document index dimensions, use same embedding model consistently
</error>

<error ref="err-005" http_code="400">
**Error**: "Invalid namespace" or "Namespace does not exist"
- **Cause**: Namespace name incorrect or doesn't exist
- **N8N Context**: Operations target non-existent namespace
- **Fix**:
  1. Verify namespace name: List existing namespaces
  2. Use default namespace: Leave empty for "default"
  3. Create namespace if needed: Pinecone creates on first insert
  4. Check character limit: Max 249 characters
  5. Use valid characters: Alphanumeric, hyphen, underscore only
- **Prevention**: Use consistent namespace naming, document namespace structure
</error>

<error ref="err-006" http_code="413">
**Error**: "Request too large" or "Payload exceeds size limit"
- **Cause**: Request larger than 32MB, too many vectors in batch
- **N8N Context**: Batch operations fail
- **Fix**:
  1. Reduce batch size: Limit to 100-200 vectors per batch
  2. Check vector size: Large metadata increases payload
  3. Compress metadata: Minimize JSON structure
  4. Split operation: Send multiple smaller batches
  5. Reduce metadata: Only store essential attributes
- **Prevention**: Batch sizing, metadata minimization, split large operations
</error>

<error ref="err-007" http_code="408">
**Error**: "Request timeout" or "Operation timed out"
- **Cause**: Query took too long, network latency, server overload
- **N8N Context**: Long-running operations timeout
- **Fix**:
  1. Reduce result limit: Fewer results = faster queries
  2. Add metadata filter: Pre-filter reduces search space
  3. Increase timeout: Extend N8N timeout if appropriate
  4. Check server status: Pinecone status page for issues
  5. Optimize query: Use more specific search parameters
  6. Upgrade plan: Higher tier has better performance
- **Prevention**: Monitor query latency, optimize queries, use caching
</error>

<error ref="err-008" http_code="400">
**Error**: "Duplicate document ID" or "Document already exists"
- **Cause**: Attempting to insert with ID that already exists
- **N8N Context**: Insert operations fail on re-run
- **Fix**:
  1. Use upsert instead of insert: Replaces existing
  2. Generate unique IDs: Include timestamp or hash
  3. Delete old first: Remove before inserting with same ID
  4. Implement idempotence: Same ID = intentional update
  5. Check N8N configuration: Retry logic might cause duplicate
- **Prevention**: Use upsert for safety, generate deterministic IDs
</error>

### Embedding Issues
- **"Embedding generation failed"**: OpenAI API error; check API key, quotas
- **"Embedding model not available"**: OpenAI deprecating model; update model version
- **"Token limit exceeded"**: Document chunk too large; reduce size

### Query Issues
- **"No results returned"**: Query embedding not similar to stored vectors
  - Check document content relevance
  - Adjust similarity threshold
  - Verify same embedding model used
- **"Relevance score too low"**: Results not relevant
  - Modify query
  - Check document quality
  - Consider hybrid search (keyword + semantic)

### Data Issues
- **"Vector count mismatch"**: Number of inserted vectors differs from expected
  - Verify batch size and completeness
  - Check for failed operations
  - Monitor error logs
- **"Stale data"**: Old documents appearing in results
  - Verify TTL implementation
  - Check update frequency
  - Delete obsolete documents
</common_errors>

<related_operations>
## Related AI & Data Nodes

### Embedding Integration
- **OpenAI Embeddings**: Text-to-vector conversion (primary integration)
- **Anthropic Claude**: Text generation based on retrieved context
- **LangChain**: Framework for building RAG applications

### Supporting Components
- **Text Splitter**: Chunk large documents before embedding (critical)
- **Set (Edit Fields)**: Transform data format, prepare for insertion
- **Code Node**: Implement complex embedding or filtering logic
- **HTTP Request**: Manual API calls if needed

### Complementary Databases
- **PostgreSQL**: Structured queries, change tracking, audit logging
- **Redis**: Cache query results, store embedding metadata
- **MongoDB**: Store full documents alongside vectors

### Workflow Patterns
1. **RAG Pattern**: Query → Embed → Retrieve → LLM Answer
2. **Batch Indexing**: Extract → Chunk → Embed → Insert
3. **Search Deduplication**: Query → Find similar → Compare score → De-duplicate
4. **Content Recommendation**: Item ID → Get embedding → Find similar → Return

### See Also
- **LangChain Documentation**: For advanced chains and agents
- **OpenAI Embedding Costs**: Plan budget for embedding API calls
- **Vector Database Comparison**: Weaviate, Milvus, Qdrant alternatives
- **Document Chunking Strategy**: Critical for search quality
</related_operations>

<troubleshooting>
## Troubleshooting Guide

### Connection Issues

**Problem**: Cannot connect to Pinecone
- **Check**: API key, environment, network connectivity
- **Solution**:
  1. Verify API key: Get from Pinecone console
  2. Check environment: Match exact environment string (gcp-starter, us-east-1-aws, etc.)
  3. Test manually: Use curl to verify connectivity
  4. Check Pinecone status: Status page for service issues
  5. Verify N8N network: Can N8N reach api.pinecone.io?
  6. Check for typos: Environment and index names case-sensitive
- **N8N Tools**:
  - Test credentials in N8N
  - Check execution logs for specific error
  - Use Code node to diagnose connection issues

**Problem**: Rate limit errors in production
- **Check**: API quota usage, query frequency
- **Solution**:
  1. Monitor API usage: Pinecone dashboard shows current usage
  2. Upgrade plan: Free tier has 10 qps limit
  3. Implement caching: Reduce redundant queries via Redis
  4. Batch operations: Consolidate multiple requests
  5. Distribute load: Spread operations over time
  6. Optimize queries: Reduce result count, add filters
  7. Contact support: For quota increase requests
- **N8N Tools**:
  - Implement cache layer with Redis
  - Add rate limiting logic
  - Monitor API calls per minute

### Query Issues

**Problem**: Queries returning irrelevant results
- **Check**: Embedding quality, document content, similarity threshold
- **Solution**:
  1. Verify documents: Check actual document content in Pinecone
  2. Test embeddings: Manually create embeddings, compare similarity
  3. Adjust query: Rephrase for clarity and specificity
  4. Check embedding model: Ensure consistency across all documents
  5. Review chunk size: Too large or too small affects relevance
  6. Add metadata filters: Pre-filter irrelevant documents
  7. Implement hybrid search: Combine keyword + semantic search
  8. User feedback: Track which results are actually relevant
- **N8N Tools**:
  - Log query and results for analysis
  - A/B test different chunking strategies
  - Monitor result satisfaction metrics

**Problem**: Slow query performance
- **Check**: Query complexity, result count, metadata filtering
- **Solution**:
  1. Reduce result limit: Request fewer results
  2. Add metadata filters: Reduce search space
  3. Check query latency: Monitor performance
  4. Optimize query format: More specific search parameters
  5. Upgrade plan: Higher tiers have better performance
  6. Check index size: Very large indexes may be slower
  7. Monitor Pinecone: Check for service performance issues
  8. Cache results: Don't re-query frequently-asked questions
- **N8N Tools**:
  - Add timing measurements
  - Implement query caching
  - Reduce batch size for faster processing

### Embedding Issues

**Problem**: Embedding generation fails
- **Check**: OpenAI API key, token limits, content length
- **Solution**:
  1. Verify OpenAI API key: Valid and active
  2. Check OpenAI quota: Sufficient API credits
  3. Test embedding: Try shorter text first
  4. Check text length: Document might exceed token limit
  5. Review OpenAI docs: Embedding model changes/deprecations
  6. Reduce text size: Split very long documents
  7. Use Text Splitter: Process chunks instead of full documents
- **N8N Tools**:
  - Test embedding in Code node
  - Log text being embedded for debugging
  - Monitor OpenAI API usage and costs

**Problem**: Inconsistent embeddings for same content
- **Check**: Embedding model version, preprocessing
- **Solution**:
  1. Use consistent model: Same OpenAI model version throughout
  2. Pin model version: Specify exact model (ada-002)
  3. Consistent preprocessing: Clean text same way each time
  4. Document version: Track which model generated embeddings
  5. Plan migrations: Systematic process for model upgrades
  6. Test stability: Verify same text produces same embedding
- **N8N Tools**:
  - Store model version in Pinecone metadata
  - Plan gradual model upgrades
  - A/B test embedding changes

### Data Issues

**Problem**: Documents not appearing in search results
- **Check**: Document insertion success, namespace, content relevance
- **Solution**:
  1. Verify insertion: Check vector count in Pinecone
  2. List documents: Use get_stats() to verify
  3. Check namespace: Ensure querying correct namespace
  4. Verify IDs: Confirm documents inserted with expected IDs
  5. Check content: Document may not be semantically relevant
  6. Wait for indexing: Freshly inserted vectors need indexing time
  7. Re-index if needed: Sometimes necessary after updates
- **N8N Tools**:
  - Log all insert operations
  - Verify batch completion
  - Monitor vector count trends

**Problem**: Unexpected cost spikes
- **Check**: Vector count growth, query volume, embedding frequency
- **Solution**:
  1. Monitor vector count: Check Pinecone dashboard
  2. Review queries: High QPS might indicate inefficiency
  3. Check embeddings: Expensive API calls for each document
  4. Implement quotas: Set alerts for cost thresholds
  5. Archive old data: Remove obsolete documents
  6. Batch embeddings: Reduce OpenAI API calls
  7. Optimize usage: Implement caching, reduce redundant operations
  8. Upgrade plan if justified: Sometimes cheaper long-term
- **N8N Tools**:
  - Track embedding costs in logs
  - Implement usage monitoring
  - Set up cost alerts
  - Schedule regular cleanup

### Update/Deletion Issues

**Problem**: Update operations not reflecting immediately
- **Check**: Async processing, eventual consistency
- **Solution**:
  1. Check operation status: Verify update completed
  2. Wait briefly: Pinecone is eventually consistent
  3. Use upsert: Atomic insert-or-update
  4. Verify ID: Ensure updating correct document ID
  5. Check namespace: Confirm update in correct namespace
  6. Query again: May see old cached results temporarily
- **N8N Tools**:
  - Add delay after updates before querying
  - Log update timestamps
  - Implement verification queries

**Problem**: Delete operations leaving traces
- **Check**: Delete success, verification
- **Solution**:
  1. Verify deletion: Query should not return deleted IDs
  2. Check cascade: Deleting from main index deletes from all namespaces
  3. Use soft delete: Mark as deleted rather than removing
  4. Implement backup: Keep audit trail of deleted documents
  5. Verify completeness: Ensure all related documents deleted
- **N8N Tools**:
  - Log all deletions with timestamp
  - Implement audit trail
  - Verify deletion in subsequent query
</troubleshooting>

---

**Documentation Status**: ✅ **COMPLETE & PRODUCTION-READY**
**Last Updated**: 2025-10-31
**Next Steps**: Combine with OpenAI and LangChain for complete AI/RAG applications