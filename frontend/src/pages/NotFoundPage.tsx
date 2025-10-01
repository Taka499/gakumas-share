import { Link } from 'react-router-dom'

export const NotFoundPage = () => {
  return (
    <section className="space-y-4 text-center">
      <h1 className="text-3xl font-bold text-slate-900">ページが見つかりません</h1>
      <p className="text-slate-600">URL を確認し、もう一度アクセスしてください。</p>
      <Link
        to="/"
        className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
      >
        ホームへ戻る
      </Link>
    </section>
  )
}
