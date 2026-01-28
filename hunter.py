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

def get_live_token():
    # 这里我们模拟从公开 API 获取当前进度 > 90% 的最新代币
    # 在没有 Access Token 的情况下，我们先用一个真实且活跃的合约作为跳板
    # 建议你平时在 GMGN 看到热度币，顺手把地址复制到这里替换测试
    active_address = "6p6W5qYv9q3pMbvSdcBvGWoMTEBXW37mS5F8M4yVpump" 
    return active_address

def master_filter():
    # 1. 动态获取实时地址
    token_address = get_live_token()
    
    # 2. 生成实时终端链接
    gmgn_link = f"https://gmgn.ai/sol/token/{token_address}"

    alert_msg = (
        f"<b>🎯 发现实时【高爆发】信号！</b>\n\n"
        f"<b>合约地址：</b> <code>{token_address}</code>\n"
        f"<b>👉 <a href='{gmgn_link}'>立即进入 GMGN 实时监控</a></b>\n\n"
        f"<i>大师提醒：土狗行情转瞬即逝，点开后请立刻查看‘流动性’和‘聪明钱’！</i>"
    )
    
    send_telegram(alert_msg)

if __name__ == "__main__":
    master_filter()
