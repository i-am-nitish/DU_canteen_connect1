<template>
  <div class="app-wrapper">
    <app-header @search="handleSearch" />
    <router-view :search-query="searchQuery" />
  </div>
</template>

<script>
import { ref, provide } from 'vue'
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    'app-header': Header
  },
  setup() {
    const searchQuery = ref('')

    function handleSearch(query) {
      searchQuery.value = query
    }

    // Provide search query to all child components
    provide('searchQuery', searchQuery)

    return {
      searchQuery,
      handleSearch
    }
  }
}
</script>

<style scoped>
.app-wrapper {
  overflow-y: auto;
  min-height: 100vh;
  background: url('@/assets/back.jpeg') no-repeat center center;
  background-size: cover;
  background-attachment: fixed;
}
</style>
