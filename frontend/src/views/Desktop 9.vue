<template>
  <div class="page-wrapper">
    <!-- Header -->
    <Header />
    <div class="dashboard-wrapper">
    <!-- canteen Profile Section -->
    <section class="card profile-section">
      <h2>Profile</h2>
      <div v-if="loading && !canteenInfo" class="loading">Loading canteen info...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="canteenInfo" class="profile-content">
        <div class="profile-image"></div>
        <div class="profile-info">
        <div>
          <strong>Name:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableCanteenInfo.name" type="text" />
          </template>
          <template v-else>
            {{ canteenInfo.name || 'N/A' }}
          </template>
        </div>

        <div>
          <strong>Location:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableCanteenInfo.location" type="text" />
          </template>
          <template v-else>
            {{ canteenInfo.location || 'N/A' }}
          </template>
        </div>

        <div>
          <strong>Contact:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableCanteenInfo.contact_no" type="text" />
          </template>
          <template v-else>
            {{ canteenInfo.contact_no || 'N/A' }}
          </template>
        </div>

        <div>
          <strong>Days Open:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableCanteenInfo.days_open" type="text" />
          </template>
          <template v-else>
            {{ canteenInfo.days_open || 'N/A' }}
          </template>
        </div>

        <div>
          <strong>Opening Time:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableCanteenInfo.opening_time" type="time" />
          </template>
          <template v-else>
            {{ canteenInfo.opening_time || 'N/A' }}
          </template>
        </div>

        <div>
          <strong>Closing Time:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableCanteenInfo.closing_time" type="time" />
          </template>
          <template v-else>
            {{ canteenInfo.closing_time || 'N/A' }}
          </template>
        </div>

        <div class="profile-actions">
          <button @click="toggleEditProfile">
            {{ isEditingProfile ? 'Save Profile' : 'Edit Profile' }}
          </button>
          <button @click="loadReviewsDialog">View Reviews</button>
        </div>

        </div>
      </div>
    </section>

    <!-- Report Issues Section -->
    <section class="card report-section">
      <h2>Report Issues</h2>
      <div class="report-group">
        <input 
          v-model="issueText" 
          type="text" 
          placeholder="Report Issues" 
          :disabled="loading"
        />
        <button @click="submitIssue" :disabled="loading || !issueText.trim()">
          {{ loading ? 'Submitting...' : 'Submit' }}
        </button>
      </div>
    </section>

    <section class="card upload-menu-section">
    <h2>Upload Menu</h2>
    <div class="menu-grid">
        <!-- Left: Item List -->
        <div class="menu-items">
        <ul class="menu-list">
            <li v-for="(item, index) in menuItems" :key="index">
            <span>{{ item.name }}</span>
            <span>{{ item.price }}</span>
            <button @click="removeItem(index)">✕</button>
            </li>
        </ul>
        <div class="add-item">
            <input 
              v-model="newItem.name" 
              placeholder="Item name" 
              :disabled="loading"
            />
            <input 
              v-model="newItem.price" 
              placeholder="Price" 
              :disabled="loading"
            />
            <button @click="addItem" :disabled="loading || !newItem.name || !newItem.price">
              {{ loading ? '...' : '＋' }}
            </button>
        </div>
        </div>

        <!-- Divider -->
        <div class="menu-divider"></div>

        <!-- Right: Image Upload -->
        <div class="menu-images">
        <label for="menuImageUpload">Upload Menu Image(s) (max 2)</label>
        <input type="file" id="menuImageUpload" @change="handleMenuImageSelect" accept="image/*" multiple />
        <div v-for="(src, i) in menuSelectedPreviews" :key="'m'+i" style="margin-bottom:8px;">
  <img :src="src" :alt="'Menu Preview ' + (i+1)" @click="openFullscreen(src)" />
</div>
        <button @click="uploadSelectedMenuImages" :disabled="loading || menuSelectedFiles.length === 0">
          {{ loading ? 'Uploading...' : 'Upload Menu Image(s)' }}
        </button>

        <hr style="margin:12px 0;" />

        <!-- NEW: Canteen Images Upload -->
        <label for="canteenImageUpload">Upload Canteen Image(s) (max 2)</label>
        <input type="file" id="canteenImageUpload" @change="handleCanteenImageSelect" accept="image/*" multiple />
        <div v-for="(src, i) in canteenSelectedPreviews" :key="'c'+i" style="margin-bottom:8px;">
  <img :src="src" :alt="'Canteen Preview ' + (i+1)" @click="openFullscreen(src)" />
