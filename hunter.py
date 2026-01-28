import os
import requests
from datetime import datetime, timedelta

def send_tg(msg):
    """发送消息到 Telegram"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except Exception as e:
        print(f"📡 TG发送失败: {e}")

def main():
    # 🕒 核心修正：获取并转换北京时间
    bj_now = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_now.strftime('%H:%M:%S')
    
    # 1. 心跳确认：每 30 分钟强制发一条，确认机器人没死
    if bj_now.minute % 30 == 0:
        send_tg(f"⏰ <b>系统报时</b>\n北京时间：{time_str}\n状态：正在严密嗅探‘金狗’...")

    # 2. 抓取 GMGN 实时榜单
    url = "https://gmgn.ai/api/v1/token_list/sol/pump?limit=15&orderby=progress&direction=desc"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        tokens = res.get("data", {}).get("rank", [])
        
        found_flag = False
        for token in tokens:
            # --- 你的初衷过滤标准 ---
            progress = token.get("progress", 0)
            liquidity = token.get("liquidity", 0)
            dev_hold = token.get("dev_p", 100) # 开发者持仓比例
            
            # 标准：进度 > 80% 且 池子 > $3000 且 开发者持仓 < 10%
            if progress > 80 and liquidity > 3000 and dev_hold < 10:
                symbol = token.get("symbol")
                addr = token.get("address")
                
                msg = (
                    f"<b>🎯 发现优质目标：${symbol}</b>\n\n"
                    f"📈 进度：{progress}%\n"
                    f"💧 池子：${liquidity}\n"
                    f"👤 开发者持仓：{dev_hold}%\n"
                    f"⏰ 发现时间：{time_str}\n\n"
                    f"👉 <a href='https://gmgn.ai/sol/token/{addr}'>立即进入 GMGN 终端</a>"
                )
                send_tg(msg)
                print(f"✅ 成功锁定并发送通知: {symbol}")
                found_flag = True
                break # 每一轮只推一个最稳的

        if not found_flag:
            print(f"💡 {time_str} 扫描完毕：当前场上无符合标准的‘金狗’。")
            
    except Exception as e:
        print(f"❌ 运行异常: {e}")

if __name__ == "__main__":
    main()
