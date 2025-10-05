<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-left">
        <h2 class="footer-title">DU Canteen Connect</h2>
        <p class="footer-subtitle">Description</p>
      </div>
      <div class="footer-right">
        <p class="footer-contact">Contact</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.footer {
  position: relative;
  width: 100%;
  max-width: 1441px;
  height: 230px;
  background: #4a4a4a;
  color: #ffffff;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  width: 100%;
  max-width: 1200px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  box-sizing: border-box;
}

.footer-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
}

.footer-title {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 2.5rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
  line-height: 1.2;
}

.footer-subtitle {
  font-size: 1.2rem;
  color: #ffffff;
  margin: 0;
  font-weight: 400;
}

.footer-right {
  display: flex;
  align-items: center;
}

.footer-contact {
  font-size: 1.2rem;
  color: #ffffff;
  margin: 0;
  font-weight: 400;
}

/* Responsive Design */
@media (max-width: 768px) {
  .footer {
    height: auto;
    min-height: 150px;
    padding: 2rem 0;
  }
  
  .footer-content {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 0 1rem;
  }
  
  .footer-title {
    font-size: 2rem;
  }
  
  .footer-subtitle,
  .footer-contact {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .footer-title {
    font-size: 1.5rem;
  }
  
  .footer-subtitle,
  .footer-contact {
    font-size: 0.9rem;
  }
}
</style>