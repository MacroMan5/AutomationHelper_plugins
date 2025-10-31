---
type: node-overview
node_name: Redis
node_type: database
category: action
auth_required: true
version: 1.0
last_updated: 2025-10-31
keywords: [redis, cache, key-value, nosql, in-memory, session, queue, pub-sub, ttl, data-structure]
related_nodes: [PostgreSQL, MongoDB, Set, HTTP Request]
rate_limits:
  service_rate_limit: Depends on Redis server configuration (typically 10,000-100,000+ ops/sec)
  n8n_limit: none (N8N doesn't impose limits, server-side limits apply)
official_docs_url: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.redis/
---

<official_docs>
- **Node Documentation**: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.redis/
- **Redis Official Docs**: https://redis.io/documentation
- **Redis Commands**: https://redis.io/commands/
- **N8N Redis Queue**: https://docs.n8n.io/hosting/scaling/queue-mode/
</official_docs>

<description>
The Redis node enables N8N workflows to interact with Redis in-memory data structures for caching, session management, and real-time data operations. Redis is ideal for high-performance workflows requiring fast data access, temporary storage, and pub/sub messaging. It's commonly used for workflow queuing, caching frequently accessed data, and managing application state across distributed N8N instances.
</description>

<capabilities>
## Core Capabilities
- Get and set key-value pairs with TTL (time-to-live) support
- Increment and decrement numeric values atomically
- Publish messages to channels for real-time pub/sub messaging
- Delete keys and manage key expiration
- Retrieve information about Redis server and memory usage
- Pattern-based key matching for batch operations
- Multiple data structure support (strings, lists, sets, hashes, sorted sets)
- Atomic operations for counter management
- Batch operations for bulk key management

## Supported Operations (Core)
- **Delete Key**: Remove key-value pair from Redis
- **Get Key Value**: Retrieve value associated with key
- **Set Key Value**: Store or update key-value pair (supports TTL)
- **Publish To Channel**: Send message to Redis pub/sub channel
- **Get Info**: Retrieve server statistics and configuration
- **Increment**: Atomically increase numeric value
- **Get Keys By Pattern**: Find keys matching pattern (e.g., "session:*")
- **Delete Keys By Pattern**: Batch delete keys matching pattern

## Integration Features
- Credential-based authentication with host, port, username, password
- Optional SSL/TLS encryption for remote connections
- Support for Redis clusters and sentinels (via custom connection strings)
- Automatic connection pooling and reuse
- Optional database selection (Redis database 0-15)
- Password-protected Redis instances support
- Compatible with Redis Cloud, AWS ElastiCache, Azure Cache
- TTL-based automatic expiration
- Atomic operations for reliability
- Batch operations for performance
</capabilities>

<rate_limits>
## Rate Limits

**Service-Level Throughput**
- **Operations per second**: 10,000-100,000+ (depends on server hardware)
- **Throughput scope**: Per Redis instance
- **Concurrent connections**: Limited by Redis maxclients setting (default 10,000)
- **Retry-After header**: N/A (no standard throttling)
- **N8N built-in retry**: Yes (configurable exponential backoff)

**Operation-Specific Considerations**
- **SET operations**: Typically <1ms latency for single operations
- **PATTERN operations**: Scan is non-blocking but may require multiple iterations for large key sets
- **PUB/SUB operations**: Unlimited channels, but message latency depends on subscriber count
- **Memory operations**: Limited by available Redis memory

**N8N Platform Limits**
- No built-in rate limiting by N8N platform
- Self-hosted: Limited by server resources (CPU, memory, network)
- Cloud: Depends on N8N cloud plan and Redis server resources
- Memory per operation: Minimal (Redis is in-memory)

**Throughput Behavior**
- Standard HTTP Status: 200 (success) or connection error
- Error scenarios: Connection timeout, out-of-memory errors
- N8N automatic retry: Yes (configurable)
- Recommended retry strategy: Exponential backoff with 10-50ms delays

## Size Limits

**Data Operations**
- Max key length: **512MB** per key (practical limit: 256 bytes for performance)
- Max value size: **512MB** per value (practical limit: 1-10MB)
- Max keys per instance: Depends on available memory
- Memory per operation: Minimal

**Batch Operations**
- Max keys per pattern operation: Limited by available memory
- Max pattern results: Scan iteratively for large key sets
- Max batch size: Depends on operation complexity

## Timeout Limits
- Default connection timeout: **5 seconds**
- Command execution timeout: **1-30 seconds** (configurable)
- Max configurable timeout: **300 seconds**
- Long-running operations: Not recommended for Redis (fire-and-forget better)
</rate_limits>

<critical_limitations>
## Critical Limitations & Workarounds

<limitation id="lim-001" severity="critical">
**No Persistence by Default**
- **Issue**: Redis is in-memory; data is lost if server restarts
- **Impact**: Data loss for critical information, unreliable for permanent storage
- **Cause**: Redis designed for caching and temporary data, not durable storage
- **Workaround**:
  1. Enable persistence in Redis config: `save 900 1` (save every 15 min if 1 key changed)
  2. Use Redis snapshots: `BGSAVE` for background snapshots
  3. Enable AOF (Append Only File): `appendonly yes` in redis.conf
  4. Use Redis Cloud with persistence enabled
  5. Implement backup to permanent storage (PostgreSQL, S3) for critical data
  6. Design workflows assuming data can be lost
- **N8N Handling**: Use for caching, sessions, temporary data only; critical data to PostgreSQL
</limitation>

<limitation id="lim-002" severity="critical">
**Memory-Only Storage**
- **Issue**: All data stored in RAM; limited by available server memory
- **Impact**: Cannot store large datasets, memory exhaustion crashes instance
- **Cause**: Redis trades persistence for speed
- **Workaround**:
  1. Monitor memory usage: `INFO memory` command
  2. Set max memory limit: `maxmemory 2gb` in redis.conf
  3. Implement eviction policy: `maxmemory-policy allkeys-lru` (remove least recently used)
  4. Use separate Redis for different data types (caching, sessions, queues)
  5. Archive old data to permanent storage
  6. Implement TTL for all keys to auto-expire
  7. Use Redis Cluster for horizontal scaling
- **N8N Handling**: Set aggressive TTL values, monitor memory, implement cleanup workflows
</limitation>

<limitation id="lim-003" severity="critical">
**Pattern Scanning Performance**
- **Issue**: KEYS and pattern matching operations are slow on large datasets
- **Impact**: Workflow timeout, Redis server blocking, other operations delayed
- **Cause**: Full key space scan required; no index support for patterns
- **Workaround**:
  1. Use SCAN cursor instead of KEYS: `SCAN 0 MATCH pattern:* COUNT 100`
  2. Implement pagination: Process results in batches across workflow executions
  3. Use specific key naming: Prefix keys with category (session:user:123)
  4. Keep dataset small: Archive old keys regularly
  5. Use hashes instead of separate keys: Reduces key count
  6. Implement secondary index: Maintain separate sorted set of key names
  7. Upgrade Redis: Version 6.2+ has improved SCAN performance
- **N8N Handling**: Split pattern operations into scheduled batch jobs with pagination
</limitation>

<limitation id="lim-004" severity="high">
**Limited Query Capabilities**
- **Issue**: Redis lacks SQL-like query language; complex filtering not supported
- **Impact**: Cannot query data by value (only by key), limited aggregation
- **Cause**: Key-value store design, no built-in indexing
- **Workaround**:
  1. Use Redis Search (Redis 6.2+): Full-text search on hash fields
  2. Maintain secondary indexes: Sorted sets of keys grouped by category
  3. Store metadata in hashes: Enables filtering by field value
  4. Use Redis Streams: Better for time-series data with querying
  5. Denormalize data: Store multiple indexed copies of data
  6. Use PostgreSQL for queryable data, Redis for caching
- **N8N Handling**: Use PostgreSQL for complex queries, Redis for fast lookups only
</limitation>

<limitation id="lim-005" severity="high">
**No Transaction Rollback**
- **Issue**: Multi-step operations cannot be atomic if executed separately
- **Impact**: Partial failures, data inconsistency in complex workflows
- **Cause**: Each N8N operation is separate; no multi-command transaction support
- **Workaround**:
  1. Use Lua scripting: Atomic multi-step operations
  2. Implement idempotence: Operations safe to retry
  3. Design for eventual consistency: Accept temporary inconsistency
  4. Pre-verify state: Check conditions before operations
  5. Use PostgreSQL transactions for critical operations
  6. Implement application-level rollback logic
- **N8N Handling**: Use Code node for Lua scripting, design for eventual consistency
</limitation>

<limitation id="lim-006" severity="high">
**Single-Threaded Execution**
- **Issue**: Redis commands execute single-threaded; blocking operations block all clients
- **Impact**: Slow operations impact all connected clients, scaling limitations
- **Cause**: Redis architecture for consistency and simplicity
- **Workaround**:
  1. Use Redis Cluster: Shard data across multiple Redis instances
  2. Offload slow operations: Use background jobs, separate services
  3. Implement timeouts: Fail fast on slow operations
  4. Use non-blocking patterns: Pub/Sub instead of polling
  5. Pipeline operations: Batch commands for efficiency
  6. Optimize Lua scripts: Keep script execution time minimal
- **N8N Handling**: Use Redis Cluster for high concurrency, implement async patterns
</limitation>

<limitation id="lim-007" severity="high">
**No Built-In Encryption**
- **Issue**: Data in transit and at rest not encrypted by default
- **Impact**: Security vulnerability for sensitive data
- **Cause**: Redis designed for trusted networks, not internet-exposed
- **Workaround**:
  1. Use SSL/TLS: Enable TLS support in Redis and N8N
  2. Encrypt sensitive data: Application-level encryption before storing
  3. Private network: Restrict Redis to private subnet
  4. Use Redis Cloud: Provides encryption and security
  5. Implement access control: Redis ACL for authentication
  6. Use SSH tunnel: Encrypt connection over SSH
  7. Monitor access: Log all connections and commands
- **N8N Handling**: Enable TLS in Redis credentials, avoid storing sensitive data
</limitation>

<limitation id="lim-008" severity="medium">
**Limited Pub/Sub Guarantees**
- **Issue**: Pub/Sub messages not persisted; subscribers must be listening or messages lost
- **Impact**: Unreliable messaging, dropped notifications
- **Cause**: Pub/Sub designed for real-time, not durable messaging
- **Workaround**:
  1. Use Redis Streams: Persistent pub/sub with replay capability
  2. Implement message queuing: Store messages until processed
  3. Verify subscribers: Ensure listeners connected before publishing
  4. Use persistent queue: PostgreSQL or message broker for important messages
  5. Implement retry logic: Re-send failed messages
  6. Combine with persistent storage: Store in PostgreSQL + Redis
- **N8N Handling**: Use Streams for critical messages, Pub/Sub for real-time notifications only
</limitation>
</critical_limitations>

<authentication>
## Authentication Methods

### Standard Redis (No Auth)
**For development/trusted networks only**:
- Host: localhost or IP address
- Port: 6379 (default) or custom
- No password required
- Suitable for local development and testing

### Password-Protected Redis (Most Common)
**Requirements**:
- Host/IP address of Redis server
- Port number (default 6379)
- Password (required for authentication)
- Optional: Database number (0-15)

**Configuration in N8N**:
1. Add Redis credential in N8N credentials panel
2. Enter host, port, password
3. Test connection before saving
4. Reference in Redis node

**Security Notes**:
- Never use default port 6379 on internet-facing servers
- Use strong passwords (minimum 32 characters)
- Rotate passwords regularly
- Enable only from trusted IP addresses

### SSL/TLS Encrypted Connection
**When to use**:
- Connecting over untrusted networks
- Public Redis Cloud instances
- Compliance requirements for data encryption

**Requirements**:
- Redis configured with TLS support
- Certificate files (if self-signed)
- Port for TLS (typically 6380)

**Configuration**:
1. Enable TLS in Redis credentials
2. Provide certificate path (if self-signed)
3. Verify certificate on connection

### Redis ACL (Access Control List) - Redis 6.0+
**Fine-grained access control**:
- Create users with specific command permissions
- Restrict keys accessible per user
- Pattern-based access: `@read`, `@write`, `@admin`

**Example**:
```
ACL SETUSER cache_user on >password +get +set ~cache:* -@all
```

### Redis Cloud / Managed Services
**AWS ElastiCache**:
- Use VPC endpoint or bastion host
- IAM authentication available
- Automatic backups and failover

**Azure Cache for Redis**:
- Access key authentication
- TLS encryption by default
- Network security configuration

**Redis Cloud (redis.com)**:
- API-based authentication
- ACL support
- Built-in high availability
</authentication>

<common_use_cases>
## Common Use Cases

### 1. Session Management and Caching
**Scenario**: Cache user session data to reduce database load
- **Typical workflow**: Webhook Trigger → Redis Get (session data) → IF (cache miss) → PostgreSQL Select → Redis Set (with 1-hour TTL) → Process request
- **Why this operation**: Reduces database queries, improves response time
- **Considerations**: TTL selection, cache invalidation, session security
- **N8N Pattern**: Use key format "session:userid:timestamp" for organization

### 2. Real-Time Rate Limiting
**Scenario**: Track API request rates and enforce limits per user
- **Typical workflow**: Webhook Trigger → Redis Increment (counter) → IF (count > limit) → Return 429 error, else process request
- **Why this operation**: Prevent API abuse, protect backend services
- **Considerations**: TTL for rolling windows, distributed rate limiting
- **N8N Pattern**: Use "apikey:requests:timestamp" keys with INCR and EXPIRE

### 3. High-Performance Counter Management
**Scenario**: Track real-time metrics (page views, downloads, clicks) without database overhead
- **Typical workflow**: Event Trigger → Redis Increment (metric:date) → Schedule Trigger (daily) → Redis Get (metrics) → PostgreSQL Insert (archive) → Redis Delete
- **Why this operation**: Atomic increments, minimal latency, ideal for high-volume events
- **Considerations**: Metric naming, archival strategy, TTL expiration
- **N8N Pattern**: "metric:type:date" format, archive daily to PostgreSQL

### 4. Task Queue Management
**Scenario**: N8N queue mode using Redis to distribute tasks across workers
- **Typical workflow**: Webhook Trigger → Queue job → Worker processes → Complete/Error
- **Why this operation**: Scales N8N horizontally, manages long-running tasks
- **Considerations**: Job timeout, retry policy, queue priority
- **N8N Pattern**: Built-in queue mode, requires Redis for multi-worker setup

### 5. Pub/Sub for Real-Time Notifications
**Scenario**: Broadcast real-time updates to multiple workflow instances
- **Typical workflow**: Event source → Redis Publish → Multiple subscribers receive notification → Process independently
- **Why this operation**: Decoupled communication, real-time delivery
- **Considerations**: Subscriber availability, message loss scenarios
- **N8N Pattern**: Use Streams for durable pub/sub, Pub/Sub for real-time only

### 6. Distributed Locking
**Scenario**: Ensure only one workflow execution processes critical operation
- **Typical workflow**: Check Redis lock → IF locked, wait/retry, else acquire lock → Process critical operation → Release lock
- **Why this operation**: Prevents concurrent execution, ensures data consistency
- **Considerations**: Lock timeout, deadlock prevention, distributed clock skew
- **N8N Pattern**: Use SET with NX (only if not exists) and EX (expiration)
</common_use_cases>

<best_practices>
## Best Practices

### Performance Optimization
1. **Use appropriate data structures**: Strings for simple values, hashes for objects, sets for unique collections
   - Impact: Reduces memory usage, improves operation speed
   - N8N Implementation: Choose data type based on access patterns

2. **Implement TTL aggressively**: Set expiration for all temporary data
   - Impact: Prevents memory exhaustion, auto-cleanup
   - Example: Session data 1 hour, metrics 1 day, temporary flags 5 minutes
   - N8N Implementation: Always use TTL for cache entries

3. **Batch operations**: Use pipelining to send multiple commands together
   - Impact: Reduces round-trips, improves throughput
   - Good: SET multiple related keys in single operation
   - Bad: SET key1, then SET key2 in separate operations
   - N8N Implementation: Use Code node for multi-command operations

4. **Monitor memory usage**: Track key count and memory consumption
   - Impact: Prevents out-of-memory crashes
   - N8N Implementation: Schedule INFO command to log metrics

5. **Connection pooling**: Reuse Redis connections
   - Impact: Reduces connection overhead
   - N8N Implementation: N8N handles connection pooling automatically

### Reliability & Data Safety
1. **Implement idempotent operations**: Design for safe retry
   - Example: Use SET for idempotent updates, INCR for counters
   - Prevents inconsistency on retry

2. **Use Lua scripting for atomic operations**: When multiple steps needed
   - Ensures all-or-nothing execution
   - Example: Check value, compare, and update atomically

3. **Enable persistence**: AOF or snapshots for important data
   - AOF: Append-only file for durability
   - Snapshots: Periodic BGSAVE for recovery points

4. **Monitor Redis memory**: Set maxmemory with eviction policy
   - Prevents crashes, enables auto-cleanup
   - Recommended: allkeys-lru for caching, noeviction for queues

5. **Implement error handling**: Handle connection failures gracefully
   - Use try/catch in N8N workflows
   - Fall back to direct database queries if Redis unavailable

### Security Best Practices
1. **Use strong passwords**: Minimum 32 characters, rotate regularly
2. **Enable TLS**: Encrypt data in transit for remote connections
3. **Restrict network access**: Private subnet, firewall rules
4. **Implement Redis ACL**: Fine-grained command/key permissions (Redis 6.0+)
5. **Never store sensitive data**: PII, passwords, tokens should be encrypted
6. **Monitor access logs**: Track all client connections
7. **Use Redis Cloud**: Managed service with security built-in

### Data Hygiene
1. **Use consistent key naming**: Prefixes, separators (session:user:123)
   - Enables pattern matching, logical organization
   - Prevents key collisions

2. **Implement key expiration**: TTL for all temporary data
   - Automatic cleanup, prevents unbounded growth
   - Based on use case: 1 hour for sessions, 1 day for metrics

3. **Archive important data**: Copy to PostgreSQL periodically
   - Prevents data loss, enables long-term analysis
   - N8N Pattern: Schedule daily archive job

4. **Clean up old data**: Remove obsolete keys regularly
   - Prevents memory exhaustion
   - Use SCAN + DEL pattern for safe cleanup

5. **Version your cached data**: Include version in keys if schema changes
   - Prevents stale cache issues
   - Example: "user:v2:id:123" when schema updates

### Debugging
1. **Monitor command latency**: Track slow Redis operations
   - Enable slowlog: `slowlog get 100`
   - Review slowlog periodically
2. **Use MONITOR command**: Real-time command inspection (development only)
   - Shows all commands executing on Redis
   - Useful for debugging N8N workflows
3. **Check memory fragmentation**: Monitor `redis_memory_human` and fragmentation ratio
   - High fragmentation indicates memory issues
   - Restart Redis to defragment if needed
4. **Validate data types**: Use TYPE command to verify key data type
   - Prevents type errors in operations
5. **Test connection**: Verify Redis is reachable from N8N environment
</best_practices>

<common_errors>
## Common Errors & Troubleshooting

<error ref="err-001" http_code="E001">
**Error**: "Connection refused" or "Cannot connect to Redis"
- **Cause**: Redis server down, unreachable, or port blocked
- **N8N Context**: Node execution fails immediately when connecting
- **Fix**:
  1. Verify Redis is running: `systemctl status redis` or cloud console
  2. Check host and port: `redis-cli -h host -p port ping`
  3. Verify network connectivity: `telnet host port`
  4. Check firewall rules: Ensure port 6379 (or custom) is open
  5. For cloud Redis: Verify security groups allow N8N IP
- **Prevention**: Monitor Redis uptime, implement connection retries
</error>

<error ref="err-002" http_code="E002">
**Error**: "NOAUTH Authentication required" or "invalid password"
- **Cause**: Incorrect password or authentication not enabled
- **N8N Context**: Connection succeeds but commands fail with auth error
- **Fix**:
  1. Verify password: Check Redis requirepass configuration
  2. Test manually: `redis-cli -h host -a password ping`
  3. Check ACL (Redis 6.0+): Verify user has required permissions
  4. Update N8N credentials: Ensure password matches Redis configuration
  5. Verify no extra spaces: Passwords are case-sensitive
- **Prevention**: Use strong passwords, document credentials securely
</error>

<error ref="err-003" http_code="E003">
**Error**: "OOM command not allowed, used memory" or "out of memory"
- **Cause**: Redis running out of available memory
- **N8N Context**: Operations fail with memory-related errors
- **Fix**:
  1. Check memory usage: `INFO memory`
  2. Reduce data size: Delete old keys with `SCAN + DEL`
  3. Increase available memory: Upgrade server or enable swap
  4. Enable eviction: Set `maxmemory-policy allkeys-lru`
  5. Implement aggressive TTL: Delete old data automatically
  6. Use smaller keys: Optimize key naming and data structures
- **Prevention**: Monitor memory usage, implement TTL policies, archive data
</error>

<error ref="err-004" http_code="E004">
**Error**: "WRONGTYPE Operation against a key holding the wrong kind of value"
- **Cause**: Operating on key with wrong data type (e.g., GET on hash)
- **N8N Context**: Command executes but fails with type mismatch
- **Fix**:
  1. Check key type: `TYPE keyname`
  2. Use correct operation: GET for strings, HGET for hashes
  3. Delete and recreate key if needed: `DEL keyname`
  4. Validate data structure: Ensure consistency across workflows
  5. Update N8N operation: Use correct Redis command for data type
- **Prevention**: Use consistent data types, test operations before deploying
</error>

<error ref="err-005" http_code="E005">
**Error**: "TIMEOUT redis operation timeout" or command exceeds timeout
- **Cause**: Redis operation taking too long or server unresponsive
- **N8N Context**: Workflow execution timeout
- **Fix**:
  1. Optimize query: Large SCAN or key pattern match too slow
  2. Reduce result set: Use LIMIT, pagination
  3. Check server load: Increase timeout setting if justified
  4. Break operation into smaller pieces: Loop through results
  5. Restart Redis: May be stuck in bad state
- **Prevention**: Monitor operation latency, optimize patterns, implement pagination
</error>

<error ref="err-006" http_code="E006">
**Error**: "NOSCRIPT No matching script" or Lua script not found
- **Cause**: Lua script SHA not found on Redis server
- **N8N Context**: Code node executing Redis Lua script fails
- **Fix**:
  1. Load script first: Use SCRIPT LOAD before EVALSHA
  2. Use EVAL instead: Send script directly (slower)
  3. Verify script syntax: Test in redis-cli
  4. Check Redis persistence: Script may be lost on restart
  5. Store script in N8N environment variable
- **Prevention**: Load scripts at workflow start, use EVAL for one-off scripts
</error>

<error ref="err-007" http_code="E007">
**Error**: "BUSYKEY Target key name already exists" or key collision
- **Cause**: Operation conflicts with existing key, or race condition
- **N8N Context**: Concurrent workflows modifying same key
- **Fix**:
  1. Use unique keys: Timestamp or ID in key name
  2. Implement distributed locking: SET with NX flag
  3. Use RENAME: Atomic key rename for safety
  4. Implement retry: Exponential backoff on conflict
  5. Use transactions: MULTI/EXEC for atomic operations
- **Prevention**: Unique key design, implement locking for critical operations
</error>

<error ref="err-008" http_code="E008">
**Error**: "MOVED 9189 host:port" or cluster redirection
- **Cause**: Using Redis Cluster without proper cluster awareness
- **N8N Context**: Cluster mode enabled but N8N not configured for it
- **Fix**:
  1. Enable cluster mode in Redis credentials (if available)
  2. Use all cluster endpoints: Connect to any node, gets redirected automatically
  3. Use Redis Proxy: HAProxy or similar to abstract cluster
  4. Use single-node mode: If not requiring cluster
- **Prevention**: Verify Redis setup (cluster vs standalone), configure N8N accordingly
</error>

### Performance Issues
- **Slow SCAN operations**: Use COUNT parameter, reduce key count, implement pagination
- **High latency**: Check network, Redis server load, use connection pooling
- **Memory growth**: Implement TTL for all keys, monitor with INFO, enable eviction policy

### Pub/Sub Issues
- **Messages lost**: Subscribers not connected when published; use Streams for persistence
- **No message delivery**: Verify subscribers active, check channel name spelling
- **High latency**: Too many subscribers, network issues, use Streams instead

### Data Consistency Issues
- **Stale cache**: Implement cache invalidation strategy, refresh on updates
- **Partial updates**: Use Lua scripting for atomic multi-step operations
- **Data loss on restart**: Enable persistence (AOF or snapshots)
</common_errors>

<related_operations>
## Related Data Nodes

### Complementary Databases
- **PostgreSQL**: For durable, queryable data; use Redis as cache layer
- **MongoDB**: For document storage; combine with Redis for hot data
- **SQLite**: For embedded data; less suitable for N8N workflows

### Common Supporting Nodes
- **Set (Edit Fields)**: Format data before storing in Redis
- **Code Node**: Implement Lua scripting for complex operations
- **Schedule Trigger**: Periodic cache refresh, metrics archival
- **Loop Over Items**: Batch process Redis keys
- **Webhook Trigger**: Real-time event handling with Redis

### Workflow Patterns
1. **Cache-Aside Pattern**: Check Redis → DB miss → Fetch → Store in Redis
2. **Write-Through Pattern**: Update both Redis and DB for consistency
3. **Event Notification**: Publish events to Redis channel for subscribers
4. **Rate Limiting**: Increment counter, check threshold, enforce limits
5. **Distributed Lock**: Acquire lock with SET NX, process, release

### See Also
- **Queue Mode**: Use Redis for N8N horizontal scaling
- **Session Storage**: Cache user sessions for reduced database load
- **Real-Time Analytics**: Use Redis for high-frequency metric updates
- **Message Queue**: Combine with PostgreSQL for durable queuing
</related_operations>

<troubleshooting>
## Troubleshooting Guide

### Connection Issues

**Problem**: "Connection refused" repeatedly
- **Check**: Redis status, host/port configuration, network connectivity
- **Solution**:
  1. Verify server: `systemctl status redis-server` or cloud console
  2. Test connectivity: `redis-cli -h host -p 6379 ping`
  3. Check firewall: `sudo ufw status` or security groups
  4. Verify N8N can reach Redis: SSH to N8N server, test from there
  5. Check Redis config: Verify `bind` setting allows connections
  6. Enable remote access: `bind 0.0.0.0` if needed (behind firewall)
- **N8N Tools**:
  - Test connection in Redis credentials
  - Check N8N execution logs
  - Verify network configuration

**Problem**: Intermittent connection timeouts
- **Check**: Redis server load, network latency, connection pool
- **Solution**:
  1. Monitor Redis: `INFO stats` for client connections
  2. Increase timeout: Configure in Redis credentials
  3. Check server resources: CPU, memory, disk I/O
  4. Enable slow query log: `slowlog len`, `slowlog get 10`
  5. Optimize queries: Use SCAN instead of KEYS
  6. Scale up: Upgrade Redis or use cluster
- **N8N Tools**:
  - Monitor execution time trends
  - Log connection timing
  - Implement automatic retries

### Data Issues

**Problem**: Data lost after Redis restart
- **Check**: Persistence configuration, memory policy
- **Solution**:
  1. Enable persistence: Add to redis.conf:
     ```
     appendonly yes
     appendfsync everysec
     save 900 1
     ```
  2. Verify AOF: Check `/var/lib/redis/appendonly.aof` exists
  3. Monitor rewrite: Large AOF files trigger rewrite
  4. Backup data: Copy RDB files to backup storage
  5. Use Redis Cloud: Automatic replication and backup
- **N8N Tools**:
  - Archive critical data to PostgreSQL
  - Schedule backup workflows
  - Monitor Redis persistence

**Problem**: Memory constantly growing
- **Check**: TTL settings, eviction policy, key count
- **Solution**:
  1. Monitor memory: `INFO memory` regularly
  2. Set max memory: `config set maxmemory 2gb`
  3. Set eviction: `config set maxmemory-policy allkeys-lru`
  4. Audit keys: `SCAN 0 | wc -l` to count
  5. Review TTLs: `TTL keyname` for keys without expiration
  6. Archive data: Move old data to PostgreSQL
  7. Enable DEBUG OBJECT: Analyze large keys
- **N8N Tools**:
  - Schedule INFO command to log metrics
  - Create alerts for memory threshold
  - Implement auto-archive workflows

### Performance Issues

**Problem**: Slow SCAN operations
- **Check**: Key count, query pattern, Redis configuration
- **Solution**:
  1. Count keys: `DBSIZE`
  2. Use pagination: Process results in batches
  3. Optimize patterns: More specific match patterns reduce scan time
  4. Use SCAN instead of KEYS: Non-blocking iteration
  5. Implement cursor: SCAN returns cursor for continuation
  6. Archive old data: Reduce active key count
- **N8N Tools**:
  - Split SCAN into scheduled jobs
  - Implement resumable pagination
  - Use Code node for complex filtering

**Problem**: High latency on basic operations
- **Check**: Network latency, Redis server load, command complexity
- **Solution**:
  1. Check latency: Use Redis client benchmarking
  2. Monitor server: `INFO stats` for ops/sec
  3. Check network: Ping latency, MTU size
  4. Simplify operations: Reduce command complexity
  5. Use connection pooling: Reuse connections
  6. Upgrade infrastructure: Faster network, better CPU/memory
- **N8N Tools**:
  - Monitor execution metrics
  - Log operation timing
  - Test under load before deployment

### Pub/Sub Issues

**Problem**: Messages not being received
- **Check**: Subscriber status, channel name, publish timing
- **Solution**:
  1. Verify subscribers: `PUBSUB CHANNELS`
  2. Check messages: `PUBSUB NUMSUB channel` shows subscriber count
  3. Verify publishing: Use `redis-cli PUBLISH` to test
  4. Check channel name: Exact match required (case-sensitive)
  5. Use Streams for persistence: Pub/Sub loses messages without subscribers
- **N8N Tools**:
  - Log publish/subscribe events
  - Implement fallback: Use Streams if message loss occurs
  - Monitor channel activity

**Problem**: Message delivery delays
- **Check**: Subscriber workload, Redis server capacity
- **Solution**:
  1. Reduce subscriber load: Distribute processing
  2. Use multiple channels: Separate message streams
  3. Implement batching: Group messages before processing
  4. Monitor queue: Check `COMMAND INFO` for command latency
- **N8N Tools**:
  - Implement multi-worker setup
  - Use queue mode for scaling
  - Monitor message latency

### Security Issues

**Problem**: Unauthorized access detected
- **Check**: Authentication configuration, network access
- **Solution**:
  1. Enable authentication: Require password
  2. Implement ACL: Fine-grained access control (Redis 6.0+)
  3. Restrict network: Private subnet, firewall rules
  4. Change password: Rotate regularly
  5. Monitor connections: `CLIENT LIST` shows active connections
  6. Review logs: Check for failed auth attempts
- **N8N Tools**:
  - Monitor connection logs
  - Implement access alerts
  - Audit credentials usage

**Problem**: Data exposure in logs
- **Check**: Command logging configuration
- **Solution**:
  1. Disable command logging: `loglevel notice` or `warning`
  2. Encrypt logs: Store logs with encryption
  3. Sanitize logs: Remove sensitive data
  4. Restrict log access: Filesystem permissions
  5. Use Redis ACL: Audit command execution
- **N8N Tools**:
  - Avoid logging passwords/tokens
  - Use N8N credential system for sensitive values
  - Enable transaction logging for audit trail
</troubleshooting>

---

**Documentation Status**: ✅ **COMPLETE & PRODUCTION-READY**
**Last Updated**: 2025-10-31
**Next Steps**: Combine with PostgreSQL for complete data management strategy