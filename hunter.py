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
    # 🔥 大师级测试：这是一个正在实时波动的真实代币合约地址
    # 请注意：这仅供技术测试，不作为投资建议！
    token_address = "HeLp6NMvS7VScRwJnkSNTfL9JC2fzTSDHCwX6vpyL9pk" 

    # 进化版链接：直接指向 GMGN 实战终端
    # GMGN 会自动识别它是内盘还是外盘 Raydium
    gmgn_link = f"https://gmgn.ai/sol/token/{token_address}"

    alert_msg = (
        f"<b>🌟 发现【真实地址】测试信号！</b>\n\n"
        f"<b>代币地址：</b> <code>{token_address}</code>\n"
        f"<b>👉 <a href='{gmgn_link}'>立即进入 GMGN 查看 K 线图</a></b>\n\n"
        f"<i>大师提醒：如果这次点开能看到波动的图表，说明你的‘指挥部’已经连通了真实的战场！</i>"
    )
    
    send_telegram(alert_msg)

if __name__ == "__main__":
    master_filter()
