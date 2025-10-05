<template>
  <div class="wrapper">
    <Header />

    <div class="public-container">
      <!-- Left Section -->
      <div class="canteens-section">
        <h3>Canteens Around You</h3>
        <div class="canteen-grid">
          <div class="canteen-card" v-for="canteen in canteens" :key="canteen.id" @click="goToCanteen(canteen.id)">
            <h4>{{ canteen.name }}</h4>
            <p><strong>Location:</strong> {{ canteen.location }}</p>
            <p><strong>Timings:</strong> {{ canteen.timings }}</p>
            <p><strong>Rating:</strong> ⭐ {{ canteen.rating }}</p>
            <div class="click-hint">Click to view this canteen</div>
          </div>
        </div>
        <button class="view-all-btn" @click="goToCanteens">View All Canteens</button>
      </div>

      <!-- Divider -->
      <div class="divider"></div>

      <!-- Right Section -->
      <div class="menu-section">
        <h3>Today's Menu</h3>
        <div class="menu-images">
          <!-- Placeholder for menu images -->
          <p style="color: #999;">Menu images will appear here soon...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/Header.vue'

export default {
  components: { Header },
  data() {
    return {
      canteens: [
        { 
          id: 1,
          name: 'Central Canteen', 
          location: 'Arts Faculty, North Campus', 
          timings: '7:00 AM - 9:00 PM', 
          rating: '4.5/5' 
        },
        { 
          id: 2,
          name: 'Science Faculty Canteen', 
          location: 'Science Faculty, North Campus', 
          timings: '8:00 AM - 6:00 PM', 
          rating: '4.2/5' 
        },
        { 
          id: 3,
          name: 'Ramjas College Canteen', 
          location: 'Ramjas College, North Campus', 
          timings: '9:00 AM - 7:00 PM', 
          rating: '4.3/5' 
        },
        { 
          id: 4,
          name: 'LSR College Canteen', 
          location: 'Lady Shri Ram College, South Campus', 
          timings: '8:00 AM - 6:30 PM', 
          rating: '4.6/5' 
        }
      ]
    }
  },
  methods: {
    goToCanteens() {
      this.$router.push('/canteenpage')
    },
    goToCanteen(canteenId) {
      this.$router.push(`/canteen/${canteenId}`)
    }
  }
}
</script>

<style scoped>
.wrapper {
  padding-top: 60px;
}

.public-container {
  display: flex;
  max-width: 1000px;
  margin: 4rem auto;
  background: rgba(219, 223, 208, 0.18);
  border-radius: 25px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  padding: 2rem;
  position: relative;
}

.canteens-section,
.menu-section {
  flex: 1;
  padding: 1rem;
}

.divider {
  width: 2px;
  background-color: #696D5F;
  margin: 0 1rem;
}

.canteen-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.canteen-card {
  background: rgba(71, 71, 71, 0.41);
  color: white;
  padding: 1rem;
  border-radius: 15px;
  backdrop-filter: blur(2px);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.canteen-card:hover {
  background: rgba(71, 71, 71, 0.6);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.click-hint {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

.view-all-btn {
  width: 100%;
  margin-top: 1.5rem;
  padding: 1rem;
  background: linear-gradient(45deg, #3498db, #2ecc71);
  color: white;
  border: none;
  border-radius: 15px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-all-btn:hover {
  background: linear-gradient(45deg, #2980b9, #27ae60);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.menu-images {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  border: 2px dashed #ccc;
  border-radius: 15px;
  padding: 2rem;
}
</style>

