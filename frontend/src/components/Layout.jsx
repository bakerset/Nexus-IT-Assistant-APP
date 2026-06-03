import Sidebar from './Sidebar'
import AgentPanel from './AgentPanel'
import NudgeBadge from './NudgeBadge'
import QuickCapture from './QuickCapture'

export default function Layout() {
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar />
      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-auto">
          {/* Router outlet would go here */}
        </div>
        <QuickCapture />
      </main>
      <aside className="w-96 border-l border-gray-700 flex flex-col">
        <AgentPanel />
        <NudgeBadge />
      </aside>
    </div>
  )
}
