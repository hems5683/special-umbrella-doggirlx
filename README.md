# Doggirlx video frame gallery

This repository generates a static page for each video with 30 sampled JPG frames, publishes the pages using GitHub Pages, and stores each page URL in `doggirlx.frames_url`.

## Setup

1. In **Settings → Secrets and variables → Actions**, add:
   - `DATABASE_URL`: connection URL for the PostgreSQL database containing table `doggirlx`.
   - `VIDEO_SIGNING_SECRET`: the same secret used to sign `b2/` video URLs. Required only when rows use `b2/` paths.
2. In **Settings → Pages**, set the build and deployment source to **GitHub Actions**.
3. Run **Actions → Generate video frames → Run workflow**.

The workflow adds `frames_url TEXT` and `frames_status TEXT` if they do not exist. It processes up to 30 rows per run where `frames_url` is empty, samples 30 frames at evenly spaced points between the start and end, and creates pages under `frames/<database-id>-<video-name>/`. It also runs every six hours.

Full HTTP(S) `video_src` values are used as-is. Bare filenames are resolved against `media2.doggirlx.com`; `b2/` values are signed using `VIDEO_SIGNING_SECRET`.

## Notes

- Do not commit database URLs or signing secrets to source files.
- Generated frames are published as static repository-site assets. Check repository storage and bandwidth if processing a large library.
- Failed rows receive a descriptive `frames_status` error and can be retried by clearing `frames_url` and running the workflow again.
