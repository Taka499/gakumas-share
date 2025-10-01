/// <reference types="vite/client" />

declare interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly VITE_DISCORD_LOGIN_PATH?: string
  readonly VITE_DISCORD_CLIENT_ID?: string
  readonly VITE_DISCORD_REDIRECT_URI?: string
  readonly VITE_AUTH_SUCCESS_PATH?: string
  readonly VITE_AUTH_ERROR_PATH?: string
}

declare interface ImportMeta {
  readonly env: ImportMetaEnv
}
