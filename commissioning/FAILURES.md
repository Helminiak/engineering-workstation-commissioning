# Failures
- Earlier restricted session could not communicate with NVIDIA driver; unrestricted session retest passes. Do not repair driver based on that obsolete result.
- gh CLI absent; authentication and remote workflow remain unverified.

- Local acceptance harness first attempt failed: installed MCP SDK exposes input_schema/is_error, not camelCase. Adapted client; no server/config change required.
