from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = 'DEMO_KEY'  
API_URL = 'https://api.nasa.gov/neo/rest/v1/feed'

def get_neo_data(start_date, end_date):
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error fetching data: {response.status_code}"}

@app.route('/neo', methods=['GET'])
def neo():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Date validation
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    data = get_neo_data(start_date, end_date)
    if "error" in data:
        return jsonify(data), 500

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)