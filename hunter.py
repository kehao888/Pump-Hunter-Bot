import os
import requests
from datetime import datetime, timedelta

def main():
    # 强制校准北京时间
    bj_now = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_now.strftime('%Y-%m-%d %H:%M:%S')
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print(f"🕵️ 正在尝试发送测试消息... 当前北京时间: {time_str}")
    
    msg = f"⏰ <b>指挥部紧急调试</b>\n\n北京时间：{time_str}\n状态：如果看到这条消息，说明你的密钥和网络全部通了！"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    r = requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
    print(f"📡 响应状态码: {r.status_code}")
    print(f"📡 响应内容: {r.text}")

if __name__ == "__main__":
    main()
