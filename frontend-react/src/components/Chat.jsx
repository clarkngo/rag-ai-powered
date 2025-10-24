import React, { useState } from 'react'
import axios from 'axios'
import './chat.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:3000'

export default function Chat() {
  const [history, setHistory] = useState([])
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(false)

  async function send(e) {
    e && e.preventDefault()
    if (!msg.trim()) return
    const userMsg = msg.trim()
    setHistory((h)=>[...h, { role: 'user', text: userMsg }])
    setMsg('')
    setLoading(true)
    try {
      const res = await axios.post(`${API_BASE}/chat`, { query_text: userMsg })
      setHistory((h)=>[...h, { role: 'assistant', text: res.data.response }])
    } catch (err) {
      setHistory((h)=>[...h, { role: 'assistant', text: `Error: ${err.message}` }])
    } finally { setLoading(false) }
  }

  return (
    <div className="chat">
      <div className="chat__window">
        {history.map((m, idx)=> (
          <div key={idx} className={`chat__msg chat__msg--${m.role}`}>{m.text}</div>
        ))}
      </div>
      <form className="chat__form" onSubmit={send}>
        <input value={msg} onChange={(e)=>setMsg(e.target.value)} placeholder="Ask about a movie or request recommendations" />
        <button className="btn" type="submit" disabled={loading}>{loading? 'Sending…':'Send'}</button>
      </form>
    </div>
  )
}
