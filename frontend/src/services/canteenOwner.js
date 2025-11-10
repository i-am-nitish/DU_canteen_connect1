import api from './api'


// All these functions automatically add JWT token from api.js
// Just call them and handle success/error

// 1. Get your canteen information
export const getCanteenInfoOwner = async () => {
  const response = await api.get('/get_canteen_info_owner')
  return response.data
}

// 2. Add a new food item to your menu
export const addFoodItem = async (itemName, itemPrice) => {
  const formData = new FormData()
  formData.append('item_name', itemName)
  formData.append('item_price', itemPrice)
  

  const response = await api.post('/add_food_item', formData)
  return response.data
}

// 3. Report an issue to admin
export const reportIssueByOwner = async (issueText) => {
  const formData = new FormData()
  formData.append('issue_text', issueText)

  const response = await api.post('/report_issue_canteen_owner', formData)
  return response.data
}

// 4. Get all reviews for your canteen
export const getCanteenReviewsOwner = async () => {
  const response = await api.get('/canteen_reviews_owner')
  return response.data
}

// 5. Get all food items for your canteen
export const getFoodItemsOwner = async () => {
  const response = await api.get('/food_items_owner')
  return response.data
}

// 6. Set menu for a specific day (Monday-Sunday)
export const updateDayWiseMenu = async (canteenId, day, foodIds) => {
  const formData = new FormData()
  formData.append('canteen_id', canteenId)
  formData.append('day', day)
  
  // Add each food_id separately
  foodIds.forEach(id => {
    formData.append('food_ids', id)
  })

  const response = await api.post('/menu/update_day', formData)
  return response.data
}
