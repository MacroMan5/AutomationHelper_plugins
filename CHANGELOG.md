# Changelog

All notable changes to Automation Helper will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.2.0
- Complete SharePoint documentation (currently 20%)
- Complete OneDrive documentation (currently 20%)
- Improve skill trigger accuracy
- Add more n8n node documentation
- Bug fixes from community feedback

### Planned for v0.3.0
- Make/Integromat basic support
- Zapier basic support
- Improve JSON generation quality
- Add validation hooks

### Planned for v1.0.0 (Stable)
- Complete documentation for major platforms
- Stable skills with comprehensive testing
- Custom commands support
- Workflow hooks support
- Performance optimizations

## [0.1.0-alpha] - 2025-10-31

### Added
- Initial public alpha release
- 6 specialized skills for automation workflows:
  - `automation-brainstorm` - Interactive workflow design advisor
  - `automation-build-flow` - Complete workflow JSON generator
  - `automation-debugger` - Deep error analysis with fix generation
  - `automation-quick-fix` - Fast fixes for common error patterns (401, 403, 429)
  - `automation-refactor` - Workflow optimization & best practices application
  - `automation-validator` - Pre-deployment validation & quality checks
- 4 specialized sub-agents:
  - `flow-builder` - Generates workflow JSON
  - `docs-researcher` - Searches documentation
  - `flow-debugger` - Debugs workflows
  - `flow-documenter` - Creates workflow documentation
- Power Automate documentation (partial):
  - Forms connector (100%)
  - Excel connector (100%)
  - Outlook connector (100%)
  - Teams connector (100%)
  - Built-in actions (100%)
  - SharePoint (20%)
  - OneDrive (20%)
- n8n documentation (basic):
  - Core nodes (HTTP, Webhook, Code, Schedule)
  - AI nodes (OpenAI, Anthropic)
  - App integrations (basic)
  - Database nodes (basic)
- Documentation-driven approach (no hallucinations)
- Agent-optimized documentation format (XML + YAML)
- GitHub Actions for validation and releases
- MIT License

### Known Issues
- Skills may trigger incorrectly in some contexts
- Generated JSON may need manual tweaks
- Documentation coverage incomplete for some connectors
- Error detection could be improved
- Performance needs optimization

### Limitations
- Make/Integromat not yet supported
- Zapier not yet supported
- Advanced n8n nodes not documented
- No custom slash commands yet
- No workflow hooks yet
- SharePoint & OneDrive documentation incomplete (20%)

### Notes
- This is an **alpha release** - expect bugs and rough edges
- Plugin is in active development
- Contributions, issues, and feedback are welcome!
- Focus is on Power Automate and n8n core functionality

## [0.0.1] - 2025-10-30

### Added
- Initial development version (not publicly released)
- Basic skill structure
- Initial documentation format

---

## Legend

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security vulnerability fixes

## Version Numbering

- **Major** (1.0.0): Breaking changes, major features
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes, backward compatible
- **Pre-release** (-alpha, -beta, -rc): Development versions

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to contribute to this changelog.
