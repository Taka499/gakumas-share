# Backend Development Notes

このドキュメントはバックエンド (FastAPI) 開発時の基本的な手順と運用メモをまとめたものです。

## 環境要件
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー
- MongoDB (Atlas など) ※接続設定は別途実施

## 環境変数
`backend/.env` に以下の値を設定してください。

| 変数名 | 説明 |
| --- | --- |
| `MONGODB_URI` | MongoDB の接続文字列 |
| `MONGODB_DB` | 使用するデータベース名（未指定時は `gakumas-share`） |

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

## 開発時のヒント
- ルーターは `app/routers/` に配置し、`app/main.py` でインポートして登録します。
- 非同期テストは `pytest.mark.asyncio` と `httpx.ASGITransport` を併用するとスムーズです。
- 仕様変更は `docs/MVP.md` と合わせて更新し、齟齬を防ぎましょう。
