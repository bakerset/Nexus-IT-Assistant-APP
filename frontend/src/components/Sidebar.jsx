export default function Sidebar() {
  return (
    <nav className="w-64 bg-gray-800 border-r border-gray-700 p-4">
      <h1 className="text-2xl font-bold mb-8">Nexus IT</h1>
      <ul className="space-y-4">
        <li><a href="/" className="hover:text-blue-400">Dashboard</a></li>
        <li><a href="/notes" className="hover:text-blue-400">Notes</a></li>
        <li><a href="/tickets" className="hover:text-blue-400">Tickets</a></li>
        <li><a href="/devices" className="hover:text-blue-400">Devices</a></li>
        <li><a href="/infrastructure" className="hover:text-blue-400">Infrastructure</a></li>
        <li><a href="/threats" className="hover:text-blue-400">Threats</a></li>
      </ul>
    </nav>
  )
}
