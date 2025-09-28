<template>
  <div class="wrapper">
    <Header />

    <div class="signup-container">
      <h2>Signup</h2>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="email">Phone</label>
          <input v-model="phone" type="phone" id="phone" />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" />
        </div>

        <button type="submit" class="signup-btn">Signup</button>
      </form>

      <div class="login-prompt">
        <p>Already have an account?</p>
        <router-link to="/login" class="signup-link">Login</router-link>
      </div>
    </div>
  </div>
</template>


<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'

export default {
  components: { Header },
  setup() {
    const phone = ref('')
    const password = ref('')
    const router = useRouter()

    function handleSignup() {
        router.push('/signup/profile')
    }

    return {
      phone,
      password,
      handleSignup
    }
  }
}
</script>


<style scoped>
.wrapper{
    padding-top: 60px;
}
.signup-container {
  position:relative;
  max-width: 500px;
  margin: 5rem auto;
  padding: 2rem;
  background: rgba(219, 223, 208, 0.18);
  box-shadow: 0px 4px 10px 3px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(5px);
  border-radius: 25px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label,h2 {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #696D5F;
}

h2{
    position: relative;
    text-align: center;
}

input {
  width: 100%;
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

.signup-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
}

.signup-btn:hover {
  background-color: #333;
}

.login-prompt {
  text-align: center;
  margin-top: 2rem;
  font-size: 1rem;
  color: #696D5F;
}

.login-prompt a {
  text-decoration: underline;
  color: #696D5F;
}
</style>
