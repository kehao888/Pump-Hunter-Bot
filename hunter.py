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
    
    print(f"🕵️ 猎手巡逻中... 北京时间: {time_str}")

    # 1. 嗅探数据：GMGN Pump 实时榜单
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=15&orderby=progress&direction=desc"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        tokens = res.get("data", {}).get("rank", [])
        
        found_flag = False
        for token in tokens:
            # --- 硬核初衷标准 ---
            progress = token.get("progress", 0)
            liquidity = token.get("liquidity", 0)
            dev_hold = token.get("dev_p", 100)
            
            # 标准：进度>80% 且 池子>$3000 且 开发者持仓<10%
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
                print(f"✅ 成功锁定并推送: {symbol}")
                found_flag = True
                break # 每一轮抓一个最稳的，防止刷屏

        if not found_flag:
            print(f"💡 {time_str} 扫描完毕，暂无符合硬核标准的信号。")
            
    except Exception as e:
        print(f"❌ 数据抓取异常: {e}")

if __name__ == "__main__":
    main()
