import os
import requests

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
    # 🔥 大师级测试地址：这是一个正在交易的真实代币 (请勿直接购买)
    # 我们用它来测试跳转链接是否正常
    token_address = "HeLp6NMvS7VScRwJnkSNTfL9JC2fzTSDHCwX6vpyL9pk" 

    # 进化版链接：直接指向 GMGN 实战终端
    gmgn_link = f"https://gmgn.ai/sol/token/{token_address}"

    alert_msg = (
        f"<b>🌟 发现【真实地址】测试信号！</b>\n\n"
        f"<b>代币地址：</b> <code>{token_address}</code>\n"
        f"<b>👉 <a href='{gmgn_link}'>立即进入 GMGN 查看 K 线</a></b>\n\n"
        f"<i>大师提醒：如果这次点开能看到图表，说明你的指挥部通信完全正常了！</i>"
    )
    
    send_telegram(alert_msg)

if __name__ == "__main__":
    master_filter()
