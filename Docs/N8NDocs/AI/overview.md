# N8N AI Nodes Overview

---
type: category-overview
category: AI Nodes
node_count: 10+
version: 1.0
last_updated: 2025-10-31
keywords: [ai, llm, openai, anthropic, langchain, machine-learning, gpt, embeddings, agents]
official_docs_url: https://docs.n8n.io/integrations/builtin/cluster-nodes/
---

<description>
AI nodes integrate large language models (LLMs) and machine learning capabilities into N8N workflows. These nodes enable intelligent automation through natural language processing, image generation, speech recognition, semantic search, and AI agents. Primary providers include OpenAI (GPT-4, DALL-E), Anthropic (Claude), and the LangChain framework for building advanced AI applications.
</description>

<ai_categories>
## Node Categories

### Language Models (LLMs)
- **OpenAI**: GPT-4, GPT-3.5-turbo for chat and completion
- **Anthropic Claude**: Claude 3 family (Opus, Sonnet, Haiku)
- **Google PaLM / Gemini**: Google's LLMs
- **Cohere**: Commercial LLM provider
- **Hugging Face**: Open-source model hub

### Image Generation
- **OpenAI DALL-E**: Text-to-image generation
- **Stability AI**: Stable Diffusion models
- **Midjourney**: (via API when available)

### Speech and Audio
- **OpenAI Whisper**: Speech-to-text transcription
- **ElevenLabs**: Text-to-speech with voice cloning
- **Google Speech-to-Text**: Transcription service

### Embeddings and Search
- **OpenAI Embeddings**: Vector representations for semantic search
- **Cohere Embeddings**: Alternative embedding models
- **Pinecone**: Vector database for similarity search
- **Qdrant**: Open-source vector database

### AI Frameworks
- **LangChain**: 70+ nodes for building AI applications
- **AI Agent**: Autonomous AI agents with tool use
- **Vector Store**: Store and query embeddings
- **Document Loaders**: Ingest various document formats
</ai_categories>

<node_listing>
## Available AI Nodes

### [OpenAI](./openai.md) ⭐ Most Popular
**Purpose**: Access GPT models, DALL-E, Whisper, and embeddings

**Key Features**:
- GPT-4 and GPT-3.5-turbo for chat
- DALL-E 3 for image generation
- Whisper for audio transcription
- Embeddings for semantic search
- Function calling and JSON mode
- Vision capabilities (GPT-4V)

**Use Cases**:
- Chatbots and customer support
- Content generation
- Data extraction
- Image creation
- Meeting transcription
- Semantic search

**Pricing**: Pay-per-use (tokens/images)
**Complexity**: Low-Medium

---

### Anthropic Claude
**Purpose**: Claude 3 family LLMs (Opus, Sonnet, Haiku)

**Key Features**:
- 200K token context window
- Strong reasoning capabilities
- Longer conversations than GPT-4
- Vision capabilities
- Lower cost than GPT-4 (Sonnet/Haiku)

**Use Cases**:
- Long document analysis
- Complex reasoning tasks
- Research and summarization
- Code generation

**Pricing**: Pay-per-use, varies by model
**Complexity**: Low-Medium

**Documentation**: Coming soon

---

### LangChain Integration ⭐ Advanced
**Purpose**: Build complex AI applications with 70+ nodes

**Key Features**:
- AI agents with tool use
- RAG (Retrieval Augmented Generation)
- Memory management
- Chain multiple LLM calls
- Vector database integration
- Document processing

**Use Cases**:
- AI chatbots with custom knowledge
- Autonomous agents
- Document Q&A systems
- Multi-step AI workflows

**Pricing**: Depends on underlying LLM + vector DB
**Complexity**: High

**Documentation**: Coming soon

---

### AI Agent
**Purpose**: Create autonomous AI agents

**Key Features**:
- Tool/function calling
- Multi-step reasoning
- Memory across turns
- Integrate with APIs
- Decision making

**Use Cases**:
- Research assistants
- Task automation
- Data gathering
- Complex workflows

**Complexity**: High

**Documentation**: Coming soon

---

### Vector Store Nodes
**Purpose**: Store and query embeddings for semantic search

**Available Providers**:
- Pinecone (managed vector DB)
- Qdrant (open-source)
- Weaviate (open-source)
- Chroma (open-source)
- Supabase (Postgres + pgvector)

