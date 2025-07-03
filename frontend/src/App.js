import React, { useState } from "react";
import axios from "axios";
import {
  ClipboardList,
  Globe,
  Loader2,
  CheckCircle,
  AlertCircle,
  Info,
} from "lucide-react";

function App() {
  const [urls, setUrls] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleScrape = async () => {
    const urlList = urls.split("\n").map((u) => u.trim()).filter(Boolean);

    if (urlList.length === 0) {
      setError("Please enter at least one valid URL.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("Scraping in progress...");
    setResults([]);

    requestAnimationFrame(async () => {
      try {
        const res = await axios.post(
          "https://unicraft-tech-web-scraper.onrender.com/api/scrape",
          {
            urls: urlList,
            use_dynamic: false,
          }
        );
        setResults(res.data.results || []);
        setMessage("Scraping completed successfully.");
      } catch (err) {
        setError("Failed to fetch data. Please try again.");
        setMessage("");
      } finally {
        setLoading(false);
      }
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-xl p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center flex justify-center items-center gap-2">
          <Globe className="h-7 w-7 text-blue-600" />
          Web Scraper Tool
        </h1>

        <textarea
          rows="5"
          className="w-full border border-gray-300 rounded p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Enter URLs (one per line)"
          value={urls}
          onChange={(e) => setUrls(e.target.value)}
          disabled={loading}
        />

        <button
          onClick={handleScrape}
          disabled={loading}
          className={`w-full py-2 px-4 rounded text-white font-semibold transition duration-200 flex items-center justify-center gap-2 ${
            loading
              ? "bg-blue-300 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading && <Loader2 className="animate-spin h-5 w-5 text-white" />}
          {loading ? "Scraping..." : "Start Scraping"}
        </button>

        {message && (
          <div className="mt-4 p-3 bg-blue-100 border border-blue-300 text-blue-700 rounded text-center flex items-center justify-center gap-2">
            <Info className="h-5 w-5" />
            {message}
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded text-center flex items-center justify-center gap-2">
            <AlertCircle className="h-5 w-5" />
            {error}
          </div>
        )}

        {results.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <ClipboardList className="h-5 w-5 text-blue-600" />
              Results
            </h2>
            <pre className="bg-gray-100 text-sm p-4 rounded overflow-x-auto max-h-96">
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
