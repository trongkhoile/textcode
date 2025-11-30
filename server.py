from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

SIGNAL_FILE = "signals.txt"
TEMP_FILE = SIGNAL_FILE + ".tmp"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "fail", "message": "Empty JSON"}), 400

        print("📩 Nhận tín hiệu JSON từ TradingView:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        # ⭐️ THAY ĐỔI: Dùng encoding="utf-8"
        # Ghi JSON vào file tạm
        with open(TEMP_FILE, "w", encoding="utf-8") as f:
            # Ghi JSON và thêm ký tự xuống dòng (\n) để phân biệt tín hiệu
            json_string = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            f.write(json_string + '\n') 

        # Đổi tên file tạm thành file chính (Atomic write)
        os.replace(TEMP_FILE, SIGNAL_FILE)

        return jsonify({"status": "ok"})

    except Exception as e:
        print("❌ Lỗi:", e)
        return jsonify({"status": "fail", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
