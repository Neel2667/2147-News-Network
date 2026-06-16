# Report — Download Buttons for Production Packages

Date: 2026-06-16

## What Was Built

Added download links/buttons for exported production files and render packages.

## Export Downloads

The **Export Current Draft** action now returns downloadable links for:

```text
episode-script.txt
scene-plan.json
youtube-metadata.json
README.md
2147-production-export.zip
```

The ZIP bundles the exported production files.

## Render Package Downloads

The **Create Video-Ready Scene Package** action now returns:

- full render package ZIP download
- manifest.json link
- render README link
- each standalone scene HTML render page link

## Backend Changes

- Mounted `/exports` static route.
- Render packages already served through `/renders`.
- Added ZIP creation using Python `zipfile`.
- Added ZIP output for both export packages and render packages.

## Frontend Changes

- Export Center now shows polished download links.
- Render package section now includes a full ZIP download link.

## Files Updated

```text
main.py
static/index.html
static/styles.css
static/app.js
.gitignore
docs/DOWNLOADS_AND_PACKAGES.md
```

## Note

Generated runtime folders are ignored by Git:

```text
exports/
render_packages/
```
