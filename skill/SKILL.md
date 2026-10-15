---
name: ferry
description: Move files between this machine and a home server with `ferry` (send, get, ls), sha256-verified. Use when asked to send, copy, or upload files to the server, pull results back from it, or hand the user a file produced on the server.
---

# ferry

`ferry` copies files over SSH to the host in `$FERRY_HOST` (default: the `homelab` SSH alias), with resume, retries, and a sha256 check of every file. Only the client starts a transfer; the server never connects back.

Run `command -v ferry`. If it finds ferry, follow "On the client"; otherwise you are on the server, so follow "On the server".

## On the client

1. Send: `ferry send <local paths...> [-t <remote dir>]`. Default destination: `~/Ferry` on the server.
2. Get: `ferry get <remote paths...> [-t <local dir>]`. Default destination: the current directory.
3. List: `ferry ls [remote dir]`.

Remote paths: relative ones resolve under `~/Ferry`; use `~/...` or an absolute path for anywhere else.

Transfers run at the speed of the link, so run anything large in the background rather than under a tool timeout.

Done when ferry exits 0 and prints `sha256 verified`. The indented lines after it are where each item landed; report those paths.

On exit 1, read the `ferry:` error line:
- `rerun the same command to resume`: rerun it once. Partial files pick up where they stopped.
- `ssh <host> failed`: the server is unreachable or refused the key. Run `ssh -o BatchMode=yes "${FERRY_HOST:-homelab}" true` and report its error to the user.
- `sha256 mismatch after retry`: the source changed mid-transfer. Wait for whatever is writing it to finish, then rerun.
- `no such file` / `no such remote file`: fix the path; `ferry ls` shows `~/Ferry`.

A folder lands inside the destination (`ferry send dir -t X` gives `X/dir`). Same-named files are overwritten and folders merge; ferry never deletes, so remove remote files over `ssh`. Use git, not ferry, for repositories.

## On the server

To hand the user a file, write it under a temp name in `~/Ferry/`, `mv` it to its final name so a half-written file is never fetched, then tell the user to run `ferry get <name>` on the client.
