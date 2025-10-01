export const HomePage = () => {
  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <p className="text-sm font-semibold uppercase tracking-wide text-indigo-500">
          メモリー編成共有
        </p>
        <h1 className="text-3xl font-bold text-slate-900">最新のメモリー投稿</h1>
        <p className="text-slate-600">
          バックエンドのメモリーAPIを整備中です。準備が整い次第、この画面で編成一覧と検索が利用できるようになります。
        </p>
      </header>
      <div className="rounded-lg border border-dashed border-slate-300 bg-white p-6 text-sm text-slate-600">
        <p className="font-medium text-slate-800">進捗メモ</p>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-slate-600">
          <li>Discord OAuth でのログイン導線は利用可能です。</li>
          <li>メモリー投稿・検索APIは Issue #9-#11 で実装予定です。</li>
          <li>フロントエンドでは先にUIの骨組みを整備し、後からAPI連携を行います。</li>
        </ul>
      </div>
    </section>
  )
}
