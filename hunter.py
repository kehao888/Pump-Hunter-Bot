import os
import requests
from datetime import datetime

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    requests.post(url, json=payload)

def fetch_live_signals():
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=10&orderby=progress&direction=desc"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data.get("code") == 0:
            return data["data"]["rank"]
    except:
        return []

def master_filter():
    # 1. 获取当前北京时间 (GitHub 服务器默认是 UTC，我们加 8 小时)
    now = datetime.now()
    # 简单的报时逻辑：每小时的第 0 分钟运行那一轮会发报时包
    # 或者为了测试，我们设置成每轮运行都打印日志，每小时报一次
    
    print(f"📡 巡逻中... 当前时间: {now.strftime('%H:%M:%S')}")
    
    # 模拟心跳：如果是每小时的 0 分，发一条报时消息
    if now.minute == 0:
        send_telegram(f"⏰ <b>大师报时：指挥部运行正常！</b>\n当前时间：{now.strftime('%Y-%m-%d %H:%M')}\n状态：正在严密监控‘金狗’信号...")

    tokens = fetch_live_signals()
    
    found_any = False
    for token in tokens:
        # --- 保持你之前的硬核过滤标准 ---
        progress = token.get("progress", 0)
        dev_hold = token.get("dev_p", 100)
        liquidity = token.get("liquidity", 0)
        
        if progress > 80 and dev_hold < 10 and liquidity > 3000:
            address = token["address"]
            gmgn_link = f"https://gmgn.ai/sol/token/{address}"
            
            alert_msg = (
                f"<b>🎯 发现高价值金狗！</b>\n\n"
                f"<b>代币：</b> ${token['symbol']}\n"
                f"<b>💧 池子：</b> ${liquidity}\n"
                f"👉 <a href='{gmgn_link}'>进入终端</a>"
            )
            send_telegram(alert_msg)
            found_any = True
            break # 抓到一个最稳的就收工

    if not found_any:
        print("💡 本轮未发现符合标准的高质量信号。")

if __name__ == "__main__":
    master_filter()
