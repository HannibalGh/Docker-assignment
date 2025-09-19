from flask import Flask, jsonify 
import random 
from datetime import datetime


app = Flask(__name__)


@app.route("/data") 
def data():
    unsorted_list = [random.randint(1,30) for _ in range(15)]

    raw_sorted = sorted(unsorted_list)

    unique_sorted = []
    for num in raw_sorted:
        if not unique_sorted or num != unique_sorted[-1]:
            unique_sorted.append(num)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response = {
        "data": {
            "unsorted": unsorted_list,
            "sorted": {
                "raw": raw_sorted,
                "unique": unique_sorted
            }
        },
        "timestamp": timestamp
    }

    return jsonify(response)
    



if __name__ == "__main__":
    app.run()


