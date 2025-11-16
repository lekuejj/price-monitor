import os
import requests

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID.")
        return

    message = "✅ GitHub Actions 测试：Telegram 推送成功了！"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        resp = requests.post(url, json=payload, timeout=10)
        print("Status code:", resp.status_code)
        print("Response:", resp.text)
    except Exception as e:
        print("Error sending message:", e)

if __name__ == "__main__":
    main()
