from flask import Flask, request
import telebot

API_TOKEN = '7798685596:AAGDvfJh47-kyHbynMiDhkYB6HAIAbGfWa4'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    bot.send_message(chat_id, "Received your data: " + str(data))
    return "OK", 200

if __name__ == "__main__":
 app.run(debug=True)
