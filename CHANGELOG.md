# Changelog

This project follows a lightweight changelog policy for structural and infra changes.

Whenever a commit introduces a structural change (examples below), update this file with a short entry describing:
- What changed (concise)
- Why it changed (short rationale)
- Files/areas affected (list)
- Migration steps (if any)

Structural change examples (must be recorded):
- Adding or removing major services (Express, FastAPI, MLflow, Ollama integrations)
- Major refactors that change APIs or folder layout (moving/renaming folders such as `backend-expressjs/`, `modelserver-fastapi/`)
- Adding or removing DB schemas or migrations
- Changing build or deployment configuration (Vite, Docker, CI, MLflow tracking server)

Template (copy and paste per entry)

## [YYYY-MM-DD] — Short summary of change

- What: One-line description of the structural change.
- Why: Brief rationale.
- Affected: `path/to/file1`, `path/to/folder/*`.
- Migration: Steps to apply (if needed). Example: `run npm install && REBUILD_DB=true node scripts/populate.js`.

Examples

## [2025-10-23] — Add responsive frontend + ad placeholders

- What: Added `frontend-react` responsive components (Home, MovieDetails, MovieList, MovieCard) and `AdPlaceholder` components.
- Why: Provide mobile-first UI and prepare ad-slot integration for Google ad products.
- Affected: `frontend-react/src/pages/*`, `frontend-react/src/components/*`, `frontend-react/package.json`.
- Migration: `cd frontend-react && npm install` then `npm run dev`. Provide `VITE_API_BASE` env var if Express runs on non-default host.

Notes
- Keep entries short and focused.
- For non-structural changes (content tweaks, minor CSS), use commit messages only; only structural changes require the Changelog entry.

## [2025-10-23] — Remove Ads feature; add search and chat proxy

- What: Removed active ad rendering from frontend (AdPlaceholder now no-op); added `Search` and `Chat` frontend UIs. Added an Express `/search` proxy and a FastAPI `/search` endpoint to perform RAG retrieval. The Express server remains the main API proxy to FastAPI for chat/search/recommendations.
- Why: Focus on core features (movie chat, search, recommender) and simplify current UI for development. Ads are disabled until a later multi-agent integration is ready.
- Affected: `frontend-react/src/components/*` (Chat, Search), `frontend-react/src/pages/*` (Home, MovieDetails), `backend-expressjs/app.js`, `modelserver-fastapi/main.py`.
- Migration: `cd frontend-react && npm install && npm run dev` and ensure FastAPI and Express are running. No DB migrations.

