# Deployment Guide

このドキュメントでは Railway (バックエンド) と Vercel (フロントエンド) を用いたデプロイ手順の概要をまとめます。

## 1. 前提
- リポジトリにアクセスできる GitHub アカウント
- Railway / Vercel アカウント
- MongoDB Atlas などで稼働している MongoDB クラスタ

環境変数は `backend/.env.example` と `frontend/.env.example` を参照して準備してください。

## 2. Railway (FastAPI バックエンド)
1. Railway に新規プロジェクトを作成し、GitHub リポジトリを接続する。
2. サービス作成後、**Variables** に以下を登録する。
   - `MONGODB_URI`
   - `MONGODB_DB`
   - `DISCORD_CLIENT_ID`
   - `DISCORD_CLIENT_SECRET`
   - `DISCORD_REDIRECT_URI`
   - `JWT_SECRET_KEY`
   - `JWT_ACCESS_TOKEN_EXPIRES_IN`
3. `backend/railway.json` がデフォルトのビルド/デプロイ設定を提供する。
4. デプロイ後、`/health` エンドポイントで稼働状況を確認する。

## 3. Vercel (React フロントエンド)
1. Vercel で新しいプロジェクトを作成し、`frontend` ディレクトリをルートとして設定する。
2. **Environment Variables** に以下を設定する。
   - `VITE_API_BASE_URL` (Railway バックエンドの公開URL)
   - `VITE_DISCORD_CLIENT_ID`
   - `VITE_DISCORD_REDIRECT_URI`
3. `frontend/vercel.json` によって SPA 用のリライトルールが適用される。
4. デプロイ後、トップページが表示されることを確認する。

## 4. リリースチェックリスト
- [ ] バックエンド `/health` で `status: ok` が返る
- [ ] Discord OAuth2 のリダイレクトURIが Discord Developer Portal に登録済み
- [ ] フロントエンドから API 基盤 URL が参照できる (`VITE_API_BASE_URL`)
- [ ] MongoDB のネットワークアクセス設定で Railway ホストを許可済み
- [ ] 必要に応じて HTTPS / カスタムドメイン設定を行う

## 5. 継続的デプロイ
- GitHub の `main` ブランチにマージされると Railway / Vercel で自動デプロイが走る設定を推奨。
- 検証用にステージング環境が必要な場合は、それぞれのプラットフォームで環境を分け、`.env` の値を管理する。

