# OpenAI Node Overview

---
type: node-overview
node_name: OpenAI
node_type: app
category: action
auth_required: true
version: 1.0
last_updated: 2025-10-31
keywords: [openai, gpt, ai, llm, chatgpt, dall-e, whisper, embeddings, chat, image-generation, transcription]
related_nodes: [Code, HTTP Request, Anthropic Claude, LangChain]
rate_limits:
  service_rate_limit: Varies by model and tier (60-10000 RPM)
  n8n_limit: none
official_docs_url: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.openai/
api_docs_url: https://platform.openai.com/docs/
npm_package: n/a (built-in app node)
---

<official_docs>
https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.openai/
https://platform.openai.com/docs/api-reference
https://platform.openai.com/docs/guides
</official_docs>

<description>
The OpenAI node integrates GPT models (GPT-4, GPT-3.5-turbo), DALL-E image generation, Whisper audio transcription, and text embeddings into N8N workflows. It enables AI-powered automation including chatbots, content generation, image creation, voice transcription, semantic search, and intelligent data processing through OpenAI's industry-leading large language models and AI capabilities.
</description>

<capabilities>
## Core Capabilities
- Chat completion with GPT-4, GPT-3.5-turbo, and other models
- Image generation with DALL-E 3 and DALL-E 2
- Audio transcription and translation with Whisper
- Text embeddings for semantic search and RAG
- Function calling for structured outputs
- Vision capabilities (image understanding with GPT-4V)
- JSON mode for structured responses

## Supported Operations
- **Chat**: Conversational AI, content generation, text analysis
- **Image Generation**: Create images from text descriptions
- **Audio Transcription**: Speech-to-text conversion
- **Audio Translation**: Translate audio to English
- **Embeddings**: Convert text to vector representations
- **Moderation**: Content moderation and safety checks
- **Edit**: Text editing and rewriting (legacy models)

## Integration Features
- **Streaming**: Real-time response streaming
- **Function Calling**: Integrate AI with APIs and databases
- **Vision**: Analyze images with GPT-4V
- **JSON Mode**: Guaranteed JSON responses
- **System Prompts**: Set AI behavior and personality
- **Temperature Control**: Creativity vs consistency tuning
- **Token Management**: Max tokens, stop sequences
- **Multi-turn Conversations**: Maintain conversation context
</capabilities>

<rate_limits>
## OpenAI API Rate Limits

**Tier-Based Limits** (varies by usage/payment)

**Free Tier**:
- GPT-3.5-turbo: 3 RPM, 200 RPD (requests per minute/day)
- GPT-4: Not available
- DALL-E: 5 images per minute

**Tier 1** ($5+ spent):
- GPT-3.5-turbo: 3,500 RPM, 200 RPD
- GPT-4: 500 RPM
- DALL-E-3: 7 images per minute

**Tier 5** (highest):
- GPT-3.5-turbo: 10,000 RPM
- GPT-4: 10,000 RPM
- DALL-E-3: 15 images per minute

**Token Limits per Request**:
- GPT-4-turbo: 128,000 tokens context
- GPT-4: 8,192 tokens context
- GPT-3.5-turbo: 16,385 tokens context
- GPT-4-vision: 128,000 tokens

**Throttling Behavior**:
- HTTP 429: Rate limit exceeded
- HTTP 503: Server overloaded (temporary)
- Automatic retry recommended with exponential backoff

## Cost Considerations

**Pricing** (as of 2025-10-31, subject to change):

**GPT-4-turbo**:
- Input: $0.01 per 1K tokens
- Output: $0.03 per 1K tokens

**GPT-3.5-turbo**:
- Input: $0.0005 per 1K tokens
- Output: $0.0015 per 1K tokens

**DALL-E-3**:
- 1024x1024: $0.040 per image
- 1024x1792 / 1792x1024: $0.080 per image

**Whisper**:
- $0.006 per minute

**Embeddings (text-embedding-3-small)**:
- $0.00002 per 1K tokens

## N8N Platform Limits
- No N8N-imposed limits
- Rate limits are from OpenAI API
- Consider workflow execution timeout
- Large context may cause memory issues
</rate_limits>

<critical_limitations>
## Model Availability

<limitation id="lim-001" severity="high">
**API Key Tier Restrictions**: Access to models depends on API key tier

- **Impact**: GPT-4 and advanced features require paid tier
- **Scope**: Model selection
- **Workaround**: Upgrade OpenAI account tier, use GPT-3.5 for development
- **Affected Operations**: Chat with GPT-4, advanced vision

**Example Scenario**: Free tier API key cannot use GPT-4 models
</limitation>

