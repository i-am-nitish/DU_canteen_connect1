<template>
  <div class="page-wrapper">
    <!-- Header -->
    <Header />
    <div class="dashboard-wrapper">
    <!-- Profile Section -->
    <section class="card profile-section">
      <h2>Profile</h2>
      <div class="profile-fields">
        <div class="field">
          <strong>Name:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableUserInfo.name" type="text" />
          </template>
          <template v-else>
            {{ userInfo.name || 'Loading...' }}
          </template>
        </div>

        <div class="field">
          <strong>Email:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableUserInfo.email" type="email" />
          </template>
          <template v-else>
            {{ userInfo.email || 'Loading...' }}
          </template>
        </div>

        <div class="field">
          <strong>Phone number:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableUserInfo.phone_number" type="text" />
          </template>
          <template v-else>
            {{ userInfo.phone_number || 'Loading...' }}
          </template>
        </div>

        <div class="field">
          <strong>Password:</strong>
          <template v-if="isEditingProfile">
            <input v-model="editableUserInfo.password" type="password" />
          </template>
          <template v-else>
            ********
          </template>
        </div>
      </div>

      <button @click="toggleEditProfile" class="edit-btn">
        {{ isEditingProfile ? 'Save' : 'Edit Profile' }}
      </button>
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
            <span class="canteen-name">{{ review.canteen_name }}</span>
            <span class="stars">{{ getStars(review.overall_rating) }}</span>
          </div>
          <p class="review-text">{{ review.review_text }}</p>
          <div class="review-images">
            <div class="review-image" v-for="(img, i) in review.images" :key="i">
              <img :src="img" alt="Review image" />
            </div>
          </div>
        </li>
      </ul>
    </section>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { fetchUserInfo, fetchUserReviews, submitAppIssue, submitAppFeedback, updateUserProfile } from '@/services/user'

export default {
  name: 'DashboardPage',
  components: { Header, Footer },
  data() {
    return {
      userInfo: {},
      editableUserInfo: {},
      isEditingProfile: false,
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
        const data = await fetchUserInfo()
        // Backend returns { message, user_info }
        this.userInfo = data.user_info || {}
      } catch (error) {
        console.error('Error loading user profile:', error)
        
      }
    },

    async loadUserReviews() {
      try {
        const data = await fetchUserReviews()
        // Backend returns { message, reviews }
        this.reviews = data.reviews || []
      } catch (error) {
        console.error('Error loading user reviews:', error)
        if (error.response?.status === 422) {
          // Token invalid - already handled in loadUserProfile
          return
        }
      }
    },

    async handleReportIssue() {
      if (!this.issueText.trim()) {
        alert('Please enter issue details')
        return
      }

      try {
        await submitAppIssue({ issue_text: this.issueText })
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
        await submitAppFeedback({ feedback_text: this.feedbackText })
        this.feedbackText = ''
        alert('Thank you for your feedback!')
      } catch (error) {
        console.error('Send feedback failed:', error)
        alert('Failed to send feedback')
      }
    },
    async toggleEditProfile() {
      if (this.isEditingProfile) {
        // Save changes - only send changed fields
        try {
          const updates = {}
          if (this.editableUserInfo.name !== this.userInfo.name) {
            updates.name = this.editableUserInfo.name
          }
          if (this.editableUserInfo.email !== this.userInfo.email) {
            updates.email = this.editableUserInfo.email
          }
          if (this.editableUserInfo.phone_number !== this.userInfo.phone_number) {
            updates.phone_number = this.editableUserInfo.phone_number
          }
          if (this.editableUserInfo.password && this.editableUserInfo.password !== '********') {
            updates.password = this.editableUserInfo.password
          }

          if (Object.keys(updates).length > 0) {
            await updateUserProfile(updates)
            await this.loadUserProfile() // Reload to show updated data
            alert('Profile updated successfully!')
          }
        } catch (error) {
          console.error('Failed to update profile:', error)
          alert(error.response?.data?.message || 'Failed to save changes')
          return
        }
      } else {
        // Enter edit mode
        this.editableUserInfo = { ...this.userInfo, password: '' }
      }
      this.isEditingProfile = !this.isEditingProfile
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
.page-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.dashboard-wrapper {
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
  margin-top: auto;        /* pushes footer to bottom */
  position: relative; 
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

.profile-fields input {
  margin-left: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.edit-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
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
