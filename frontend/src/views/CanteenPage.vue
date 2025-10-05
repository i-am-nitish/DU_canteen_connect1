<template>
  <Header />
  <div class="canteen-page">
    <!-- Info Card -->
    <div class="card info-card">
      <div class="info-content">
        <div class="info-text">
          <h2 class="canteen-name">Canteen Name</h2>
          <div class="info-row">
            <span class="label">Location:</span>
            <span class="value">North Campus</span>
          </div>
          <div class="info-row">
            <span class="label">Description:</span>
            <span class="value">Cozy spot with affordable meals</span>
          </div>
          <div class="info-row">
            <span class="label">Contact:</span>
            <span class="value">+91 9876543210</span>
          </div>
          <div class="info-row">
            <span class="label">Timings:</span>
            <span class="value">8 AM - 6 PM</span>
          </div>
          <div class="info-row">
            <span class="label">Peak Hours:</span>
            <span class="value">1 PM - 3 PM</span>
          </div>
          <div class="info-row">
            <span class="label">Overall Rating:</span>
            <span class="value">★★★★★</span>
          </div>

        </div>
        <div class="info-images">
          <div class="image-square" v-for="n in 4" :key="n"></div>
        </div>

      </div>
    </div>

    <!-- Menu Card -->
    <div class="card menu-card">
      <div class="menu-header">
        <h3>Menu</h3>
      </div>
      <div class="menu-content">
        <div class="menu-list-wrapper">
          <ul class="menu-list">
            <li v-for="(item, index) in menu" :key="index">
              <span>{{ item.name }}</span>
              <span class="price">₹{{ item.price }}</span>
            </li>
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


    <!-- Review Card -->
    <div class="card review-card">
      <div class="review-header-block">
        <h3>Reviews</h3>
        <div class="ratings-breakdown">
          <span><strong>Food:</strong> ★★★★☆</span>
          <span><strong>Staff:</strong> ★★★☆☆</span>
          <span><strong>Hygiene:</strong> ★★★★☆</span>
          <span><strong>Facility:</strong> ★★★☆☆</span>
        </div>
      </div>
      <div class="review-content">
        <ul class="review-list">
          <li v-for="(review, index) in reviews" :key="index">
            <div class="review-item">
              <div class="review-text">
                {{ review.text }} — <span class="stars">{{ review.rating }}</span>
              </div>
              <div class="review-square"></div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    </div>

  <Footer />
</template>



<script>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
export default {
  name: 'CanteenPage',
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      menu: [
        { name: 'Item 1', price: 40 },
        { name: 'Item 2', price: 60 },
        { name: 'Item 3', price: 30 },
        { name: 'Item 4', price: 50 },
        { name: 'Item 5', price: 70 },
        { name: 'Item 6', price: 45 },
        { name: 'Item 7', price: 55 },
        { name: 'Item 8', price: 35 }
      ],
      reviews: [
        { text: 'review1', rating: '★★★☆☆' },
        { text: 'review2', rating: '★★★★☆' },
        { text: 'review3', rating: '★★★☆☆' },
        { text: 'review4', rating: '★★★☆☆' }
      ]
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

.card {
  background: rgba(219, 223, 208, 0.18);
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

.info-content {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}

.info-text {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: center;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.3);
  padding: 0.75rem 1rem;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.label {
  font-weight: 600;
  color: #474747;
  font-size: 1rem;
}

.value {
  font-size: 1rem;
  color: #333;
  text-align: right;
}

.info-images {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  height: 100%;
  align-self: stretch;
  margin-top: 70px;
}

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
  overflow: hidden;
}


.canteen-name {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.image-placeholder {
  height: 100px;
  background: #d9d9d9;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #333;
}

/* Menu Card */
.menu-card {
  padding: 0;
  overflow: hidden;
}

.menu-header {
  background: rgba(255, 255, 255, 0.3);
  padding: 1rem 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 1.6rem;
  font-weight: 600;
  color: #474747;
  font-family: 'Playfair Display', serif;
  font-style: italic;
}

.menu-header h3 {
  font-size: 2rem;
  font-weight: 600;
  margin:0;
}

.menu-content {
  display: flex;
  height: 250px;
  overflow: hidden;
  padding: 1.5rem 2rem;
  gap: 1rem;
}

.menu-list-wrapper {
  flex: 1;
  overflow-y: auto;
  margin-right: 1.5rem;
}

.image-grid-wrapper {
  flex: 1;
  overflow-y: auto;
}

.divider-line {
  width: 1px;
  background-color: #ccc;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.2); 
}


.menu-list li {
  display: grid;
  grid-template-columns: 11fr 1fr;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #ccc;
}


.price {
  font-weight: 600;
  color: #000;
}

/* Square image placeholders */
.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

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
}


/* Review Card */
.review-card {
  padding: 0;
  overflow: hidden;
}

.review-header-block {
  background: rgba(255, 255, 255, 0.3);
  padding: 1rem 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 1.6rem;
  font-weight: 600;
  color: #474747;
  font-family: 'Playfair Display', serif;
  font-style: italic;
}

.review-header-block h3 {
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
}

.ratings-breakdown {
  display: flex;
  gap: 1.5rem;
  font-size: 0.95rem;
  margin-top: 0.5rem;
}

.review-content {
  padding: 1.5rem 2rem;
  border-top: 1px solid rgba(0, 0, 0, 0.2);
}

.review-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.review-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px dashed #aaa;
}

.review-text {
  flex: 1;
  font-size: 1rem;
  color: #333;
}

.review-square {
  width: 60px;
  aspect-ratio: 1 / 1;
  background: #d9d9d9;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-left: 1rem;
}

.stars {
  color: #f5a623;
  font-weight: bold;
}

</style>