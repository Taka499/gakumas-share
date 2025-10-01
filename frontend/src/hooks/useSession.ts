import { useEffect, useMemo, useState } from 'react'
import { http } from '../lib/http'

type SessionStatus = 'unknown' | 'authenticated' | 'unauthenticated'

type SessionSummary = {
  status: SessionStatus
  isLoading: boolean
  error?: string
}

export const useSession = (): SessionSummary => {
  const [status, setStatus] = useState<SessionStatus>('unknown')
  const [error, setError] = useState<string | undefined>(undefined)

  useEffect(() => {
    let isMounted = true

    const checkSession = async () => {
      try {
        await http.post('/api/auth/session/verify')
        if (isMounted) {
          setStatus('authenticated')
        }
      } catch (err) {
        if (!isMounted) return
        setStatus('unauthenticated')
        if (err instanceof Error) {
          setError(err.message)
        }
      }
    }

    checkSession()

    return () => {
      isMounted = false
    }
  }, [])

  return useMemo(
    () => ({ status, isLoading: status === 'unknown', error }),
    [status, error],
  )
}
