import os
import requests
from datetime import datetime, timedelta

def send_tg(msg):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except:
        print("📡 TG发送超时")

def main():
    bj_now = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_now.strftime('%H:%M:%S')
    print(f"🕵️ 正在尝试深度嗅探... 北京时间: {time_str}")

    # 1. 深度伪装：模拟最新版 Chrome 浏览器的请求头
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=15&orderby=progress&direction=desc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://gmgn.ai/pump",
        "Origin": "https://gmgn.ai"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        # 如果返回 403 或 429，说明被拦截了
        if response.status_code != 200:
            print(f"❌ 抓取被拦截！状态码: {response.status_code}")
            # 如果是 403，可能需要换个时间点或者更新 User-Agent
            return

        data = response.json()
        tokens = data.get("data", {}).get("rank", [])
        print(f"✅ 成功抓取到 {len(tokens)} 个实时代币数据")

        found_flag = False
        for token in tokens:
            # --- 你的硬核过滤初衷 ---
            progress = token.get("progress", 0)
            liquidity = token.get("liquidity", 0)
            dev_hold = token.get("dev_p", 100)
            
            if progress > 80 and liquidity > 3000 and dev_hold < 10:
                symbol = token.get("symbol")
                addr = token.get("address")
                msg = (
                    f"<b>🎯 发现优质目标：${symbol}</b>\n\n"
                    f"📈 进度：{progress}%\n"
                    f"💧 池子：${liquidity}\n"
                    f"👤 开发者：{dev_hold}%\n"
                    f"⏰ 时间：{time_str}\n\n"
                    f"👉 <a href='https://gmgn.ai/sol/token/{addr}'>立即进入终端</a>"
                )
                send_tg(msg)
                print(f"✅ 发现金狗: {symbol}")
                found_flag = True
                break 

        if not found_flag:
            print(f"💡 {time_str} 扫描完成，目前没有符合标准的猎物。")

    except Exception as e:
        print(f"📡 抓取过程中出现崩溃: {e}")

if __name__ == "__main__":
    main()
