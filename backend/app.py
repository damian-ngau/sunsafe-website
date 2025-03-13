from flask import Flask, request, jsonify
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration for PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/weatherdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# OpenWeatherMap API key and base URL
API_KEY = os.getenv('OPENWEATHER_API_KEY')  # Store API key as an environment variable
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

print(f"API_KEY: {API_KEY}")  

# Database model to store weather search history
class WeatherSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WeatherSearch {self.city}>'

# Route to fetch weather data
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400

    # Query OpenWeatherMap API for weather data
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Get temperature in Celsius
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch weather data"}), 500

    data = response.json()

    # Extract relevant weather information
    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity']
    }

    # Store the search in the database
    weather_search = WeatherSearch(city=city)
    db.session.add(weather_search)
    db.session.commit()

    return jsonify(weather_info)

@app.route("/history", methods=["GET"])
def get_history():
    # Get the weather search history from the database
    searches = WeatherSearch.query.all()
    history = [
        {"city": search.city, "timestamp": search.timestamp} for search in searches
    ]
    return jsonify(history)

if __name__ == "__main__":
    # Make sure the database is created
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=False, host="0.0.0.0", port=5000)
