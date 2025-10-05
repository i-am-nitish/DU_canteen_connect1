<template>
  <div class="canteen-page">
    <!-- Main Content -->
    <div class="main-content">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="page-title">Delhi University Canteens</h1>
        <p class="page-description">
          Discover delicious and affordable meals across all DU campuses. Choose from a variety of canteens offering different cuisines and specialties.
        </p>
      </div>

      <!-- Filter Section Only -->
      <div class="filter-section">
        <div class="filter-buttons">
          <button 
            class="filter-btn" 
            :class="{ active: selectedFilter === 'all' }"
            @click="filterByType('all')"
          >
            All Canteens
          </button>
          <button 
            class="filter-btn" 
            :class="{ active: selectedFilter === 'north-campus' }"
            @click="filterByType('north-campus')"
          >
            North Campus
          </button>
          <button 
            class="filter-btn" 
            :class="{ active: selectedFilter === 'south-campus' }"
            @click="filterByType('south-campus')"
          >
            South Campus
          </button>
          <button 
            class="filter-btn" 
            :class="{ active: selectedFilter === 'open-now' }"
            @click="filterByType('open-now')"
          >
            Open Now
          </button>
        </div>
      </div>

      <!-- Canteens Grid -->
      <div class="canteens-section">
        <div class="canteen-grid">
          <div class="canteen-card" v-for="canteen in filteredCanteens" :key="canteen.id" @click="goToCanteen(canteen.id)">
            <h4>{{ canteen.name }}</h4>
            <p><strong>Location:</strong> {{ canteen.location }}</p>
            <p><strong>Timings:</strong> {{ canteen.timing }}</p>
            <p><strong>Rating:</strong> ⭐ {{ canteen.rating }}/5</p>
            <p><strong>Cuisine:</strong> {{ canteen.cuisine }}</p>
            <p><strong>Price Range:</strong> {{ canteen.priceRange }}</p>
            <div class="status-badge" :class="canteen.status">
              {{ canteen.status === 'open' ? 'Open' : 'Closed' }}
            </div>
            <div class="click-hint">Click to view menu and details</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<script>
