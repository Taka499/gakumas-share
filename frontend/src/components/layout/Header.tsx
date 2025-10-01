import { Link, NavLink } from 'react-router-dom'
import { env } from '../../lib/env'
import { useSession } from '../../hooks/useSession'

const linkClass = ({ isActive }: { isActive: boolean }) =>
  [
    'rounded-md px-3 py-2 text-sm font-medium transition-colors',
    isActive
      ? 'bg-slate-900 text-white'
      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100',
  ].join(' ')

export const Header = () => {
  const { status, isLoading } = useSession()
  return (
    <header className="border-b border-slate-200 bg-white shadow-sm">
      <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6">
        <Link to="/" className="text-lg font-semibold text-slate-900" aria-label="Home">
          Gakumas Share
        </Link>
        <div className="flex items-center gap-4">
          <nav className="flex items-center gap-2">
            <NavLink to="/" className={linkClass} end>
              ホーム
            </NavLink>
            <NavLink to="/my" className={linkClass}>
              マイ投稿
            </NavLink>
            <a
              href={env.discordLoginUrl}
              className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-indigo-500"
            >
              Discordでログイン
            </a>
          </nav>
          <div className="hidden text-xs font-medium uppercase tracking-wide text-slate-500 sm:block">
            {isLoading
              ? 'セッション確認中...'
              : status === 'authenticated'
                ? 'ログイン済み'
                : '未ログイン'}
          </div>
        </div>
      </div>
    </header>
  )
}
