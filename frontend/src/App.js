import React, { useState } from "react";
import axios from "axios";
function App() {
  const [urls, setUrls] = useState("");
  const [results, setResults] = useState([]);

  const handleScrape = async () => {
    const urlList = urls.split("\n").map(u => u.trim()).filter(Boolean);
    const res = await axios.post("http://localhost:5000/api/scrape", {
      urls: urlList,
      use_dynamic: false
    });
    setResults(res.data.results);
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Web Scraper</h1>
      <textarea
        rows="5"
        className="w-full border p-2"
        placeholder="Enter URLs (one per line)"
        value={urls}
        onChange={(e) => setUrls(e.target.value)}
      />
      <button className="mt-2 px-4 py-2 bg-blue-500 text-white" onClick={handleScrape}>
        Scrape
      </button>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Results:</h2>
        <pre className="bg-white p-4 rounded shadow mt-2">
          {JSON.stringify(results, null, 2)}
        </pre>
      </div>
    </div>
  );
}

export default App;
