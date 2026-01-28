import os
import requests
from datetime import datetime, timedelta

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

def fetch_live_signals():
    # 模拟请求 GMGN 的 Pump 实时榜单
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
    # 🕒 核心修正：获取 UTC 并增加 8 小时转换为北京时间
    bj_time = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_time.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"🚀 大师级指挥部正在巡逻... 北京时间: {time_str}")

    # --- 1. 每整点发一次心跳包报时 ---
    if bj_time.minute == 0:
        send_telegram(f"⏰ <b>大师报时：指挥部运行正常！</b>\n北京时间：{time_str}\n状态：正在严密嗅探‘金狗’...")

    # --- 2. 扫描市场 ---
    tokens = fetch_live_signals()
    found_any = False
    
    for token in tokens:
        # 硬核过滤标准：池子 > $3000，持仓 < 10%
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
                f"<b>北京时间：</b> {time_str}\n"
                f"👉 <a href='{gmgn_link}'>立即进入终端</a>"
            )
            send_telegram(alert_msg)
            found_any = True
            print(f"✅ 已捕捉并发送信号: {token['symbol']}")
            break 

    if not found_any:
        print(f"💡 {time_str} 扫描完毕：暂无符合硬核标准的信号。")

if __name__ == "__main__":
    master_filter()
