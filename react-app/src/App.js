import React from "react";
import { KeplerGl } from "kepler.gl";

const mapBoxAPIKey = process.env.REACT_APP_MAPBOX_TOKEN;

function App() {
  // Kepler.gl configuration to be centered in Masacheusettes
  const config = {
    mapState: {
      latitude: 42.4072,
      longitude: -71.3824,
      zoom: 8,
    },
  };

  return (
    <div className="App">
      <header>
        <h1> We Care </h1>
      </header>
      <main>
        <div>
          {/* <KeplerGl
            id="app-map"
            mapboxApiAccessToken={mapBoxAPIKey}
            initialConfig={config}
          ></KeplerGl> */}
        </div>
      </main>
    </div>
  );
}

export default App;
