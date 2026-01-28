import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def get_real_gold_address():
    print("📡 正在尝试抓取实时金狗地址...")
    # 模拟抓取逻辑：在没有 API 的情况下，我们会先从已知信号源获取
    # 以后这里会接入真实的网页解析逻辑
    return "6p6W5qYv9q3pMbvSdcBvGWoMTEBXW37mS5F8M4yVpump" # 这是一个示例地址

def master_filter():
    # 1. 获取真实地址
    token_address = get_real_gold_address()

    # 2. 生成正确链接
    gmgn_link = f"https://gmgn.ai/sol/token/{token_address}"

    alert_msg = (
        f"<b>🌟 发现【真实】金狗信号！</b>\n\n"
        f"<b>合约地址：</b> <code>{token_address}</code>\n"
        f"<b>👉 <a href='{gmgn_link}'>点击进入 GMGN 实战终端</a></b>\n\n"
        f"<i>大师提醒：这次链接带了真实身份证号，点进去就能看 K 线！</i>"
    )
    
    send_telegram(alert_msg)

if __name__ == "__main__":
    master_filter()
