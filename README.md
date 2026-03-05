# FriendsOfShopware Agent Skills

Agent Skills to help developers using AI agents with Shopware.

Built on the [Agent Skills Open Standard](https://agentskills.io/).

## Installation

### Agent Skills CLI

```bash
npx skills add FriendsOfShopware/agent-skills
```

### Claude Code Plugin

```bash
/plugin marketplace add FriendsOfShopware/agent-skills
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [shopware-phpunit](skills/shopware-phpunit/) | Best practices for writing PHPUnit tests in Shopware 6 projects |
| [shopware-admin-crud-module](skills/shopware-admin-crud-module/) | Creates a standalone CRUD administration module for a Shopware DAL entity |

## Structure

```
skills/
  {skill-name}/
    SKILL.md            # Skill manifest (required)
    AGENTS.md           # Generated navigation guide for agents
    CLAUDE.md           # Symlink to AGENTS.md
    references/         # Detailed reference documents
      _sections.md      # Category definitions
      _template.md      # Template for new references
      {prefix}-{name}.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
