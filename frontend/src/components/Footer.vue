<template>
  <footer class="footer">
    <div class="footer-left">
      <div class="footer-logo">
        <span class="app-name">DU Canteen Connect</span>
      </div>
    </div>

    <div class="footer-right">
      <div class="map-wrapper">
        <div id="map" style="width: 100%; height: 100%;"></div>
      </div>
    </div>
  </footer>
</template>

<script>
// Import Leaflet
import L from 'leaflet';

export default {
  name: "Footer",
  mounted() {
    // Initialize the map inside the 'map' div
    const map = L.map('map', {
      zoomControl: false, // Hides the +/- buttons to keep it clean
      attributionControl: false // Hides the "Leaflet" text to save space
    }).setView([28.6139, 77.2090], 13);

    // Add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19
    }).addTo(map);

    // Add a marker for Delhi University (North Campus area)
    L.marker([28.6902, 77.2072]).addTo(map)
      .bindPopup('DU North Campus')
      .openPopup();

    // --- OPTIONAL: Keep the "Live Location" feature if you want ---
    // If you want the footer map to track the user, uncomment this block:
    /*
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition((position) => {
        const lat = position.coords.latitude;
        const long = position.coords.longitude;
        
        // Move the view to user
        map.setView([lat, long], 15);

        // Add a user marker
        L.marker([lat, long]).addTo(map)
          .bindPopup("You are here");
      });
    }
    */
  }
};
</script>

<style scoped>
.footer {
  width: 100%;
  min-height: 200px;
  background: #474747;
  color: #DBDFD0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 2rem;
  box-sizing: border-box;
  flex-wrap: wrap; 
  gap: 1.5rem;
  margin-top: auto;        /* pushes footer to bottom */
  position: relative; 
}

.footer-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 1;
  min-width: 200px;
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
  flex: 1;
  min-width: 200px;
}

.map-wrapper {
  /* I increased the size slightly so the map is more useful */
  width: 250px; 
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin: 1rem 0;
  /* This ensures the map stays inside the rounded corners */
  z-index: 0; 
}

@media (max-width: 768px) {
  .footer {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.5rem;
    gap: 2rem;
  }

  .app-name {
    font-size: 2rem;
    text-align: center;
  }

  .footer-left,
  .footer-right {
    width: 100%;
    align-items: center;
    justify-content: center;
  }

  .map-wrapper {
    width: 100%;
    max-width: 300px;
    height: 200px;
  }
}
</style>