## Token Limitations

<limitation id="lim-002" severity="critical">
**Context Window Limits**: Each model has maximum token limit

- **Impact**: Long conversations or documents truncated
- **Scope**: All chat operations
- **Workaround**: Summarize earlier context, use models with larger windows (GPT-4-turbo: 128K)
- **Affected Operations**: Long conversations, document analysis

**Example Scenario**: Analyzing 200-page document exceeds even GPT-4-turbo's 128K token limit
</limitation>

<limitation id="lim-003" severity="medium">
**Output Token Limit**: Response length capped by max_tokens parameter

- **Impact**: Long outputs truncated mid-sentence
- **Scope**: Content generation
- **Workaround**: Set appropriate max_tokens, request continuation if truncated
- **Affected Operations**: Long-form content generation

**Example Scenario**: Requesting blog post but max_tokens too low, article cuts off
</limitation>

## Response Limitations

<limitation id="lim-004" severity="high">
**Non-Deterministic**: Same prompt may produce different outputs

- **Impact**: Inconsistent results, difficult to debug
- **Scope**: All AI operations
- **Workaround**: Set temperature=0 for consistency, use JSON mode for structured data
- **Affected Operations**: All chat and completion operations

**Example Scenario**: Data extraction produces different field names on each run
</limitation>

<limitation id="lim-005" severity="medium">
**Knowledge Cutoff**: Training data ends at specific date (GPT-4: April 2023)

- **Impact**: No knowledge of recent events
- **Scope**: Information retrieval
- **Workaround**: Provide current information in prompts, use web search integration
- **Affected Operations**: Current events, recent technology

**Example Scenario**: Asking about 2024 events returns "I don't have information after April 2023"
</limitation>

## Image Generation Limitations

<limitation id="lim-006" severity="medium">
**DALL-E Content Policy**: Strict content restrictions

- **Impact**: Rejected prompts for faces of public figures, violent content, etc.
- **Scope**: Image generation
- **Workaround**: Rephrase prompts, avoid restricted content
- **Affected Operations**: Image generation

**Example Scenario**: Cannot generate images of specific celebrities or copyrighted characters
</limitation>

<limitation id="lim-007" severity="low">
**Image Size Restrictions**: Limited resolution options

- **Impact**: Cannot generate custom sizes
- **Scope**: DALL-E operations
- **Workaround**: Generate at available size, resize post-generation
- **Affected Operations**: Image generation
- **Available Sizes**: 1024x1024, 1024x1792, 1792x1024 (DALL-E-3)

**Example Scenario**: Need 800x600 image, must generate 1024x1024 and resize
</limitation>

## Audio Limitations

<limitation id="lim-008" severity="medium">
**Audio File Size Limit**: 25 MB maximum for Whisper

- **Impact**: Long recordings must be split
- **Scope**: Audio transcription
- **Workaround**: Split audio files, process in chunks
- **Affected Operations**: Whisper transcription

**Example Scenario**: 1-hour meeting recording exceeds limit, needs splitting
</limitation>
</critical_limitations>

<authentication>
## Authentication Method

### API Key Authentication (Required)
- **Type**: Bearer token in Authorization header
- **How to Obtain**:
  1. Create account at https://platform.openai.com/
  2. Navigate to API Keys section
  3. Click "Create new secret key"
  4. Copy key (shown only once)
  5. Store securely

### N8N Credential Configuration

1. Go to **Credentials** in N8N
2. Click **Add Credential**
3. Select **OpenAI API**
4. Enter **API Key**
5. (Optional) Set **Organization ID** if using multiple orgs
6. **Test** connection
7. **Save**

### Required Scopes/Permissions

OpenAI API keys have full access to:
- All models available to your tier
- All operations (chat, images, audio, embeddings)
- Usage billing (pay-per-use)

### Security Best Practices

1. **Never Hardcode**: Use N8N credential store
2. **Rotate Keys**: Change keys periodically
3. **Monitor Usage**: Check OpenAI dashboard for unexpected usage
4. **Set Budgets**: Configure spending limits in OpenAI account
5. **Restrict by IP**: Use OpenAI's IP allowlist feature if available

## Troubleshooting Authentication

- **401 Unauthorized**: Invalid API key, regenerate
- **403 Forbidden**: Model not available on your tier, upgrade account
- **Invalid Organization**: Check Organization ID in credentials
</authentication>

<common_use_cases>
## 1. AI Chatbot / Customer Support

**Description**: Build intelligent chatbot for customer inquiries

**Typical Workflow**:
```
Webhook → OpenAI (Chat) → Respond to Webhook
```

