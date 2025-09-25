# 学マス メモリー共有サイト MVP設計書

## 1. MVP機能範囲

### 1.1 最小限の核心機能のみ
- **メモリー編成投稿**: 基本情報 + メモリー構成
- **編成一覧表示**: シンプルなカード形式
- **基本検索**: ステージ・アイドル別フィルター
- **編成詳細**: 投稿内容の閲覧
- **メモリー編成編集**: 投稿内容の更新
- **マイ投稿一覧**: 自身の投稿をまとめて表示
- **認証**: Discord OAuth2 + SuperTokens セッション

### 1.2 MVP除外機能（フェーズ2以降）
- いいね・コメント機能
- 高度な検索・フィルタリング
- ユーザープロフィール
- ユーザーによる画像アップロード
- 複数OAuthプロバイダー対応
- レスポンシブデザイン（PC優先）
- 通知機能
- 統計・分析

※ メモリーやアイテムの仕様は `docs/gakumas-memory.md` を参照。

## 2. 技術スタック（コスト最適化）

### 2.1 フロントエンド
- **Vite + React + TypeScript**: 高速開発
- **Tailwind CSS**: 迅速なスタイリング
- **React Hook Form**: フォーム管理
- **Axios**: API通信
- **React Router**: ルーティング

### 2.2 バックエンド
- **Python + FastAPI**: 最速API開発
- **uv**: 超高速パッケージ管理
- **Motor**: 非同期MongoDB接続
- **Pydantic / Pydantic Settings**: 設定とバリデーション
- **Authlib**: Discord OAuth2 クライアント
- **SuperTokens Python SDK**: セッション／トークン管理

### 2.3 データベース
- **MongoDB**: ドキュメント型DB
- **MongoDB Atlas Free Tier**: 512MB無料

### 2.4 ホスティング
- **Vercel**: フロントエンド（無料枠）
- **Railway**: バックエンド（$5/月〜）
- **Cloudinary**: 画像アセット保管（カード・アイテム素材の静的配信。ユーザーアップロードはフェーズ2以降）

**予想月額コスト: $5-10**

## 3. データベース設計（MVP簡略版）

### 3.1 Users Collection
```javascript
{
  _id: ObjectId,
  provider: String,            // 例: "discord"
  provider_account_id: String, // プロバイダー内のユーザーID
  username: String,
  avatar_url: String | null,
  created_at: Date,
  updated_at: Date
}
```

### 3.2 MemorySets Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  title: String,
  
  // 基本情報
  stage_type: String,    // "contest" | "idol_road"
  stage_category: String, // "Vo" | "Da" | "Vi"
  p_idol: String,
  clear_rank: String,    // "A+" | "S" | "S+"
  
  // メモリー構成
  p_items: [
    {
      name: String,
      effect: String,
      is_guaranteed: Boolean
    }
  ], // 0件でも可
  skill_cards: [
    {
      name: String,
      rarity: String,
      effect: String,
      enhancement_level: Number,
      is_guaranteed: Boolean
    }
  ], // 1件以上必須
  
  // 簡易メモ
  notes: String,
  
  created_at: Date,
  updated_at: Date
}
```

### 3.3 インデックス（最小限）
```javascript
// Users
db.users.createIndex(
  { "provider": 1, "provider_account_id": 1 },
  { unique: true, name: "provider_account_unique" }
)

