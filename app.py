from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import telebot

# إعداد التوكن الخاص بتيليجرام
API_TOKEN = '7798685596:AAGDvfJh47-kyHbynMiDhkYB6HAIAbGfWa4'
bot = telebot.TeleBot(API_TOKEN)

# تهيئة التطبيق
app = Flask(__name__)
CORS(app)

# تحميل بيانات تسجيل الدخول إلى Firebase
cred = credentials.Certificate("echo.json")  # استبدل بالمسار الصحيح للمفتاح
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://echo-10c66-default-rtdb.firebaseio.com/'  # استبدل برابط قاعدة بياناتك
})



# تسجيل المستخدمين في Firebase
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json(force=True)  # تجنب الأخطاء في البيانات
        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

        user_id = str(data.get('user_id'))
        username = data.get('username')

        if not user_id or not username:
            return jsonify({"status": "error", "message": "Missing user data"}), 400

        ref = db.reference(f'/users/{user_id}')
        user_data = ref.get()

        if user_data:
            return jsonify({"status": "exists", "message": "User already registered!"})

        ref.set({
            'username': username,
            'balance': 0.0
        })

        bot.send_message(user_id, f"Welcome {username}, you have been registered successfully!")
        return jsonify({"status": "success", "message": "User registered successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# استرجاع الإعلانات من Firebase
@app.route('/get_ads', methods=['POST'])
def get_ads():
    try:
        ads_ref = db.reference('/ads')
        ads = ads_ref.get()

        if not ads or len(ads) == 0:
            return jsonify({"status": "error", "message": "No ads available"}), 404

        ads_list = [{"ad_id": key, "ad_text": value.get('ad_text', 'No text'), "reward": value.get('reward', 0)} for key, value in ads.items()]

        user_id = request.json.get('user_id')
        for ad in ads_list:
            bot.send_message(user_id, f"{ad['ad_text']} - Reward: {ad['reward']}")

        return jsonify({"status": "success", "ads": ads_list})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
