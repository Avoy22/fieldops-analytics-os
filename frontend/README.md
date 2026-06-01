# FieldOps Analytics OS React Dashboard

This folder contains the React TypeScript dashboard for FieldOps Analytics OS. It is a static Vite app that reads exported JSON from `public/data/`.

## React Dashboard

The React dashboard does not use a backend or API yet. Vercel serves the app as static files, and the dashboard loads:

- `public/data/dashboard-data.json`
- `public/data/metadata.json`

Keep both JSON files committed so the deployed dashboard has data available at build and runtime.

## Export Data

Run the exporter from the repository root after regenerating or refreshing the Python/SQLite analytics data:

```bash
python -m src.export_react_data
```

The exporter writes the static dashboard payloads to:

```text
frontend/public/data/dashboard-data.json
frontend/public/data/metadata.json
```

Do not ignore `frontend/public/data/`; Vercel needs these files.

## Run Locally

Install frontend dependencies from this folder:

```bash
npm install
```

Start the local Vite dev server:

```bash
npm run dev
```

## Build

Create a production build:

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

The build output is generated in `dist/`. This folder should stay ignored because Vercel builds it during deployment.

## Vercel Deployment Settings

Use these settings when importing the GitHub repository into Vercel:

```text
Root Directory: frontend
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
```

No backend, API route, or serverless function is required for v1.1.
