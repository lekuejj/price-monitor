import json
import os
import requests
from datetime import datetime, timezone, timedelta
from openai import OpenAI

DATA_FILE = "data/products.json"

def get_raw_prices():
    """
    从 JSON 文件加载商品数据。
    """
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_prompt(price_data):
    """
    把原始价格数据塞进 prompt，让模型来：
    - 比较当前价 vs 目标价
    - 用中文写一份 Markdown 报告
    """
    est = timezone(timedelta(hours=-5))
    now = datetime.now(est).strftime("%Y-%m-%d %H:%M")

    return f"""
你是一个帮我做价格监控汇总的助手。现在时间是美东时间 {now}。

下面是一组商品的价格数据（JSON）：

{price_data}

请你根据这些数据，输出一段 **中文 Markdown** 报告，要求：

1. 先给一个标题，比如“📊 今日价格监控结果（美东时间 xxxx-xx-xx xx:xx）”
2. 对每个商品逐条列出：
   - 商品名称
   - 当前价格（保留两位小数，美元）
   - 目标价格
   - 当前价格是否低于目标价（给一句简短建议：例如“已低于目标价，可以考虑下手”或“还没到目标价，继续观望”）
3. 如果所有商品都没有低于目标价，请在最后加一句类似“今天没有达到目标价的商品”。

格式用 Markdown，语气正常一点就行，不要太啰嗦。
"""


def call_openai_to_build_report(price_data):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)

    prompt = build_prompt(price_data)

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",  # 或你有权限的其他模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return resp.choices[0].message.content.strip()


def send_telegram_message(text: str):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }

    resp = requests.post(url, json=payload, timeout=15)
    print("Telegram status code:", resp.status_code)
    print("Telegram response:", resp.text)


def main():
    prices = get_raw_prices()
    report = call_openai_to_build_report(prices)
    print("=== OpenAI Report ===")
    print(report)
    send_telegram_message(report)


if __name__ == "__main__":
    main()
