export const MyMemoriesPage = () => {
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">マイ投稿一覧</h1>
      <p className="text-slate-600">
        認証後に作成したメモリー投稿をここで管理できます。バックエンドのAPIが整い次第、一覧と編集フォームを表示します。
      </p>
      <div className="rounded-lg border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-600">
        <p className="font-medium text-slate-800">TODO</p>
        <ul className="mt-2 list-disc space-y-1 pl-5">
          <li>公開済みメモリーの一覧と並び替え</li>
          <li>編集・削除へのショートカット</li>
          <li>セッション別のドラフト保存</li>
        </ul>
      </div>
    </section>
  )
}
