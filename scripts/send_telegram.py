import os

def main():
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    print("Script is running.")
    print(f"TELEGRAM_BOT_TOKEN set: {bool(bot_token)}")
    print(f"TELEGRAM_CHAT_ID set: {bool(chat_id)}")

if __name__ == "__main__":
    main()
