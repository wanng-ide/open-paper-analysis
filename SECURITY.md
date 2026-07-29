# Security Policy

## Report a vulnerability

Do not open a public issue containing credentials, tokens, private database
identifiers, personal paths, or exploit details.

Use the repository Security tab and select **Report a vulnerability** to open a
private report with the maintainers:

https://github.com/wanng-ide/open-paper-analysis/security/advisories/new

If a real credential was exposed, revoke or rotate it before reporting. Include
the affected file or commit and the minimum information needed to reproduce
the issue, but do not paste a still-valid secret into the report.

## Repository controls

This repository uses GitHub secret scanning, push protection, and a full-history
Gitleaks check in continuous integration. Local Notion configuration and common
credential file formats are excluded from version control.
