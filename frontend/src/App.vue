<template>
  <div class="app-wrapper">
    <Header />
    <router-view />
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App'
}
</script>

<style scoped>
.app-wrapper {
  overflow-y: auto;
  min-height: 100vh;
  background: url('@/assets/back.jpeg') no-repeat center center;
  background-size: cover;
  background-attachment: fixed;
  overflow: hidden;
}
</style>
