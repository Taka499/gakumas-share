import { useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { env } from '../lib/env'

const ERROR_MESSAGES: Record<string, string> = {
  oauth_authorisation: 'Discord 認証に失敗しました。時間を置いて再度お試しください。',
  profile_unavailable: 'Discord プロフィール情報を取得できませんでした。アクセス権限を確認してください。',
}

export const AuthErrorPage = () => {
  const [params] = useSearchParams()
  const errorCode = params.get('error') ?? 'unknown'

  const message = useMemo(() => {
    return ERROR_MESSAGES[errorCode] ?? '原因不明のエラーが発生しました。再度ログインをお試しください。'
  }, [errorCode])

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-rose-600">ログインに失敗しました</h1>
      <p className="text-slate-600">{message}</p>
      <div className="flex items-center gap-3">
        <Link
          to="/"
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
        >
          ホームへ戻る
        </Link>
        <a
          href={env.discordLoginUrl}
          className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
        >
          再度ログインする
        </a>
      </div>
      <p className="text-xs text-slate-400">エラーコード: {errorCode}</p>
    </section>
  )
}
