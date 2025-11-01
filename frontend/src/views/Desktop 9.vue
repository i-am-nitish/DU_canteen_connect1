<template>
  <div class="dashboard-wrapper">
    <!-- Header -->
    <Header />

    <!-- Profile Section -->
    <section class="card profile-section">
      <h2>Profile</h2>
      <div class="profile-content">
        <div class="profile-image"></div>
        <div class="profile-info">
          <div>Name</div>
          <div>Location</div>
          <div>Canteen Info</div>
          <div class="profile-actions">
            <button>Edit Profile</button>
            <button>View Routes</button>
          </div>
        </div>
      </div>
    </section>

    <!-- Report Issues Section -->
    <section class="card report-section">
      <h2>Report Issues</h2>
      <div class="report-group">
        <input type="text" placeholder="Report Issues" />
        <button>Submit</button>
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
            <input v-model="newItem.name" placeholder="Item name" />
            <input v-model="newItem.price" placeholder="Price" />
            <button @click="addItem">＋</button>
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
        >
          {{ day }}
        </button>
      </div>
      <div class="day-menu">
        <label>Select items for {{ selectedDay }}:</label>
        <div class="checkbox-list">
          <label v-for="item in menuItems" :key="item.name">
            <input
              type="checkbox"
              :value="item.name"
              v-model="weeklyMenu[selectedDay]"
            />
            {{ item.name }}
          </label>
        </div>
        <button @click="submitDayMenu">Submit Menu for {{ selectedDay }}</button>
      </div>
    </section>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'CanteenDashboard',
  components: { Header, Footer },
  data() {
    return {
      menuItems: [
        { name: 'item1', price: '₹50' },
        { name: 'item2', price: '₹30' },
        { name: 'item3', price: '₹40' }
      ],
      newItem: { name: '', price: '' },
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      selectedDay: 'Monday',
      uploadedImage: null,
      weeklyMenu: {
        Monday: [],
        Tuesday: [],
        Wednesday: [],
        Thursday: [],
        Friday: [],
        Saturday: [],
        Sunday: []
      }
    }
  },
  methods: {
    addItem() {
      if (this.newItem.name && this.newItem.price) {
        this.menuItems.push({ ...this.newItem })
        this.newItem.name = ''
        this.newItem.price = ''
      }
    },
    removeItem(index) {
      this.menuItems.splice(index, 1)
    },
    submitDayMenu() {
      alert(`Menu for ${this.selectedDay} submitted: ${this.weeklyMenu[this.selectedDay].join(', ')}`)
    },
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


</style>