import { inject, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppFooter from '@/components/Footer.vue'

export default {
  name: 'CanteenPage',
  components: {
    AppFooter
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // Inject search query from App.vue
    const headerSearchQuery = inject('searchQuery')
    
    // Local reactive data
    const selectedFilter = ref('all')
    
    // Initialize search from route query if present
    if (route.query.search) {
      headerSearchQuery.value = route.query.search
    }

    const canteens = ref([
        {
          id: 1,
          name: 'Central Canteen',
          description: 'The main dining facility offering diverse cuisines and fresh meals for students and faculty.',
          location: 'North Campus - Arts Faculty',
          timing: '7:00 AM - 9:00 PM',
          rating: 4.5,
          reviews: 324,
          cuisine: 'Multi-cuisine',
          status: 'open',
          campus: 'north-campus',
          priceRange: '₹30 - ₹120',
          image: 'https://via.placeholder.com/400x250/FFB6C1/000000?text=Central+Canteen',
          specialties: ['Rajma Chawal', 'Chicken Curry', 'Fresh Parathas', 'Samosas']
        },
        {
          id: 2,
          name: 'Science Faculty Canteen',
          description: 'Quick bites and healthy meals for the science community with focus on nutritious options.',
          location: 'North Campus - Science Faculty',
          timing: '8:00 AM - 6:00 PM',
          rating: 4.2,
          reviews: 189,
          cuisine: 'North Indian, Snacks',
          status: 'open',
          campus: 'north-campus',
          priceRange: '₹20 - ₹80',
          image: 'https://via.placeholder.com/400x250/98FB98/000000?text=Science+Canteen',
          specialties: ['Maggi', 'Sandwiches', 'Tea & Coffee', 'Pakoras']
        },
        {
          id: 3,
          name: 'Ramjas College Canteen',
          description: 'Popular student hangout spot known for affordable meals and vibrant atmosphere.',
          location: 'North Campus - Ramjas College',
          timing: '9:00 AM - 7:00 PM',
          rating: 4.3,
          reviews: 267,
          cuisine: 'Street Food, Indian',
          status: 'open',
          campus: 'north-campus',
          priceRange: '₹15 - ₹70',
          image: 'https://via.placeholder.com/400x250/F0E68C/000000?text=Ramjas+Canteen',
          specialties: ['Chole Bhature', 'Momos', 'Burger', 'Lassi']
        },
        {
          id: 4,
          name: 'Hindu College Cafeteria',
          description: 'Modern cafeteria with contemporary seating and fusion food options.',
          location: 'North Campus - Hindu College',
          timing: '8:30 AM - 8:00 PM',
          rating: 4.4,
          reviews: 156,
          cuisine: 'Continental, Indian',
          status: 'open',
          campus: 'north-campus',
          priceRange: '₹40 - ₹150',
          image: 'https://via.placeholder.com/400x250/DDA0DD/000000?text=Hindu+College',
          specialties: ['Pasta', 'Pizza', 'Wraps', 'Fresh Juices']
        },
        {
          id: 5,
          name: 'LSR College Canteen',
          description: 'Cozy canteen serving home-style meals with a focus on healthy and hygienic food.',
          location: 'South Campus - Lady Shri Ram College',
          timing: '8:00 AM - 6:30 PM',
          rating: 4.6,
          reviews: 203,
          cuisine: 'Home-style, Healthy',
          status: 'open',
          campus: 'south-campus',
          priceRange: '₹25 - ₹90',
          image: 'https://via.placeholder.com/400x250/F4A460/000000?text=LSR+Canteen',
          specialties: ['Dal Rice', 'Roti Sabzi', 'Fruit Salad', 'Buttermilk']
        },
        {
          id: 6,
          name: 'Venkateshwara College Food Court',
          description: 'Multi-vendor food court offering variety of cuisines and quick service.',
          location: 'South Campus - Venkateshwara College',
          timing: '9:00 AM - 8:00 PM',
          rating: 4.1,
          reviews: 145,
          cuisine: 'Multi-cuisine, Fast Food',
          status: 'open',
          campus: 'south-campus',
          priceRange: '₹30 - ₹200',
          image: 'https://via.placeholder.com/400x250/FFE4B5/000000?text=Venky+Food+Court',
          specialties: ['Biryani', 'Chinese', 'South Indian', 'Ice Cream']
        },
        {
          id: 7,
          name: 'Gargi College Canteen',
          description: 'Student-friendly canteen known for pocket-friendly prices and tasty snacks.',
          location: 'South Campus - Gargi College',
          timing: '8:00 AM - 5:00 PM',
          rating: 4.0,
          reviews: 112,
          cuisine: 'Snacks, Indian',
          status: 'closed',
          campus: 'south-campus',
          priceRange: '₹10 - ₹60',
          image: 'https://via.placeholder.com/400x250/FFB6C1/000000?text=Gargi+Canteen',
          specialties: ['Samosa', 'Kachori', 'Chai', 'Biscuits']
        },
        {
          id: 8,
          name: 'Miranda House Dining Hall',
          description: 'Traditional dining hall with emphasis on nutritious meals and clean environment.',
          location: 'North Campus - Miranda House',
          timing: '7:30 AM - 8:30 PM',
          rating: 4.7,
          reviews: 189,
          cuisine: 'Traditional Indian',
          status: 'open',
          campus: 'north-campus',
          priceRange: '₹35 - ₹100',
          image: 'https://via.placeholder.com/400x250/98FB98/000000?text=Miranda+Dining',
          specialties: ['Thali', 'Fresh Rotis', 'Seasonal Vegetables', 'Kheer']
      }
    ])

    const filteredCanteens = computed(() => {
      let filtered = canteens.value

      // Filter by search query from header
      if (headerSearchQuery.value) {
        const query = headerSearchQuery.value.toLowerCase()
        filtered = filtered.filter(canteen => 
          canteen.name.toLowerCase().includes(query) ||
          canteen.location.toLowerCase().includes(query) ||
          canteen.cuisine.toLowerCase().includes(query) ||
          canteen.specialties.some(specialty => specialty.toLowerCase().includes(query))
        )
      }

      // Filter by selected filter
      if (selectedFilter.value !== 'all') {
        if (selectedFilter.value === 'open-now') {
          filtered = filtered.filter(canteen => canteen.status === 'open')
        } else {
          filtered = filtered.filter(canteen => canteen.campus === selectedFilter.value)
        }
      }

      return filtered
    })

    function filterByType(type) {
      selectedFilter.value = type
    }

    function goToCanteen(canteenId) {
      router.push(`/canteen/${canteenId}`)
    }

    function viewCanteenMenu(canteenId) {
      const canteen = canteens.value.find(c => c.id === canteenId)
      if (canteen) {
        alert(`🍽️ Opening menu for ${canteen.name}!\n\n📍 Location: ${canteen.location}\n⭐ Rating: ${canteen.rating}/5\n🍽️ Cuisine: ${canteen.cuisine}\n💰 Price Range: ${canteen.priceRange}\n\n🔜 Individual menu pages coming soon!`)
      }
    }

    return {
      selectedFilter,
      canteens,
      filteredCanteens,
      filterByType,
      goToCanteen,
      viewCanteenMenu
    }
  }
}
</script>

<style scoped>
.canteen-page {
  min-height: 100vh;
  padding-top: 65px; /* Account for fixed header */
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Page Header */
.page-header {
  background: rgba(219, 223, 208, 0.18);
  border-radius: 25px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
}

.page-title {
  font-size: 3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-family: 'Playfair Display', serif;
}

.page-description {
  font-size: 1.2rem;
  color: #5a6c7d;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
}

/* Search and Filter Section */
.filter-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.filter-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.filter-btn {
  background: rgba(255, 255, 255, 0.2);
  color: #2c3e50;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.filter-btn.active {
  background: rgba(52, 152, 219, 0.8);
  color: white;
}

/* Canteens Section */
.canteens-section {
  background: rgba(219, 223, 208, 0.18);
  border-radius: 25px;
  padding: 2rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.canteen-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.canteen-card {
  background: rgba(71, 71, 71, 0.41);
  color: white;
  padding: 1.5rem;
  border-radius: 15px;
  backdrop-filter: blur(2px);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  min-height: 200px;
}

.canteen-card:hover {
  background: rgba(71, 71, 71, 0.6);
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.3);
}

.canteen-card h4 {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #ffffff;
  font-family: 'Playfair Display', serif;
}

.canteen-card p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.canteen-card strong {
  color: #e8f5e8;
}

.status-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.status-badge.open {
  background: #2ecc71;
  color: white;
}

.status-badge.closed {
  background: #e74c3c;
  color: white;
}

.click-hint {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2.2rem;
  }
  
  .page-description {
    font-size: 1rem;
  }
  
  .search-bar {
    flex-direction: column;
  }
  
  .filter-buttons {
    gap: 0.5rem;
  }
  
  .filter-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
  
  .canteens-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .canteen-card {
    margin: 0;
  }
  
  .canteen-content {
    padding: 1.5rem;
  }
  
  .canteen-name {
    font-size: 1.3rem;
  }
  
  .specialty-tags {
    gap: 0.3rem;
  }
  
  .specialty-tag {
    font-size: 0.75rem;
    padding: 0.25rem 0.6rem;
  }
  
  .canteen-actions {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .view-menu-btn {
    width: 100%;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .page-header,
  .search-filter-section,
  .canteens-section {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .search-bar input {
    padding: 0.8rem 1rem;
  }
  
  .filter-buttons {
    flex-direction: column;
  }
  
  .filter-btn {
    width: 100%;
  }
  
  .canteen-image {
    height: 200px;
  }
  
  .meta-item {
    font-size: 0.85rem;
  }
  
  .canteen-actions {
    text-align: center;
  }
}
</style>
