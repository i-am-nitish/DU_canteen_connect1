// src/services/user.js
import api from '@/api/api'  // adjust path if needed

// Protected: requires Authorization header with JWT (api.js adds it)
export const fetchUserInfo = async () => {
  const res = await api.get('/display_user_info')
  return res.data // backend should return user info object
}

export const fetchUserReviews = async () => {
  const res = await api.get('/display_user_reviews')
  return res.data // backend should return list/structure of reviews
}

// Feedback about the app (text)
export const submitAppFeedback = async (payload) => {
  // payload: { feedback_text: "..." }
  const res = await api.post('/give_app_feedback', payload)
  return res.data
}

// Report an issue (text)
export const submitAppIssue = async (payload) => {
  // payload: { issue_text: "..." }
  const res = await api.post('/report_app_issue', payload)
  return res.data
}
