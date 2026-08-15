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

CI also rejects credential-shaped assignments, private Notion or Lark document
URLs, opaque page IDs, signed media URLs, personal machine paths, and known
local identities in public text artifacts. Golden examples use only public
paper sources and stable repository assets.

Real-platform smoke tests must use clearly marked temporary pages or documents.
Read-back logs and pull requests may record capability names, block counts, and
pass/fail status, but must redact page/document IDs, URLs, account names,
workspace schemas, and signed media locations. Move the temporary artifact to
trash after verification.

Public documentation screenshots exclude visible account, recorder, comment,
and avatar metadata by default. Such display metadata may remain only after
the owner explicitly approves publication. Private URLs, page/document IDs,
workspace schemas, credentials, tokens, and authentication data are never
covered by that exception.
