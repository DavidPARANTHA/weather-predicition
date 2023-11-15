from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_weather(api_key, city_name):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temperature_kelvin = data["main"]["temp"]
        temperature_celsus= temperature_kelvin - 273.15
        humidity = data["main"]["humidity"]
        return weather, temperature_celsus, humidity
    else:
        return "City not found"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_name = request.form["city"]
        api_key = "9d9a02ad4f3aae4cfdaab78542c01132"  # Replace with your OpenWeatherMap API key
        weather, temperature, humidity = get_weather(api_key, city_name)

        return render_template("index.html", city=city_name, weather=weather, temperature=temperature, humidity=humidity)

    return render_template("index.html", city=None, weather=None, temperature=None, humidity=None)

if __name__ == "__main__":
    app.run(debug=True)