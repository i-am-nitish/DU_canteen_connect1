<template>
  <div class="wrapper">
    <Header />

    <div class="profile-container">
      <h2>Create Canteen Profile</h2>
      <form @submit.prevent="handleCanteenProfile">
        
        <div class="form-row">
          <div class="form-group">
            <label for="name">Canteen Name</label>
            <input v-model="name" type="text" id="name" />
          </div>
          <div class="form-group">
            <label for="location">Location</label>
            <input v-model="location" type="text" id="location" />
          </div>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <input v-model="description" type="text" id="description" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="contact">Contact Info</label>
            <input v-model="contact" type="text" id="contact" />
          </div>
          <div class="form-group">
            <label for="daysOpen">Days Open</label>
            <input v-model="daysOpen" type="text" id="daysOpen" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="timings">Opening Time</label>
            <input v-model="timings" type="text" id="atimings" />
          </div>
          <div class="form-group">
            <label for="timings">Closing Time</label>
            <input v-model="timings" type="text" id="btimings" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="peakHours">Starting Peak Hour</label>
            <input v-model="peakHours" type="text" id="apeakHours" />
          </div>
          <div class="form-group">
            <label for="peakHours">Closing Peak Hour</label>
            <input v-model="peakHours" type="text" id="bpeakHours" />
          </div>
        </div>

        <div class="form-group">
          <label for="menuUpload">Upload Menu</label>
          <input type="file" id="menuUpload" @change="handleFileUpload" />
        </div>

        <button type="submit" class="create-btn">Create</button>
      </form>
    </div>
    <Footer />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'

export default {
  components: { Header, Footer },
  setup() {
    const router = useRouter()

    const name = ref('')
    const location = ref('')
    const description = ref('')
    const contact = ref('')
    const daysOpen = ref('')
    const timings = ref('')
    const peakHours = ref('')
    const menuFile = ref(null)

    function handleFileUpload(event) {
      menuFile.value = event.target.files[0]
    }

    function handleCanteenProfile() {
      router.push('/canteenpage')
    }

    return {
      name,
      location,
      description,
      contact,
      daysOpen,
      timings,
      peakHours,
      menuFile,
      handleFileUpload,
      handleCanteenProfile
    }
  }
}
</script>

<style scoped>
.wrapper {
  padding-top: 60px;
}

.profile-container {
  position: relative;
  max-width: 600px;
  margin: 5rem auto;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  box-shadow: 0px 4px 10px 3px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border-radius: 25px;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #696D5F;
}

.form-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #696D5F;
}

input {
  padding: 0.75rem;
  border-radius: 10px;
  border: none;
  background: rgba(71, 71, 71, 0.41);
  color: white;
  font-size: 1rem;
  backdrop-filter: blur(2px);
}

input::placeholder {
  color: rgba(255, 255, 255, 0.58);
}

.create-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 2rem;
}

.create-btn:hover {
  background-color: #333;
}
</style>
