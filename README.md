# railcorp-apps

Two small Flask services used as demo workloads for a Kubernetes webhook that
migrates upstream container images to Chainguard bases.

- `ingest/` detects the MIME type of uploaded files with libmagic.
  `POST /upload` (multipart field `file`), `GET /healthz`.
- `departures/` serves a static departures board. `GET /`, `GET /healthz`.

Both are built `FROM python:3.13` on purpose: they are the "before" images.
`build.sh` builds and pushes them with the OCI source labels the migrator
follows back to this repository. `recipes/` describe how each app is built
and what its acceptance test checks. `fixtures/` are the test inputs.

Nothing here is specific to any company's infrastructure. The apps log the
Python version, user and `RAILCORP_*` environment they run with, which makes
"before and after" comparisons easy to read.
