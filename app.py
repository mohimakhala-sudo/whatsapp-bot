import os
from flask import Flask, request
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

allowed_str = os.environ.get("ALLOWED_NUMBERS", "")
ALLOWED_NUMBERS = [num.strip() for num in allowed_str.split(",") if num.strip()]

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    sender = request.form.get('From')
    user_msg = request.form.get('Body')
    
    resp = MessagingResponse()
    
    if sender in ALLOWED_NUMBERS:
        try:
            ai_response = model.generate_content(user_msg)
            reply_text = ai_response.text
        except Exception as e:
            reply_text = "দুঃখিত, এআই সার্ভারে কোনো সমস্যা হয়েছে।"
    else:
        return str(resp)

    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
