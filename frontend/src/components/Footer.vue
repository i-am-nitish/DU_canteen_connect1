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
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet's default icon paths (Vite doesn't bundle them automatically)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

export default {
  name: "Footer",
  mounted() {
    // 1. Initialize the map
    const map = L.map('map', {
      zoomControl: false,
      attributionControl: false
    }).setView([28.6902, 77.2072], 14); // Centered on DU North Campus

    // 2. Add the OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19
    }).addTo(map);

    // 3. LIST OF CANTEENS TO TARGET
    // You can add more here. Format: { name: "Name", coords: [lat, long] }
    const canteens = [
      { name: "Jubilee Hall Mess", coords: [28.691932306052973, 77.21864410793967] },
      { name: "SOL Canteen", coords: [28.693296619827898, 77.21302418024278] },
      { name: "Pandit ji Canteen", coords: [28.691272006641036, 77.21729857816447] },
      { name: "Gwyer Hall Mess", coords: [28.690749198518496, 77.2168453693132] },
      { name: "PG Men's Hostel", coords: [28.69042294104146, 77.2167504278964] },
      { name: "Arts Faculty Canteen", coords: [28.6890, 77.2060] },
      { name: "Departmental Canteen Gate No. 4", coords: [28.68814746482982, 77.20980843458463] }
    ];

    // 4. Loop through the list and add markers
    canteens.forEach(canteen => {
      L.marker(canteen.coords)
        .addTo(map)
        .bindPopup(`<b>${canteen.name}</b>`); // Bold text for popup
    });

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