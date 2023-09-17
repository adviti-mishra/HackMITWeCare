import React from "react";

function App() {
  return (
    <div className="App">
      <main>
        {/* Render the EmbeddedMap component
        src="https://kepler.gl/demo?mapUrl=https://gist.githubusercontent.com/adviti-mishra/e5e432fb8776b59e0055d845a0d82b59/raw/ad2cf4761fc7fffdff50d6b122a500ba3fd458d6/mapBos.json"
        
        */}
        <iframe
          title="Embedded HTML"
          src="https://kepler.gl/demo?mapUrl=https://gist.githubusercontent.com/adviti-mishra/45913b66bc14a0f2363cd98f77e62fb0/raw/19216c90bdff01fa61be830ea8197864318c4b36/mapFinal.json"
          width="100%"
          height="400px"
          style={{ overflow: "hidden" }}
          scrolling="no" // Add this attribute
        ></iframe>
      </main>
    </div>
  );
}

export default App;
