from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Đặt đường dẫn tuyệt đối cho file chính
SIGNAL_FILE = "signals.txt"

# Đặt đường dẫn cho file tạm thời
TEMP_FILE = SIGNAL_FILE + ".tmp"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = None
        raw_data = request.get_data(as_text=True)  # lấy raw text

        # Nếu Content-Type là JSON
        if request.is_json:
            data = request.get_json()
            print("Nhận tín hiệu JSON từ TradingView:", json.dumps(data, indent=2))
            save_data = json.dumps(data)  # lưu JSON dạng chuỗi
        else:
            # Nếu là text thường
            data = raw_data
            print("Nhận tín hiệu TEXT từ TradingView:", data)
            save_data = data  # lưu text gốc

        if not data:
            return jsonify({"status": "fail", "message": "No data received"}), 400

        # Ghi dữ liệu vào file tạm
        with open(TEMP_FILE, "w", encoding="utf-16") as f:
            f.write(save_data)

        # Đổi tên file tạm thành file chính (atomic replace)
        os.replace(TEMP_FILE, SIGNAL_FILE)

        return jsonify({"status": "ok"})

    except Exception as e:
        print("Lỗi:", e)
        return jsonify({"status": "fail", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
