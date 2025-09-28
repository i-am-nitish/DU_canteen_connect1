<template>
  <div class="header" :class="{ centered: isAuthPage }">
    <div class="logo">
      <router-link to="/" class="logo-link">
        <img src="@/assets/logo.jpeg" alt="Logo" class="logo-img" />
        <span class="app-name">DU Canteen Connect</span>
      </router-link>
    </div>

    <ul v-if="!isAuthPage" class="nav-links">
      <li><router-link to="/">Home</router-link></li>
      <li v-if="!isLoggedIn"><router-link to="/login">Login</router-link></li>
      <li v-else><router-link to="/account">Account</router-link></li>
      <li v-if="isLoggedIn">
        <button @click="logout" class="logout-btn">Logout</button>
      </li>
    </ul>
    
    <div v-if="!isAuthPage" class="searchbar">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search by canteens/items..."
        @keyup.enter="handleSearch"
      />
      <button @click="handleSearch">🔍</button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const isLoggedIn = ref(true)
    const searchQuery = ref('')

    const isAuthPage = computed(() =>
      ['/login', '/signup', '/signup/profile', '/signup/canteenprofile'].includes(route.path)
    )

    function logout() {
      isLoggedIn.value = false
      alert('Logged out!')
    }

    function handleSearch() {
      console.log('Searching for:', searchQuery.value)
    }

    return {
      isLoggedIn,
      isAuthPage,
      searchQuery,
      logout,
      handleSearch
    }
  }
}
</script>


<style scoped>
.header {
  position: absolute;
  width: 100%;
  height: 65px;
  left: 0;
  top: 0;
  background: #FFFFFF;
  display: flex;
  align-items: center; /* vertical centering */
  justify-content: space-between;
  padding: 0 2rem;
  box-sizing: border-box;
  z-index: 1000;
}

.header.centered {
  justify-content: center;
}

.logo {
    display: flex;
  align-items: center; /* vertical centering inside logo block */
  height: 100%;
}

.logo-img {
  width: 50px;
  height: auto;
  margin-right: 1rem;
}

.app-name {
  font-size: 2rem;
  font-weight: 600;
  color: #474747;
  font-family: 'Playfair Display', serif;
  font-style: italic;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links li {
  font-size: 1rem;
  font-weight: 500;
  color: #474747;
}

.logout-btn {
  background: none;
  border: none;
  font-weight: 500;
  cursor: pointer;
  color: #474747;
}

.searchbar {
  position: absolute;
  width: 30%;
  height: 50px;
  left: 500px;
  top: 50px;

  background: #D9D9D9;
  border-radius: 25px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.searchbar input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1.2rem;
  color: #333;
  outline: none;
}

.searchbar button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #474747;
}


</style>
