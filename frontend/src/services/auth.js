import api from './api'

// Login API
export const loginUser = async (phone_number, password) => {
  const formData = new FormData()
  formData.append('phone_number', phone_number)
  formData.append('password', password)

  const res = await api.post('/login', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

  console.log('res from login: ', res, 'res.data: ', res.data)
  return res.data
}

// Signup API
export const signupUser = async ({ name, phone_number, email, set_password, confirm_password, role }) => {
  const formData = new FormData()
  formData.append('name', name)
  formData.append('phone_number', phone_number)
  formData.append('email', email)
  formData.append('set_password', set_password)
  formData.append('confirm_password', confirm_password)
  formData.append('role', role)

  const res = await api.post('/signup', formData)
  const data = res.data

  // For canteen owners, extract user_id from backend next_url
  if (!data.token && data.next_url) {
    const url = new URL(data.next_url, window.location.origin)
    const owner_id = url.searchParams.get("owner_id")
    return { user: { user_id: owner_id }, message: data.message }
  }

  return data
}





// Create Canteen Profile API
export const createCanteenProfile = async (ownerId, profileData) => {
  try {
    // Create a FormData object for multipart/form-data
    const formData = new FormData();

    // Add all profile fields
    formData.append("owner_id", ownerId);
    formData.append("canteen_name", profileData.canteen_name);
    formData.append("location", profileData.location);
    formData.append("description", profileData.description);
    formData.append("contact_number", profileData.contact_number);
    formData.append("days_open", profileData.days_open);
    formData.append("opening_time", profileData.opening_time);
    formData.append("closing_time", profileData.closing_time);
    formData.append("peak_hr_start_time", profileData.peak_hr_start_time);
    formData.append("peak_hr_end_time", profileData.peak_hr_end_time);

    // If menu file exists, append it
    if (profileData.menu_file) {
      formData.append("menu_file", profileData.menu_file);
    }

    // ✅ Use api.post instead of axios.post
    const response = await api.post('/create_canteen_profile', formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": `Bearer ${localStorage.getItem("token") || ""}`
      }
    });

    // Expect backend to return { token?, redirect_url?, message? }
    return response.data;

  } catch (err) {
    console.error("Error creating canteen profile:", err);
    throw err; // Let component handle errorMsg
  }
};
