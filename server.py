from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_uv_index(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=uv_index"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        uv_index = data["hourly"]["uv_index"][0]  # 获取当前小时的 UV 值
        return uv_index
    except requests.exceptions.RequestException as e:
        print(f"Error fetching UV data: {e}")
        return None

@app.route('/api/uv', methods=['GET'])
def uv_api():
    latitude = request.args.get("lat")
    longitude = request.args.get("lng")

    if not latitude or not longitude:
        return jsonify({"error": "Invalid coordinates"}), 400

    # 这里需要转换字符串为 float，否则 Open-Meteo API 会报错
    uv_index = get_uv_index(float(latitude), float(longitude))
    
    if uv_index is None:
        return jsonify({"error": "Unable to get UV data"}), 500

    return jsonify({"uv_index": uv_index})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
