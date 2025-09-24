# 学マス メモリー共有サイト MVP設計書

## 1. MVP機能範囲

### 1.1 最小限の核心機能のみ
- **メモリー編成投稿**: 基本情報 + メモリー構成
- **編成一覧表示**: シンプルなカード形式
- **基本検索**: ステージ・アイドル別フィルター
- **編成詳細**: 投稿内容の閲覧
- **メモリー編成編集**: 投稿内容の更新
- **マイ投稿一覧**: 自身の投稿をまとめて表示
- **簡易認証**: ユーザー登録・ログイン

### 1.2 MVP除外機能（フェーズ2以降）
- いいね・コメント機能
- 高度な検索・フィルタリング
- ユーザープロフィール
- ユーザーによる画像アップロード
- リフレッシュトークン運用
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
- **Pydantic**: データバリデーション
- **python-jose**: JWT認証
- **python-multipart**: ファイルアップロード

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
  username: String, // ユニーク
  email: String,    // ユニーク  
  password_hash: String,
  created_at: Date
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
db.users.createIndex({ "username": 1 }, { unique: true })
db.users.createIndex({ "email": 1 }, { unique: true })

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
POST /api/auth/register
POST /api/auth/login
```

> MVP方針: 有効期限の短いアクセストークンのみを採用し、リフレッシュトークンはフェーズ2で検討する。

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
- **/login** : ログイン
- **/register** : ユーザー登録  
- **/create** : 編成投稿
- **/memory/{id}** : 編成詳細
- **/memory/{id}/edit** : 編成編集
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
│       ├── LoginForm.tsx
│       └── RegisterForm.tsx
├── pages/
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   ├── CreateMemoryPage.tsx
│   ├── MemoryDetailPage.tsx
│   └── MemoryEditPage.tsx
├── hooks/
│   ├── useAuth.tsx
│   └── useMemories.tsx
├── services/
│   └── api.ts
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
├── uv.lock                # ロックファイル
├── .python-version        # Python 3.11指定
├── .env.example           # 環境変数テンプレート
├── railway.json           # Railway設定
├── Dockerfile             # Docker設定
├── app/
│   ├── main.py              # FastAPI アプリケーション
│   ├── config.py            # 設定管理
│   ├── database.py          # MongoDB接続
│   ├── auth.py              # JWT認証
│   ├── startup.py           # アプリ初期化
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # ユーザーモデル
│   │   └── memory.py        # メモリー編成モデル
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # 認証API
│   │   └── memories.py      # メモリー編成API
│   └── tests/
│       └── test_main.py     # テストファイル
└── scripts/                # ユーティリティスクリプト
```

### 7.2 主要ファイル例

**pyproject.toml**
```toml
[project]
name = "gakumas-memory-backend"
version = "0.1.0"
description = "学園アイドルマスター メモリー編成共有サイト - Backend API"
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "motor>=3.3.2",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
]
requires-python = ">=3.11"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "httpx>=0.25.2",
    "black>=23.11.0",
    "isort>=5.12.0",
    "mypy>=1.7.1",
]

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
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
from ..auth import get_current_user

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
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    # 編成投稿処理
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
git clone https://github.com/[USERNAME]/gakumas-memory-sharing.git
cd gakumas-memory-sharing/backend

# 2. Python バージョン設定
echo "3.11" > .python-version

# 3. プロジェクト初期化
uv init --python 3.11

# 4. 依存関係インストール
uv add fastapi uvicorn[standard] motor pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart

# 5. 開発依存関係インストール  
uv add --dev pytest pytest-asyncio httpx black isort mypy

# 6. 環境変数設定
cp .env.example .env
# .envファイルを編集してMongoDB URLなどを設定

# 7. 開発サーバー起動
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
uv run pytest                          # テスト実行
uv run black app/                      # コード整形
uv run mypy app/                       # 型チェック

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
- [ ] バックエンド: JWT認証実装
- [ ] フロントエンド: React プロジェクト初期化

### uvの主要コマンド
```bash
uv init --python 3.11          # プロジェクト初期化
uv add package-name            # 依存関係追加
uv add --dev package-name      # 開発依存関係追加
uv sync                        # 依存関係同期
uv run command                 # コマンド実行
uv python install 3.11        # Python バージョンインストール
```
