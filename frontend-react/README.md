# Frontend (React) — Movie Explorer

This is a responsive React frontend (Vite) for the Movie Explorer app. It is mobile-first and prepared to work with the existing backend services:

- Express.js API: `http://127.0.0.1:3000` (movie data, proxy to FastAPI)
- FastAPI: `http://127.0.0.1:8000` (recommendations, chat)
- MLflow/Ollama/Chroma: used on server-side (no direct client access required)

Key features added:

- Movie list grid (responsive) and movie details page
- Recommendation trigger (client calls Express `/recommend` which proxies to FastAPI)
- Chat-ready UX (the client will call `/chat` proxy)

Run locally

1. Install dependencies

```bash
cd frontend-react
npm install
```

2. Provide environment variables

Copy the example env and edit if needed:

```bash
cp .env.example .env
# edit .env to set VITE_API_BASE if your Express server runs on a different host
```

3. Start dev server

```bash
npm run dev
```

Notes on running

- Vite reads env vars prefixed with `VITE_` at build time. The frontend defaults to `http://127.0.0.1:3000` if you don't set `VITE_API_BASE`.
- If you still have problems starting the dev server, run `npm run dev` and paste the error here and I will help fix it.

Next steps (optional)

- Add a Chat UI wrapper that streams tokens for nicer UX.
- Add tests (React Testing Library) and e2e smoke tests that hit the Express endpoints (mock if needed).
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
