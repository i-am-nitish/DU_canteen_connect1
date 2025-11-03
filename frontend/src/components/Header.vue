<template>
  <div class="header" :class="{ centered: isAuthPage }">
    <div class="logo-row">
      <div class="logo">
        <router-link to="/" class="logo-link">
          <img src="@/assets/logo.jpeg" alt="Logo" class="logo-img" />
          <span class="app-name">DU Canteen Connect</span>
        </router-link>
      </div>

      <button
        v-if="!isAuthPage"
        class="menu-toggle"
        @click="menuOpen = !menuOpen"
      >
        ☰
      </button>
    </div>

    <div v-if="!isAuthPage" :class="['menu-wrapper', { open: menuOpen }]">
      <ul class="nav-links">
        <li><router-link to="/">Home</router-link></li>
        <li v-if="!isLoggedIn"><router-link to="/login">Login</router-link></li>
        <li v-else><router-link to="/Desktop8">Account</router-link></li>
        <li v-if="isLoggedIn">
          <button @click="logout" class="logout-btn">Logout</button>
        </li>
      </ul>

      <div class="searchbar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by canteens/items..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">🔍</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const isLoggedIn = ref(false);
    const searchQuery = ref("");
    const menuOpen = ref(false);

    // ✅ Check login state on mount
    onMounted(() => {
      const token = localStorage.getItem("token");
      if (token) {
        isLoggedIn.value = true;
      } else {
        isLoggedIn.value = false;
      }
    });

    const isAuthPage = computed(() =>
      ["/login", "/signup", "/signup/profile", "/signup/canteenprofile"].includes(route.path)
    );

    // ✅ Logout function clears storage + redirects
    function logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      isLoggedIn.value = false;
      alert("Logged out!");
      router.push("/login");
    }

    // ✅ Search
    function handleSearch() {
      console.log("Searching for:", searchQuery.value);
      if (!searchQuery.value.trim()) return;
      router.push(`/desktop11?q=${encodeURIComponent(searchQuery.value)}`);
    }

    return {
      isLoggedIn,
      isAuthPage,
      searchQuery,
      logout,
      handleSearch,
      menuOpen,
    };
  },
};
</script>

<style scoped>
.header {
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
  background: #ffffff;
  box-sizing: border-box;
  z-index: 1000;
  padding: 1rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.header.centered {
  justify-content: center;
}

.logo-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo {
  display: flex;
  align-items: center;
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
  font-family: "Playfair Display", serif;
  font-style: italic;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #474747;
}

.menu-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
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
  width: 30%;
  height: 50px;
  background: #d9d9d9;
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

/* 📱 Mobile Styles */
@media (max-width: 768px) {
  .logo-row {
    flex-direction: row;
    align-items: center;
  }

  .app-name {
    font-size: 1.5rem;
  }

  .menu-toggle {
    display: block;
  }

  .menu-wrapper {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    width: 100%;
    display: none;
  }

  .menu-wrapper.open {
    display: flex;
  }

  .nav-links {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .searchbar {
    width: 100%;
    height: 45px;
  }

  .searchbar input {
    font-size: 1rem;
  }

  .searchbar button {
    font-size: 1.2rem;
  }
}
</style>
