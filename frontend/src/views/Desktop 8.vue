<template>
  <div class="dashboard-wrapper">
    <!-- Header -->
    <Header />

    <!-- Profile Section -->
    <section class="card profile-section">
      <h2>Profile</h2>
      <div class="profile-fields">
        <div class="field"><strong>Name:</strong> {{ userInfo.name || 'Loading...' }}</div>
        <div class="field"><strong>Email:</strong> {{ userInfo.email || 'Loading...' }}</div>
        <div class="field"><strong>Phone number:</strong> {{ userInfo.phone_number || 'Loading...' }}</div>
        <div class="field"><strong>Password:</strong> ********</div>
      </div>
    </section>

    <!-- Report Issues Section -->
    <section class="card report-section">
      <h2>Report Issues</h2>
      <div class="report-fields">
        <div class="report-group">
          <input type="text" placeholder="Describe the issue" v-model="issueText" />
          <button @click="handleReportIssue">Submit</button>
        </div>
        <div class="report-group" style="margin-top:1rem;">
          <input type="text" placeholder="App feedback (optional)" v-model="feedbackText" />
          <button @click="handleGiveFeedback">Send</button>
        </div>
      </div>
    </section>

    <!-- Reviews and Ratings Section -->
    <section class="card review-section">
      <h2>Your Reviews and Ratings</h2>
      <ul class="review-list">
        <li v-for="(review, index) in reviews" :key="index" class="review-item">
          <div class="review-header">
            <span class="canteen-name">{{ review.canteenName }}</span>
            <span class="stars">{{ getStars(review.rating) }}</span>
          </div>
          <p class="review-text">{{ review.text }}</p>
          <div class="review-images">
            <div class="review-image" v-for="(img, i) in review.images" :key="i">
              <img :src="img" alt="Review image" />
            </div>
          </div>
        </li>
      </ul>
    </section>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { getUserProfile, getUserReviews } from '@/services/auth'

export default {
  name: 'DashboardPage',
  components: { Header, Footer },
  data() {
    return {
      userInfo: {},
      reviews: [],
      issueText: '',
      feedbackText: ''
    }
  },
  methods: {
    getStars(rating) {
      return '★'.repeat(rating) + '☆'.repeat(5 - rating)
    },

    async loadUserProfile() {
      try {
        const data = await getUserProfile()
        this.userInfo = data
      } catch (error) {
        console.error('Error loading user profile:', error)
      }
    },

    async loadUserReviews() {
      try {
        const data = await getUserReviews()
        // `getUserReviews()` returns an array (res.data.reviews) in services/auth.js.
        // Accept either an array or an object with a `reviews` property to be robust.
        this.reviews = Array.isArray(data) ? data : (data.reviews || [])
      } catch (error) {
        console.error('Error loading user reviews:', error)
      }
    },

    async handleReportIssue() {
      if (!this.issueText.trim()) {
        alert('Please enter issue details')
        return
      }

      try {
        await this.$root.$options.config.globalProperties.$api // noop to satisfy linter
      } catch (e) {}

      try {
        // lazy import service function to avoid changing imports at top
        const { reportAppIssue } = await import('@/services/auth')
        await reportAppIssue(this.issueText)
        this.issueText = ''
        alert('Issue reported — admin will review it.')
      } catch (error) {
        console.error('Report issue failed:', error)
        alert('Failed to report issue')
      }
    },

    async handleGiveFeedback() {
      if (!this.feedbackText.trim()) {
        alert('Please enter feedback')
        return
      }

      try {
        const { giveAppFeedback } = await import('@/services/auth')
        await giveAppFeedback(this.feedbackText)
        this.feedbackText = ''
        alert('Thank you for your feedback!')
      } catch (error) {
        console.error('Send feedback failed:', error)
        alert('Failed to send feedback')
      }
    }
  },
  async mounted() {
    // Require authentication for this page (minimal change)
    if (!localStorage.getItem('token')) {
      // redirect to login if not authenticated
      this.$router.push('/desktop6')
      return
    }

    // load profile and reviews
    await this.loadUserProfile()
    await this.loadUserReviews()
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

/* Card Sections */
.card {
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Profile */
.profile-fields .field {
  margin-bottom: 1rem;
  font-size: 1rem;
  color: #333;
}

/* Report */
.report-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

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

/* Reviews */
.review-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.review-item {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.canteen-name {
  color: #474747;
}

.stars {
  color: #f5a623;
}

.review-text {
  font-size: 1rem;
  color: #333;
  margin-bottom: 1rem;
}

.review-images {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.review-image img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
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

.footer-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-right {
  display: flex;
  align-items: center;
}

.map-square {
  width: 180px;
  height: 180px;
  background: #d9d9d9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive tweaks */
@media (max-width: 768px) {
  .review-item {
    padding: 1rem;
  }

  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .review-text {
    font-size: 0.95rem;
  }

  .review-image img {
    width: 80px;
    height: 80px;
  }

  .searchbar {
    width: 100%;
    margin-top: 0.5rem;
  }

  .nav-links {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
