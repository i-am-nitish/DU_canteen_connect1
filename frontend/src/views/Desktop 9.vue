<template>
  <div class="dashboard-wrapper">
    <!-- Header -->
    <Header />

    <!-- canteen Profile Section -->
    <section class="card profile-section">
      <h2>Profile</h2>
      <div v-if="loading && !canteenInfo" class="loading">Loading canteen info...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="canteenInfo" class="profile-content">
        <div class="profile-image"></div>
        <div class="profile-info">
          <div><strong>Name:</strong> {{ canteenInfo.name || 'N/A' }}</div>
          <div><strong>Location:</strong> {{ canteenInfo.location || 'N/A' }}</div>
          <div><strong>Contact:</strong> {{ canteenInfo.contact_no || 'N/A' }}</div>
          <div><strong>Days Open:</strong> {{ canteenInfo.days_open || 'N/A' }}</div>
          <div><strong>Opening Time:</strong> {{ canteenInfo.opening_time || 'N/A' }}</div>
          <div><strong>Closing Time:</strong> {{ canteenInfo.closing_time || 'N/A' }}</div>
          <div class="profile-actions">
            <button>Edit Profile</button>
            <button @click="loadReviews">View Reviews</button>
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
        <label for="menuImageUpload">Upload Menu Image</label>
        <input type="file" id="menuImageUpload" @change="handleImageUpload" />
        <div v-if="uploadedImage" class="image-preview">
            <img :src="uploadedImage" alt="Menu Preview" />
        </div>
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

    <!-- Footer -->
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
  updateDayWiseMenu 
} from '@/services/canteenOwner'

export default {
  name: 'CanteenDashboard',
  components: { Header, Footer },
  
  data() {
    return {
      // Canteen profile data
      canteenInfo: null,
      
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
      
      // Image upload (UI only, not saved to backend)
      uploadedImage: null,
      
      // Loading and error states
      loading: false,
      error: null
    }
  },
  
  async mounted() {
    // Load canteen info and existing food items when page loads
    await this.loadCanteenInfo()
    await this.loadFoodItems()
  },
  
  methods: {
    
    //  LOAD CANTEEN PROFILE
    
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

    
    //  IMAGE UPLOAD (UI only)
    
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.uploadedImage = URL.createObjectURL(file)
      }
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  padding-top: 100px;
  max-width: 1200px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
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
