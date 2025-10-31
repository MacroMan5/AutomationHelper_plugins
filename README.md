# Automation Helper - Claude Code Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.com/code)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-orange)](https://github.com/therouxe/automation-helper/releases)
[![Status](https://img.shields.io/badge/status-in%20development-yellow)]()

> **AI assistant for Power Automate and n8n workflows** - Help design, build, debug, and refactor automation workflows with Claude Code.

⚠️ **Alpha Version** - Skills in active development. Power Automate and n8n focus. Make/Zapier not yet supported.

## What This Plugin Does

This plugin adds 6 AI skills to Claude Code that help you work with automation workflows:

1. **Design** workflows through conversation (brainstorm)
2. **Generate** workflow JSON from requirements (build-flow)
3. **Debug** errors with documentation research (debugger)
4. **Fix** common errors quickly (quick-fix)
5. **Refactor** workflows for performance (refactor)
6. **Validate** before deployment (validator)

### What's Actually Complete

✅ **Power Automate (Partial)**
- Forms connector (100%)
- Excel connector (100%)
- Outlook connector (100%)
- Teams connector (100%)
- Built-in actions (100%)
- SharePoint (20% - needs work)
- OneDrive (20% - needs work)

✅ **n8n (Core + Database)**
- Core nodes (HTTP, Webhook, Code, Schedule, Set, IF - 6/15 nodes)
- AI nodes (OpenAI - 1/10 nodes)
- App integrations (Google Sheets, Drive, Gmail - 3/300 nodes)
- Database nodes (PostgreSQL, Redis, Pinecone - 3/10 nodes)

❌ **Not Yet Supported**
- Make/Integromat
- Zapier
- Advanced n8n nodes
- Custom slash commands
- Workflow hooks

## Installation

```bash
# Add marketplace
/plugin marketplace add MacroMan5/automation-helper

# Install plugin
/plugin install automation-helper
```

## Quick Example

```
You: "I'm getting a 429 error in my Excel flow"

→ automation-quick-fix or automation-debugger activates
  - Searches documentation
  - Finds rate limit (100 calls/60s)
  - Suggests adding delays
  - Outputs fixed JSON
  - or provides quick fix suggestions
```

## How It Works

**Documentation-Driven**: Skills search real documentation in `Docs/` folder (100+ files) to avoid hallucinations.

**Multi-Phase Approach**: Each skill follows a structured process: analyze → research → design → generate → validate.

**No Placeholders**: Generated JSON is complete and ready to paste into your platform.

## What's In Development

🚧 **Active Development**
- All 6 skills (working but improving)
- Power Automate SharePoint & OneDrive docs (20% → 100%)
- More n8n node coverage
- Better error detection

📋 **Planned Features**
- Make/Integromat support
- Zapier support
- Custom slash commands
- Workflow validation hooks
- More connector documentation

## Current Limitations

**Be Aware:**
- Make and Zapier are NOT supported yet
- Skills are in alpha - expect rough edges
- Some Power Automate connectors incomplete
- n8n coverage is basic (core nodes only)
- No custom commands or hooks yet
- Documentation gaps exist

**⚠️ IMPORTANT - How to Use Effectively:**

❌ **Don't do this:**
- Send a 3000-line workflow JSON and expect perfect results
- Ask to "fix everything" in a complex flow
- Expect it to understand your entire workflow at once

✅ **Do this instead:**
- **Section your workflow** - Work on one part at a time
- **Focus on specific issues** - Debug one error at a time
- **Provide context** - Explain what the section should do
- **Keep it manageable** - Max ~200-300 lines of JSON per request

**Example:**
```
❌ Bad: "Fix this entire workflow [paste 3000 lines]"

✅ Good: "I have an error in the SharePoint loop section.
         Here's the relevant part [paste 150 lines].
         It's supposed to filter items by date but getting 429 errors."
```

**Why?** AI has context limits. Smaller, focused requests = better results.

## Contributing

**We Need Help!** 🙏

This is an open-source project in active development. Contributions welcome:

### Most Needed
- 📚 **Documentation**: Add Make, Zapier, more Power Automate connectors
- 🐛 **Bug Reports**: Test skills and report issues
- 💡 **Ideas**: Suggest improvements via Issues
- 🔧 **Code**: Fix bugs, improve skills

### How to Contribute

1. **Fork this repo**
2. **Try the plugin** and find issues
3. **Open an Issue** with what you found
4. **Submit PRs** to fix bugs or add docs

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

### 📖 Read This First!

**[BEST_PRACTICES.md](./BEST_PRACTICES.md)** - How to use this plugin effectively

**TL;DR:** Don't send 3000-line workflows. Section them into manageable chunks (200-300 lines). One problem at a time. Provide context.

## Documentation Structure

```
Docs/
├── PowerAutomateDocs/
│   ├── Forms/         ✅ Complete (100%)
│   ├── Excel/         ✅ Complete (100%)
│   ├── Outlook/       ✅ Complete (100%)
│   ├── Teams/         ✅ Complete (100%)
│   ├── SharePoint/    🚧 20% (needs expansion)
│   └── OneDrive/      🚧 20% (needs expansion)
└── N8NDocs/
    ├── Core/          ✅ Growing (6/15 = 40%)
    │   ├── HTTP Request ✅
    │   ├── Webhook ✅
    │   ├── Code ✅
    │   ├── Schedule ✅
    │   ├── Set ✅
    │   └── IF ✅
    ├── AI/            ✅ Started (1/10 = 10%)
    │   └── OpenAI ✅
    ├── Apps/          ✅ Started (3/300 = 1%)
    │   ├── Google Sheets ✅
    │   ├── Google Drive ✅
    │   └── Gmail ✅
    └── Database/      ✅ Started (3/10 = 30%)
        ├── PostgreSQL ✅
        ├── Redis ✅
        └── Pinecone ✅
```

## Skills Overview

| Skill | Status | What It Does |
|-------|--------|-------------|
| automation-brainstorm | 🚧 Alpha | Helps design workflows through questions |
| automation-build-flow | 🚧 Alpha | Generates workflow JSON from requirements |
| automation-debugger | 🚧 Alpha | Debugs errors using documentation |
| automation-quick-fix | 🚧 Alpha | Fast fixes for common errors (401, 429, etc) |
| automation-refactor | 🚧 Alpha | Optimizes workflows (reduce API calls, add error handling) |
| automation-validator | 🚧 Alpha | Validates workflows before deployment |

## Known Issues

- Documentation coverage is incomplete
- Error detection could be better
- Performance needs optimization
- Sub Agent doesnt seem to be invoked as much

**See [Issues](https://github.com/therouxe/automation-helper/issues) for full list**

## Getting Help

- **Issues**: [Report bugs](https://github.com/therouxe/automation-helper/issues)
- **Discussions**: [Ask questions](https://github.com/therouxe/automation-helper/discussions)
- **Email**: [email protected]

## Roadmap

### v0.2.0 (Next Release)
- [ ] Complete SharePoint documentation
- [ ] Complete OneDrive documentation
- [ ] Improve skill trigger accuracy
- [ ] Add more n8n nodes
- [ ] Bug fixes from community feedback

### v0.3.0
- [ ] Add Make/Integromat basic support
- [ ] Add Zapier basic support
- [ ] Improve JSON generation quality
- [ ] Add validation hooks

### v1.0.0 (Stable)
- [ ] Complete documentation for all major platforms
- [ ] Stable skills with comprehensive testing
- [ ] Custom commands support
- [ ] Workflow hooks support
- [ ] Performance optimizations

## Project Stats

- **Skills**: 6 (all in alpha)
- **Agents**: 4 sub-agents
- **Documentation**: 17 comprehensive node files (100,600+ lines)
- **N8N Nodes Documented**: 13 of 1835+ (6 Core, 1 AI, 3 App, 3 Database)
- **Documentation Coverage**: 0.7% of all N8N nodes, 74% of high-priority nodes
- **Status**: Active development
- **Contributors**: Looking for more!

## License

MIT License - Free to use, modify, fork, and distribute.

## Credits

- **Author**: MacroMan5
- **Built for**: [Claude Code](https://claude.com/code) by Anthropic
- **Inspired by**: The workflow automation community

## Support This Project

- ⭐ **Star this repo** if you find it useful
- 🐛 **Report bugs** to help improve it
- 📚 **Add documentation** for connectors you know with AI templates for quick search
- 💬 **Share feedback** on what works and what doesn't
- 🔧 **Submit PRs** to fix issues or add features

---

**Current Status**: 🚧 Alpha - In Active Development

**Honest Assessment**: This plugin works for basic Power Automate and n8n workflows, but it's not production-ready. Expect bugs, gaps, and rough edges. Your feedback and contributions are essential to making it better!

**Fork it, break it, improve it!** 🚀
