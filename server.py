from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Đặt đường dẫn tuyệt đối cho file chính
SIGNAL_FILE = "signals.txt"
# File tạm để ghi an toàn
TEMP_FILE = SIGNAL_FILE + ".tmp"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Lấy dữ liệu JSON từ TradingView
        data = request.get_json(force=True)  # ép đọc JSON dù header có sai
        if not data:
            return jsonify({"status": "fail", "message": "Empty JSON"}), 400

        print("📩 Nhận tín hiệu JSON từ TradingView:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # Ghi JSON vào file tạm
        with open(TEMP_FILE, "w", encoding="utf-16") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Đổi tên file tạm thành file chính
        os.replace(TEMP_FILE, SIGNAL_FILE)

        return jsonify({"status": "ok"})

    except Exception as e:
        print("❌ Lỗi:", e)
        return jsonify({"status": "fail", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
 
