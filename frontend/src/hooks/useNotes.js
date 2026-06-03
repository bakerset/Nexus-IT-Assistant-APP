import { useState } from 'react'

export function useNotes() {
  const [notes, setNotes] = useState([])
  return { notes, setNotes }
}