**Configuration**:
- **Model**: gpt-3.5-turbo (fast, cost-effective) or gpt-4 (higher quality)
- **System Prompt**: "You are a helpful customer support agent for [Company]. Be professional, friendly, and concise."
- **Messages**: User message from webhook
- **Temperature**: 0.7 (balanced)
- **Max Tokens**: 500

**Best For**: Customer support, FAQ bots, interactive assistants

---

## 2. Content Generation

**Description**: Generate blog posts, product descriptions, marketing copy

**Typical Workflow**:
```
Manual Trigger / Schedule → OpenAI (Chat) → Format → Google Docs / CMS
```

**Configuration**:
- **Model**: gpt-4 (higher quality content)
- **System Prompt**: "You are an expert content writer specializing in [topic]. Write engaging, SEO-optimized content."
- **User Prompt**: "Write a 500-word blog post about [topic]"
- **Temperature**: 0.8 (more creative)
- **Max Tokens**: 2000

**Best For**: Blogs, marketing, social media, product descriptions

---

## 3. Data Extraction and Structuring

**Description**: Extract structured data from unstructured text

**Typical Workflow**:
```
Email / Webhook → OpenAI (Chat with JSON mode) → Database
```

**Configuration**:
- **Model**: gpt-3.5-turbo or gpt-4
- **System Prompt**: "Extract structured data from the following text and return as JSON with fields: name, email, phone, company, message"
- **Response Format**: JSON mode enabled
- **Temperature**: 0 (consistent)
- **Max Tokens**: 500

**Example Output**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "company": "Acme Corp",
  "message": "Interested in pricing"
}
```

**Best For**: Form processing, email parsing, invoice extraction, resume parsing

---

## 4. Image Generation for Marketing

**Description**: Create marketing visuals, social media images

**Typical Workflow**:
```
Schedule / Manual → OpenAI (Image Generation) → Download → Social Media APIs
```

**Configuration**:
- **Model**: dall-e-3
- **Prompt**: "A modern, professional illustration of [concept] in minimalist style with blue and white colors"
- **Size**: 1024x1024 or 1792x1024 (landscape)
- **Quality**: hd (for better quality)
- **Style**: vivid or natural

**Best For**: Social media graphics, blog images, product mockups, concept art

---

## 5. Meeting Transcription and Summarization

**Description**: Transcribe audio recordings and generate summaries

**Typical Workflow**:
```
Webhook (audio upload) → OpenAI (Whisper) → OpenAI (Chat - summarize) → Email / Database
```

**Whisper Configuration**:
- **Operation**: Transcribe Audio
- **Model**: whisper-1
- **Language**: auto-detect or specify
- **Response Format**: text or verbose_json

**Chat Summarization**:
- **Model**: gpt-4
- **System Prompt**: "Summarize the following meeting transcript. Include key points, decisions, and action items."
- **User Prompt**: [Transcript from Whisper]

**Best For**: Meeting notes, podcast transcripts, interview processing

---

## 6. Semantic Search and RAG

**Description**: Build semantic search using embeddings

**Typical Workflow**:
```
Document Upload → Split → OpenAI (Embeddings) → Vector DB

