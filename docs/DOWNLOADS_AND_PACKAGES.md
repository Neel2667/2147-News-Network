# Downloads and Production Packages

Last updated: 2026-06-16

## Purpose

The Studio app now creates downloadable files for production handoff.

## Export Current Draft

In **Save, Load & Export Center**, click:

```text
Export Current Draft
```

The app creates downloadable files under:

```text
exports/
```

Files:

```text
episode-script.txt
scene-plan.json
youtube-metadata.json
README.md
2147-production-export.zip
```

The UI displays download links for each file and the ZIP package.

## Create Video-Ready Scene Package

Click:

```text
Create Video-Ready Scene Package
```

The app creates:

```text
render_packages/{episode_id}/
  README.md
  manifest.json
  draft.json
  {episode_id}-render-package.zip
  scenes/*.html
```

The UI displays links to:

- download full render ZIP
- open/download manifest
- open/download README
- open each scene render page

## Important Persistence Note

Generated `exports/` and `render_packages/` are runtime production artifacts. They are ignored by Git and should not be committed unless intentionally archived.

On Hugging Face, runtime files may not persist permanently unless persistent storage is configured.
