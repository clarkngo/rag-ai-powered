// Simple intent classifier/router based on keywords. Returns one of: 'qa', 'recommend', 'conversational'
function classifyIntent(text) {
  if (!text || typeof text !== 'string') return 'qa'
  const t = text.toLowerCase()
  // recommendation intent
  const recKeywords = ['recommend', 'suggest', 'similar', 'like', 'more like']
  if (recKeywords.some(k => t.includes(k))) return 'recommend'

  // conversational intent
  const convKeywords = ['hello', 'hi', 'how are you', 'tell me a story', 'chat']
  if (convKeywords.some(k => t.includes(k))) return 'conversational'

  // default to question/QA
  return 'qa'
}

module.exports = { classifyIntent }
