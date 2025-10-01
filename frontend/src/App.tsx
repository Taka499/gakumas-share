import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/layout/AppLayout'
import { AuthErrorPage } from './pages/AuthErrorPage'
import { AuthSuccessPage } from './pages/AuthSuccessPage'
import { HomePage } from './pages/HomePage'
import { MyMemoriesPage } from './pages/MyMemoriesPage'
import { NotFoundPage } from './pages/NotFoundPage'

export const App = () => {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/auth/success" element={<AuthSuccessPage />} />
          <Route path="/auth/error" element={<AuthErrorPage />} />
          <Route path="/my" element={<MyMemoriesPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  )
}

export default App
