// Import Axios
import axios from 'axios'

// 🔹 Create Axios instance
const api = axios.create({
  baseURL: 'https://du-canteen-connect1.onrender.com', // Render backend URL
})

// 🔹 Automatically attach JWT token (if exists) to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api
