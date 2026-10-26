# Doggirlx video frame gallery

This repository generates a static gallery page for each video, with 30 sampled JPG frames. Frame images and gallery pages are committed under `frames/<database-id>-<video-name>/` and published with GitHub Pages.

PostgreSQL stores the relative repository path in `doggirlx.frames_path`, not a full public URL. The public URL can be reconstructed as:

`https://hems5683.github.io/special-umbrella-doggirlx/` + `frames_path`

## Setup

1. In **Settings → Secrets and variables → Actions**, add:
   - `DATABASE_URL`: connection URL for the PostgreSQL database containing table `doggirlx`.
   - `VIDEO_SIGNING_SECRET`: the same secret used to sign `b2/` video URLs. Required only when rows use `b2/` paths.
   - `FRAME_WORKFLOW_TOKEN`: a fine-grained GitHub token with Actions read/write and Contents read permissions, so the workflow can trigger the next batch.
2. In **Settings → Pages**, set the build and deployment source to **GitHub Actions**.
3. Run **Actions → Generate video frames → Run workflow**.

The database should contain these tracking columns: `frames_path`, `frames_status`, `frames_attempts`, `frames_error`, and `frames_generated_at`. The workflow does not alter the table schema. Run the SQL migration supplied with the setup before starting the workflow.

Each run processes up to 30 videos and extracts 30 frames at evenly spaced points between the start and end. The workflow also runs every six hours and retries failures up to five times.

Full HTTP(S) `video_src` values are used as-is. Bare filenames are resolved against `media2.doggirlx.com`; `b2/` values are signed using `VIDEO_SIGNING_SECRET`.

## Troubleshooting

- `frames_status = 'done'` means the gallery exists in the deployed Pages site.
- `frames_status = 'error'` records the last error in `frames_error`; check the GitHub Actions log for more context.
- `frames_path` records the relative path such as `frames/402-example-video/`.
- Do not commit database URLs or signing secrets to source files.
