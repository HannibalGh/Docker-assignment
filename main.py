from flask import Flask, jsonify 
import random 
from datetime import datetime

# Initialise the Flask app
# Flask is lightweight and lets me quickly spin up APIs without much setup
app = Flask(__name__)

# Ensure jsonify does not sort keys alphabetically and the output order is preserved.
app.json.sort_keys = False

# Define an endpoint at /data
@app.route("/data") 
def data():
    # Step 1: Generate a random list
    # 15 random integers between 1–30 (so each call to the endpoint looks different)
    unsorted_list = [random.randint(1,30) for _ in range(15)]

    # Step 2: Sort the list
    # Python's sorted() returns a new list in ascending order
    raw_sorted = sorted(unsorted_list)

    # Step 3: Build a list of unique values
    # Could have just used set(), but set() doesn’t guarantee order.
    # Doing it manually here means I preserve the sorted order while removing duplicates.
    unique_sorted = []
    for num in raw_sorted:
        # Only add the number if it's different from the last one we added
        if not unique_sorted or num != unique_sorted[-1]:
            unique_sorted.append(num)

    # Step 4: Add a timestamp
    # Helpful for debugging/testing — makes it obvious when the response was generated
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Step 5: Package everything into a JSON structure
    # This makes the response easy to parse if I query with curl, Postman, or from another service
    response = {
        "data": {
            "unsorted": unsorted_list,   # Original random numbers
            "sorted": {
                "raw": raw_sorted,       # Sorted with duplicates
                "unique": unique_sorted  # Sorted with duplicates removed
            }
        },
        "timestamp": timestamp          # Current time of generation
    }

    # Step 6: Return JSON to the client
    return jsonify(response)


    
# Only run the Flask dev server if this file is executed directly
# Default is http://127.0.0.1:5000 but can be changed with host/port params
# Preserved in case I want to run the app locally 
if __name__ == "__main__":
    app.run()  