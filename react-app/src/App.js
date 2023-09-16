import React from "react";

const mapBoxAPIKey = process.env.MAPBOX_TOKEN;

function App() {
  // Kepler.gl configuration to be centered in Masacheusettes
  const config = {
    mapState: {
      latitude: 42.4072,
      longitude: 71.3824,
      zoom: 8,
    },
  };

  return (
    <div className="App">
      <header>
        <h1> We Care </h1>
      </header>
      <main>Kepler Map</main>
    </div>
  );
}

export default App;
