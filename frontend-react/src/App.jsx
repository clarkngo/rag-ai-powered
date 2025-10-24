import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import MovieDetails from './pages/MovieDetails'
import './App.css'

export default function App() {
  return (
    <BrowserRouter>
      <div id="app-root">
        <nav className="app-nav">
          <Link to="/" className="app-nav__brand">Movie Explorer</Link>
          <div className="app-nav__links">
            <Link to="/">Home</Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/movie/:id" element={<MovieDetails />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
