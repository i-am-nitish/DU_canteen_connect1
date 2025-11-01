<template>
  <div class="search-results-wrapper">
    <!-- Header -->
    <Header />

    <!-- Results Panels -->
    <main class="results-panels">
      <!-- Canteens Panel -->
      <section class="card canteen-panel">
        <h2>Canteens</h2>
        <div class="canteen-list">
          <div class="canteen-entry" v-for="canteen in filteredCanteens" :key="canteen.name">
            <p><strong>Name:</strong> {{ canteen.name }}</p>
            <p><strong>Location:</strong> {{ canteen.location }}</p>
            <p><strong>Timings:</strong> {{ canteen.timings }}</p>
            <p><strong>Rating:</strong> {{ getStars(canteen.rating) }}</p>
          </div>
        </div>
      </section>

      <!-- Items Panel -->
      <section class="card items-panel">
        <h2>Items</h2>
        <div class="item-list">
          <div class="item-entry" v-for="canteen in filteredCanteens" :key="canteen.name">
            <p><strong>{{ canteen.name }}</strong></p>
            <ul>
              <li v-for="(item, index) in canteen.items" :key="index">
                {{ item.name }} — {{ item.price }}
              </li>
            </ul>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

export default {
  name: 'SearchResults',
  components: { Header, Footer },
  data() {
    return {
      searchQuery: '',
      canteens: [
        {
          name: 'Canteen1',
          location: 'North Campus',
          timings: '9 AM – 6 PM',
          rating: 4,
          items: [
            { name: 'item1', price: '₹50' },
            { name: 'item2', price: '₹30' }
          ]
        },
        {
          name: 'Canteen2',
          location: 'South Campus',
          timings: '10 AM – 5 PM',
          rating: 5,
          items: [
            { name: 'item3', price: '₹40' },
            { name: 'item4', price: '₹35' }
          ]
        }
      ]
    }
  },
  computed: {
    filteredCanteens() {
      if (!this.searchQuery) return this.canteens
      const query = this.searchQuery.toLowerCase()
      return this.canteens.filter(c =>
        c.name.toLowerCase().includes(query) ||
        c.location.toLowerCase().includes(query) ||
        c.items.some(item => item.name.toLowerCase().includes(query))
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
.search-results-wrapper {
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

.searchbar {
  width: 30%;
  height: 40px;
  border-radius: 20px;
  border: none;
  background: #d9d9d9;
  padding: 0 1rem;
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

/* Panels */
.results-panels {
  display: flex;
  gap: 2rem;
}

.card {
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  flex: 1;
}

.canteen-entry,
.item-entry {
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.3);
  padding: 1rem;
  border-radius: 12px;
}

.scroll-arrows {
  text-align: center;
  font-size: 1.5rem;
  margin-top: 1rem;
  color: #474747;
}

/* Footer */
.footer {
  width: 100%;
  background: #474747;
  color: #DBDFD0;
  display: flex;
  justify-content: space-between;
  padding: 2rem;
  border-radius: 20px;
}

.footer-left,
.footer-right {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
