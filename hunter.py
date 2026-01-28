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
        print("📡 TG通信略有延迟")

def main():
    # 🕒 自动校准北京时间
    bj_now = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_now.strftime('%H:%M:%S')
    
    # 1. 准点报时：确认指挥部在线
    if bj_now.minute % 30 == 0:  # 每30分钟报时一次
        send_tg(f"⏰ <b>海南陵水指挥部报时</b>\n时间：{time_str}\n状态：正在严密监控中...")

    # 2. 嗅探数据
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=15&orderby=progress&direction=desc"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        tokens = res.get("data", {}).get("rank", [])
        
        for token in tokens:
            # --- 你的初衷过滤标准 ---
            progress = token.get("progress", 0)
            liquidity = token.get("liquidity", 0)
            dev_hold = token.get("dev_p", 100) # 开发者持仓比例
            
            # 过滤：进度>80% 且 池子>$3000 且 开发者持仓<10%
            if progress > 80 and liquidity > 3000 and dev_hold < 10:
                symbol = token.get("symbol")
                addr = token.get("address")
                
                msg = (
                    f"<b>🎯 发现优质金狗！</b>\n\n"
                    f"代币：${symbol}\n"
                    f"📈 进度：{progress}%\n"
                    f"💧 池子：${liquidity}\n"
                    f"👤 开发者：{dev_hold}%\n"
                    f"⏰ 时间：{time_str}\n\n"
                    f"👉 <a href='https://gmgn.ai/sol/token/{addr}'>立即进入终端</a>"
                )
                send_tg(msg)
                print(f"✅ 捕获成功: {symbol}")
                return # 抓到一个最稳的即停止，避免骚扰

        print(f"📡 {time_str} 巡逻完毕，暂未发现符合硬核标准的信号。")
        
    except Exception as e:
        print(f"❌ 数据抓取异常: {e}")

if __name__ == "__main__":
    main()
