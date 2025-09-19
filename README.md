#  Dockerised Flask Data API

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Testing](#usage)
- [Example Response](#example-response)
- [What I Learned](#what-i-learned)

##  Overview
This project is a lightweight Flask web service, containerised with Docker.

It exposes a single endpoint:
- **`/data`** → which returns JSON with the following structure:
  - **unsorted** → A list of randomly generated positive integers  
  - **sorted.raw** → The **unsorted** list sorted in ascending order  
  - **sorted.unique** → A de-duplicated and sorted version of the **unsorted** list  
  - **timestamp** → The time the request was made, formatted as `YYYY-MM-DD HH:MM:SS`   

This setup demonstrates how to wrap a simple API inside a container — a common real-world practice to make services portable, reproducible, and easy to test across environments.

## Project Structure
```bash
docker-assignment/
├── main.py          # Flask app
├── Dockerfile       # Container instructions
├── requirements.txt # Python dependencies
├── README.md        # Documentation
└── .gitignore       # Ignore venv, cache files, etc.
```

## Setup & Installation
To run this project on your local machine, follow these steps:
### 1. Clone the repo
```bash
git clone https://github.com/HannibalGh/docker-assignment.git
cd docker-assignment
```
### 2. Build the Docker image
```bash
docker build -t jagex-data-api .
```
### 3. Run the container
```bash
docker run --rm -p 7774:7774 jagex-data-api
```
- `--rm` → cleans up container after exit  
- `-p 7774:7774` → maps port 7774 inside the container to port 7774 on the host (your local machine)  

The service will now be available at: http://localhost:7774/data

## Testing

You can query the API with a curl command:

**On Git Bash (Linux/Mac/Windows Git Bash):**
```bash
curl http://localhost:7774/data
```
On PowerShell (Windows):
```bash
curl.exe http://localhost:7774/data
```
Alternatively, PowerShell also supports:
```bash
Invoke-RestMethod http://localhost:7774/data
```
Unlike ```curl.exe```, which displays the raw JSON as a single text string,
```Invoke-RestMethod``` parses the response into a PowerShell object.


## Example Response

```json
{
  "data": {
    "unsorted": [11, 3, 24, 3, 25, 1, 26, 12, 18, 27, 16, 10, 24, 14, 29],
    "sorted": {
      "raw": [1, 3, 3, 10, 11, 12, 14, 16, 18, 24, 24, 25, 26, 27, 29],
      "unique": [1, 3, 10, 11, 12, 14, 16, 18, 24, 25, 26, 27, 29]
    }
  },
  "timestamp": "2025-09-19 03:17:14"
}
```

## What I Learned

### My Learning Approach

#### Planning
- **What I did:** I broke down the assignment requirements: *“Run a lightweight webserver, expose `/data`, return JSON”*.  
- **How I approached it:** I researched which lightweight Python web frameworks are commonly used for quick JSON APIs. From reading tutorials and developer discussions, I found that Flask was the most popular and simple option for this kind of task.  
- **What I learned:** Even if you don’t know the answer immediately, you can analyse requirements and research the right tool to match the problem.  

---

#### Execution

**1. Flask basics**  
- **What I learned:** How to create a minimal Flask application, what `Flask(__name__)` does, and how `@app.route` defines endpoints. Function names don’t affect the URL path, but the route path (e.g. `/data`) does — if it doesn’t match, `curl` will return a *404 Not Found* error.  
- **How I learned it:** I read Flask’s official quickstart guide, tested small snippets locally (e.g., changing function names vs. route paths), and experimented until I understood how requests mapped to functions.  

---

**2. Returning JSON properly**  
- **What I learned:**  
  - The difference between returning raw text, dictionaries, and `jsonify()`.  
  - Flask will still return JSON if you return a dictionary directly (it auto-converts in modern versions).  
  - Using `jsonify()` is safer and more explicit — it ensures the response has the correct JSON formatting and headers.  
  - APIs need structured JSON because they’re designed for machines (browsers, apps, other services) to consume data reliably. JSON provides a consistent, language-independent way to structure responses. Unlike raw text, JSON can be parsed unambiguously — e.g., a mobile app doesn’t need to “guess” what `"hello world"` means, it gets `{"hello": "world"}` instead.  
- **How I learned it:** I tested different return types in Flask:  
  - Plain string → came back as raw text with `Content-Type: text/html`.  
  - Dictionary → Flask auto-returned JSON with correct headers.  
  - `jsonify(...)` → explicitly returned JSON safely.  
  I used `curl -i http://localhost:7774/data` to inspect both response body and headers.  

---

**3. Generating and manipulating data**  
- **What I learned:**  
  - How to remove duplicates efficiently without sorting twice.  
  - Using `set()` would require re-sorting afterwards, which adds extra *O(n log n)* complexity.  
  - This helped me understand the importance of considering time and space complexity when choosing an approach.  
  - Through trial, I found that generating 15 numbers in a range of 1–30 increased the chance of duplicates, making the deduplication effect clearer.  
  - I also came across alternatives (`dict.fromkeys()`, `itertools.groupby()`), but I opted for a manual loop because it makes the logic clearer for the reader.  
- **How I learned it:** I broke the problem into steps in my script: generating lists with `random`, then testing different deduplication methods. I compared `sorted(set(...))` (two sorts) with single-pass approaches. After experimenting, I chose a manual loop for clarity.  

---

**4. Running Flask locally vs. Docker**  
- **What I learned:**  
  - The assignment required binding to `0.0.0.0:7774`.  
  - Flask defaults to `127.0.0.1:5000`, which works fine locally but fails once containerised. Docker needs the app bound to `0.0.0.0` so it’s reachable from outside the container.  
  - Flask automatically pulls in sub-dependencies (Werkzeug, Jinja2, MarkupSafe, Click, Itsdangerous, Blinker, Colorama), which are captured in `requirements.txt` via `pip freeze`.  
- **How I learned it:** I first ran Flask locally with defaults (`127.0.0.1:5000`) and confirmed it worked. After moving to Docker, I couldn’t reach it from my host until I switched to `app.run(host="0.0.0.0", port=7774)`. Research into Flask + Docker networking explained why.  

---

**5. Docker basics**  
- **What I learned:**  
  - How to write a Dockerfile to containerise a Flask app, install dependencies from `requirements.txt`, and expose ports.  
  - Host/port can be moved out of `app.run()` and handled in the Dockerfile, separating **application logic** from **deployment configuration**.  
  - Why `python:3.12-slim` is preferred (removes unnecessary libraries → smaller, faster image).  
  - The importance of Docker caching: copying `requirements.txt` first allows dependency layers to be cached, so changes in code don’t force a reinstall of dependencies unless `requirements.txt` changes.  
- **How I learned it:** I studied Python + Flask Dockerfile examples, then rebuilt the image step by step (`docker build`, `docker run`). I found the host/port configuration detail in the Docker docs and confirmed it by testing.  

---

**6. Testing with curl**  
- **What I learned:** How to verify endpoints from outside the container using `curl`.  
- **How I learned it:** I ran `curl http://localhost:7774/data` on my host machine after starting the container. This confirmed the endpoint worked and returned valid JSON.  
