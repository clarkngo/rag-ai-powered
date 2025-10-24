import React, { useEffect, useState } from 'react'
import axios from 'axios'
import MovieCard from './MovieCard'
import './movie-list.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:3000'

export default function MovieList() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        setLoading(true)
        const res = await axios.get(`${API_BASE}/movies?limit=50`)
        if (mounted) setMovies(res.data)
      } catch (err) {
        setError(err.message)
      } finally { if (mounted) setLoading(false) }
    }
    load()
    return () => { mounted = false }
  }, [])

  if (loading) return <div className="movie-list__empty">Loading movies…</div>
  if (error) return <div className="movie-list__empty">Error: {error}</div>

  return (
    <section className="movie-list">
      {movies.map((m) => (
        <MovieCard key={m._id || m.id || m.title} movie={m} onClick={() => window.location.assign(`/movie/${m._id || m.id}`)} />
      ))}
    </section>
  )
}
