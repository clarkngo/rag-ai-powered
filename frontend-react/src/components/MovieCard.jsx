import React from 'react'
import './movie-card.css'

export default function MovieCard({ movie, onClick }) {
  const title = movie.title || movie.name || 'Untitled'
  const genres = movie.genres || []
  const cast = movie.cast || []

  return (
    <article className="movie-card" onClick={onClick} role="button" tabIndex={0}>
      <div className="movie-card__thumb">
        {/* Placeholder poster area; server can supply poster URLs in future */}
        <div className="poster-placeholder">{title.charAt(0)}</div>
      </div>
      <div className="movie-card__body">
        <h3 className="movie-card__title">{title}</h3>
        <div className="movie-card__meta">
          <span className="movie-card__genres">{genres.slice(0,3).join(', ')}</span>
          <span className="movie-card__cast">{cast.slice(0,2).join(', ')}</span>
        </div>
      </div>
    </article>
  )
}
