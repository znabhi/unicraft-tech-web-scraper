# unicraft-tech-web-scraper

> **Web Scraping Tool** – Unicraft Tech Assignment

---

## 🎯 Features Implemented

- ✅ **Basic Info**  
  - Company Name, Website URL, Email, Phone  
- ✅ **Optional Info**  
  - Physical Address & Social Links (if found)  
  - Tech Stack (detected via HTML analysis)  
  - Current Projects & Competitors (when listed)  
- ✅ **Headless Browser** (Selenium) support for JS‑rendered pages  
- ✅ **React Dashboard** to monitor scraping jobs  
- ✅ **Error Handling & Logging** (graceful failures + clear messages)  
- ✅ **Output** saved in `data/output.json`

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask, Requests, BeautifulSoup, Selenium  
- **Frontend**: React, Axios, Create‑React‑App  
- **Output Format**: JSON

---

## 🚀 How to Run

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Demo

<video src="demo.mp4" controls width="600">
  Your browser does not support the video tag.
</video>

[▶️ Watch the full demo video](demo.mp4)
