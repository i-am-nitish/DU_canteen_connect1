import api from './api'

export const fetchAllCanteens = async () => {
  try {
    const res = await api.get('/canteens')
    return res.data.canteens || []
  } catch (error) {
    console.log(error)
    return [];
  }
}

export const fetchCanteenInfo = async (canteenId) => {
  try {
    const res = await api.get(`/canteen_info?canteen_id=${canteenId}`)
    return res.data.canteen_info || {}
  } catch (error) {
    console.log(error);
    return null ;
  }
}

export const fetchCanteenMenu = async (canteenId) => {
  try {
    const res = await api.get(`/canteen_menu_details?canteen_id=${canteenId}`)
    console.log('res from menu fetch: ', res)
    const menu = (res.data.data.menu || []).map(day => {
           return {
             ...day,
             items: JSON.parse(day.items.replace(/'/g, '"')),  // convert to real array --- this should be done only if backend saves these respective fields with single quotes like ['noodles','thali']
             price: JSON.parse(day.price.replace(/'/g, '"')),  // convert to real array
           }
         })
    console.log('menu: ', menu)
    return menu || {}
  } catch (error) {
    console.log(error)
    return null;
  }
}

export const fetchCanteenReviews = async (canteenId) => {
  try {
    const res = await api.get(`/canteen_review_ratings?canteen_id=${canteenId}`)
    console.log('response from retings and review fetch: ', res)
    console.log('ratings: ', res.data.data)
    return res.data.data || null ;
  } catch (error) {
    console.log(error)
    return null ;
  }
  
}
// gpt added this too
export const submitCanteenReview = async (canteenId, reviewData) => {
  const formData = new FormData()
  formData.append('canteen_id', canteenId)
  formData.append('overall_rating', reviewData.overallRating)
  formData.append('food_rating', reviewData.foodRating)
  formData.append('hygiene_rating', reviewData.hygieneRating)
  formData.append('staff_rating', reviewData.staffRating)
  formData.append('facilities_rating', reviewData.facilityRating)
  formData.append('review_text', reviewData.text)
  
  const res = await api.post('/add_review_rating', formData)
  return res.data
}
// gpt added this function
export const searchCanteens = async (query) => {
  const res = await api.get(`/search/canteens?q=${encodeURIComponent(query)}`)
  return res.data.results || []
}