</div>
        <button @click="uploadSelectedCanteenImages" :disabled="loading || canteenSelectedFiles.length === 0">
          {{ loading ? 'Uploading...' : 'Upload Canteen Image(s)' }}
        </button>
      </div>
    </div>
    </section>

    <!-- Set Weekly Menu Section -->
    <section class="card weekly-menu-section">
      <h2>Set Weekly Menu</h2>
      <div class="day-tabs">
        <button
          v-for="(day, index) in days"
          :key="index"
          :class="{ active: selectedDay === day }"
          @click="selectedDay = day"
          :disabled="loading"
        >
          {{ day }}
        </button>
      </div>
      <div class="day-menu">
        <label>Select items for {{ selectedDay }}:</label>
        <div v-if="menuItems.length === 0" class="info-message">
          Please add menu items first before setting weekly menu.
        </div>
        <div v-else class="checkbox-list">
          <label v-for="item in menuItems" :key="item.name">
            <input
              type="checkbox"
              :value="item.name"
              v-model="weeklyMenu[selectedDay]"
              :disabled="loading"
            />
            {{ item.name }}
          </label>
        </div>
        <button 
          @click="submitDayMenu" 
          :disabled="loading || weeklyMenu[selectedDay].length === 0"
        >
          {{ loading ? 'Submitting...' : `Submit Menu for ${selectedDay}` }}
        </button>
      </div>
    </section>
    
  </div>
  <transition name="fade">
    <div v-if="showReviewDialog" class="dialog-overlay" @click.self="showReviewDialog = false">
      <div class="dialog-box">
        <h3>Reviews</h3>
        <ul class="review-list">
          <li v-for="(review, index) in reviewList" :key="index">
            <p><strong>{{ review.reviewer_name || 'Anonymous' }}</strong></p>
            <p>{{ review.review_text }}</p>
            <p>Rating: {{ review.overall_rating }} ★</p>
          </li>
        </ul>
        <button @click="showReviewDialog = false">Close</button>
      </div>
    </div>
  </transition>
  <transition name="fade">
  <div v-if="fullscreenImage" class="fullscreen-overlay" @click="closeFullscreen">
    <img :src="fullscreenImage" class="fullscreen-img" />
  </div>
</transition>
  
  <Footer />
  </div>

</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { 
  getCanteenInfoOwner, 
  addFoodItem, 
  reportIssueByOwner, 
  getCanteenReviewsOwner,
  getFoodItemsOwner,
  updateDayWiseMenu,
  uploadMenuImages,        
  uploadCanteenImages,
  updateCanteenProfile
} from '@/services/canteenOwner'

