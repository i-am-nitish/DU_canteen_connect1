<template>
  <div class="wrapper">
    <Header />

    <div class="public-container">
      <!-- Left Section -->
      <div class="canteens-section">
        <h3>Canteens Around You</h3>
        <div class="canteen-grid">
          <div class="canteen-card" v-for="canteen in canteens" :key="canteen.name">
            <h4>{{ canteen.name }}</h4>
            <p><strong>Location:</strong> {{ canteen.location }}</p>
            <p><strong>Timings:</strong> {{ canteen.timings }}</p>
            <p><strong>Rating:</strong> ⭐ {{ canteen.rating }}</p>
          </div>
        </div>
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
        { name: 'Name', location: 'Location', timings: 'Timing', rating: 'Ratings' }
      ]
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

