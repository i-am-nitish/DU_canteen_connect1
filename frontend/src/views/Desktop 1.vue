<template>
  <div class="home-dashboard">
    <Header />

    <!-- Main Content -->
    <main class="main-panels">
      <!-- Canteens Around You -->
      <section class="card canteen-section">
        <h2>Canteens around you</h2>
        <p style="color: #666; padding: 10px;">Total canteens: {{ canteens.length }}</p>
        <div class="canteen-grid">
          <div class="canteen-box" v-for="canteen in filteredCanteens" :key="canteen.canteen_id">
            <p><strong>Name:</strong> {{ canteen.name }}</p>
            <p><strong>Location:</strong> {{ canteen.location }}</p>
            <p><strong>Timings:</strong> {{ canteen.opening_time }} – {{ canteen.closing_time }}</p>
            <p><strong>Rating:</strong> {{ getStars(canteen.overall_rating) }}</p>
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
import { fetchAllCanteens } from '@/services/canteen.js'

export default {
  name: 'HomeDashboard',
  components: { Header, Footer },
  data() {
    return {
      searchQuery: '',
      canteens: []
    }
  },
  computed: {
    filteredCanteens() {
      if (!this.searchQuery) return this.canteens
      const query = this.searchQuery.toLowerCase()
      return this.canteens.filter(c =>
        c.name?.toLowerCase().includes(query) ||
        c.location?.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    getStars(rating) {
      return '★'.repeat(rating) + '☆'.repeat(5 - rating)
    },
    async loadCanteens() {
      try {
        console.log('Fetching canteens...')
        const data = await fetchAllCanteens()
        console.log('Canteens received:', data)
        this.canteens = data
        console.log('this.canteens now:', this.canteens)
      } catch (error) {
        console.error('Error loading canteens:', error)
      }
    }
  },
  mounted() {
    this.loadCanteens()
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
