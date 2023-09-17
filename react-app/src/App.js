import React from "react";

function App() {
  return (
    <div className="App">
      <head>"We Care"</head>
      <main>
        {/* Render the EmbeddedMap component
        src="https://kepler.gl/demo?mapUrl=https://gist.githubusercontent.com/adviti-mishra/e5e432fb8776b59e0055d845a0d82b59/raw/ad2cf4761fc7fffdff50d6b122a500ba3fd458d6/mapBos.json"
        
        */}
        <div>
          <iframe
            title="Embedded HTML"
            src="https://kepler.gl/demo?mapUrl=https://gist.githubusercontent.com/adviti-mishra/a2cf7f08bceb88aa6153447e81edd79c/raw/7701fae7c6783831ff1f4f91a65abedfa6979d75/mapSentiments.json"
            width="100%"
            height="600px"
            style={{ overflow: "hidden" }}
            scrolling="no" // Add this attribute
          ></iframe>
        </div>
      </main>
    </div>
  );
}

export default App;
