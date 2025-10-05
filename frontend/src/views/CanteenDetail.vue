<template>
  <div class="canteen-detail-page">
    <!-- Main Content -->
    <div class="main-content">
      <div class="canteen-detail-container">
        <!-- Left Section -->
        <div class="left-section">
          <!-- Canteen Info Card -->
          <div class="canteen-info-card">
            <h2 class="canteen-name">{{ canteen.name }}</h2>
            <div class="canteen-image-placeholder">
              <img :src="canteen.image" :alt="canteen.name" class="canteen-image" />
            </div>
            <div class="canteen-details">
              <p><strong>Location:</strong> {{ canteen.location }}</p>
              <p><strong>Description:</strong> {{ canteen.description }}</p>
              <p><strong>Contact Info:</strong> {{ canteen.contact }}</p>
              <div class="hours-rating">
                <p><strong>Days:</strong> {{ canteen.days }}</p>
                <p><strong>Timings:</strong> {{ canteen.timing }}</p>
                <p><strong>Status:</strong> <span :class="canteen.status">{{ canteen.status === 'open' ? 'Open' : 'Closed' }}</span></p>
                <div class="rating">
                  <strong>Rating:</strong>
                  <span class="stars">
                    <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= canteen.ratingStars }">★</span>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Menu Section -->
          <div class="menu-section">
            <h3>Menu</h3>
            <div class="menu-grid">
              <div class="menu-column">
                <div class="menu-item" v-for="(item, index) in canteen.menuItems.slice(0, Math.ceil(canteen.menuItems.length/2))" :key="index">
                  <span class="item-name">{{ item.name }}</span>
                  <span class="item-price">{{ item.price }}</span>
                </div>
              </div>
              <div class="menu-column">
                <div class="menu-item" v-for="(item, index) in canteen.menuItems.slice(Math.ceil(canteen.menuItems.length/2))" :key="index">
                  <span class="item-name">{{ item.name }}</span>
                  <span class="item-price">{{ item.price }}</span>
                </div>
              </div>
            </div>
            <div class="menu-images">
              <div class="menu-image-placeholder" v-for="n in 3" :key="n">
                <div class="image-icon">🖼️</div>
              </div>
            </div>
          </div>

          <!-- Reviews Section -->
          <div class="reviews-section">
            <h3>Reviews and Ratings</h3>
            <div class="overall-rating">
              <strong>Overall Rating</strong>
              <span class="stars">
                <span v-for="star in 5" :key="star" class="star filled">★</span>
              </span>
            </div>
            <div class="individual-reviews">
              <div class="review-item" v-for="review in canteen.reviews" :key="review.id">
                <div class="review-rating">
                  <span class="stars">
                    <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= review.rating }">★</span>
                  </span>
                  <span class="review-text">{{ review.text }}</span>
                </div>
                <div class="review-images">
                  <div class="review-image-placeholder" v-for="img in review.images" :key="img">
                    <div class="image-icon">🖼️</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Section - Map -->
        <div class="right-section">
          <div class="map-container">
            <h3>Map</h3>
            <div class="map-placeholder">
              <div class="map-content">
                <div class="map-icon">🗺️</div>
                <p>Interactive map showing {{ canteen.name }} location</p>
                <p>{{ canteen.location }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<script>
import AppFooter from '@/components/Footer.vue'

export default {
  name: 'CanteenDetail',
  components: {
    AppFooter
  },
  props: ['id'],
  data() {
    return {
      canteens: [
        {
          id: 1,
          name: 'Central Canteen',
          description: 'The main dining facility offering diverse cuisines and fresh meals for students and faculty.',
          location: 'Arts Faculty, North Campus',
          timing: '7:00 AM - 9:00 PM',
          days: 'Monday - Sunday',
          contact: '+91 11 2766-1234',
          rating: 4.5,
          ratingStars: 5,
          status: 'open',
          image: 'https://via.placeholder.com/300x200/FFB6C1/000000?text=Central+Canteen',
          menuItems: [
            { name: 'Rajma Chawal', price: '₹65' },
            { name: 'Chicken Curry', price: '₹120' },
            { name: 'Paneer Butter Masala', price: '₹90' },
            { name: 'Chole Bhature', price: '₹70' },
            { name: 'Biryani', price: '₹130' },
            { name: 'Dal Tadka', price: '₹50' },
            { name: 'Roti (2 pcs)', price: '₹15' },
            { name: 'Fresh Salad', price: '₹40' }
          ],
          reviews: [
            { id: 1, rating: 5, text: 'Excellent food quality and service!', images: 3 },
            { id: 2, rating: 4, text: 'Good variety, reasonable prices.', images: 2 },
            { id: 3, rating: 5, text: 'Best canteen in North Campus!', images: 0 },
            { id: 4, rating: 4, text: 'Fresh ingredients, hygienic preparation.', images: 2 }
          ]
        },
        {
          id: 2,
          name: 'Science Faculty Canteen',
          description: 'Quick bites and healthy meals for the science community with focus on nutritious options.',
          location: 'Science Faculty, North Campus',
          timing: '8:00 AM - 6:00 PM',
          days: 'Monday - Saturday',
          contact: '+91 11 2766-5678',
          rating: 4.2,
          ratingStars: 4,
          status: 'open',
          image: 'https://via.placeholder.com/300x200/98FB98/000000?text=Science+Canteen',
          menuItems: [
            { name: 'Maggi', price: '₹30' },
            { name: 'Sandwiches', price: '₹45' },
            { name: 'Tea', price: '₹10' },
            { name: 'Coffee', price: '₹15' },
            { name: 'Pakoras', price: '₹35' },
            { name: 'Samosa', price: '₹12' }
          ],
          reviews: [
            { id: 1, rating: 4, text: 'Quick service, good for snacks.', images: 1 },
            { id: 2, rating: 4, text: 'Affordable prices for students.', images: 2 }
          ]
        },
        {
          id: 3,
          name: 'Ramjas College Canteen',
          description: 'Popular student hangout spot known for affordable meals and vibrant atmosphere.',
          location: 'Ramjas College, North Campus',
          timing: '9:00 AM - 7:00 PM',
          days: 'Monday - Friday',
          contact: '+91 11 2766-9012',
          rating: 4.3,
          ratingStars: 4,
          status: 'open',
          image: 'https://via.placeholder.com/300x200/F0E68C/000000?text=Ramjas+Canteen',
          menuItems: [
            { name: 'Chole Bhature', price: '₹60' },
            { name: 'Momos', price: '₹40' },
            { name: 'Burger', price: '₹55' },
            { name: 'Lassi', price: '₹25' },
            { name: 'Paratha', price: '₹30' },
            { name: 'Cold Drinks', price: '₹20' }
          ],
          reviews: [
            { id: 1, rating: 4, text: 'Great hangout spot!', images: 2 },
            { id: 2, rating: 5, text: 'Love the momos here!', images: 1 }
          ]
        },
        {
          id: 4,
          name: 'LSR College Canteen',
          description: 'Cozy canteen serving home-style meals with a focus on healthy and hygienic food.',
          location: 'Lady Shri Ram College, South Campus',
          timing: '8:00 AM - 6:30 PM',
          days: 'Monday - Saturday',
          contact: '+91 11 2766-3456',
          rating: 4.6,
          ratingStars: 5,
          status: 'open',
          image: 'https://via.placeholder.com/300x200/F4A460/000000?text=LSR+Canteen',
          menuItems: [
            { name: 'Dal Rice', price: '₹50' },
            { name: 'Roti Sabzi', price: '₹45' },
            { name: 'Fruit Salad', price: '₹35' },
            { name: 'Buttermilk', price: '₹20' },
            { name: 'Upma', price: '₹30' },
            { name: 'Idli Sambhar', price: '₹40' }
          ],
          reviews: [
            { id: 1, rating: 5, text: 'Healthy and tasty food!', images: 1 },
            { id: 2, rating: 4, text: 'Home-like feeling.', images: 0 }
          ]
        }
      ]
    }
  },
  computed: {
    canteen() {
      return this.canteens.find(c => c.id === parseInt(this.id)) || this.canteens[0]
    }
  }
}
</script>

<style scoped>
.canteen-detail-page {
  min-height: 100vh;
  padding-top: 65px;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.canteen-detail-container {
  display: flex;
  gap: 2rem;
  background: rgba(219, 223, 208, 0.18);
  border-radius: 25px;
  padding: 2rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.left-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.right-section {
  flex: 1;
}

/* Canteen Info Card */
.canteen-info-card {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.canteen-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-family: 'Playfair Display', serif;
}

.canteen-image-placeholder {
  width: 200px;
  height: 150px;
  background: rgba(248, 249, 250, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  margin: 1rem 0;
  overflow: hidden;
  backdrop-filter: blur(5px);
}

.canteen-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.canteen-details p {
  margin: 0.5rem 0;
  color: #2c3e50;
  font-size: 0.95rem;
  font-weight: 500;
}

.hours-rating {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.status.open {
  color: #27ae60;
  font-weight: bold;
}

.status.closed {
  color: #d22512;
  font-weight: bold;
}

/* Rating Stars */
.rating {
  margin-top: 0.5rem;
}

.stars {
  margin-left: 0.5rem;
}

.star {
  color: #ddd;
  font-size: 1.2rem;
}

.star.filled {
  color: #f39c12;
}

/* Menu Section */
.menu-section {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.menu-section h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

.menu-grid {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.menu-column {
  flex: 1;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.item-name {
  color: #2c3e50;
  font-weight: 500;
}

.item-price {
  color: #e74c3c;
  font-weight: 600;
}

.menu-images {
  display: flex;
  gap: 1rem;
}

.menu-image-placeholder {
  width: 80px;
  height: 60px;
  background: rgba(248, 249, 250, 0.3);
  border: 2px dashed rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
}

.image-icon {
  font-size: 1.5rem;
  color: rgba(44, 62, 80, 0.6);
}

/* Reviews Section */
.reviews-section {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.reviews-section h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

.overall-rating {
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  margin-bottom: 1rem;
}

.individual-reviews {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item {
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.review-rating {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.review-text {
  color: #2c3e50;
  font-size: 0.9rem;
  font-weight: 500;
}

.review-images {
  display: flex;
  gap: 0.5rem;
}

.review-image-placeholder {
  width: 40px;
  height: 30px;
  background: rgba(248, 249, 250, 0.3);
  border: 1px dashed rgba(255, 255, 255, 0.4);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
}

.review-image-placeholder .image-icon {
  font-size: 1rem;
}

/* Map Section */
.map-container {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
  height: fit-content;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.map-container h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

.map-placeholder {
  width: 100%;
  height: 400px;
  background: rgba(248, 249, 250, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
}

.map-content {
  text-align: center;
  color: #2c3e50;
}

.map-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .canteen-detail-container {
    flex-direction: column;
  }
  
  .menu-grid {
    flex-direction: column;
    gap: 0;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .canteen-detail-container {
    padding: 1rem;
  }
  
  .canteen-name {
    font-size: 1.5rem;
  }
  
  .menu-images {
    flex-wrap: wrap;
  }
  
  .map-placeholder {
    height: 250px;
  }
}
</style>