export default {
  name: 'CanteenDashboard',
  components: { Header, Footer },
  
  data() {
    return {
      // Canteen profile data
      canteenInfo: null,
      fullscreenImage: null,

      isEditingProfile: false,
      editableCanteenInfo: {},

      // Menu items list
      menuItems: [],
      foodItemsMap: {}, // Maps item name -> food_id
      newItem: { name: '', price: '' },
      
      // Weekly menu
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      selectedDay: 'Monday',
      weeklyMenu: {
        Monday: [],
        Tuesday: [],
        Wednesday: [],
        Thursday: [],
        Friday: [],
        Saturday: [],
        Sunday: []
      },
      
      // Issue reporting
      issueText: '',
      
      uploadedImage: null,       
      menuSelectedFiles: [],     
      menuSelectedPreviews: [],  
      canteenSelectedFiles: [],   
      canteenSelectedPreviews: [],
      
      loading: false,
      error: null,

      showReviewDialog: false,
      reviewList: []

    }
  },

  watch: {
  showReviewDialog(val) {
    document.body.classList.toggle('dialog-open', val)
  }
},
  
  async mounted() {
    // Load canteen info and existing food items when page loads
    await this.loadCanteenInfo()
    await this.loadFoodItems()
  },
  
  methods: {
    
    //  LOAD CANTEEN PROFILE

    openFullscreen(src) {
      this.fullscreenImage = src
    },
    closeFullscreen() {
      this.fullscreenImage = null
    },
    
    async loadCanteenInfo() {
      try {
        this.loading = true
        this.error = null
        
        const response = await getCanteenInfoOwner()
        this.canteenInfo = response.canteen_info
        
        console.log('✅ Canteen loaded:', this.canteenInfo)
      } catch (error) {
        console.error('❌ Error loading canteen:', error)
        this.error = error.response?.data?.message || 'Failed to load canteen'
        
        // Redirect to login if token expired
        if (error.response?.status === 401 || error.response?.status === 403) {
          localStorage.removeItem('token')
          this.$router.push('/desktop6')
        }
      } finally {
        this.loading = false
      }
    },

    async loadReviewsDialog() {
      try {
        this.loading = true
        const response = await getCanteenReviewsOwner()
        this.reviewList = response.reviews || []
        this.showReviewDialog = true
      } catch (error) {
        console.error('❌ Error loading reviews:', error)
        alert('❌ ' + (error.response?.data?.message || 'Failed to load reviews'))
      } finally {
        this.loading = false
      }
    },

    //  LOAD EXISTING FOOD ITEMS FROM DATABASE
    
    async loadFoodItems() {
      try {
        const response = await getFoodItemsOwner()
        const items = response.food_items || []
        
        // Populate menuItems with food_id included
        this.menuItems = items.map(item => ({
          name: item.name,
          price: item.price,
          food_id: item.food_id  // Keep the real food_id
        }))
        
        // Create mapping: name -> food_id
        items.forEach(item => {
          this.foodItemsMap[item.name] = item.food_id
        })
        
        console.log('✅ Food items loaded:', this.menuItems.length, 'items')
      } catch (error) {
        console.error('❌ Error loading food items:', error)
        // Don't show error to user - just start with empty list
      }
    },

    
    //  ADD MENU ITEM
    
    async addItem() {
      // Validate inputs
      if (!this.newItem.name || !this.newItem.price) {
        alert('⚠️ Please enter item name and price')
        return
      }

      try {
        this.loading = true
        
        // Remove ₹ symbol if user typed it
        const price = this.newItem.price.toString().replace(/[₹$]/g, '').trim()
        
        // Call backend
        const response = await addFoodItem(this.newItem.name, price)
        
        // Add to local list
        this.menuItems.push({ 
          name: this.newItem.name, 
          price: `₹${price}`,
          food_id: response.food_id
        })
        
        // Save food_id for weekly menu (needed later)
        this.foodItemsMap[this.newItem.name] = response.food_id
        
        // Clear inputs
        this.newItem.name = ''
        this.newItem.price = ''
        
        alert('✅ Item added successfully!')
      } catch (error) {
        console.error('❌ Error adding item:', error)
        alert('❌ ' + (error.response?.data?.message || 'Failed to add item'))
      } finally {
        this.loading = false
      }
    },

    
    //  REMOVE ITEM (local only)
    
    removeItem(index) {
      this.menuItems.splice(index, 1)
    },

    
    // SUBMIT WEEKLY MENU FOR A DAY
    
    async submitDayMenu() {
      // Check if canteen loaded
      if (!this.canteenInfo?.canteen_id) {
        alert('⚠️ Canteen info not loaded. Please refresh page.')
        return
      }

      // Check if items selected
      const selected = this.weeklyMenu[this.selectedDay]
      if (selected.length === 0) {
        alert('⚠️ Please select at least one item')
        return
      }

      try {
        this.loading = true
        
        // Convert item names to food_ids
        const foodIds = selected
          .map(itemName => this.foodItemsMap[itemName])
          .filter(id => id !== undefined)
        
        if (foodIds.length === 0) {
          alert('⚠️ Please add items using "Upload Menu" section first')
          return
        }

        // Call backend
        await updateDayWiseMenu(
          this.canteenInfo.canteen_id,
          this.selectedDay,
          foodIds
        )
        
        alert(`✅ Menu for ${this.selectedDay} submitted!`)
      } catch (error) {
        console.error('❌ Error updating menu:', error)
        alert('❌ ' + (error.response?.data?.message || 'Failed to update menu'))
      } finally {
        this.loading = false
      }
    },

    
    //  REPORT ISSUE
    
    async submitIssue() {
      if (!this.issueText.trim()) {
        alert('⚠️ Please enter issue description')
        return
      }

      try {
        this.loading = true
        
        await reportIssueByOwner(this.issueText)
        
        alert('✅ Issue reported successfully!')
        this.issueText = ''
      } catch (error) {
        console.error('❌ Error reporting issue:', error)
        alert('❌ ' + (error.response?.data?.message || 'Failed to report issue'))
      } finally {
        this.loading = false
      }
    },

    
    //  VIEW REVIEWS
    
    async loadReviews() {
      try {
        this.loading = true
        
        const response = await getCanteenReviewsOwner()
        const reviews = response.reviews || []
        
        alert(`📊 You have ${reviews.length} review(s)`)
        console.log('Reviews:', reviews)
      } catch (error) {
        console.error('❌ Error loading reviews:', error)
        alert('❌ ' + (error.response?.data?.message || 'Failed to load reviews'))
      } finally {
        this.loading = false
      }
    },
    async toggleEditProfile() {
  if (this.isEditingProfile) {
    try {
      this.loading = true
      
      //  updates object (only changed fields)
      const updates = {}
      
      if (this.editableCanteenInfo.name !== this.canteenInfo.name) {
        updates.name = this.editableCanteenInfo.name
      }
      if (this.editableCanteenInfo.location !== this.canteenInfo.location) {
        updates.location = this.editableCanteenInfo.location
      }
      if (this.editableCanteenInfo.contact_no !== this.canteenInfo.contact_no) {
        updates.contact_no = this.editableCanteenInfo.contact_no
      }
      if (this.editableCanteenInfo.days_open !== this.canteenInfo.days_open) {
        updates.days_open = this.editableCanteenInfo.days_open
      }
      if (this.editableCanteenInfo.opening_time !== this.canteenInfo.opening_time) {
        updates.opening_time = this.editableCanteenInfo.opening_time
      }
      if (this.editableCanteenInfo.closing_time !== this.canteenInfo.closing_time) {
        updates.closing_time = this.editableCanteenInfo.closing_time
      }
      
      // Check if anything changed
      if (Object.keys(updates).length === 0) {
        alert('ℹ️ No changes to save')
        this.isEditingProfile = false
        return
      }
      
      // Call API 
      await updateCanteenProfile(updates)  
      
      // Reload canteen info 
      await this.loadCanteenInfo()
      
      alert('✅ Profile updated successfully!')
      this.isEditingProfile = false
      
    } catch (error) {
      console.error('❌ Failed to update profile:', error)
      alert('❌ ' + (error.response?.data?.message || 'Failed to update profile'))
    } finally {
      this.loading = false
    }
  } else {
    //  copy current values
    this.editableCanteenInfo = { ...this.canteenInfo }
    this.isEditingProfile = true
  }
},

    handleMenuImageSelect(event) {
    const files = Array.from(event.target.files || []).slice(0, 2)
    this.menuSelectedFiles = files
    // release old preview object URLs to avoid memory leaks
    if (this.menuSelectedPreviews.length) {
      this.menuSelectedPreviews.forEach(url => URL.revokeObjectURL(url))
    }
    this.menuSelectedPreviews = files.map(f => URL.createObjectURL(f))
  },

  handleCanteenImageSelect(event) {
    const files = Array.from(event.target.files || []).slice(0, 2)
    this.canteenSelectedFiles = files
    if (this.canteenSelectedPreviews.length) {
      this.canteenSelectedPreviews.forEach(url => URL.revokeObjectURL(url))
    }
    this.canteenSelectedPreviews = files.map(f => URL.createObjectURL(f))
  },

  // --- Upload handlers (call service functions you added) ---
  async uploadSelectedMenuImages() {
    if (!this.canteenInfo?.canteen_id) {
      alert('Canteen ID missing. Refresh page.')
      return
    }
    if (this.menuSelectedFiles.length === 0) {
      alert('Select up to 2 menu images to upload.')
      return
    }
    try {
      this.loading = true
      const res = await uploadMenuImages(this.canteenInfo.canteen_id, this.menuSelectedFiles)
      console.log('uploadMenuImages response:', res)
      alert('Menu image(s) uploaded successfully!')
      // clear selection + previews
      this.menuSelectedFiles = []
      this.menuSelectedPreviews.forEach(url => URL.revokeObjectURL(url))
      this.menuSelectedPreviews = []
      // refresh menu info so frontend picks up new menu image URLs (if you show them elsewhere)
      await this.loadCanteenInfo()
      // optionally reload menu list if you have a fetch endpoint for menu
      // const menuData = await getFoodItemsOwner() or fetchCanteenMenu...
    } catch (err) {
      console.error('Failed to upload menu images:', err)
      alert('Failed to upload menu image(s)')
    } finally {
      this.loading = false
    }
  },

  async uploadSelectedCanteenImages() {
    if (!this.canteenInfo?.canteen_id) {
      alert('Canteen ID missing. Refresh page.')
      return
    }
    if (this.canteenSelectedFiles.length === 0) {
      alert('Select up to 2 canteen images to upload.')
      return
    }
    try {
      this.loading = true
      const res = await uploadCanteenImages(this.canteenInfo.canteen_id, this.canteenSelectedFiles)
      console.log('uploadCanteenImages response:', res)
      alert('Canteen image(s) uploaded successfully!')
      // clear selection + previews
      this.canteenSelectedFiles = []
      this.canteenSelectedPreviews.forEach(url => URL.revokeObjectURL(url))
      this.canteenSelectedPreviews = []
      // refresh canteen info to show updated images
      await this.loadCanteenInfo()
    } catch (err) {
      console.error('Failed to upload canteen images:', err)
      alert('Failed to upload canteen image(s)')
    } finally {
      this.loading = false
    }
  },
  }
}
</script>