User Query → OpenAI (Embeddings) → Vector Search → OpenAI (Chat with context) → Response
```

**Embeddings Configuration**:
- **Model**: text-embedding-3-small (cost-effective) or text-embedding-3-large (higher quality)
- **Input**: Document chunks or query text

**Chat with Context**:
- **Model**: gpt-4
- **System Prompt**: "Answer questions based only on the provided context"
- **User Prompt**: [Context from vector search] + [User question]

**Best For**: Document Q&A, knowledge bases, semantic search, chatbots with custom knowledge

</common_use_cases>

<best_practices>
## Prompt Engineering

### System Prompts
1. **Be Specific About Role**: Define AI's expertise and style
   - **Good**: "You are a technical support engineer specializing in Linux systems"
   - **Bad**: "You help with tech"

2. **Set Boundaries**: Specify what AI should/shouldn't do
   - **Example**: "If you don't know the answer, say 'I don't have that information' instead of guessing"

3. **Define Output Format**: Specify desired structure
   - **Example**: "Always respond in this format: 1. Summary (one sentence), 2. Details (bullet points), 3. Recommendations"

### User Prompts
1. **Provide Context**: Give necessary background information
   - **Good**: "Company: Acme Corp, Industry: SaaS, Question: How can we reduce churn?"
   - **Bad**: "How reduce churn?"

2. **Use Examples** (Few-Shot Learning): Show desired output format
   ```
   Extract name and email:
   Example: "John Doe (john@example.com)" → {"name": "John Doe", "email": "john@example.com"}

   Now extract from: "Jane Smith (jane.smith@company.com)"
   ```

3. **Break Complex Tasks**: Chain multiple calls for complex operations
   - Instead of: "Analyze this document and create a presentation"
   - Use: Call 1: Analyze, Call 2: Create outline, Call 3: Generate slides

## Cost Optimization

### Model Selection
1. **Use GPT-3.5 When Possible**: 20x cheaper than GPT-4
   - **GPT-3.5**: Simple tasks, high-volume, real-time
   - **GPT-4**: Complex reasoning, accuracy critical, low-volume

2. **Test with Cheaper Models First**: Validate workflow logic
   - Develop with GPT-3.5-turbo
   - Upgrade to GPT-4 only if needed

### Token Management
1. **Set Appropriate max_tokens**: Don't waste tokens
   - Short answers: 100-300 tokens
   - Summaries: 300-500 tokens
   - Long content: 1000-2000 tokens

2. **Manage Context Length**: Trim conversation history
   - Keep only recent N messages
   - Summarize old context instead of including full text

3. **Use Embeddings for Search**: Cheaper than querying GPT-4 multiple times
   - Embed once, search many times
   - Only send relevant context to GPT-4

## Quality and Reliability

### Temperature Settings
- **0**: Deterministic, consistent (data extraction, structured outputs)
- **0.7**: Balanced (general chat, customer support)
- **1.0**: Creative (content generation, brainstorming)
- **1.5-2**: Highly creative, less coherent (experimental)

### JSON Mode
1. **Enable for Structured Data**: Guaranteed valid JSON
   - **Use**: Data extraction, API responses, structured outputs
   - **Prompt**: Include "return JSON" in instructions

2. **Validate Schema**: Check structure matches expectations
   - Use Code node to validate returned JSON
   - Handle missing fields gracefully

### Function Calling
1. **Use for Tool Integration**: Connect AI to APIs/databases
   - **Example**: "Get weather for location X" → AI returns function call → Execute HTTP Request → Return result to AI

2. **Define Clear Functions**: Precise descriptions and parameters
   - **Function Description**: "Get current weather for a given location"
   - **Parameters**: location (string, required), units (string, optional: celsius/fahrenheit)

## Error Handling

### Retry Logic
1. **Implement Exponential Backoff**: For rate limits (429)
   - Retry after 1s, 2s, 4s, 8s
   - Max 5 retries

2. **Handle Timeouts**: Large context may timeout
   - Reduce input length
   - Split into smaller requests

3. **Catch Specific Errors**:
   - 429: Rate limit → Retry with backoff
   - 503: Server error → Retry immediately (2-3 times)
   - 400: Bad request → Fix prompt, don't retry
   - 401: Auth error → Check API key

### Output Validation
1. **Always Validate AI Output**: Don't trust blindly
   - Check for expected format
   - Validate data types
   - Handle "I don't know" responses

2. **Add Fallbacks**: Handle unexpected responses
   - Default values for missing data
   - Error messages for invalid outputs
   - Human review for critical decisions

## Security and Safety

### Content Moderation
1. **Use Moderation Endpoint**: Check user input for harmful content
   - **Before**: Chat → Moderate input → If safe → Process
   - **Categories**: hate, sexual, violence, self-harm

2. **Implement Rate Limiting**: Prevent abuse
   - Limit requests per user/IP
   - Track usage patterns

### Data Privacy
1. **Don't Send PII**: OpenAI may use data for training (opt-out available)
   - Anonymize personal information
   - Use data processing agreement if handling sensitive data

2. **Redact Sensitive Info**: Before sending to OpenAI
   - Remove credit cards, SSN, passwords
   - Use placeholders, restore after

### API Key Security
1. **Rotate Keys Regularly**: Monthly or quarterly
2. **Monitor Usage**: Set alerts for unexpected spikes
3. **Use Separate Keys**: Development vs production
</best_practices>

<troubleshooting>
## Common Errors

### Rate Limit Exceeded (429)

<error id="err-429" http_code="429">
- **Symptom**: "Rate limit exceeded" error
- **Cause**: Too many requests for API key tier
- **Immediate Fix**:
  1. Implement retry with exponential backoff
  2. Add delay between requests in workflow
  3. Upgrade OpenAI tier for higher limits
  4. Use batching to reduce request count
- **Prevention**:
  - Check tier limits before deployment
  - Implement rate limiting in workflow
  - Monitor usage dashboard
- **N8N Setting**: Enable retry with backoff in HTTP Request options
</error>

### Insufficient Quota (429 with billing message)

<error id="err-quota" http_code="429">
- **Symptom**: "You exceeded your current quota"
- **Cause**: Spending limit reached or payment method failed
- **Immediate Fix**:
  1. Check OpenAI billing dashboard
  2. Add payment method or increase limit
  3. Wait for monthly reset (free tier)
- **Prevention**:
  - Set up payment method
  - Configure spending alerts
  - Monitor costs regularly
- **OpenAI Dashboard**: https://platform.openai.com/account/billing
</error>

### Model Not Found / Access Denied (404/403)

<error id="err-403" http_code="403|404">
- **Symptom**: "Model 'gpt-4' does not exist" or access denied
- **Cause**: Model not available for API key tier
- **Immediate Fix**:
  1. Check model name spelling
  2. Verify tier has access to model
  3. Use gpt-3.5-turbo instead
  4. Upgrade account tier
- **Prevention**:
  - Verify model availability for tier
  - Use fallback models
  - Test with available models first
- **Model Check**: https://platform.openai.com/docs/models
</error>

### Context Length Exceeded (400)

<error id="err-context" http_code="400">
- **Symptom**: "This model's maximum context length is X tokens"
- **Cause**: Input + requested output exceeds model's token limit
- **Immediate Fix**:
  1. Reduce input text length
  2. Decrease max_tokens parameter
  3. Use model with larger context (GPT-4-turbo: 128K)
  4. Summarize earlier context
- **Prevention**:
  - Estimate tokens before sending (1 token ≈ 4 characters)
  - Trim conversation history
  - Use embeddings for large documents
- **Token Counter**: https://platform.openai.com/tokenizer
</error>

### Invalid API Key (401)

<error id="err-401" http_code="401">
- **Symptom**: "Incorrect API key provided"
- **Cause**: Wrong key, deleted key, typo
- **Immediate Fix**:
  1. Verify API key in N8N credentials
  2. Generate new key in OpenAI dashboard
  3. Update N8N credentials
  4. Test connection
- **Prevention**:
  - Store key securely
  - Use environment variables
  - Don't share keys
- **N8N**: Update OpenAI credential, test connection
</error>

### Empty or Invalid Response

<error id="err-empty" http_code="200">
- **Symptom**: Successful request but empty/unexpected response
- **Cause**: Model refused request (content policy), max_tokens too low
- **Immediate Fix**:
  1. Check if content violates policies
  2. Increase max_tokens
  3. Rephrase prompt
  4. Check response in execution log
- **Prevention**:
  - Follow OpenAI usage policies
  - Set reasonable max_tokens
  - Validate prompts
- **Content Policy**: https://openai.com/policies/usage-policies
</error>

## Diagnostic Steps

1. **Check API Key**
   - Verify key is valid in OpenAI dashboard
   - Test with curl or Postman
   - Check organization ID if applicable

2. **Review Error Message**
   - Read full error text
   - Check HTTP status code
   - Look for specific error code

3. **Verify Model Availability**
   - Check tier has access to model
   - Verify model name spelling
   - Test with gpt-3.5-turbo

4. **Monitor Usage**
   - Check OpenAI usage dashboard
   - Review recent API calls
   - Check rate limit status

5. **Test Incrementally**
   - Start with simple prompt
   - Add complexity gradually
   - Isolate problematic component

6. **Check N8N Execution Log**
   - View full request/response
   - Check input data format
   - Review node configuration
</troubleshooting>

<related_docs>
## Documentation Structure

- **Model Specifications**: https://platform.openai.com/docs/models
- **API Reference**: https://platform.openai.com/docs/api-reference
- **Pricing**: https://openai.com/pricing

## Related Nodes

- **[Code](../Core/code.md)** - Process AI responses, build complex prompts
- **[HTTP Request](../Core/http-request.md)** - Direct OpenAI API access
- **Anthropic Claude** - Alternative LLM provider
- **LangChain** - Advanced AI workflows, agents, RAG

## External Resources

- **Official OpenAI Docs**: https://platform.openai.com/docs/
- **OpenAI Cookbook**: https://cookbook.openai.com/
- **N8N Community**: https://community.n8n.io/tag/openai
- **Prompt Engineering Guide**: https://www.promptingguide.ai/
</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Completeness**: 95% (All major operations documented)
- **Validation Status**: Validated against OpenAI API docs
- **Next Review**: 2025-12-31 (update for new models/pricing)
- **N8N Version**: Compatible with all recent versions
- **OpenAI API Version**: Latest (v1)
</metadata_summary>