// MemorySets
db.memorySets.createIndex({ "user_id": 1 })
db.memorySets.createIndex({ "stage_type": 1, "stage_category": 1 })
db.memorySets.createIndex({ "p_idol": 1 })
db.memorySets.createIndex({ "created_at": -1 })
```

`p_idol` は「アイドル名 + 曲名」で構成される。現行12名のアイドルがメインカテゴリとして存在し、各曲には `stage_category`（センス / ロジック / アノマリー など）が紐づく。同一アイドルかつ同一カテゴリのメモリー同士でのみ編成可能。

## 4. API設計

### 4.1 認証エンドポイント
```
GET  /api/auth/discord/login     # Discord 認可URLへリダイレクト
GET  /api/auth/discord/callback  # コード受領 → SuperTokens セッション発行
POST /api/auth/logout            # SuperTokens 組み込みルートでセッション失効
POST /api/auth/session/verify    # SuperTokens 組み込みルートでセッション検証
```

> SuperTokens のデフォルト挙動でアクセストークン・リフレッシュトークンのローテーション、盗難検知、Anti-CSRF を有効化する。アプリ固有のアクセストークンレスポンスは不要。

### 4.2 メモリー編成エンドポイント
```
GET    /api/memories              # 一覧取得（ページング）
POST   /api/memories              # 新規投稿
GET    /api/memories/{id}         # 詳細取得
PUT    /api/memories/{id}         # 更新（投稿者のみ）
DELETE /api/memories/{id}         # 削除（投稿者のみ）
```

### 4.3 検索エンドポイント
```
GET /api/memories?stage_type=contest&stage_category=Vo
GET /api/memories?p_idol=花海咲季
```

- `stage_type` / `stage_category` / `p_idol` はすべて任意のパラメータ。指定された条件は AND で組み合わせて絞り込む。
- デフォルトの並び順は `created_at` 降順。`limit` の初期値は 20、最大 50 まで許容し、`skip` と併用してページネーションを行う。
- レスポンスは `items`（編成配列）と `total`（条件一致件数）を返す JSON を想定。

## 5. フロントエンド設計

### 5.1 ページ構成（最小限）
- **/** : ホーム（編成一覧）
- **/auth/success** : ログイン後の遷移先（セッション確立確認）
- **/auth/error** : OAuthエラー表示
- **/memories/create** : 編成投稿
- **/memories/{id}** : 編成詳細
- **/memories/{id}/edit** : 編成編集
- **/my** : 自分の投稿一覧

### 5.2 コンポーネント構成
```
src/
├── components/
│   ├── common/
│   │   ├── Header.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorMessage.tsx
│   ├── memory/
│   │   ├── MemoryCard.tsx      # 編成カード
│   │   ├── MemoryList.tsx      # 編成一覧
│   │   ├── MemoryForm.tsx      # 投稿・編集フォーム
│   │   └── MemoryDetail.tsx    # 編成詳細
│   └── auth/
│       ├── DiscordLoginButton.tsx
│       └── SessionGuard.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── AuthSuccessPage.tsx
│   ├── AuthErrorPage.tsx
│   ├── CreateMemoryPage.tsx
│   ├── MemoryDetailPage.tsx
│   └── MemoryEditPage.tsx
├── hooks/
│   ├── useSession.ts
│   └── useMemories.tsx
├── services/
│   ├── api.ts
│   └── auth.ts
└── types/
    └── index.ts
```

## 6. 開発フェーズ計画

### Week 1-2: 基盤構築
- プロジェクトセットアップ
- 認証システム構築
- 基本的なUIコンポーネント

### Week 3-4: 核心機能
- メモリー編成投稿機能
- 編成一覧・詳細表示
- 基本検索機能

### Week 5-6: 統合・デプロイ
- フロントエンド・バックエンド統合
- テスト・バグ修正
- デプロイ・本番環境構築

## 7. FastAPI バックエンド構造

### 7.1 プロジェクト構造
```
backend/
├── pyproject.toml          # uv設定・依存関係管理
├── uv.lock                 # ロックファイル
├── .env.example           # 環境変数テンプレート
├── app/
│   ├── main.py              # FastAPI アプリケーション
│   ├── config.py            # 設定管理
│   ├── database.py          # MongoDB接続
│   ├── oauth.py             # OAuthクライアント設定
│   ├── supertokens.py       # SuperTokens 初期化
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # ユーザーモデル
│   │   └── memory.py        # メモリー編成モデル
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── root.py          # ルートレスポンス
│   │   ├── health.py        # ヘルスチェック
│   │   └── auth.py          # Discord OAuth + セッション
│   ├── repositories/
│   │   └── user_repository.py
│   └── tests/
│       └── test_main.py     # テストファイル
└── scripts/                # ユーティリティスクリプト
```

### 7.2 主要ファイル例

**pyproject.toml**
```toml
[project]
name = "backend"
version = "0.1.0"
description = "Gakumas Share backend API"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "authlib>=1.6.4",
    "fastapi[standard]>=0.117.1",
    "itsdangerous>=2.2.0",
    "motor>=3.7.1",
    "pydantic>=2.11.9",
    "pydantic-settings>=2.10.1",
    "pymongo[srv]>=4.15.1",
    "supertokens-python>=0.30.2",
]

[dependency-groups]
dev = [
    "httpx>=0.28.1",
    "mongomock>=4.3.0",
    "pytest>=8.4.2",
    "pytest-asyncio>=1.2.0",
    "ruff>=0.13.1",
]
```

**.python-version**
```
3.11
```
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PItem(BaseModel):
    name: str
    effect: str
    is_guaranteed: bool = False

class SkillCard(BaseModel):
    name: str
    rarity: str
    effect: str
    enhancement_level: int = 1
    is_guaranteed: bool = False

class MemorySetCreate(BaseModel):
    title: str
    stage_type: str
    stage_category: str
    p_idol: str
    clear_rank: str
    p_items: List[PItem]
    skill_cards: List[SkillCard]
    notes: Optional[str] = ""

class MemorySetResponse(MemorySetCreate):
    id: str
    user_id: str
    created_at: datetime
```

