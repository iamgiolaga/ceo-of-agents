# Security policy

## Supported versions

Only the latest release gets security fixes. Update with `/plugin`, Installed tab, Update now, then apply any pending migration to your hq.

## Reporting a vulnerability

Please do not open a public issue. Report it privately through GitHub: on this repository, open the **Security** tab and choose **Report a vulnerability**. Include the plugin version, what you did, what happened and, if you can, a minimal example with placeholder names and no real secrets.

This is a small project maintained in spare time. Reports are read and answered as soon as possible, and reporters of fixed issues are credited unless they ask otherwise.

## What counts

The plugin is made of instructions, templates and settings that Claude Code agents follow. Examples of security problems here:

- an instruction or template that makes an agent expose secrets, credentials or personal data, for example by writing them into a git-tracked file;
- a way to get past an approval gate, so that an outward-facing or irreversible action runs without the user's OK;
- a generated hq that grants a department tools, connectors or permissions it was not given during setup, or that lets one organization's agents use another account's connectors;
- an `allowed-tools` entry or permission rule broader than its skill needs.

Problems in Claude Code itself go to Anthropic, not here.
