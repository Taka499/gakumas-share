# Backend Development Notes

このドキュメントはバックエンド (FastAPI) 開発時の基本的な手順と運用メモをまとめたものです。

## 環境要件
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー
- MongoDB (Atlas など) ※接続設定は別途実施

## 環境変数
`backend/.env` に以下の値を設定してください。`backend/.env.example` をコピーするとスムーズです。

| 変数名 | 説明 |
| --- | --- |
| `MONGODB_URI` | MongoDB の接続文字列 |
| `MONGODB_DB` | 使用するデータベース名（未指定時は `gakumas-share`） |
| `DISCORD_CLIENT_ID` | DiscordアプリケーションのクライアントID |
| `DISCORD_CLIENT_SECRET` | Discordアプリケーションのクライアントシークレット |
| `DISCORD_REDIRECT_URI` | DiscordリダイレクトURI（例: `http://localhost:8000/api/auth/discord/callback`） |
| `JWT_SECRET_KEY` | JWT署名用シークレット（開発ではダミー値でも可） |
| `JWT_ACCESS_TOKEN_EXPIRES_IN` | JWTアクセストークンの有効期限（秒） |

## 依存関係インストール
```bash
cd backend
uv sync
```

## 開発サーバー起動
```bash
cd backend
uv run uvicorn app.main:app --reload
```

デフォルトでは `http://127.0.0.1:8000` で起動します。

- ルート: `GET /` → `{ "message": "Gakumas Share API" }`
- ヘルスチェック: `GET /health` → `{ "status": "ok", "timestamp": ... }`

## テスト実行
```bash
cd backend
uv run pytest
```

`app/tests/test_main.py` にはルートとヘルスチェックのスモークテストが含まれています。今後の機能追加に合わせてテストケースを拡張してください。

## フロントエンド環境変数
`frontend/.env` に以下の値を設定してください。`frontend/.env.example` をコピーして編集します。

| 変数名 | 説明 |
| --- | --- |
| `VITE_API_BASE_URL` | バックエンドAPIのベースURL（例: `http://localhost:8000`） |
| `VITE_DISCORD_CLIENT_ID` | DiscordクライアントID（認可URL生成に使用） |
| `VITE_DISCORD_REDIRECT_URI` | DiscordリダイレクトURI（バックエンドと同値） |

## 開発時のヒント
- ルーターは `app/routers/` に配置し、`app/main.py` でインポートして登録します。
- 非同期テストは `pytest.mark.asyncio` と `httpx.ASGITransport` を併用するとスムーズです。
- 仕様変更は `docs/MVP.md` と合わせて更新し、齟齬を防ぎましょう。
