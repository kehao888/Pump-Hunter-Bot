import os
import requests

# 1. 定义发送工具 (必须保留，否则机器人没法说话)
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

def master_filter():
    # 2. 这里填入一个测试地址，或者以后留给爬虫自动填入
    # 示例地址：Pump.fun 某个热点币的合约
    token_address = "此处请填入真实合约地址" 

    # 3. 进化版链接：直接指向 GMGN 终端
    gmgn_link = f"https://gmgn.ai/sol/token/{token_address}"

    alert_msg = (
        f"<b>🌟 发现高爆信号！</b>\n\n"
        f"<b>👉 <a href='{gmgn_link}'>立即点击进入交易终端</a></b>\n"
        f"（GMGN 会自动识别它是内盘还是外盘 Raydium）"
    )
    
    send_telegram(alert_msg)

if __name__ == "__main__":
    master_filter()
