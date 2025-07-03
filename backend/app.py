from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import extract_info
from dynamic_scraper import extract_dynamic_info
from utils import save_json

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        urls = data.get("urls", [])
        use_dynamic = data.get("use_dynamic", False)
        results = []

        for url in urls:
            info = extract_dynamic_info(url) if use_dynamic else extract_info(url)
            results.append(info)

        save_json(results, "data/output.json")
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
