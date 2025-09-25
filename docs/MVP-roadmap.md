# MVP Implementation Roadmap

学園アイドルマスターのメモリー共有サイトをMVPリリースまで進めるための実装ロードマップです。`docs/MVP.md`で定義した機能と整合した工程を扱います。

## 0. ゴールと前提
- 目標: メモリー投稿・編集・検索・共有が可能な最小構成を6週間で公開。
- スコープ: 認証、メモリーCRUD、My投稿一覧、基本検索（`stage_type` / `stage_category` / `p_idol`のANDフィルタ）。
- 制約: Python 3.11 / FastAPI / MongoDB構成、フロントは React + Vite、デプロイは Vercel + Railway。
- 参照資料: `docs/MVP.md`, `docs/gakumas-memory.md`。

## フェーズ構成

### Phase 1: Foundation（Week 1-2）
**目的**: 開発環境と認証基盤を整備し、最小のAPI・UI枠組みを用意する。
- バックエンド
  - uv プロジェクト初期化、主要ディレクトリ雛形生成。
  - MongoDB Atlas 接続設定、`users`コレクションのCRUDユーティリティ実装。
  - Discord OAuth2 + Authlib + SuperTokens でセッション発行。
  - `/api/auth/discord/login` `/api/auth/discord/callback` の実装と最小テスト。
- フロントエンド
  - Vite + React プロジェクト初期化、Tailwindセットアップ。
  - ルーティング枠 (`/`, `/auth/success`, `/auth/error`) と共通レイアウトを用意。
  - Discord OAuth リダイレクトボタンとセッション確認ロジックを実装。
- インフラ/運用
  - 環境変数管理、開発用 `.env` 整備。
  - Railway・Vercel プロジェクトの雛形作成（デプロイスクリプト確認）。
- 成果物
  - ローカルでDiscord OAuth→SuperTokensセッション取得→保護ルートアクセスまで通ること。
  - ベースUIでログイン導線とセッション確認ページが動作。

### Phase 2: Core Memory Sharing（Week 3-4）
**目的**: メモリー投稿・編集・閲覧・My投稿一覧・基本検索を完成させる。
- バックエンド
  - `MemorySets`スキーマ・バリデーション（`p_items`空配列許容、`skill_cards`必須）。
  - `/api/memories` CRUD 実装（作成・取得・更新・削除）。
  - 検索クエリ処理：`stage_type` / `stage_category` / `p_idol` の任意パラメータ AND フィルタ、`skip` / `limit` ページング、`created_at`降順、`items` + `total` レスポンス。
  - My投稿一覧向けクエリ（`user_id`フィルタ）。
  - 基本的なAPIテスト（pytest + httpx）を整備。
- フロントエンド
  - メモリー投稿・編集フォーム（同コンポーネント共用）実装。
  - 一覧カード・詳細ビュー・My投稿一覧ページ構築。
  - 検索UI（ドロップダウン / 入力フォーム）とAPI連携。
  - ドメイン参照データ（アイドル12名 + 曲名 + `stage_category`）の定数化とフォームとの連携。
- インフラ/運用
  - MongoDBインデックス適用 (`user_id`, `stage_type`+`stage_category`, `p_idol`, `created_at`)。
  - 開発用シードスクリプトまたはサンプルデータの準備。
- 成果物
  - 認証後、メモリーCRUDと検索が一通り動作。
  - UI上で一覧→詳細→編集→My投稿確認までシナリオテストが可能。

### Phase 3: Integration & Release Prep（Week 5-6）
**目的**: 仕様整合、QA、デプロイ準備を完了し初回リリースへ。
- バックエンド
  - エラーハンドリング・認可チェックの精査（投稿者のみ更新/削除）。
  - ロギング、ヘルスチェックエンドポイント整備。
- フロントエンド
  - バリデーションメッセージ、ローディング／エラーステートの強化。
  - My投稿一覧のUI改善（並び順、ページング）。
- QA/デプロイ
  - E2E動作確認リスト作成と実施。
  - Railway / Vercel への初回デプロイ、環境差異の検証。
  - README・MVP・ドメイン資料の最終同期、スクリーンショットや利用ガイドの準備（必要最小限）。
- 成果物
  - ステージング/本番 URL でMVP要件を満たす。
  - 既知の重大バグが解消され、初期ユーザーに共有可能な状態。

## 横断的ワークストリーム

### ドメインデータ整備
- `p_idol`（アイドル名 + 曲名）と `stage_category` の対応表を定義し、バックエンド/フロント双方で参照できるようにする。
- 将来の新アイドル追加を想定し、マスターデータ更新手順をドキュメント化。

### 品質保証とテスト
- API: pytest + httpx による主要シナリオの自動化（認証、CRUD、検索、My投稿）。
- フロント: 重要画面のコンポーネントテスト、手動E2Eチェックリスト（Discordログイン→投稿→検索→編集→削除）。
- デプロイ前: Vercel/ Railway 上での接続確認と環境変数検証。

### ドキュメントとナレッジ共有
- フェーズごとに `docs/MVP.md` と README の更新点をレビューし齟齬を解消。
- `docs/gakumas-memory.md` の知見を開発メンバーへ共有するクイックリファレンスを作成（任意）。

## ロードマップ運用
- 各フェーズの開始時に具体的なタスクをIssue化し、完了条件と担当を明確化。
- 週次で進捗レビューを行い、仕様変更が発生した場合は本ロードマップとMVP設計書を同期。
- 検索機能拡張やリフレッシュトークン導入などフェーズ2以降の要望はバックログに積み、MVPリリース後の改善計画を策定。
