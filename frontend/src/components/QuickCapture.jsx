export default function QuickCapture() {
  return (
    <div className="border-t border-gray-700 p-4 bg-gray-800">
      <input
        type="text"
        placeholder="Quick capture a note..."
        className="w-full px-4 py-2 bg-gray-700 rounded border border-gray-600 text-white focus:outline-none focus:border-blue-400"
      />
    </div>
  )
}
