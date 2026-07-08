import { BrowserRouter, Navigate, Route, Routes, useParams } from 'react-router-dom'
import { SettingsProvider } from '@/context/SettingsContext'
import { AppShell } from '@/components/layout/AppShell'
import { TopicList } from '@/components/topics/TopicList'
import { TopicWorkspace } from '@/components/workspace/TopicWorkspace'
import { SettingsPage } from '@/pages/SettingsPage'

export default function App() {
  return (
    <SettingsProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<TopicList />} />
            <Route path="topics/:topicId" element={<TopicPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </SettingsProvider>
  )
}

function TopicPage() {
  const { topicId } = useParams<{ topicId: string }>()
  if (!topicId) return <Navigate to="/" replace />
  return <TopicWorkspace topicId={topicId} />
}