<style scoped>
.fullscreen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  cursor: zoom-out;
}

.fullscreen-img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.page-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.dialog-box {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.dialog-box h3 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: #474747;
}

.dialog-box button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.review-list {
  list-style: none;
  padding: 0;
}

.review-list li {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 1rem;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

body.dialog-open {
  overflow: hidden;
}

.dashboard-wrapper {
  padding-top: 100px;
  max-width: 1200px;
  min-height: 100vh;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.footer {
  margin-top: auto;        /* pushes footer to bottom */
  position: relative;      /* ensure it doesn’t overlap */
}

/* Header */
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 75px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  width: 40px;
  margin-right: 1rem;
}

.app-name {
  font-size: 1.8rem;
  font-weight: 600;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  color: #474747;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  text-decoration: none;
  color: #474747;
  font-weight: 500;
}

/* Card */
.card {
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Profile */
.profile-content {
  display: flex;
  gap: 2rem;
}

.profile-image {
  width: 120px;
  height: 120px;
  background: #d9d9d9;
  border-radius: 12px;
}

.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.profile-actions button {
  margin-right: 1rem;
  padding: 0.5rem 1rem;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.profile-info input {
  margin-left: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}


/* Report */
.report-group {
  display: flex;
  gap: 1rem;
}

.report-group input {
  flex: 1;
  padding: 0.75rem;
  border-radius: 10px;
  border: none;
  background: rgba(71, 71, 71, 0.1);
}

.report-group button {
  padding: 0.75rem 1.5rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

/* Upload Menu */
.menu-list {
  list-style: none;
  padding: 0;
  margin-bottom: 1rem;
}

.menu-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.add-item {
  display: flex;
  gap: 1rem;
}

.add-item input {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.add-item button {
  padding: 0.5rem 1rem;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* Weekly Menu */
.day-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.day-tabs button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  background: #d9d9d9;
  cursor: pointer;
}

.day-tabs button.active {
  background: #474747;
  color: white;
}

.day-menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.checkbox-list label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.day-menu button {
  align-self: flex-start;
  padding: 0.5rem 1rem;
  background: #474747;
}

.menu-grid {
  display: grid;
  grid-template-columns: 1fr 2px 1fr;
  gap: 2rem;
  align-items: start;
}

.menu-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.add-item {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.add-item input {
  flex: 1;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.add-item button {
  padding: 0.5rem 1rem;
  background: #474747;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.menu-divider {
  background: rgba(71, 71, 71, 0.3);
  height: 100%;
  width: 2px;
}

.menu-images {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.menu-images label {
  font-weight: 500;
  color: #474747;
}

.menu-images input[type="file"] {
  padding: 0.5rem;
  border-radius: 8px;
  background: rgba(71, 71, 71, 0.1);
  border: none;
  color: #333;
}

.image-preview img {
  max-width: 100%;
  max-height: 300px; /* or any height you prefer */
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Loading and Error States */
.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}

.error {
  padding: 1rem;
  background: rgba(255, 0, 0, 0.1);
  color: #d32f2f;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.info-message {
  padding: 1rem;
  background: rgba(33, 150, 243, 0.1);
  color: #1976d2;
  border-radius: 8px;
  margin-bottom: 1rem;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
