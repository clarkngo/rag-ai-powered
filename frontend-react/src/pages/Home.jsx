import React, { useState } from 'react'
import MovieList from '../components/MovieList'
import Search from '../components/Search'
import Chat from '../components/Chat'
import './home.css'

export default function Home() {
  const [results, setResults] = useState(null)

  return (
    <main className="home">
      <header className="home__header">
        <h1 className="home__title">Movie Explorer</h1>
        <p className="home__subtitle">Discover movies, get recommendations, and ask about plots.</p>
      </header>

      <section className="home__search">
        <Search onResults={setResults} />
      </section>

      <section className="home__chat">
        <Chat />
      </section>

      <section className="home__list">
        <MovieList />
      </section>

      {results && (
        <section className="home__results">
          <h3>Search Results</h3>
          <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(results, null, 2)}</pre>
        </section>
      )}
    </main>
  )
}
