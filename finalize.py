import os
import re
from pathlib import Path
from urllib.parse import urlparse
from html import escape

import psycopg

REPO = "hems5683/special-umbrella-doggirlx"
SITE_BASE = f"https://{REPO.split('/')[0]}.github.io/{REPO.split('/')[1]}"


def safe_stem(source, row_id):
    source = str(source)
    name = urlparse(source).path.rsplit("/", 1)[-1] if source.startswith(("http://", "https://")) else source
    name = name.removeprefix("b2/").rsplit("/", 1)[-1]
    name = re.sub(r"\.mp4$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-_")
    return name[:100] or f"video-{row_id}"


def main():
    database_url = os.environ["DATABASE_URL"]
    with psycopg.connect(database_url, autocommit=True) as conn:
        rows = conn.execute(
            """SELECT id, video_src FROM doggirlx
               WHERE frames_status = 'generated'
                 AND COALESCE(frames_url, '') = ''"""
        ).fetchall()
        for row_id, source in rows:
            folder = Path("frames") / f"{row_id}-{safe_stem(source, row_id)}"
            if not (folder / "index.html").is_file():
                print(f"Skip id={row_id}: generated gallery folder not present in checkout")
                continue
            url = f"{SITE_BASE}/{folder.as_posix()}/"
            conn.execute(
                """UPDATE doggirlx
                   SET frames_url = %s, frames_status = 'done',
                       frames_error = NULL
                   WHERE id = %s""",
                (url, row_id),
            )
            print(f"Published gallery URL saved for id={row_id}: {url}")


if __name__ == "__main__":
    main()
