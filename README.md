#  Dockerised Flask Data API
## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Example Response](#example-response)
- [Challenges & Lessons Learned](#challenges--lessons-learned)
- [Reflections & Next Steps](#reflections--next-steps)


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

## Getting Started
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

## Challenges & Lessons Learned

### Approach & Process
When I first read the assignment specification, I recognised that I was already familiar with some of the required tasks, but other parts would require further research. I also factored the suggested three-hour time box into my planning, which shaped how I prioritised learning and execution.



#### Planning
- **Understanding requirements:** I carefully read the assignment and broke it down into smaller tasks:  
  1. Run a lightweight webserver.  
  2. Expose a `/data` endpoint.  
  3. Return a JSON response with unsorted numbers, sorted numbers, unique numbers, and a timestamp.  
  4. Containerise the application with Docker and make it accessible via `curl`.  

- **Researching options:** I explored which Python web frameworks are suitable for building small APIs quickly. From tutorials and developer discussions, I compared options like **Flask** (minimal, widely used), **FastAPI** (modern, async, but heavier for a simple task), and **Django** (too big for the scope). Flask stood out as the most appropriate choice.  

- **Planning the API flow:** I mapped out the steps the application would need to follow:  
  1. Generate random integers.  
  2. Sort and deduplicate the list.  
  3. Wrap results in JSON with a timestamp.  
  4. Return the JSON when `/data` is requested.  

- **Designing for containerisation:** I considered how the application would run inside Docker:  
  - The app should bind to `0.0.0.0` so it’s reachable outside the container.  
  - Ports needed to be explicitly mapped (`7774:7774`).  
  - Dependencies should be captured in `requirements.txt` for reproducibility.  

- **What I learned:** Even without knowing the solution up front, you can break down requirements into smaller problems, research the right tools for each, and sketch out the architecture before writing a single line of code.

---

#### Execution

**1. Flask basics**  

- **What I learned:**  
  - How to create a minimal Flask application.  
  - Why `Flask(__name__)` is used — it tells Flask where to find resources (templates, configs) and establishes the current module as the application entry point.  
  - How `@app.route` defines endpoints. Function names themselves don’t affect the URL path, but the route string (e.g. `/data`) does — if it doesn’t match, requests will return a **404 Not Found**.  

- **How I learned it:**  
I read Flask’s [official quickstart guide](https://flask.palletsprojects.com/en/latest/quickstart/) and then tested small snippets locally — for example, changing function names vs. route paths to see which ones actually changed the behaviour. This hands-on debugging helped me understand exactly how Flask maps requests to functions.



---
**2. Returning JSON properly**  

- **What I learned:**  
  - The difference between returning raw text, dictionaries, and `jsonify()`.  
  - Flask will auto-convert a dictionary into JSON in modern versions, but `jsonify()` is safer and more explicit — it guarantees correct formatting and sets the proper `Content-Type: application/json` header.  
  - APIs need structured JSON because they’re consumed by machines (apps, browsers, services), not humans. JSON provides a standard, language-independent structure that avoids ambiguity — unlike raw text, which could be misinterpreted. For example, instead of guessing what `"hello world"` means, a client receives `{"hello": "world"}`, which is unambiguous.  

- **How I learned it:**  
  I experimented with different return types:  
  - Returning a plain string → came back as raw text with `Content-Type: text/html`.  
  - Returning a dictionary → Flask auto-returned JSON with correct headers.  
  - Returning `jsonify(...)` → explicitly returned JSON safely every time.  
  I confirmed these differences locally using `curl -i http://localhost:7774/data` to inspect both the body and the response headers.


---

**3. Generating and manipulating data**  
- **What I learned:**  
  - How to generate lists of random numbers using Python’s `random` module.  
  - How to remove duplicates efficiently without sorting twice. Using `set()` works for deduplication but, because sets are unordered, it forces a second sort — which i learned adds extra *O(n log n)* complexity. Encountering this made me think more carefully about time and space complexity when writing code.  
  - The alternatives to `set()` such as `dict.fromkeys()` and `itertools.groupby()`. I ultimately opted for a manual loop because it keeps the logic transparent and easy for readers to follow.  
  - Through experimentation, I found that generating 15 numbers within a range of 1–30 struck a good balance: it produced enough duplicates to demonstrate the deduplication step clearly, without creating an overwhelming list.  

- **How I learned it:**  
  - Consulted Python documentation and [online examples](https://www.datacamp.com/tutorial/python-how-to-remove-the-duplicates-from-a-list) for deduplication techniques.  
  - Generated random lists with `random` and inspected the results.  
  - Tested different approaches:  
    - `sorted(set(...))` → simple, but involves two sorts.  
    - `dict.fromkeys()` / `itertools.groupby()` → efficient, but less readable.  
    - Manual loop → slightly longer, but the clearest way to show exactly how duplicates are removed.  



---

**4. Running Flask locally vs Docker**  
- **What I learned:**  
  - Flask defaults to `127.0.0.1:5000`, which works fine when running locally.  
  - However, inside Docker, this binding fails because the service is only visible inside the container. To make it accessible externally, Flask needs to bind to `0.0.0.0`.  
  - The binding that was specified in the assignment (`0.0.0.0:7774`) ensured the service was reachable from outside the container.

- **How I learned it:**  
  I first ran Flask locally with defaults (`127.0.0.1:5000`) and confirmed it worked. When I moved it into Docker, I anticipated that the default binding would fail (since I had already noted in my planning phase that the app needed to bind to `0.0.0.0`). As expected, I couldn’t reach it from the host until I switched to:  
  ```python
  app.run(host="0.0.0.0", port=7774)
  ```
---

**5. Docker fundamentals**  
- **What I learned:**  
  - How to write a Dockerfile to containerise a Flask app, install dependencies from `requirements.txt`, and expose ports.  
  - The Flask dependencies that are captured when freezing requirements (Werkzeug, Jinja2, MarkupSafe, Click, Itsdangerous, Blinker, Colorama).  
  - That host and port can be configured outside of `app.run()` and handled in the Dockerfile. This separates **application logic** from **deployment configuration**, which I learned is best practice → I adopted approach and updated my Python code accordingly.  
  - Why `python:3.12-slim` is preferred (fewer unnecessary libraries → smaller, faster image).  
  - The importance of Docker caching layers: copying `requirements.txt` first allows dependency layers to be cached, so only changes to `requirements.txt` trigger a reinstall.  

- **How I learned it:**  
I studied Dockerfile examples for Flask applications using [online resources](https://www.geeksforgeeks.org/devops/dockerize-your-flask-app/), then rebuilt the image step by step (`docker build`, `docker run`). While reviewing the [Docker documentation](https://docs.docker.com/build/concepts/context/), I learned that host/port configurations could be placed inside the Dockerfile and confirmed this by testing different builds.


---

**6. Testing with curl**  

- **What I learned:**  
  - How to verify that a Flask service running inside Docker is accessible from the host machine.  
  - That `curl` can be used not just to fetch the raw response body but also to inspect HTTP status codes and headers, which is essential when testing APIs.  
  - The different options for testing JSON responses: using `curl` in Git Bash (`curl http://localhost:7774/data`), `curl.exe` in PowerShell (`curl.exe http://localhost:7774/data`), and the PowerShell-native alternative `Invoke-RestMethod`.


- **How I learned it:**  
  I followed the [curl manual](https://curl.se/docs/manual.html) to understand available flags and behaviour. I then ran `curl http://localhost:7774/data` on my host after starting the container, which confirmed the endpoint was reachable and returned valid JSON.  
  I also used the `-i` flag (`curl -i http://localhost:7774/data`) to inspect response headers such as `Content-Type: application/json`, reinforcing why APIs must return structured JSON.  
  On Windows, I checked the [Microsoft docs](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod) to understand the differences between PowerShell’s `curl` alias, `curl.exe`, and `Invoke-RestMethod`.  

## Reflections & Next Steps
Overall, this project taught me a lot. It was a very enjoyable experience, which gave me the opportunity to deepen my understanding of familiar technologies (Docker) while also exploring new ones (Flask). More importantly, it reinforced the value of breaking problems into manageable steps, planning carefully, and researching solutions before writing code — an approach that makes the journey more productive but also feel more rewarding.

The majority of my time was spent researching approaches, consulting documentation, and writing this README. Once I understood the requirements and the tools, the implementation was straightforward. In total, the project took me slightly longer than the three-hour time box I had originally planned.  

Looking ahead, I plan to use this knowledge as a springboard to explore more advanced solutions. In particular, I intend to attempt the same task using AWS services such as Lambda, which I will document in a separate repository located [here]().

