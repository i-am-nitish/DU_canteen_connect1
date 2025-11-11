import api from './api'

// Function 1: Search canteens 
export const searchCanteens = async (query) => {
    const res = await api.get('/search/canteens', { params: { q: query } })
    return res.data
  // Make GET request to /search/canteens with query parameter
  // Return response data
}

// Function 2: Search food items
export const searchFoodItems = async (query) => {
    const res = await api.get('/search/food_items', { params: { q: query } })
    return res.data
  // Make GET request to /search/food_items with q parameter
  // Return response data
}