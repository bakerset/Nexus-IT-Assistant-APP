import { useState } from 'react'

export function useAgent() {
  const [messages, setMessages] = useState([])
  const [nudges, setNudges] = useState([])
  return { messages, setMessages, nudges, setNudges }
}
