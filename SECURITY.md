# Security notes

- Local web apps bind to 127.0.0.1 by default; no accounts or authentication are included. Do not expose them to the internet as-is.
- Host checks, origin validation, JSON mutation headers and body limits reduce local browser abuse. They are not a replacement for authentication, TLS or a production server.
- Browser clients use textContent for user-generated strings. SQL data values use placeholders; no shell/eval execution of job payloads occurs.
- SQLite files, .env and runtime logs are ignored by git. Never commit real secrets or customer datasets.
- Optional RAG live mode sends selected excerpts to the configured OpenAI model. Review data and consent before using it. Retrieved-text instructions are treated as untrusted, but no perfect prompt-injection defense is claimed.
- Container Guard is a heuristic policy linter, not a CVE/vulnerability scanner.
- Durable jobs have at-least-once semantics and a 30-second lease. Only safe short operations are included. For external side effects, implement durable idempotency and lease renewal first.
- No malicious URL fetching, arbitrary filesystem reads, arbitrary shell jobs or kubectl mutations are implemented.

For public deployment, add authentication/authorization, request throttling, HTTPS, secret management, migrations, audit retention, monitoring and an independent security review.
