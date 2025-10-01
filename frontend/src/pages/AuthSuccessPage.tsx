import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { env } from '../lib/env'

export const AuthSuccessPage = () => {
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const sessionState = params.get('session')

  useEffect(() => {
    const timer = window.setTimeout(() => {
      navigate('/', { replace: true })
    }, 2000)

    return () => window.clearTimeout(timer)
  }, [navigate])

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold text-slate-900">ログインしました</h1>
      <p className="text-slate-600">
        Discord 認証が完了し、セッションが作成されました。数秒後にホームへ戻ります。
      </p>
      {sessionState && (
        <div className="rounded-md border border-slate-200 bg-white p-4 text-sm text-slate-500">
          セッションステータス: <span className="font-semibold text-slate-700">{sessionState}</span>
        </div>
      )}
      <p className="text-sm text-slate-500">
        もし自動で戻らない場合は <a className="text-indigo-600" href={env.discordLoginUrl}>こちら</a> から再度ログインしてください。
      </p>
    </section>
  )
}
