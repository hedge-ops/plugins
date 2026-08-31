# People Work Plugin Marketplace

This repository publishes the official People Work plugin for Codex and
Claude Code.

The plugin is intentionally thin: it contains metadata, artwork, and MCP
configuration, but no People Work executable. It requires the People Work app
installed on your computer with Agent Mode turned on. The plugin then starts
the app's local MCP server with `people mcp`.

The plugin and application have independent versions. Update this repository
only when the plugin metadata, presentation, or `people mcp` invocation
contract changes; ordinary People Work releases do not republish the plugin.

## Release

Plugin releases follow semantic versioning independently of the People Work
application. For each release:

1. Add the user-visible changes to [`CHANGELOG.md`](./CHANGELOG.md).
2. Set the same new version in the Codex and Claude plugin manifests.
3. Run `python3 scripts/validate.py`.
4. Commit and tag the release as `v<version>`.

Claude Code can notify users when an enabled marketplace installs a new plugin
version. Codex users refresh the marketplace with
`codex plugin marketplace upgrade hedge-ops`.

## Install

### Codex

```sh
codex plugin marketplace add hedge-ops/plugins --ref main
```

### Claude Code

```sh
claude plugin marketplace add hedge-ops/plugins
```

## Licensing

This repository and its packaged software are proprietary. Public availability
does not grant an open-source license. Downloading, installing, caching,
updating, running, and redistribution are governed by the included
[People Work Proprietary Software License](./LICENSE).
