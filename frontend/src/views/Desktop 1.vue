<template>
  <div class="home-dashboard">
    <Header />

    <!-- Main Content -->
    <main class="main-panels">
      <!-- Canteens Around You -->
      <section class="card canteen-section">
        <h2>Canteens around you</h2>
        <div class="canteen-grid">
          <div class="canteen-box" v-for="(canteen, index) in filteredCanteens" :key="index">
            <p><strong>Name:</strong> {{ canteen.name }}</p>
            <p><strong>Location:</strong> {{ canteen.location }}</p>
            <p><strong>Timings:</strong> {{ canteen.timings }}</p>
            <p><strong>Rating:</strong> {{ getStars(canteen.rating) }}</p>
            <div class="arrow">→</div>
          </div>
        </div>
      </section>

      <!-- Today's Menus -->
      <section class="card menu-section">
        <h2>Today's Menus</h2>
        <div class="menu-grid">
          <div class="menu-box" v-for="n in 6" :key="n">
            <div class="image-placeholder"></div>
          </div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'HomeDashboard',
  components: { Header, Footer },
  data() {
    return {
      searchQuery: '',
      canteens: [
        { name: 'Canteen A', location: 'North Campus', timings: '9 AM – 6 PM', rating: 4 },
        { name: 'Canteen B', location: 'South Campus', timings: '10 AM – 5 PM', rating: 5 },
        { name: 'Canteen C', location: 'East Block', timings: '8 AM – 4 PM', rating: 3 },
        { name: 'Canteen D', location: 'West Wing', timings: '11 AM – 7 PM', rating: 4 }
      ]
    }
  },
  computed: {
    filteredCanteens() {
      if (!this.searchQuery) return this.canteens
      const query = this.searchQuery.toLowerCase()
      return this.canteens.filter(c =>
        c.name.toLowerCase().includes(query) ||
        c.location.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    getStars(rating) {
      return '★'.repeat(rating) + '☆'.repeat(5 - rating)
    }
  }
}
</script>

<style scoped>
.home-dashboard {
  padding-top: 100px;
  max-width: 1200px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Panels */
.main-panels {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

/* Card */
.card {
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  flex: 1;
}

/* Canteens */
.canteen-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.canteen-box {
  background: rgba(255, 255, 255, 0.3);
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

.arrow {
  position: absolute;
  bottom: 10px;
  right: 10px;
  font-size: 1.5rem;
  color: #474747;
}

/* Menus */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.menu-box {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  font-size: 2rem;
  color: #333;
}

</style>
