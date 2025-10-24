import React, { useState } from 'react'
import axios from 'axios'
import './search.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:3000'

export default function Search({ onResults }) {
  const [q, setQ] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function submit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      // Use ADK endpoint which will handle intent routing (recommendation, QA, conversational)
      const res = await axios.post(`${API_BASE}/adk_query`, { query_text: q })
      const data = res.data
      onResults && onResults(data)
    } catch (err) {
      setError(err.message)
    } finally { setLoading(false) }
  }

  return (
    <form className="search" onSubmit={submit}>
      <input className="search__input" placeholder="Search movies or ask a question" value={q} onChange={(e)=>setQ(e.target.value)} />
      <button className="btn" type="submit" disabled={loading || !q.trim()}>{loading? 'Searching…':'Search'}</button>
      {error && <div className="search__error">{error}</div>}
    </form>
  )
}