**Use Cases**:
- Semantic search
- RAG systems
- Similarity matching
- Content recommendations

**Complexity**: Medium

**Documentation**: Coming soon

</node_listing>

<getting_started>
## Getting Started with AI Nodes

### Prerequisites
1. **API Keys**: OpenAI, Anthropic, or other provider accounts
2. **Understanding**: Basic prompt engineering concepts
3. **Budget**: AI APIs are pay-per-use (can accumulate costs)

### Essential Nodes for Beginners
1. **OpenAI (Chat)**: Start with GPT-3.5-turbo for simple AI interactions
2. **Set Node**: Format prompts and parse responses
3. **Code Node**: Process AI outputs, build complex prompts
4. **IF Node**: Route based on AI responses

### Recommended Learning Path
1. **Simple Chat**: Build basic chatbot with OpenAI
2. **Data Extraction**: Use JSON mode to extract structured data
3. **Content Generation**: Generate text content
4. **Image Generation**: Create images with DALL-E
5. **Embeddings**: Implement semantic search
6. **RAG System**: Build Q&A with custom knowledge (LangChain)

### Common Patterns

**Pattern 1: Simple Chatbot**
```
Webhook → OpenAI (Chat) → Respond to Webhook
```

**Pattern 2: Data Extraction**
```
Email/Form → OpenAI (JSON mode) → Parse → Database
```

**Pattern 3: Content Generation**
```
Schedule → OpenAI (Chat) → Format → Post to Social Media
```

**Pattern 4: Semantic Search (RAG)**
```
Query: User Question → OpenAI (Embeddings) → Vector Search → OpenAI (Chat with context) → Response
Index: Documents → Split → OpenAI (Embeddings) → Vector DB
```

**Pattern 5: AI Agent**
```
Trigger → AI Agent → [Calls tools as needed] → Final Response
Tools: Database Query, HTTP Request, Calculator, etc.
```
</getting_started>

<best_practices>
## General AI Best Practices

### Cost Management
1. **Start with Cheaper Models**: GPT-3.5 before GPT-4
2. **Set Max Tokens**: Limit response length
3. **Cache When Possible**: Store AI responses
4. **Use Embeddings Once**: Generate embeddings once, search many times
5. **Monitor Usage**: Track API costs daily

### Quality and Reliability
1. **Set Temperature Appropriately**:
   - 0: Deterministic (data extraction)
   - 0.7: Balanced (chat)
   - 1.0+: Creative (content generation)

2. **Provide Context**: Give AI necessary information
3. **Use System Prompts**: Define behavior and constraints
4. **Validate Outputs**: Don't trust AI blindly
5. **Handle Errors**: Implement retry logic and fallbacks

### Prompt Engineering
1. **Be Specific**: Clear, detailed instructions
2. **Provide Examples**: Show desired output format
3. **Use Structured Formats**: JSON mode for structured data
4. **Set Boundaries**: Tell AI what NOT to do
5. **Iterate**: Test and refine prompts

### Security and Privacy
1. **Don't Send PII**: Anonymize personal data
2. **Implement Moderation**: Check inputs for harmful content
3. **Rate Limit**: Prevent abuse
4. **Monitor Usage**: Detect unusual patterns
5. **Secure API Keys**: Use N8N credential store

## Model Selection Guide

### When to Use GPT-3.5-turbo
- Simple tasks (Q&A, basic chat)
- High volume / real-time requirements
- Cost-sensitive applications
- Development and testing

**Cost**: ~$0.001 per request (simple query)

### When to Use GPT-4
- Complex reasoning
- Accuracy critical
- Code generation
- Advanced analysis
- Professional content

**Cost**: ~$0.03 per request (similar query)

### When to Use Claude (Anthropic)
- Long documents (200K context)
- Detailed analysis
- Less cost than GPT-4 (Sonnet)
- Constitutional AI (safer)

**Cost**: Varies by model (Haiku < Sonnet < Opus)

### When to Use Embeddings
- Semantic search
- Similarity matching
- RAG (Retrieval Augmented Generation)
- Content recommendations
- Not for generating text

**Cost**: Very cheap (~$0.00002 per 1K tokens)

## Common Patterns Explained

### RAG (Retrieval Augmented Generation)
**Purpose**: Give AI access to custom knowledge

