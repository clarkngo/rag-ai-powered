// Keyword-based retriever using the Movie Mongoose model.
// Exposes a function `keywordSearch(MovieModel, query, limit)` that returns matching movies.
async function keywordSearch(MovieModel, query, limit = 10) {
  if (!MovieModel) return []
  if (!query || !query.trim()) return []

  // Build a basic regex search across title, cast, and genres
  const re = new RegExp(query.split(/\s+/).join('|'), 'i')
  try {
    const results = await MovieModel.find({
      $or: [
        { title: { $regex: re } },
        { cast: { $elemMatch: { $regex: re } } },
        { genres: { $elemMatch: { $regex: re } } }
      ]
    })
      .limit(limit)
      .lean()

    return results
  } catch (err) {
    console.error('keywordSearch error', err.message || err)
    return []
  }
}

module.exports = { keywordSearch }
