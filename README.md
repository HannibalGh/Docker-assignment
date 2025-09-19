#  Flask Data Service (Dockerised)

##  Overview
This project is a lightweight Flask web service containerised with Docker.

It exposes one endpoint:

- **`/data`** → returns JSON with:
  - `unsorted` → random positive integers
  - `sorted.raw` → sorted version of that list
  - `sorted.unique` → deduplicated + sorted list
  - `timestamp` → request time in `YYYY-MM-DD HH:MM:SS`

This setup demonstrates how to wrap a simple API inside a container — a common real-world practice to make services portable, reproducible, and easy to test.

---

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```
### 2. Build the Docker image
```bash
docker build -t jagex-data-api
```
### 3. Run the container
```bash
docker run --rm -p 7774:7774 jagex-data-api
```
--rm → cleans up container after exit

-p 7774:7774 → maps container port 7774 to host port 7774

The service will be available at: http://localhost:7774/data

Alternatively - We can run through our GIT/Bash terminal

```bash
curl http://localhost:7774/data
```

