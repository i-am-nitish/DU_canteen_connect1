<template>
  <div class="wrapper">
    <Header />

    <div class="signup-container">
      <h2>Signup</h2>
      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label for="name">Name</label>
          <input v-model="name" type="text" id="name" />
        </div>

        <div class="form-group">
          <label for="phone">Phone</label>
          <input v-model="phone" type="tel" id="phone" />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="email" type="email" id="email" />
        </div>

        <div class="form-group radio-group">
          <label>User Type</label>
          <div class="radio-container">
            <div
              class="radio-option"
              v-for="option in roles"
              :key="option"
              :class="{ selected: selectedRole === option }"
            >
              <label>
                <input
                  type="radio"
                  :value="option"
                  v-model="selectedRole"
                  name="user-role"
                />
                <span class="custom-radio">{{ option }}</span>
              </label>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Re-enter Password</label>
          <input v-model="confirmPassword" type="password" id="confirmPassword" />
          <p v-if="passwordMismatch" class="error-text">Passwords do not match</p>
        </div>

        <button type="submit" class="signup-btn" :disabled="loading">
          {{ loading ? "Signing up..." : "Signup" }}
        </button>
      </form>

      <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>

      <div class="login-prompt">
        <p>Already have an account?</p>
        <router-link to="/desktop6" class="signup-link">Login</router-link>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import { ref } from "vue"
import { useRouter } from "vue-router"
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import { signupUser } from "@/services/auth"

export default {
  components: { Header, Footer },

  setup() {
    const name = ref("")
    const phone = ref("")
    const password = ref("")
    const confirmPassword = ref("")
    const email = ref("")
    const passwordMismatch = ref(false)
    const roles = ["General", "Canteen Owner"]
    const selectedRole = ref("")
    const errorMsg = ref("")
    const loading = ref(false)
    const router = useRouter()

    const handleSignup = async () => {
      if (loading.value) return
      loading.value = true

      // Password match validation
      if (password.value !== confirmPassword.value) {
        passwordMismatch.value = true
        loading.value = false
        return
      } else {
        passwordMismatch.value = false
      }

      try {
        const roleMap = {
          General: "general",
          "Canteen Owner": "canteen_owner"
        }

        const data = await signupUser({
          name: name.value,
          phone_number: phone.value,
          email: email.value,
          set_password: password.value,
          confirm_password: confirmPassword.value,
          role: roleMap[selectedRole.value]
        })

        if (selectedRole.value === "General" && data.token) {
          localStorage.setItem("token", data.token)
          alert("Signup successful!")
          router.push("/Desktop1")
        } else if (selectedRole.value === "Canteen Owner" && data.user?.user_id) {

          localStorage.setItem("owner_id", data.user.user_id)
          router.push({
            path: "/signup/canteenprofile",
            query: { owner_id: data.user.user_id }
          })
        }
      } catch (err) {
        console.error(err)
        errorMsg.value = err.response?.data?.message || "Signup failed"
      } finally {
        loading.value = false
      }
    }

    return {
      name,
      phone,
      email,
      password,
      confirmPassword,
      passwordMismatch,
      roles,
      selectedRole,
      handleSignup,
      errorMsg,
      loading
    }
  }
}
</script>

<style scoped>
.error-text {
  color: #ff4d4d;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 80px;
  background: transparent;
}

.signup-container {
  width: 100%;
  max-width: 480px;
  margin: auto;
  padding: 2rem 2.5rem;
  background: rgba(219, 223, 208, 0.18);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(6px);
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
  color: #474747;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 1rem;
  font-weight: 500;
  color: #696d5f;
}

input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  border: none;
  background: rgba(71, 71, 71, 0.41);
  color: white;
  font-size: 1rem;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.58);
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.radio-container {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

.radio-option {
  flex: 1;
  background: rgba(71, 71, 71, 0.3);
  padding: 0.75rem;
  border-radius: 10px;
  text-align: center;
  border: 2px solid transparent;
  transition: background 0.3s ease, border 0.3s ease;
  cursor: pointer;
}

.radio-option:hover {
  background: rgba(71, 71, 71, 0.5);
}

.radio-option.selected {
  border-color: #dbdfd0;
  background: rgba(71, 71, 71, 0.6);
}

.radio-option input[type="radio"] {
  display: none;
}

.radio-option label {
  cursor: pointer;
  width: 100%;
  display: block;
}

.custom-radio {
  color: white;
  font-size: 1rem;
  font-weight: 500;
}

.signup-btn {
  width: 100%;
  padding: 0.85rem;
  background-color: #474747;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 1rem;
  transition: background 0.3s ease;
}

.signup-btn:hover {
  background-color: #333;
}

.error-text {
  color: #ff4d4d;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.login-prompt {
  text-align: center;
  font-size: 1rem;
  margin-top: 1.5rem;
  color: #696d5f;
}

.signup-link {
  text-decoration: underline;
  color: #696d5f;
  font-weight: 500;
  margin-left: 0.25rem;
}

/* Mobile */
@media (max-width: 768px) {
  .signup-container {
    margin: 3rem 1rem;
    padding: 2rem;
  }

  h2 {
    font-size: 1.6rem;
  }

  input {
    font-size: 0.95rem;
    padding: 0.65rem 0.75rem;
  }

  .signup-btn {
    font-size: 1rem;
    padding: 0.75rem;
  }

  .radio-container {
    flex-direction: column;
    gap: 0.75rem;
  }

  .radio-option {
    width: 100%;
    text-align: center;
  }

  .custom-radio {
    font-size: 0.95rem;
  }

  .login-prompt {
    font-size: 0.95rem;
  }
}

</style>
