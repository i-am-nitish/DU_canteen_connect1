import api from './api'

export const fetchAllCanteens = async () => {
  const res = await api.get('/canteens')
  return res.data.canteens || []
}

export const fetchCanteenInfo = async (canteenId) => {
  const res = await api.get(`/canteen_info?canteen_id=${canteenId}`)
  return res.data.canteen_info || {}
}

export const fetchCanteenMenu = async (canteenId) => {
  const res = await api.get(`/canteen_menu_details?canteen_id=${canteenId}`)
  return res.data || {}
}

export const fetchCanteenReviews = async (canteenId) => {
  const res = await api.get(`/canteen_review_ratings?canteen_id=${canteenId}`)
  return res.data.data || []
}