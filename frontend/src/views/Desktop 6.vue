<template>
  <div class="wrapper">
    <Header />

    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Phone</label>
          <input v-model="phone_number" type="tel" id="phone" required />

        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" required />
        </div>

        <button type="submit" class="login-btn">Login</button>
      </form>
      
      <!--  Show backend error if any -->
      <p v-if="errorMsg" style="color:red; text-align:center;">{{ errorMsg }}</p>

      <!-- Signup prompt -->
      <div class="signup-prompt">
        <p>Don’t have an account?</p>
        <router-link to="/signup" class="signup-link">Sign up</router-link>
      </div>
    </div>
    <Footer />
  </div>
</template>


<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import { loginUser } from '@/services/auth'

export default {
  components: { Header, Footer },
  setup() {
    const phone_number = ref('')
    const password = ref('')
    const router = useRouter()
    const errorMsg = ref('')

    // 🔹 Main login handler using reusable auth function
    const handleLogin = async () => {
      try {
        const data = await loginUser(phone_number.value, password.value)

        // Save JWT and user info if login successful
        if (data.token) {
          localStorage.setItem('token', data.token)
          localStorage.setItem('user', JSON.stringify(data.user))
          router.push('/home')
        }
      } catch (err) {
        console.error(err)
        errorMsg.value = err.response?.data?.message || 'Login failed'
      }
    }

    return { phone_number, password, handleLogin, errorMsg }
  }
}
</script>

  

<style scoped>
.wrapper{
    padding-top: 60px;
}
.login-container {
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

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #333;
}

.signup-prompt {
  text-align: center;
  margin-top: 2rem;
  font-size: 1rem;
  color: #696D5F;
}

.signup-prompt a {
  text-decoration: underline;
  color: #696D5F;
}
</style>
