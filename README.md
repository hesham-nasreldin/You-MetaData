YouTube Metadata — Local demo (English + Arabic RTL)

This project provides two ways to fetch basic metadata (title, channel, upload date) for YouTube videos using `yt-dlp`:

- A small Flask JSON API: `test.py` exposes `POST /metadata` and returns metadata for a single URL.
- A Streamlit UI: `main.py` — paste one or multiple YouTube URLs (one per line) and get a table of results. Supports English and Arabic (RTL).

Requirements

- Python 3.8+
- Install the dependencies in a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Running the Flask API (single-URL JSON API)

```bash
# from project root
python test.py
# POST to http://127.0.0.1:5000/metadata with JSON: {"url": "https://..."}
```

Running the Streamlit UI (multi-URL, RTL support)

```bash
streamlit run main.py
```

Open the Streamlit URL the command prints (usually http://localhost:8501).

Optional: Serving the static frontend
If you prefer the original static frontend (index.html) and want it to call the Flask API, serve the folder with a simple static server:

```bash
python -m http.server 8000
# then open http://127.0.0.1:8000/index.html
```

Notes & Tips

- `yt-dlp` requires network access to fetch metadata and may be rate-limited by YouTube.
- If you add many URLs at once, expect the process to take time; Streamlit shows a spinner per URL.
- To export results from Streamlit, use the table and copy/paste, or I can add a CSV export button.

Files of interest

- `test.py` — Flask API
- `main.py` — Streamlit UI (supports multiple URLs and Arabic/RTL)
- `index.html`, `script.js`, `style.css` — static frontend with language toggle
- `requirements.txt` / `requirementst.txt` — Python dependencies

If you want, I can pin exact package versions, add a `make`/PowerShell script to run everything, or add CSV export in the Streamlit UI.