**How it Works**:
1. Split documents into chunks
2. Generate embeddings for each chunk
3. Store in vector database
4. When user asks question:
   - Generate embedding for question
   - Search for similar chunks
   - Send relevant chunks + question to LLM
   - LLM answers based on context

**Use Cases**: Document Q&A, knowledge bases, support bots

### Function Calling
**Purpose**: Connect AI to tools (APIs, databases)

**How it Works**:
1. Define available functions/tools
2. AI decides which function to call
3. Execute function with AI-provided parameters
4. Return result to AI
5. AI incorporates result in response

**Use Cases**: AI agents, tool integration, structured outputs

### Multi-Turn Conversations
**Purpose**: Maintain conversation context

**How it Works**:
1. Store conversation history
2. Send recent messages with each request
3. AI maintains context across turns
4. Trim old messages to stay within limits

**Use Cases**: Chatbots, assistants, interviews

## Troubleshooting AI Nodes

### Common Issues

**Issue**: AI responses inconsistent
- **Solution**: Lower temperature (0-0.3), use JSON mode, add more examples

**Issue**: Context too long error
- **Solution**: Summarize earlier context, use model with larger window, trim history

**Issue**: Unexpected costs
- **Solution**: Set max_tokens, monitor usage, use cheaper models, cache responses

**Issue**: AI refuses to answer
- **Solution**: Rephrase prompt, check content policies, adjust system prompt

**Issue**: Slow responses
- **Solution**: Use faster model (GPT-3.5), enable streaming, optimize prompt length

**Issue**: Rate limited
- **Solution**: Implement retry logic, upgrade tier, reduce request frequency

</best_practices>

<comparison>
## AI Provider Comparison

| Feature | OpenAI GPT-4 | OpenAI GPT-3.5 | Claude 3 Opus | Claude 3 Sonnet |
|---------|--------------|----------------|---------------|-----------------|
| **Context** | 128K tokens | 16K tokens | 200K tokens | 200K tokens |
| **Cost (Input)** | $0.01/1K | $0.0005/1K | $0.015/1K | $0.003/1K |
| **Cost (Output)** | $0.03/1K | $0.0015/1K | $0.075/1K | $0.015/1K |
| **Speed** | Medium | Fast | Slow | Fast |
| **Quality** | Excellent | Good | Excellent | Very Good |
| **Code Gen** | Excellent | Good | Excellent | Very Good |
| **Reasoning** | Excellent | Good | Excellent | Very Good |
| **Best For** | Complex tasks | High volume | Long docs | Balanced |

## Use Case Recommendations

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Chatbot (Simple) | GPT-3.5-turbo | Fast, cheap, good quality |
| Chatbot (Complex) | GPT-4 or Claude Sonnet | Better reasoning |
| Content Generation | GPT-4 | Higher quality |
| Data Extraction | GPT-3.5 + JSON | Fast, structured |
| Code Generation | GPT-4 | Best for code |
| Document Analysis (short) | GPT-4 | Excellent reasoning |
| Document Analysis (long) | Claude Opus/Sonnet | 200K context |
| Real-time Chat | GPT-3.5-turbo | Fastest |
| Cost-Sensitive | GPT-3.5-turbo | Cheapest |

</comparison>

<related_docs>
## Documentation

### Individual Node Docs
- **[OpenAI](./openai.md)** - GPT, DALL-E, Whisper, Embeddings
- **Anthropic Claude** - Coming soon
- **LangChain** - Coming soon
- **AI Agent** - Coming soon

### External Resources
- **OpenAI Docs**: https://platform.openai.com/docs/
- **Anthropic Docs**: https://docs.anthropic.com/
- **LangChain Docs**: https://docs.langchain.com/
- **Prompt Engineering Guide**: https://www.promptingguide.ai/

## Related Categories
- **[Core Nodes](../Core/overview.md)** - Code, HTTP Request, Set for AI workflows
- **[Database Nodes](../Database/overview.md)** - Store AI responses and embeddings
- **[App Nodes](../Apps/overview.md)** - Integrate AI with external services

</related_docs>

<metadata_summary>
## Document Information

- **Last Updated**: 2025-10-31
- **Version**: 1.0
- **Documented Nodes**: 1/10+ (10% complete)
- **Priority Nodes Remaining**: Claude, LangChain, AI Agent
- **Next Review**: 2025-12-15
</metadata_summary>