**app/routers/memories.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..models.memory import MemorySetCreate, MemorySetResponse
from ..database import get_database
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

router = APIRouter(prefix="/api/memories", tags=["memories"])

@router.get("/", response_model=List[MemorySetResponse])
async def get_memories(
    skip: int = 0,
    limit: int = 20,
    stage_type: Optional[str] = None,
    stage_category: Optional[str] = None,
    p_idol: Optional[str] = None,
    db=Depends(get_database)
):
    # 検索・ページング処理
    pass

@router.post("/", response_model=MemorySetResponse)
async def create_memory(
    memory: MemorySetCreate,
    session: SessionContainer = Depends(verify_session()),
    db=Depends(get_database)
):
    # session.get_user_id() で投稿者IDを取得
    pass
```

## 8. 開発セットアップ手順

### 8.1 事前準備
- Python 3.11以上
- uv（`curl -LsSf https://astral.sh/uv/install.sh | sh`）
- Node.js 18以上
- MongoDB Atlas アカウント

### 8.2 バックエンドセットアップ
```bash
# 1. リポジトリクローン
git clone https://github.com/[USERNAME]/gakumas-share.git
cd gakumas-share/backend

# 2. 依存関係同期
uv sync

# 3. 環境変数設定
cp .env.example .env
# .envファイルを編集してMongoDB, Discord, SuperTokens の値を設定

# 4. 開発サーバー起動
uv run uvicorn app.main:app --reload
```

### 8.3 フロントエンドセットアップ
```bash
cd frontend
npm install
npm run dev
```

### 8.4 開発コマンド
```bash
# バックエンド
cd backend
uv run uvicorn app.main:app --reload    # 開発サーバー
uv run pytest                           # テスト実行
uv run ruff check app/                  # 静的解析
uv run ruff format app/                 # コード整形

# フロントエンド
cd frontend  
npm run dev                            # 開発サーバー
npm run build                          # ビルド
npm run lint                           # リント
```

### 9.1 主要コンポーネント例

**components/memory/MemoryCard.tsx**
```tsx
interface MemoryCardProps {
  memory: MemorySet;
}

export const MemoryCard: React.FC<MemoryCardProps> = ({ memory }) => {
  return (
    <div className="border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="font-bold text-lg mb-2">{memory.title}</h3>
      <div className="text-sm text-gray-600 mb-2">
        {memory.stage_type} - {memory.stage_category} | {memory.p_idol}
      </div>
      <div className="text-sm mb-2">
        ランク: {memory.clear_rank}
      </div>
      <div className="flex justify-between items-center">
        <span className="text-xs text-gray-500">
          {new Date(memory.created_at).toLocaleDateString()}
        </span>
        <Link to={`/memory/${memory.id}`} className="text-blue-600 hover:underline">
          詳細を見る
        </Link>
      </div>
    </div>
  );
};
```

**hooks/useMemories.tsx**
```tsx
export const useMemories = () => {
  const [memories, setMemories] = useState<MemorySet[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMemories = async (filters?: SearchFilters) => {
    setLoading(true);
    try {
      const response = await api.get('/memories', { params: filters });
      setMemories(response.data);
    } catch (err) {
      setError('編成の取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return { memories, loading, error, fetchMemories };
};
```

## 9. React フロントエンド構造

## 10. デプロイ設定

### 10.1 Railway（バックエンド）
**railway.json**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "uv sync --frozen"
  },
  "deploy": {
    "startCommand": "uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30
  }
}
```

### 10.2 Vercel（フロントエンド）
**vercel.json**
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## 11. 開発開始チェックリスト

### 事前準備
- [ ] GitHub リポジトリ作成
- [ ] MongoDB Atlas アカウント作成
- [ ] Railway アカウント作成  
- [ ] Vercel アカウント作成
- [ ] uv インストール確認

### 開発環境セットアップ
- [ ] Python 3.11+ インストール
- [ ] uv パッケージマネージャー設定
- [ ] Node.js 18+ インストール
- [ ] VSCode + 拡張機能設定

### 第1週目標
- [ ] バックエンド: uv でプロジェクト初期化
- [ ] バックエンド: FastAPI基本構造実装
- [ ] バックエンド: MongoDB 接続確認
- [ ] バックエンド: Discord OAuth2 + SuperTokens セッション実装
- [ ] フロントエンド: React プロジェクト初期化

### uvの主要コマンド
```bash
uv init --python 3.11          # 新規プロジェクト初期化
uv add package-name            # 依存関係追加
uv add --dev package-name      # 開発依存関係追加
uv sync                        # 依存関係同期
uv run command                 # 仮想環境でコマンド実行
uv python install 3.11         # Python バージョンインストール
```
