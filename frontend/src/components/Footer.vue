<template>
  <footer class="footer">
    <div class="footer-left">
      <div class="footer-logo">
        <span class="app-name">DU Canteen Connect</span>
      </div>
    </div>

    <div class="footer-right">
      <div class="map-wrapper">
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14009.123456789!2d77.216721!3d28.644800!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390ce2b123456789%3A0xabcdef123456789!2sNorth%20Campus%2C%20Delhi%20University!5e0!3m2!1sen!2sin!4v1696521234567"
          width="100%"
          height="100%"
          style="border:0;"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>
    </div>
  </footer>
</template>



<script>
export default {
  name: "Footer",
};
</script>

<style>
.footer {
  width: 100%;
  height: 200px; /* 👈 increased height */
  background: #474747;
  color: #DBDFD0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem 2rem; /* 👈 more padding top/bottom */
  box-sizing: border-box;
}

.footer-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.app-name {
  font-size: 2.5rem;
  font-weight: 600;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  color: #DBDFD0;
}

.footer-right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-wrapper {
  width: 180px;
  height: 180px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin: 1rem 0; 
}
</style>