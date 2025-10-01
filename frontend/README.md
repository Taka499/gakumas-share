# Gakumas Share Frontend

React + TypeScript + Vite setup for the MVP UI. Tailwind CSS v4 is integrated through the official Vite plugin, and the layout includes placeholders for the upcoming memory features.

## Getting Started

```bash
cd frontend
npm install
cp .env.example .env       # Update the values as needed
npm run dev
```

### Required environment variables

| Variable | Description |
| --- | --- |
| `VITE_API_BASE_URL` | Backend origin used for API calls (e.g. `http://localhost:8000`) |
| `VITE_DISCORD_LOGIN_PATH` | Path to the login endpoint, defaults to `/api/auth/discord/login` |
| `VITE_DISCORD_CLIENT_ID` | Discord OAuth client ID (used by the future login button) |
| `VITE_DISCORD_REDIRECT_URI` | Redirect URI registered in Discord Developer Portal |
| `VITE_AUTH_SUCCESS_PATH` | SPA route to show after successful login |
| `VITE_AUTH_ERROR_PATH` | SPA route to show when login fails |

## Available Scripts

- `npm run dev` – Start Vite dev server with HMR.
- `npm run build` – Type-check and create a production build.
- `npm run preview` – Preview the production build locally.
- `npm run lint` – Run ESLint against the project.

## Project Structure

```
src/
├── components/
│   └── layout/       # Header and shell components
├── hooks/            # React hooks (e.g., session state)
├── lib/              # Environment + HTTP helpers
├── pages/            # Route-level pages
├── App.tsx           # Router definition
├── index.css         # Tailwind entrypoint and base styles
└── main.tsx          # Application bootstrap
```

## Current Status

- Header, shared layout, and routing for `/`, `/auth/success`, `/auth/error`, and `/my` are ready.
- Session verification hook (`useSession`) checks the SuperTokens session endpoint and surfaces a simple status badge.
- Memory list, post creation, and search UIs are placeholders until backend Issues #9–#11 ship.

Contributions should follow the repository’s gitflow (feature branches → PR) and keep docs in sync with backend/API progress.
