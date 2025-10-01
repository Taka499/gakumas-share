import type { PropsWithChildren } from 'react'
import { Header } from './Header'

export const AppLayout = ({ children }: PropsWithChildren) => {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Header />
      <main className="mx-auto w-full max-w-5xl px-4 py-10 sm:px-6 sm:py-12">
        {children}
      </main>
    </div>
  )
}
