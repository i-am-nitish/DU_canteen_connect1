<template>
  <Header />

  <div class="canteen-page">
    <!-- Info Card -->
    <div class="card info-card" v-if="canteenInfo">
      <div class="info-content">
        <div class="info-text">
          <h2 class="canteen-name">{{ canteenInfo?.name || 'Canteen Name' }}</h2>
          <div class="info-row">
            <span class="label">Location:</span>
            <span class="value">{{ canteenInfo?.location || 'Not specified' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Description:</span>
            <span class="value">{{ canteenInfo?.description || 'No description available' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Contact:</span>
            <span class="value">{{ canteenInfo?.contact_number || 'N/A' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Timings:</span>
            <span class="value">
              {{ canteenInfo?.opening_time || 'N/A' }} – {{ canteenInfo?.closing_time || 'N/A' }}
            </span>
          </div>
          <div class="info-row">
            <span class="label">Peak Hours:</span>
            <span class="value">
              {{ canteenInfo?.peak_hr_start_time || 'N/A' }} – {{ canteenInfo?.peak_hr_end_time || 'N/A' }}
            </span>
          </div>
          <div class="info-row">
            <span class="label">Overall Rating:</span>
            <span class="value">
              {{ canteenInfo?.overall_rating ? canteenInfo.overall_rating + ' ★' : 'Not rated yet' }}
            </span>
          </div>
        </div>

        <div class="info-images">
          <div class="image-square" v-for="n in 4" :key="n"></div>
        </div>
      </div>
    </div>

    <div v-else class="loading">Loading canteen info...</div>

    <!-- Menu Card -->
    <div class="card menu-card" v-if="menu?.length">
      <div class="menu-header">
        <h3>Menu</h3>
      </div>
      <div class="menu-content">
        <div class="menu-list-wrapper">
          <ul class="menu-list">
           <div v-for="(item, index) in menu" :key="index">
           <h1>{{item?.day || '-'}}</h1>
            <li v-for="(dayMenu ,idx) in zip(item.items, item.price)" :key="idx">
              <span>{{ dayMenu[0] || 'Unnamed item' }}</span>
              <span class="price">₹{{ dayMenu[1]|| '-' }}</span>
            </li>
           </div>
          </ul>
        </div>
        <div class="divider-line"></div>
        <div class="image-grid-wrapper">
          <div class="image-grid">
            <div class="image-square" v-for="n in 4" :key="n"></div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="loading">Menu is loading...</div>

    <!-- Review Card -->
    <!-- Review Card -->
    <div class="card review-card" v-if="ratings">
      <div class="review-header-block">
        <h3>Reviews</h3>
        <div class="ratings-breakdown">
          <span><strong>Food:</strong> {{ getStars(ratings.overall_food) || 'N/A' }}</span>
          <span><strong>Staff:</strong> {{ getStars(ratings.overall_staff) || 'N/A' }}</span>
          <span><strong>Hygiene:</strong> {{ getStars(ratings.overall_hygiene) || 'N/A' }}</span>
          <span><strong>Facility:</strong> {{ getStars(ratings.overall_facilities) || 'N/A' }}</span>
          <span><strong>Overall:</strong> {{ getStars(ratings.overall_rating) || 'N/A' }}</span>
        </div>
      </div>

      <div class="review-content">
        <ul class="review-list">
          <li v-for="(review, index) in reviews || []" :key="index">
            <div class="review-item">
              <div class="review-text">
                {{ review?.review_text || 'No review text' }} — <span class="stars">({{ review?.overall_rating || 'N/A' }})</span>
              </div>
              <div class="review-square"></div>
            </div>
          </li>
        </ul>

        <!-- ✅ Write Review Section (only if logged in) -->
        <div v-if="isLoggedIn" class="write-review">
          <h4>Write a review...</h4>
          <textarea v-model="newReviewText" placeholder="Type here..."></textarea>
          <div class="rating-select">
            <label>Food:</label>
            <select v-model="newFoodRating">
              <option disabled value="">Select</option>
              <option v-for="n in 5" :key="'food' + n" :value="n">{{ n }} ★</option>
            </select>

            <label>Staff:</label>
            <select v-model="newStaffRating">
              <option disabled value="">Select</option>
              <option v-for="n in 5" :key="'staff' + n" :value="n">{{ n }} ★</option>
            </select>

            <label>Hygiene:</label>
            <select v-model="newHygieneRating">
              <option disabled value="">Select</option>
              <option v-for="n in 5" :key="'hygiene' + n" :value="n">{{ n }} ★</option>
            </select>

            <label>Facility:</label>
            <select v-model="newFacilityRating">
              <option disabled value="">Select</option>
              <option v-for="n in 5" :key="'facility' + n" :value="n">{{ n }} ★</option>
            </select>
          </div>

          <button @click="submitReview" class="submit-review-btn">Post Review</button>
        </div>
      </div>
    </div>
    </div>


  <Footer />
</template>

<script>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import { fetchCanteenInfo, fetchCanteenMenu, fetchCanteenReviews, submitCanteenReview } from '@/services/canteen'

export default {
  name: 'CanteensPage',
  components: { Header, Footer },

  data() {
    return {
      canteenInfo: null,
      menu: [],
      reviews: [],
      ratings: null,
      errorMsg: '',
      isLoggedIn: false,
      newReviewText: '',
      newFoodRating: '',
      newStaffRating: '',
      newHygieneRating: '',
      newFacilityRating: '',

    }
  },

  mounted() {
    this.isLoggedIn = !!localStorage.getItem('token')
  },

  methods: {
    getStars(rating) {
      if (!rating) return 'N/A'
      return '★'.repeat(Math.round(rating))
    },

    zip(a, b) {
      if (!Array.isArray(a) || !Array.isArray(b)) return []
      return a.map((item, i) => [item, b[i]])
    },

    async submitReview() {
      if (
        !this.newReviewText ||
        !this.newFoodRating ||
        !this.newStaffRating ||
        !this.newHygieneRating ||
        !this.newFacilityRating
      ) {
        alert('Please fill in all ratings and review text')
        return
      }

      const canteenId = this.$route.query.canteen_id
      const overallRating = Math.round(
        (Number(this.newFoodRating) + Number(this.newStaffRating) + 
         Number(this.newHygieneRating) + Number(this.newFacilityRating)) / 4
      )

      try {
        await submitCanteenReview(canteenId, {
          overallRating,
          foodRating: this.newFoodRating,
          staffRating: this.newStaffRating,
          hygieneRating: this.newHygieneRating,
          facilityRating: this.newFacilityRating,
          text: this.newReviewText
        })

        this.newReviewText = ''
        this.newFoodRating = ''
        this.newStaffRating = ''
        this.newHygieneRating = ''
        this.newFacilityRating = ''

        alert('Review posted successfully!')
        
        const reviewsData = await fetchCanteenReviews(canteenId)
        this.reviews = reviewsData?.top_reviews || []
      } catch (error) {
        console.error('Failed to submit review:', error)
        alert('Failed to post review')
      }
    }
  },

  async created() {
    const canteenId = this.$route.query.canteen_id
    if (!canteenId) {
      this.errorMsg = 'Missing canteen ID in URL'
      return
    }

    try {
      const info = await fetchCanteenInfo(canteenId);
      const menuData = await fetchCanteenMenu(canteenId);
      const reviewsData = await fetchCanteenReviews(canteenId)

      console.log('info: ', info, 'menuData: ', menuData, 'reviewsData: ', reviewsData)

      this.canteenInfo = info
      console.log('menu data: ', menuData)
      this.menu = menuData
      this.reviews = reviewsData?.top_reviews || []
      this.ratings = reviewsData || null
    } catch (err) {
      console.error(err)
      this.errorMsg = 'Error fetching canteen data'
    }
  }
}
</script>

<style> 
.canteen-page { 
display: flex; 
flex-direction: column; 
gap: 2rem; 
padding: 2rem; 
background: rgba(219, 223, 208, 0.18); 
border-radius: 25px; 
box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25); 
backdrop-filter: blur(5px); 
max-width: 1200px; 
margin: 130px auto 3rem; 
} 

.card 
{ background: rgba(219, 223, 208, 0.18); 
backdrop-filter: blur(3px); 
border-radius: 20px; 
padding: 2rem; 
color: rgb(0, 0, 0); 
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
} 

/* Info Card */ 
.info-card { 
  max-height: 450px; 
  overflow: hidden; 
  } 
  .info-content 
  { display: flex; 
  justify-content: space-between; 
  gap: 2rem; 
  } 
  .info-text 
  { flex: 2; 
  display: flex; 
  flex-direction: column; 
  gap: 1rem; 
  justify-content: center; } 
  
.info-row { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  background: rgba(255, 255, 255, 0.3); 
  padding: 0.75rem 1rem; 
  border-radius: 10px; 
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1); } 
    
.label { 
  font-weight: 600; 
  color: #474747; 
  font-size: 1rem; } 
  
.value { 
  font-size: 1rem; 
  color: #333; 
  text-align: right; } 
  
.info-images { 
  flex: 1; 
  display: grid; 
  grid-template-columns: repeat(2, 1fr); 
  gap: 0.75rem; 
  height: 100%; 
  align-self: stretch; 
  margin-top: 70px; } 

.image-square { 
  width: 100%; 
  aspect-ratio: 1 / 1; 
  background: #d9d9d9; 
  border-radius: 10px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-size: 1.5rem; 
  color: #333; 
  overflow: hidden; } 
  
.canteen-name { 
  font-size: 2rem; 
  font-weight: 600; 
  margin-bottom: 1rem; } 
  
.image-placeholder { 
  height: 100px; 
  background: #d9d9d9; 
  border-radius: 10px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-size: 2rem; 
  color: #333; } 
  
  
  /* Menu Card */ 
  .menu-card { 
    padding: 0; 
    overflow: hidden; } 
    
.menu-header { 
  background: rgba(255, 255, 255, 0.3); 
  padding: 1rem 2rem; 
  border-bottom: 1px solid rgba(0, 0, 0, 0.1); 
  font-size: 1.6rem; 
  font-weight: 600; 
  color: #474747; 
  font-family: 'Playfair Display', serif; 
  font-style: italic; } 
  
.menu-header h3 { 
  font-size: 2rem; 
  font-weight: 600; 
  margin:0; } 
  
.menu-content { 
  display: flex; 
  height: 250px; 
  overflow: hidden; 
  padding: 1.5rem 2rem; 
  gap: 1rem; } 
  
.menu-list-wrapper { 
  flex: 1; 
  overflow-y: auto; 
  margin-right: 1.5rem; } 
  
.image-grid-wrapper { 
  flex: 1; 
  overflow-y: auto; } 
  
.divider-line { 
  width: 1px; 
  background-color: #ccc; } 
  
.menu-list { 
  list-style: none; 
  padding: 0; 
  margin-top: 1rem; 
  border-top: 1px solid rgba(0, 0, 0, 0.2); } 
  
.menu-list li { 
  display: grid; 
  grid-template-columns: 11fr 1fr; 
  align-items: center; 
  padding: 0.75rem 0; 
  border-bottom: 1px solid #ccc; } 
  
.price { 
  font-weight: 600; 
  color: #000; } 

.image-grid { 
  display: grid; 
  grid-template-columns: repeat(2, 1fr); 
  gap: 0.75rem; } 
  
.image-square { 
  width: 100%; 
  aspect-ratio: 1 / 1; 
  background: #d9d9d9; 
  border-radius: 10px; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  font-size: 1.5rem; 
  color: #333; } 
  
  /* Review Card */ 
.review-card { 
  padding: 0; 
  overflow: hidden; } 
  
.review-header-block { 
  background: rgba(255, 255, 255, 0.3); 
  padding: 1rem 2rem; 
  border-bottom: 1px solid rgba(0, 0, 0, 0.1); font-size: 1.6rem; font-weight: 600; color: #474747; font-family: 'Playfair Display', serif; font-style: italic; } .review-header-block h3 { font-size: 2rem; font-weight: 600; margin: 0; } .ratings-breakdown { display: flex; gap: 1.5rem; font-size: 0.95rem; margin-top: 0.5rem; } .review-content { padding: 1.5rem 2rem; border-top: 1px solid rgba(0, 0, 0, 0.2); } .review-list { list-style: none; padding: 0; margin: 0; } .review-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px dashed #aaa; } .review-text { flex: 1; font-size: 1rem; color: #333; } .review-square { width: 60px; aspect-ratio: 1 / 1; background: #d9d9d9; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-left: 1rem; } .stars { color: #f5a623; font-weight: bold; } /* 📱 Responsive Layout for Mobile & Tablets */ @media (max-width: 768px) { .canteen-page { padding: 1rem; margin: 100px 1rem 2rem; } .info-content { flex-direction: column; gap: 1rem; } .info-images { grid-template-columns: 1fr; margin-top: 1rem; } .menu-content { flex-direction: column; height: auto; padding: 1rem; } .divider-line { display: none; } .menu-list-wrapper, .image-grid-wrapper { margin: 0; overflow: visible; } .menu-list li { grid-template-columns: 1fr auto; font-size: 0.95rem; } .image-grid { grid-template-columns: 1fr; } .ratings-breakdown { flex-direction: column; gap: 0.5rem; } .review-item { flex-direction: column; align-items: flex-start; gap: 0.5rem; } .review-square { margin-left: 0; width: 100%; max-width: 100px; } .review-text { font-size: 0.95rem; } .canteen-name { font-size: 1.5rem; text-align: center; } .menu-header h3, .review-header-block h3 { font-size: 1.5rem; text-align: center; } .menu-header, .review-header-block { padding: 1rem; text-align: center; } } 

.write-review {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.write-review textarea {
  width: 100%;
  padding: 0.75rem;
  border-radius: 10px;
  border: none;
  background: rgba(71, 71, 71, 0.1);
  font-size: 1rem;
  color: #333;
  resize: vertical;
}

.rating-select {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-select select {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.submit-review-btn {
  align-self: flex-start;
  padding: 0.75rem 1.5rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
}

.submit-review-btn:hover {
  background-color: #333;
}

</style>