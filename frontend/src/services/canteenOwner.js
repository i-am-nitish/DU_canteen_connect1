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


export const uploadMenuImages = async (canteenId, files /* Array or FileList */) => {
  const formData = new FormData()
  formData.append('canteen_id', canteenId)

  // Accept only up to 2 files (preserve order)
  const fileArr = Array.from(files || []).slice(0, 2)
  if (fileArr[0]) formData.append('menu_file_1', fileArr[0])
  if (fileArr[1]) formData.append('menu_file_2', fileArr[1])

  const res = await api.post('/upload_menu_image', formData) // let axios set Content-Type
  return res.data
}

// 8. Upload canteen images (up to 2 files)
export const uploadCanteenImages = async (canteenId, files /* Array or FileList */) => {
  const formData = new FormData()
  formData.append('canteen_id', canteenId)

  const fileArr = Array.from(files || []).slice(0, 2)
  if (fileArr[0]) formData.append('canteen_image_1', fileArr[0])
  if (fileArr[1]) formData.append('canteen_image_2', fileArr[1])

  const res = await api.post('/upload_canteen_images', formData)
  return res.data
}

// edit canteen profile
export const updateCanteenProfile = async (payload) => {
  // Convert JSON object to FormData
  const formData = new FormData()
  
  // Add each field to FormData 
  for (const key in payload) {
    if (payload[key] !== null && payload[key] !== undefined) {
      formData.append(key, payload[key])
    }
  }

  const response = await api.post('/canteen_profile_update', formData)
  return response.data
}
