<template>
  <div class="page-wrapper">
    <!-- Header -->
    <Header />
  <div class="search-results-wrapper">
    <!-- Results Panels -->
    <main class="results-panels">
      <!-- Canteens Panel -->
      <section class="card canteen-panel">
        <h2>Canteens</h2>
        <div class="canteen-list">
          <div 
            class="canteen-entry" v-for="canteen in filteredCanteens" 
            :key="canteen.name"
            @click="goToCanteen(canteen.canteen_id)"
            style="cursor: pointer;">
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
    <div class="item-entry" v-for="(item, index) in allFoodItems" :key="index">
      <p><strong>{{ item.foodName }}</strong> — {{ item.price }}</p>
      <p style="font-size: 0.9rem; color: #666;">📍 {{ item.canteenName }}</p>
    </div>
  </div>
</section>
    </main>

  </div>
  <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { searchCanteens, searchFoodItems } from '@/services/search.js'

export default {
  name: 'SearchResults',
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
        c.name.toLowerCase().includes(query) ||
        c.location.toLowerCase().includes(query) ||
        c.items.some(item => item.name.toLowerCase().includes(query))
      )
    },
    allFoodItems() {
    const items = []
    this.canteens.forEach(canteen => {
      canteen.items.forEach(item => {
        items.push({
          foodName: item.name,
          price: item.price,
          canteenName: canteen.name
        })
      })
    })
    return items
  }
  },
  watch: {
    // Watch for changes in the URL query parameter
    '$route.query.q': {
      handler(newQuery, oldQuery) {
        console.log('Query changed from', oldQuery, 'to', newQuery)
        // Re-run search when query changes
        if (newQuery) {
          this.performSearch()
        }
      },
      immediate: true // Run immediately on component load
    }
  },
  methods: {
    getStars(rating) {
      return '★'.repeat(rating) + '☆'.repeat(5 - rating)
    },
    goToCanteen(canteenId) {
      if (!canteenId) {
         alert('Canteen ID not available')
         return
      }
      this.$router.push(`/desktop27?canteen_id=${canteenId}`)
    },
    
    async performSearch() {
      const query = this.$route.query.q
      if (!query) return

      this.searchQuery = query
      try {
        // Call both APIs in parallel
        const [canteensResponse, foodResponse] = await Promise.all([
          searchCanteens(query),
          searchFoodItems(query)
        ])
        console.log('Canteens Response:', canteensResponse)
        console.log('Food Response:', foodResponse)
        console.log('Canteens List:', canteensResponse.results)
        console.log('Food List:', foodResponse.results)

        // Extract results arrays
        const canteensList = canteensResponse.results || []
        const foodList = foodResponse.results || []

        // Create a map to merge canteens with their food items
        const canteenMap = {}

        // Add all canteens to map
        canteensList.forEach(canteen => {
          canteenMap[canteen.canteen_name] = {
             canteen_id: canteen.canteen_id,  //canteen was required 
            name: canteen.canteen_name,
            location: canteen.location,
            timings: canteen.timings,
            rating: Math.round(canteen.overall_rating || 0),
            items: []
          }
        })

        // Add food items to their canteens
        foodList.forEach(food => {
          const canteenName = food.canteen_name
          
          if (!canteenMap[canteenName]) {
            // Create canteen entry from food search results (includes canteen details)
            canteenMap[canteenName] = {
              canteen_id: food.canteen_id,
              name: canteenName,
              location: food.location || 'N/A',
              timings: food.opening_time && food.closing_time 
                ? `${food.opening_time} - ${food.closing_time}` 
                : 'N/A',
              rating: Math.round(food.overall_rating || 0),
              items: []
            }
          }
          
          canteenMap[canteenName].items.push({
            name: food.food_name,
            price: `₹${food.price}`
          })
        })

        // Convert map to array
        this.canteens = Object.values(canteenMap)

      } catch (error) {
        console.error('Search failed:', error)
        alert('Search failed. Please try again.')
      }
    }
  },
  
}
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.search-results-wrapper {
  padding-top: 100px;
  max-width: 1200px;
  width: 100%;
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
  cursor: pointer;  /* added some css */
  transition: transform 0.2s, box-shadow 0.2s;
}
/* added hover effect */
.canteen-entry:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
  background: rgba(255, 255, 255, 0.5);
}

.scroll-arrows {
  text-align: center;
  font-size: 1.5rem;
  margin-top: 1rem;
  color: #474747;
}

.footer{
  margin-top: auto;       
  position: relative; 
}

</style>
