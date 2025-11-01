<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <Header />

    <!-- Reported Issues -->
    <section class="card issues-section">
      <h2>Reported Issues</h2>
      <ul class="issue-list">
        <li v-for="(issue, index) in reportedIssues" :key="index">
          {{ issue }}
        </li>
      </ul>
    </section>

    <!-- Feedback/Suggestions -->
    <section class="card feedback-section">
      <h2>Feedback/Suggestions</h2>
      <ul class="feedback-list">
        <li v-for="(feedback, index) in feedbackEntries" :key="index">
          {{ feedback }}
        </li>
      </ul>
    </section>

    <!-- Reviews and Ratings -->
    <section class="card review-section">
      <h2>Reviews and Ratings</h2>
      <ul class="review-list">
        <li v-for="(review, index) in reviews" :key="index" class="review-item">
          <span class="stars">{{ getStars(review.rating) }}</span>
          <span class="review-text">{{ review.text }}</span>
          <div class="review-actions">
            <button @click="editReview(index)">✎</button>
            <button @click="deleteReview(index)">✕</button>
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

export default {
  name: 'AdminDashboard',
  components: { Header, Footer },
  data() {
    return {
      reportedIssues: [
        'UserId Name Phone number Issue1',
        'UserId Name Phone number Issue2',
        'UserId Name Phone number Issue3'
      ],
      feedbackEntries: [
        'UserId Name Phone number Feedback1',
        'UserId Name Phone number Feedback2',
        'UserId Name Phone number Feedback3'
      ],
      reviews: [
        { rating: 5, text: 'review1' },
        { rating: 5, text: 'review2' },
        { rating: 5, text: 'review3' },
        { rating: 5, text: 'review4' },
        { rating: 5, text: 'review5' }
      ]
    }
  },
  methods: {
    getStars(rating) {
      return '✪'.repeat(rating)
    },
    editReview(index) {
      alert(`Edit review ${index + 1}`)
    },
    deleteReview(index) {
      this.reviews.splice(index, 1)
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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

/* Card */
.card {
  background: rgba(219, 223, 208, 0.18);
  backdrop-filter: blur(5px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Lists */
.issue-list,
.feedback-list,
.review-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
}

.issue-list li,
.feedback-list li {
  padding: 0.5rem 0;
  font-size: 1rem;
  color: #333;
  border-bottom: 1px dashed #aaa;
}

/* Reviews */
.review-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px dashed #aaa;
}

.stars {
  color: #f5a623;
  font-weight: bold;
  margin-right: 1rem;
}

.review-text {
  flex: 1;
  color: #333;
}

.review-actions button {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  margin-left: 0.5rem;
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
