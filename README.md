#  Dockerised Flask Data API

##  Overview
This project is a lightweight Flask web service, containerised with Docker.

It exposes a single endpoint:
- **`/data`** → which returns JSON with the following structure:
  - **unsorted** → A list of randomly generated positive integers  
  - **sorted.raw** → The **unsorted** list sorted in ascending order  
  - **sorted.unique** → A de-duplicated and sorted version of the **unsorted** list  
  - **timestamp** → The time the request was made, formatted as `YYYY-MM-DD HH:MM:SS`   

This setup demonstrates how to wrap a simple API inside a container — a common real-world practice to make services portable, reproducible, and easy to test across environments.

---

## Setup & Run
To run this project on your local machine, follow these steps:
### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
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

### 4. Test the endpoint
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
