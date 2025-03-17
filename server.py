from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

# Route to serve CSV file
@app.route('/data/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('/home/liixnyu/FIT5120_onboarding/data', filename)

# ✅ 确保 Flask 能正确找到 HTML 文件
frontend_path = "/home/liixnyu/FIT5120_onboarding/project_frontend"

# ✅ OpenWeatherMap API Key（请确保安全存储，在生产环境中建议通过环境变量设置）
WEATHER_API_KEY = "5e0aeb5696124e92aaa63354251503"

# ✅ 获取 UV 指数的函数
def get_uv_index(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=uv_index"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "hourly" in data and "uv_index" in data["hourly"]:
            return data["hourly"]["uv_index"][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching UV data: {e}")
        return None

# ✅ 获取温度数据的函数
def get_temperature(city):
    if not WEATHER_API_KEY:
        return {"error": "API Key is missing"}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "main" in data and "temp" in data["main"]:
            return {"temperature": data["main"]["temp"]}
        return {"error": "No temperature data found"}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching temperature data: {e}")
        return {"error": "Unable to fetch temperature data"}

# ✅ 路由：返回前端 HTML 页面
@app.route('/')
def home():
    return send_from_directory(frontend_path, "pgp_onboarding_home.html")

@app.route('/calculator')
def calculator():
    return send_from_directory(frontend_path, "pgp_onboarding_calculator.html")

@app.route('/uvlevels')
def uvlevels():
    return send_from_directory(frontend_path, "pgp_onboarding_uvlevels.html")

@app.route('/information')
def information():
    return send_from_directory(frontend_path, "pgp_onboarding_information.html")

# ✅ API 接口：获取 UV 指数
@app.route('/api/uv', methods=['GET'])
def uv_api():
    latitude = request.args.get("lat")
    longitude = request.args.get("lng")
    if not latitude or not longitude:
        return jsonify({"error": "Invalid coordinates"}), 400

    uv_index = get_uv_index(float(latitude), float(longitude))
    if uv_index is None:
        return jsonify({"error": "Unable to get UV data"}), 500

    return jsonify({"uv_index": uv_index})

# ✅ API 接口：获取温度数据
@app.route('/api/temperature', methods=['GET'])
def temperature_api():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    temperature_data = get_temperature(city)
    return jsonify(temperature_data)

# ✅ 让 PythonAnywhere 识别 Flask 应用
application = app

if __name__ == '__main__':
    app.run(debug=True)
