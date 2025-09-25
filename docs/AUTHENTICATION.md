# Authentication & Session Specification (MVP)

このドキュメントでは、Discord OAuth2 を入口としたログイン導線と、SuperTokens を用いたセッション／トークン戦略を定義します。Issue #3, #7 の実装指針となります。

## 全体像

1. フロントエンドは Authlib で構成したバックエンドの `/api/auth/discord/login` にリダイレクトし、Discord の Authorization Code フローを開始する。
2. Back: `/api/auth/discord/callback` でアクセストークン／ユーザー情報を取得し、`UserRepository` を介してユーザーを登録／更新する。
3. Back: SuperTokens の `create_new_session` を呼び出し、セッション情報を生成する（アクセストークン／リフレッシュトークン／Anti-CSRF トークン）。
4. Back: SuperTokens の返却値に従ってレスポンスヘッダー／Cookie をセットし、アクセストークンはレスポンスボディに返さない（HttpOnly Cookie のみで管理）。
5. Front: SuperTokens の Frontend SDK（もしくは fetch での Cookie 同送）によってアクセストークンを自動的に更新。API 呼び出しは `Authorization: Bearer <token>` を付与。

## セッション／トークン設定

| 項目 | 値 | 備考 |
| --- | --- | --- |
| アクセストークン有効期限 | SuperTokens デフォルト（5分） | SDK設定値に準拠 |
| リフレッシュトークン有効期限（スライディング） | SuperTokens デフォルト（約30日） | SDK設定値に準拠 |
| リフレッシュ絶対期限 | 未設定（将来拡張） | SuperTokens の sliding window を利用 |
| 再利用（トークン盗難）検知 | 有効 | SuperTokens のデフォルトローテーションを利用 |
| Anti-CSRF | 有効 | Cookie 運用のため `enableAntiCsrf` を true |
| Cookie SameSite | `lax` | SPA + OAuth コールバックを許容 |
| Cookie Secure | 本番 true / ローカル false | HTTPS 前提かどうかで切替 |

### セッションメタデータ

SuperTokens の session data / access token payload を活用し、最低限以下を格納します。

- `provider`: `discord`
- `provider_account_id`: Discord ユーザーID
- `username`: 表示名
- `avatar_url`: サムネイルURL（任意）

これらは SuperTokens の access token payload に入り、API ハンドラで `session.get_access_token_payload()` から参照できます。ユーザーID (`sub`) は SuperTokens が自動で設定します。

### 端末別セッション管理

SuperTokens はセッションごとに `sessionHandle` が割り当てられるため、MongoDB 側で個別に台帳を持たずとも、SuperTokens のダッシュボード / API から単一セッション失効が可能です。必要に応じて以下のメタデータを追加し、今後の拡張に備えます。

- `device`（User-Agent などから推測）
- `ip_address`

メタデータ更新は `session.update_session_data` で行います。

## 必要な環境変数

`backend/.env.example` へ以下を追加済み（SuperTokens Self-Hosted 前提）。マネージド（SupterTokens Managed Service）を利用する場合は該当URLを指定します。

| 変数名 | 説明 |
| --- | --- |
| `SUPERTOKENS_CORE_URL` | SuperTokens Core のエンドポイント例: `http://127.0.0.1:3567` |
| `SUPERTOKENS_CORE_API_KEY` | Core にアクセスするための API Key（有効化していない場合は不要） |

## フロー詳細

1. `/api/auth/discord/login`
   - Authlib で Discord 認可URLを生成
   - Starlette の `SessionMiddleware` で `state` をブラウザCookieに保存
2. `/api/auth/discord/callback`
   - Authlib で Discord アクセストークン取得
   - Discord API からユーザー情報を取得（`/users/@me`）
   - `UserRepository.get_by_provider_account` でユーザー検索、存在しなければ作成
   - `supertokens_python.recipe.session.create_new_session` でセッション生成
   - レスポンス: SuperTokensが提供する`set-cookie`ヘッダをそのまま返却。フロントには成功レスポンス（例: 200 + ユーザープロフィール）を返す。
3. `/auth/refresh`
   - SuperTokens の `/session/refresh` 標準ルートを利用（FastAPI ミドルウェアでの自動化が可能）
   - アクセストークン再発行／リフレッシュローテーション／盗難検知に対応
4. `/auth/logout`
   - `session.revoke_session` を呼び、セッションを失効

## 実装メモ

- FastAPI 側では `supertokens_python` の FastAPI ミドルウェアを適用し、保護されたエンドポイントに `@verify_session()` デコレータを付与する。
- 認証済みリクエストでは `session.get_user_id()` でMongoDB上のユーザーIDを直接取得可能。
- フロントエンドでは SuperTokens Frontend SDK (例: `supertokens-auth-react`) を採用すると、Cookieハンドリングと自動リフレッシュが容易になる。
- Discord OAuth の `redirect_uri` はバックエンドのコールバックURLと一致させ、フロントからは `/api/auth/discord/login` へのリンクを提供するだけで良い。

## テスト方針

- **セッション生成**: `/api/auth/discord/callback` でユーザー作成／更新→`create_new_session` 呼び出し→`Set-Cookie` ヘッダーが返却されることを httpx + SuperTokens のモックで検証する。
- **トークンローテーション**: SuperTokens の `/auth/session/refresh` を利用した際に新しいアクセストークン／リフレッシュトークンが払い出されること、盗難検知時の 401 応答を確認する。
- **クッキー属性**: `cookie_secure` / `same_site` 設定が環境に応じて切り替わることを設定値テストで確認する。
- **端末別失効**: `session.revoke_session` や Management API を利用してセッションを失効させた際、保護エンドポイントが 401 を返すことを確認する。

## 今後の拡張

- 端末別失効をユーザー設定画面から行いたい場合は、SuperTokens の Management API を呼び、ユーザーのセッション一覧を取得して個別失効するUIを追加する。
- 通知やログ監査が必要になったときは、SuperTokens の webhook / event API を利用して、セッション作成／破棄をログに記録する。
