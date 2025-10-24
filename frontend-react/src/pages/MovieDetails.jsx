import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import './movie-details.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:3000'

export default function MovieDetails() {
  const { id } = useParams()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        setLoading(true)
        const res = await axios.post(`${API_BASE}/movies`, { movie_ids: [id] })
        if (mounted) setMovie(res.data[0] || null)
      } catch (err) { setError(err.message) }
      finally { if (mounted) setLoading(false) }
    }
    load()
    return () => { mounted = false }
  }, [id])

  if (loading) return <div className="details__empty">Loading…</div>
  if (error) return <div className="details__empty">Error: {error}</div>
  if (!movie) return <div className="details__empty">Movie not found</div>

  return (
    <article className="movie-details">
      <div className="movie-details__main">
        <h2>{movie.title}</h2>
        <div className="movie-details__meta">
          <div><strong>Genres:</strong> {movie.genres?.join(', ')}</div>
          <div><strong>Cast:</strong> {movie.cast?.slice(0,5).join(', ')}</div>
        </div>
        <p className="movie-details__plot">{movie.plot || movie.description || 'No plot available.'}</p>
      </div>

      <aside className="movie-details__aside">
        <div className="movie-details__actions">
          <button className="btn" onClick={async () => {
            // request recommendations via the proxy /recommend endpoint
            try {
              const recRes = await axios.post(`${API_BASE}/recommend`, { movieIds: [id] })
              alert(`Got ${recRes.data.recommendations?.length || 0} recommendations (open console).`)
              console.log('recommendations', recRes.data)
            } catch (e) { console.error(e); alert('Error fetching recommendations') }
          }}>Get Recommendations</button>
        </div>
      </aside>
    </article>
  )
}
