import grp
import logging
import os
import platform
import pwd
import sys

from flask import Flask, request
from waitress import serve

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("ingest")

# A known file for the startup self-check: the first bytes of a PDF.
SAMPLE = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
SAMPLE_TYPE = "application/pdf"

app = Flask(__name__)


def lookup_name(lookup, id_):
    try:
        return lookup(id_)[0]
    except KeyError:
        return "(no entry)"


def log_runtime():
    """Log the Python, who we run as and the app's own environment, which an image's config can set."""
    # In a venv, sys.executable is the venv's symlink; realpath is the image's interpreter behind it.
    log.info(
        "python %s at %s (%s)",
        platform.python_version(),
        sys.executable,
        os.path.realpath(sys.executable),
    )
    uid, gid = os.getuid(), os.getgid()
    log.info(
        "running as user %s (uid %d), group %s (gid %d)",
        lookup_name(pwd.getpwuid, uid),
        uid,
        lookup_name(grp.getgrgid, gid),
        gid,
    )
    settings = {
        k: v for k, v in sorted(os.environ.items()) if k.startswith("RAILCORP_")
    }
    if not settings:
        log.info("environment: no RAILCORP_* variables set")
    for name, value in settings.items():
        log.info("environment: %s=%s", name, value)


def self_check():
    """Identify a known sample, so a missing libmagic or magic database stops the service now, not on the first upload."""
    log.info("self-check: identifying a sample %s with libmagic", SAMPLE_TYPE)
    try:
        import magic

        detected = magic.from_buffer(SAMPLE, mime=True)
    except Exception as e:  # noqa: BLE001 -- any failure here means the service can't do its job
        # MagicException carries libmagic's own message, as bytes.
        message = getattr(e, "message", e)
        if isinstance(message, bytes):
            message = message.decode(errors="replace")
        log.error("self-check failed: %s: %s", type(e).__name__, message)
        sys.exit(1)
    if detected != SAMPLE_TYPE:
        log.error(
            "self-check failed: sample detected as %s, expected %s",
            detected,
            SAMPLE_TYPE,
        )
        sys.exit(1)
    version = magic.version()
    log.info("self-check passed: libmagic %d.%02d", version // 100, version % 100)


@app.post("/upload")
def upload():
    import magic

    file = request.files["file"]
    detected = magic.from_buffer(file.read(2048), mime=True)
    log.info("%s detected as %s", file.filename, detected)
    return {"filename": file.filename, "detected": detected}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    log_runtime()
    self_check()
    port = int(os.environ.get("PORT", "8080"))
    log.info("listening on port %d", port)
    serve(app, host="0.0.0.0", port=port)
